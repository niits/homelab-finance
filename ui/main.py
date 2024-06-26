import os

import pandas as pd
import streamlit as st
from dagster_graphql import DagsterGraphQLClientError
from dagster_graphql.client import DagsterGraphQLClient
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

st.set_page_config(layout="wide")

st.title("Data labeling app")

DAGSTER_HOST = os.environ.get("DAGSTER_HOST")

if not DAGSTER_HOST:
    st.error("No Dagster host or port found")
    st.stop()

client = DagsterGraphQLClient(
    DAGSTER_HOST,
    port_number=3000,
)


query = """
SELECT t.*
FROM   public.stg_tpbank__transactions t
       LEFT JOIN stg_tpbank__transaction_categories c
              ON c.id = t.id
WHERE  c.id IS NULL
"""

posgres_dns = os.environ.get(
    "POSTGRES_DNS",
)
if not posgres_dns:
    st.error("No Postgres DNS found")
    st.stop()
try:
    engine = create_engine(posgres_dns)
    engine.connect()
except SQLAlchemyError as err:
    st.error(f"Error connecting to database: {err}")
    st.stop()

categories = {
    "income": [
        "Thưởng",
        "Tiền lãi",
        "Lương",
        "Được tặng",
        "Bán đồ",
        "Thu nhập khác",
        "Chuyển tiền vào tài khoản",
        "Được trả nợ",
        "Đi vay",
        "Được hoàn tiền",
        "Đầu tư: bán tài sản",

    ],
    "outcome": [
        "Ăn uống: Nhà hàng và Cà phê",
        "Ăn uống: Mua thức ăn",
        "Ăn uống: Ăn vặt",
        "Dịch vụ và hoá đơn: Tiền nhà",
        "Dịch vụ và hoá đơn: Dịch vụ Cloud",
        "Dịch vụ và hoá đơn: Thanh toán thẻ tín dụng",
        "Dịch vụ và hoá đơn: Điện thoại và Internet",
        "Dịch vụ và hoá đơn: Sửa chữa",
        "Di chuyển: Taxi và Grab",
        "Di chuyển: Xăng dầu và Bảo dưỡng xe",
        "Mua sắm: Quần áo và Giày dép",
        "Mua sắm: Thiết bị điện tử",
        "Mua sắm: Thiết bị gia dụng",
        "Mua sắm: Mua sắm khác",
        "Chi tiêu khác: Du lịch",
        "Chi tiêu khác: Khám chữa bệnh và tiền thuốc",
        "Chi tiêu khác: Quà tặng và Quyên góp",
        "Chi tiêu khác: Sách, học online và học phí",
        "Chi tiêu khác: Rút tiền",
        "Chi tiêu khác: Chưa phân loại",
        "Đầu tư: coin",
        "Đầu tư: chứng chỉ quỹ",
        "Đầu tư: chứng khoán",
        "Đầu tư: mua vàng",
        "Trả nợ",
        "Cho vay",
    ],
}
if "df" not in st.session_state:
    df = pd.read_sql_query(
        query,
        con=engine,
    )
    st.session_state.df = df
else:
    df = st.session_state.df


income_df = df[df.amount > 0]
income_df["category"] = ""
income_df["category"] = income_df["category"].astype(
    pd.CategoricalDtype(categories["income"] + [""])
)

outcome_df = df[df.amount < 0]
outcome_df["category"] = ""
outcome_df["category"] = outcome_df["category"].astype(
    pd.CategoricalDtype(categories["outcome"] + [""])
)

income_df = st.data_editor(income_df, width=1500)

outcome_df = st.data_editor(outcome_df, width=1500)

button = st.button("Save")

if button:
    final_df = pd.concat([income_df, outcome_df])
    st.dataframe(final_df)

    final_df = final_df[final_df.category != ""]

    final_df["category_group"] = final_df.category.apply(
        lambda x: x.split(":")[0].strip()
    )
    final_df["category"] = final_df.category.apply(
        lambda x: x.split(":")[1].strip() if ":" in x else ""
    )

    final_df = final_df[["id", "category", "category_group"]]

    final_df["updated_at"] = pd.Timestamp.now()

    final_df.to_sql(
        "transaction_categories",
        con=engine,
        if_exists="append",
        index=False,
    )
    st.success("Data saved")

    try:
        new_run_id: str = client.submit_job_execution(
            "tpbank_transactions_transform_job",
            run_config={},
        )
        st.success(f"Submitted job with run_id: {new_run_id}")
        st.markdown(
            f"View the run [here](http://{DAGSTER_HOST}:3000/runs/{new_run_id})"
        )
    except DagsterGraphQLClientError as exc:
        st.error(f"Error submitting job: {exc}")
