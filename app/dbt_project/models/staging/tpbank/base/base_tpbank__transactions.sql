with
    renamed as (
        select
            cast({{ adapter.quote("id") }} as bigint) as id,
            {{ adapter.quote("arrangementId") }},
            {{ adapter.quote("reference") }},
            {{ adapter.quote("xref") }},
            {{ adapter.quote("description") }},
            {{ adapter.quote("bookingDate") }},
            {{ adapter.quote("valueDate") }},
            {{ adapter.quote("amount") }} * case
                when {{ adapter.quote("creditDebitIndicator") }} = 'CRDT'
                then 1
                when {{ adapter.quote("creditDebitIndicator") }} = 'DBIT'
                then -1
                else null
            end as amount,
            {{ adapter.quote("currency") }},
            {{ adapter.quote("updated_at") }}
        from {{ source("tpbank", "transactions") }}
    )
select *
from renamed
