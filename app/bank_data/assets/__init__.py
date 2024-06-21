from bank_data.assets import tpbank_transactions, updated_transactions
from dagster import load_assets_from_modules

RAW_TRANSACTIONS = "raw_transactions"
INTERMEDIATE_TRANSFORM_OUTPUT = "intermediate_transform_output"

tpbank_assets = load_assets_from_modules(
    [tpbank_transactions], group_name=RAW_TRANSACTIONS
)

updated_transactions_assets = load_assets_from_modules(
    [updated_transactions], group_name=INTERMEDIATE_TRANSFORM_OUTPUT
)
