with dividends as (
    select * from {{ ref('stg_dividends') }}
)

select
    year_month,
    year,
    month,
    account,
    ticker,
    security_name,
    currency,
    count(*) as num_distributions,
    round(sum(dividend_amount), 2) as total_dividends
from dividends
group by year_month, year, month, account, ticker, security_name, currency
order by year_month desc, account, ticker
