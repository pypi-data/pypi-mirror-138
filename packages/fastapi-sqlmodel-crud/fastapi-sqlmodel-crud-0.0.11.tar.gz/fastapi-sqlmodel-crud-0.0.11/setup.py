import setuptools


def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()


setuptools.setup(
    name="fastapi-sqlmodel-crud",
    python_requires=">=3.6.1",
    version='0.0.11',
    license="Apache",
    author="Atomi",
    author_email="1456417373@qq.com",
    description="fastapi-sqlmodel-crud is a program which is based on fastapi+sqlmodel and used to quickly build the Create, Read, Update, Delete generic API interface.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url='https://github.com/amisadmin/fastapi_amis_admin',
    install_requires=[
        "fastapi>=0.68.0",
        "sqlmodel>=0.0.4",
        "ujson>=4.0.1"
    ],
    packages=setuptools.find_packages(exclude=["tests*"]),
    package_data={"": ["*.md"]},
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    project_urls={  # Optional
        'Documentation': 'http://docs.amis.work/',
    },
)
