from pathlib import Path

from bank_data.project import dbt_project
from dagster_dbt import DbtCliResource

dbt = DbtCliResource(project_dir=dbt_project)

(
    dbt.cli(
        ["--quiet", "parse"],
        target_path=Path("target"),
    )
    .wait()
    .target_path.joinpath("manifest.json")
)


from bank_data.assets import tpbank_assets, updated_transactions_assets
from bank_data.jobs import (
    tpbank_transactions_import_job,
    tpbank_transactions_import_schedule,
    tpbank_transactions_transform_job,
)
from bank_data.resources.sql_database import DatabaseResource
from bank_data.resources.tpbank_transaction import TPBankResource
from dagster import Definitions, EnvVar

defs = Definitions(
    assets=tpbank_assets + updated_transactions_assets,
    resources={
        "tpbank_connection": TPBankResource(
            account_number=EnvVar("TPBANK_ACCOUNT_NUMBER"),
            password=EnvVar("TPBANK_PASSWORD"),
            device_id=EnvVar("TPBANK_DEVICE_ID"),
        ),
        "db_engine": DatabaseResource(database_dns=EnvVar("DATABASE_DSN")),
        "dbt": dbt,
    },
    schedules=[tpbank_transactions_import_schedule],
    jobs=[tpbank_transactions_import_job, tpbank_transactions_transform_job],
)
