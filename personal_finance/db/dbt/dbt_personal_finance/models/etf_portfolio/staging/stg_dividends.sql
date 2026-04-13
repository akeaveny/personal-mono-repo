select
    id,
    transaction_date,
    account,
    ticker,
    security_name,
    amount as dividend_amount,
    currency,
    execution_date,
    year,
    month,
    year_month
from {{ ref('stg_transactions') }}
where transaction_type = 'DIV'
