with sells as (
    select * from {{ ref('stg_sells') }}
)

select
    year_month,
    year,
    month,
    account,
    ticker,
    security_name,
    currency,
    count(*) as num_sells,
    round(sum(shares), 4) as total_shares_sold,
    round(sum(proceeds), 2) as total_proceeds,
    round(avg(price_per_share), 2) as avg_sell_price
from sells
group by year_month, year, month, account, ticker, security_name, currency
order by year_month desc, account, ticker
