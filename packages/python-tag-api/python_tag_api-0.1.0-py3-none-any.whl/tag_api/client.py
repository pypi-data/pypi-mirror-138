from typing import List, Union
import requests

from .models import ChangeContractRequestParams, GetContractByParametersParams, GetOptInsParams, NewContractRequestParams, OptIn, OptInNewCogevarageDate, PaginationInfo, TagBaseModel, OptInRequestParams
from .util.base import HttpMethod
from .util.base.decorators import retry_if_unauthorized
from .util.base.excpetions import UnauthorizedException, TagApiException


class Client:
    __session: requests.Session
    __base_url: str

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        audience: str,
        grant_type: str,
        tag_base_url: str,
        access_token=None,
    ) -> None:
        self.__base_url = tag_base_url
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__audience = audience
        self.__grant_type = grant_type
        self.__access_token = access_token

        self.__session = requests.Session()
        self._authorize()

    def _get_access_token(
        self, client_id: str, client_secret: str, audience: str, grant_type: str
    ) -> str:
        with self.__session as session:
            body_params = {
                "client_id": client_id,
                "client_secret": client_secret,
                "audience": audience,
                "grant_type": grant_type,
            }

            response = session.post(
                f"{self.__base_url}/token", json=body_params)
            response_data = response.json()

            if response.status_code == 401:
                raise UnauthorizedException(
                    401,
                    response_data.get("error"),
                    response_data.get("error_description"),
                )

        return response.json().get("access_token")

    def _authorize(self) -> None:
        self.__access_token = self._get_access_token(
            self.__client_id, self.__client_secret, self.__audience, self.__grant_type
        )
        self.__session.headers.update(
            {"Authorization": f"Bearer {self.__access_token}"}
        )

    @retry_if_unauthorized
    def _request(
        self,
        method: HttpMethod,
        path: str,
        body_params: TagBaseModel = None,
        path_params: dict = None,
        query_params: TagBaseModel = None,
    ) -> requests.Response:
        request_path = path if path_params is None else path.format(
            **path_params)
        request_url = f"{self.__base_url}/{request_path}"

        try:
            with self.__session as session:
                res = session.request(
                    method.value,
                    request_url,
                    params=query_params.format() if query_params is not None else None,
                    json=body_params.format() if body_params is not None else None
                )
                res.raise_for_status()
                return res
        except requests.exceptions.HTTPError as http_error:
            response_data = {}
            http_error_code = http_error.response.status_code

            if http_error_code == 401:
                raise UnauthorizedException(401, None, None)

            if self._is_json_response(http_error.response):
                response_data = http_error.response.json()
            raise TagApiException(
                http_error_code,
                response_data.get('errors'),
                response_data.get('processKey'),
                response_data.get('createdAt')
            )

    def _is_json_response(self, res: requests.Response):
        try:
            content_type = res.headers.get('content-type')
            if 'application/json' in content_type:
                return True
        except:
            return False


class TagClient:
    __client: Client

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        audience: str,
        grant_type: str,
        tag_base_url: str,
        access_token=None,
    ) -> None:
        self.__client = Client(
            client_id,
            client_secret,
            audience,
            grant_type,
            tag_base_url,
            access_token,
        )

    def opt_in(self, opt_ins: Union[OptIn, List[OptIn]]):
        path = "receivable/consent/optin"

        if isinstance(opt_ins, list):
            opt_ins = OptInRequestParams(opt_ins)
        else:
            opt_ins = OptInRequestParams([opt_ins])

        res = self.__client._request(
            HttpMethod.POST,
            path,
            body_params=opt_ins
        )
        return res.json()

    def get_opt_in(self, opt_in_key: str):
        path = "receivable/consent/optin/{key}"
        res = self.__client._request(
            HttpMethod.GET,
            path,
            path_params={'key': opt_in_key}
        )
        return res.json()

    def get_opt_ins(self, opt_ins_params: GetOptInsParams):
        path = "receivable/consent/optin/parameters"
        res = self.__client._request(
            HttpMethod.GET,
            path,
            query_params=opt_ins_params
        )
        if res.status_code == 204:
            # Returns No Content if no optin was found
            return []
        return res.json()

    def opt_out(self, opt_in_key: str):
        path = "receivable/consent/optout/{key}"
        res = self.__client._request(
            HttpMethod.PATCH,
            path,
            path_params={'key': opt_in_key}
        )
        return res.json()

    def update_opt_in_coverage_date(self, opt_in_key: str, params: OptInNewCogevarageDate):
        path = "receivable/consent/optin/{key}"
        res = self.__client._request(
            HttpMethod.PATCH,
            path,
            path_params={'key': opt_in_key},
            body_params=params
        )
        return res.json()

    def new_contract(self, new_contract: NewContractRequestParams):
        path = "receivable/contract"
        res = self.__client._request(
            HttpMethod.POST,
            path,
            body_params=new_contract
        )
        return res.json()

    def change_contract(self, contract: ChangeContractRequestParams):
        path = "receivable/contract"
        res = self.__client._request(
            HttpMethod.PATCH,
            path,
            body_params=contract
        )
        return res.json()

    def get_contract(self, contract_key: str):
        path = "receivable/contract/key/{key}"
        res = self.__client._request(
            HttpMethod.GET,
            path,
            path_params={'key': contract_key}
        )
        return res.json()

    def get_process_contracts(self, process_key: str):
        path = "receivable/contract/processkey/{process_key}"
        res = self.__client._request(
            HttpMethod.GET,
            path,
            path_params={'process_key': process_key},
            query_params=PaginationInfo(page=1, perPage=100)
        )
        return res.json()

    def get_contracts_by_reference(self, reference: str):
        path = "receivable/contract/reference/{reference}"
        res = self.__client._request(
            HttpMethod.GET,
            path,
            path_params={'reference': reference},
            query_params=PaginationInfo(page=1, perPage=100)
        )
        return res.json()

    def get_contracts_by_parameters(self, params: GetContractByParametersParams):
        path = "receivable/contract"
        res = self.__client._request(
            HttpMethod.GET,
            path,
            query_params=params
        )
        return res.json()
