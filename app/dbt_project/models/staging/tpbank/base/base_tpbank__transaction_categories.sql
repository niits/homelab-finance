with
    source as (select * from {{ source("tpbank", "transaction_categories") }}),
    renamed as (
        select
            {{ adapter.quote("category") }},
            {{ adapter.quote("category_group") }},
            {{ adapter.quote("updated_at") }},
            cast({{ adapter.quote("id") }} as bigint) as id
        from source
    )
select *
from renamed
