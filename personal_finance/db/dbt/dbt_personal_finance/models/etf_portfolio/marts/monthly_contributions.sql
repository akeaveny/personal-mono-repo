with buys as (
    select * from {{ ref('stg_buys') }}
)

select
    year_month,
    year,
    month,
    account,
    ticker,
    security_name,
    currency,
    count(*) as num_purchases,
    round(sum(shares), 4) as total_shares,
    round(sum(cost), 2) as total_cost,
    round(avg(price_per_share), 2) as avg_price
from buys
group by year_month, year, month, account, ticker, security_name, currency
order by year_month desc, account, ticker
