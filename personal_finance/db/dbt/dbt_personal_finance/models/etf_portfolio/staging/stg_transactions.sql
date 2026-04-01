with source as (
    select * from {{ source('etf_portfolio', 'etf_transactions') }}
)

select
    id,
    date as transaction_date,
    account,
    transaction_type,
    ticker,
    security_name,
    shares,
    price_per_share,
    amount,
    balance,
    currency,
    execution_date,
    fx_rate,
    cast(strftime('%Y', date) as text) as year,
    strftime('%m', date) as month,
    strftime('%Y-%m', date) as year_month,
    cast(strftime('%W', date) as text) as week_number
from source
where date is not null
