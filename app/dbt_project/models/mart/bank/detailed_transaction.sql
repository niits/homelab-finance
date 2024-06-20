{{ config(materialized="materialized_view") }}


with
    transactions as (select * from {{ ref("stg_tpbank__transactions") }}),
    categories as (select * from {{ ref("stg_tpbank__transaction_categories") }})

select transactions.*, categories.category, categories.category_group
from transactions
left join categories on transactions.id = categories.id
