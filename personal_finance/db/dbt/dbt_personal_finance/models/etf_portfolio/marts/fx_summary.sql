with fx as (
    select * from {{ ref('stg_fx') }}
)

select
    year_month,
    year,
    month,
    account,
    currency,
    count(*) as num_conversions,
    round(sum(amount), 2) as total_amount,
    round(avg(fx_rate), 4) as avg_fx_rate
from fx
group by year_month, year, month, account, currency
order by year_month desc, currency
