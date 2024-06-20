with
    transactions as (select * from {{ ref("base_tpbank__transactions") }}),
    update_times as (
        select * from {{ ref("base_tpbank__transaction_last_update_times") }}
    )

select transactions.*
from transactions
inner join
    update_times
    on transactions.id = update_times.id
    and transactions.updated_at = update_times.last_update_time
