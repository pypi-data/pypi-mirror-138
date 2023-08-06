import enum
from typing import List
from .util.base import PaymentScheme, DocumentType
from .util.contracts import AccountType, EffectType, EffectStrategy, WarrantyType
from dataclasses import dataclass
import datetime


@dataclass
class TagBaseModel:
    def format(self) -> dict:
        result = {}
        for field, value in self.__dict__.items():
            if value is not None:
                result[field] = format_to_tag(value)
        return result

@dataclass
class OptIn(TagBaseModel):
    beneficiary: str
    assetHolder: str
    signatureDate: str
    startDate: str
    endDate: str
    acquirer: str = None
    paymentScheme: PaymentScheme = None

@dataclass
class OptInRequestParams(TagBaseModel):
    optIns: List[OptIn]

@dataclass
class GetOptInsParams(TagBaseModel):
    assetHolder: str
    initialDate: str
    finalDate: str
    beneficiary: str = None
    acquirer: str = None
    paymentScheme: PaymentScheme = None
    reject: bool = None


@dataclass
class OptInNewCogevarageDate(TagBaseModel):
    endDate: str
    startDate: str = None


@dataclass
class BankAccount(TagBaseModel):
    branch: str
    account: str
    accountDigit: str
    accountType: AccountType
    ispb: str
    documentType: DocumentType
    documentNumber: str


@dataclass
class ContractSpecifications(TagBaseModel):
    expectedSettlementDate: str
    originalAssetHolder: str
    receivableDebtor: str
    paymentScheme: PaymentScheme
    effectValue: str


@dataclass
class Contract(TagBaseModel):
    reference: str
    contractDueDate: str
    assetHolderDocumentType: DocumentType
    assetHolder: str
    contractUniqueIdentifier: str
    signatureDate: str
    effectType: EffectType
    balanceDue: str
    divisionMethod: str
    effectStrategy: EffectStrategy
    bankAccount: BankAccount
    contractSpecifications: List[ContractSpecifications]
    percentageValue: str = None
    warrantyType: WarrantyType = None
    warrantyAmount: str = None


@dataclass
class NewContractRequestParams(TagBaseModel):
    idempotencyKey: str
    contracts: List[Contract]


@dataclass
class PaginationInfo(TagBaseModel):
    page: int = 1
    perPage: int = 100

@dataclass
class GetContractByParametersParams(TagBaseModel):
    startSignatureDate: str = None
    assetHolder: str = None
    startContractDueDate: str = None
    endContractDueDate: str = None
    endSignatureDate: str = None
    startCreatedAt: str = None
    endCreatedAt: str = None
    PaginationInfo

@dataclass
class ContractToChange(TagBaseModel):
    key: str
    isCanceled: bool = None
    contractDueDate: str = None
    contractUniqueIdentifier: str = None
    warrantyAmount: str = None
    balanceDue: str = None
    percentageValue: str = None
    bankAccount: BankAccount = None
    contractSpecifications: List[ContractSpecifications] = None


@dataclass
class ChangeContractRequestParams(TagBaseModel):
    contracts: List[ContractToChange]

def format_to_tag(value):
    if isinstance(value, TagBaseModel):
        return value.format()
    elif isinstance(value, list):
        return [format_to_tag(x) for x in value]
    elif isinstance(value, dict):
        return {k: format_to_tag(v) for k,v in value.items()}
    elif isinstance(value, bool):
        return 'true' if value else 'false'
    elif isinstance(value, datetime.date):
        return value.isoformat()
    elif isinstance(value, enum.Enum):
        return value.value
    else:
        return str(value)
