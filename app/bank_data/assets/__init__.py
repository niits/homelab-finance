from dagster import load_assets_from_modules

from bank_data.assets import tpbank

TPBANK = "tpbank"

tpbank_assets = load_assets_from_modules([tpbank], group_name=TPBANK)
