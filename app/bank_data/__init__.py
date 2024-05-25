from dagster import Definitions, EnvVar

from bank_data.assets import tpbank_assets
from bank_data.jobs import tpbank_transactions_import_schedule
from bank_data.resources.sql_database import DatabaseResource
from bank_data.resources.tpbank_transaction import TPBankResource

defs = Definitions(
    assets=[*tpbank_assets],
    resources={
        "tpbank_connection": TPBankResource(
            account_number=EnvVar("TPBANK_ACCOUNT_NUMBER"),
            password=EnvVar("TPBANK_PASSWORD"),
            device_id=EnvVar("TPBANK_DEVICE_ID"),
        ),
        "db_engine": DatabaseResource(database_dns=EnvVar("DATABASE_DSN")),
    },
    schedules=[tpbank_transactions_import_schedule],
)
