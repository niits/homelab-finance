{% snapshot transaction_snapshots %}

    {{
        config(
            target_schema="public",
            unique_key="id",
            strategy="timestamp",
            updated_at="updated_at",
        )
    }}

    select *
    from {{ source("tpbank", "transactions") }}

{% endsnapshot %}
