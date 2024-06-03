import pandas as pd
from dagster import (
    MetadataValue,
    OpExecutionContext,
    graph_asset,
    op,
)
from pandas import DataFrame

from bank_data.partitions import daily_partitions
from bank_data.resources.sql_database import DatabaseResource
from bank_data.resources.tpbank_transaction import TPBankResource, TransactionData


@op
def data_from_service(
    context: OpExecutionContext,
    tpbank_connection: TPBankResource,
) -> TransactionData:
    return tpbank_connection.request(
        start_date=context.partition_time_window.start,
        end_date=context.partition_time_window.end,
    )


@op
def data_to_dataframe(
    context: OpExecutionContext,
    data: TransactionData,
    db_engine: DatabaseResource,
) -> DataFrame:
    data = pd.DataFrame.from_records(
        [transaction.model_dump() for transaction in data.transactionInfos]
    )

    data["bookingDate"] = pd.to_datetime(data["bookingDate"])
    data["valueDate"] = pd.to_datetime(data["valueDate"])
    data["amount"] = data["amount"].astype(int)
    data["runningBalance"] = data["runningBalance"].astype(int)
    data["updated_at"] = pd.Timestamp.now()

    context.add_output_metadata(
        metadata={
            "num_rows": len(data),
            "preview": MetadataValue.md(data.head().to_markdown()),
        },
    )

    db_engine.insert_dataframe(data)
    return data


@graph_asset(partitions_def=daily_partitions)
def tpbank_transactions() -> DataFrame:
    return data_to_dataframe(data_from_service())
