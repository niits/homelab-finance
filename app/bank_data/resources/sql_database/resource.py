from dagster import ConfigurableResource, InitResourceContext
from pandas import DataFrame
from pydantic import PostgresDsn, PrivateAttr
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


class DatabaseResource(ConfigurableResource):
    database_dns: str
    transaction_table: str = "transactions"
    _engine: Engine = PrivateAttr()

    def setup_for_execution(self, context: InitResourceContext) -> None:
        context.log.info("Creating database engine")
        try:
            database_dns = PostgresDsn(self.database_dns)
        except Exception:
            raise ValueError("Invalid database DNS provided")
        self._engine = create_engine(str(database_dns))
        context.log.info("Database engine created")

    def insert_dataframe(self, data: DataFrame) -> None:
        data.to_sql(
            self.transaction_table, self._engine, if_exists="append", index=False
        )
