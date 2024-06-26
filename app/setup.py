from setuptools import find_packages, setup

setup(
    name="bank_data",
    packages=find_packages(exclude=["bank_data_tests"]),
    install_requires=[
        "dagster==1.7.6",
        "dagster-aws==0.23.6",
        "dagster-postgres==0.23.6",
        "dagster-dbt==0.23.6",
        "dbt-core==1.7.16",
        "dbt-postgres==1.7.16",
        "pandas==2.2.2",
        "matplotlib==3.9.0",
        "requests==2.32.1",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
