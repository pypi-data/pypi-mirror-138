from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='python-tag-api',
    version='0.1.0',
    install_requires=[
        'requests>=2.27.1,<2.3'
    ],
    url='https://github.com/bordax/python-tag-api',
    license='MIT',
    author='Rafael Bordin',
    author_email='rafael.bordin@live.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='Python wrapper for the TAG IMF API',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        'Intended Audience :: Developers'
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)