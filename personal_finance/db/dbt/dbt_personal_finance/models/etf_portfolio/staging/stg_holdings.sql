with source as (
    select * from {{ source('etf_portfolio', 'etf_holdings') }}
)

select
    id,
    date as snapshot_date,
    account,
    ticker,
    total_units,
    avg_cost_per_unit,
    book_value,
    currency,
    cast(strftime('%Y', date) as text) as year,
    strftime('%m', date) as month
from source
