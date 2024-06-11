from bank_data.assets import TPBANK
from bank_data.partitions import daily_partitions
from dagster import (
    AssetSelection,
    build_schedule_from_partitioned_job,
    define_asset_job,
)

tpbank_transactions_import_schedule = build_schedule_from_partitioned_job(
    define_asset_job(
        "tpbank_transactions_import_job",
        selection=AssetSelection.groups(TPBANK),
        partitions_def=daily_partitions,
    )
)
