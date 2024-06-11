import json
from datetime import datetime

import requests
from bank_data.resources.tpbank_transaction import Transaction, TransactionData
from dagster import ConfigurableResource, InitResourceContext
from pydantic import PrivateAttr

TPBANK_BASE_URL = "https://ebank.tpb.vn/gateway/api"
AUTH_ENDPOINT = "auth/login"
TRANSACTION_ENDPOINT = "smart-search-presentation-service/v2/account-transactions/find"
HEADERS = {
    "APP_VERSION": "2024.05.17",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
    "Authorization": "Bearer",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "DEVICE_NAME": "Chrome",
    "DNT": "1",
    "Origin": "https://ebank.tpb.vn",
    "PLATFORM_NAME": "WEB",
    "PLATFORM_VERSION": "125",
    "Referer": "https://ebank.tpb.vn/retail/vX/",
    "SOURCE_APP": "HYDRO",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}


class TPBankResource(ConfigurableResource):
    account_number: str
    password: str
    device_id: str
    _api_token: str = PrivateAttr()

    def setup_for_execution(self, context: InitResourceContext) -> None:
        headers = HEADERS.copy()
        headers["DEVICE_ID"] = self.device_id

        context.log.info("Authenticating with TPBank API")
        response = requests.request(
            "POST",
            f"{TPBANK_BASE_URL}/{AUTH_ENDPOINT}",
            headers=headers,
            data=json.dumps(
                {
                    "username": self.account_number[:8],
                    "password": self.password,
                    "step_2FA": "VERIFY",
                    "deviceId": self.device_id,
                }
            ),
        )

        response.raise_for_status()

        data = response.json()

        assert (
            "token_type" in data
        ), "Invalid response from TPBank API, missing 'token_type'"
        assert (
            "access_token" in data
        ), "Invalid response from TPBank API, missing 'access_token'"

        self._api_token = f"{data['token_type']} {data['access_token']}"
        context.log.info("Successfully authenticated with TPBank API")

    def request(self, start_date: datetime, end_date: datetime) -> dict:
        headers = HEADERS.copy()
        headers["DEVICE_ID"] = self.device_id
        headers["Authorization"] = self._api_token

        response = requests.request(
            "POST",
            f"{TPBANK_BASE_URL}/{TRANSACTION_ENDPOINT}",
            headers=headers,
            data=json.dumps(
                {
                    "pageNumber": 1,
                    "pageSize": 400,
                    "accountNo": self.account_number,
                    "currency": "VND",
                    "maxAcentrysrno": "",
                    "fromDate": start_date.strftime("%Y%m%d"),
                    "toDate": end_date.strftime("%Y%m%d"),
                    "keyword": "",
                }
            ),
        )

        response.raise_for_status()
        data = response.json()

        return TransactionData(
            totalRows=data.get("totalRows"),
            maxAcentrysmo=data.get("maxAcentrysmo"),
            transactionInfos=[
                Transaction(**transaction)
                for transaction in data.get("transactionInfos", [])
            ],
        )
