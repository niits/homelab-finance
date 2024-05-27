from typing import List, Optional

from pydantic import BaseModel


class Transaction(BaseModel):
    id: str
    arrangementId: str
    reference: str
    xref: str
    description: str
    bookingDate: str
    valueDate: str
    amount: str
    currency: str
    creditDebitIndicator: str
    runningBalance: str


class TransactionData(BaseModel):
    totalRows: str
    maxAcentrysmo: Optional[str]
    transactionInfos: List[Transaction]
