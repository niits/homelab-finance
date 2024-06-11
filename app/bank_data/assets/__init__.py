from bank_data.assets import tpbank
from dagster import load_assets_from_modules

TPBANK = "tpbank"

tpbank_assets = load_assets_from_modules([tpbank], group_name=TPBANK)
