with
    snapshots as (select * from {{ ref("transaction_snapshots") }}),
    renamed as (
        select
            {{ adapter.quote("id") }},
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
        from snapshots
    )
select *
from renamed
