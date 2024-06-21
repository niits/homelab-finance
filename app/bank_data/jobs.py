from bank_data.assets import INTERMEDIATE_TRANSFORM_OUTPUT, RAW_TRANSACTIONS
from bank_data.partitions import daily_partitions
from dagster import (
    AssetSelection,
    build_schedule_from_partitioned_job,
    define_asset_job,
)

tpbank_transactions_transform_job = define_asset_job(
    "tpbank_transactions_transform_job",
    selection=AssetSelection.groups(INTERMEDIATE_TRANSFORM_OUTPUT),
)


tpbank_transactions_import_job = define_asset_job(
    "tpbank_transactions_import_job",
    selection=AssetSelection.groups(RAW_TRANSACTIONS, INTERMEDIATE_TRANSFORM_OUTPUT),
    partitions_def=daily_partitions,
)
tpbank_transactions_import_schedule = build_schedule_from_partitioned_job(
    tpbank_transactions_import_job
)
