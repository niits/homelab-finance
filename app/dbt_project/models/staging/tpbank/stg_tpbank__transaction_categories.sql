with
    descriptions as (select * from {{ ref("base_tpbank__transaction_categories") }}),
    update_times as (
        select * from {{ ref("base_tpbank__transaction_categories_last_update_times") }}
    )

select descriptions.*
from descriptions
inner join
    update_times
    on descriptions.id = update_times.id
    and descriptions.updated_at = update_times.last_update_time
