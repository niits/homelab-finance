with
    transactions_data as (select * from {{ ref("base_tpbank__transactions") }}),

    update_times as (
        select
            {{ adapter.quote("id") }},
            max({{ adapter.quote("updated_at") }}) as last_update_time
        from transactions_data
        group by {{ adapter.quote("id") }}
    )
select *
from update_times
