select
    id,
    transaction_date,
    account,
    ticker,
    security_name,
    shares,
    price_per_share,
    amount as proceeds,
    currency,
    execution_date,
    year,
    month,
    year_month
from {{ ref('stg_transactions') }}
where transaction_type = 'SELL'
