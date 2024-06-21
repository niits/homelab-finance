from bank_data.project import dbt_project
from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets


@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_assets(
    context: AssetExecutionContext,
    dbt: DbtCliResource,
):
    yield from dbt.cli(["build"], context=context).stream()
