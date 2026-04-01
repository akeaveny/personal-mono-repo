{{
  config(
    materialized='view'
  )
}}

with patterns_ranked as (
    select
        t.*,
        p.category as pattern_category,
        p.subcategory as pattern_subcategory,
        row_number() over (
            partition by t.bank, t.account_type, t.transaction_date, t.description_1, t.amount
            order by p.priority desc
        ) as pattern_rank
    from {{ ref('mart_transactions') }} t
    left join {{ ref('source_category_patterns') }} p
        on t.description_1 like p.pattern
)

select
    t.bank,
    t.account_type,
    t.account_number,
    t.transaction_date,
    t.cheque_number,
    t.description_1,
    t.description_2,
    t.amount,
    t.currency,
    t.cad,
    t.usd,
    t.status,
    t.transaction_type,
    coalesce(o.category_override, t.pattern_category, 'Uncategorized') as category,
    coalesce(o.subcategory_override, t.pattern_subcategory) as subcategory,
    coalesce(o.description_override, t.description_1) as display_description,
    case
        when o.category_override is not null then 'override'
        when t.pattern_category is not null then 'pattern'
        else 'none'
    end as categorization_source,
    o.notes as override_notes,
    t.source_file,
    t.created_at,
    t.updated_at

from patterns_ranked t

left join {{ ref('source_transaction_overrides') }} o
    on t.bank = o.bank
    and t.account_type = o.account_type
    and t.transaction_date = o.transaction_date
    and t.description_1 = o.description_1
    and t.amount = o.amount

where t.pattern_rank = 1 or t.pattern_category is null
