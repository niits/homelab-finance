with
    transaction_categories as (select * from {{ ref("base_tpbank__transaction_categories") }}),

    update_times as (
        select
            {{ adapter.quote("id") }},
            max({{ adapter.quote("updated_at") }}) as last_update_time
        from transaction_categories
        group by {{ adapter.quote("id") }}
    )
select *
from update_times
