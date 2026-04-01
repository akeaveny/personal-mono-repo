select
    id,
    transaction_date,
    account,
    amount,
    currency,
    fx_rate,
    execution_date,
    year,
    month,
    year_month
from {{ ref('stg_transactions') }}
where transaction_type = 'FXCONVERSION'
