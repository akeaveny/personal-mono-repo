with latest_snapshot as (
    select
        h.*,
        row_number() over (partition by account, ticker order by snapshot_date desc) as rn
    from {{ ref('stg_holdings') }} h
),

current_holdings as (
    select * from latest_snapshot where rn = 1
),

etfs as (
    select * from {{ ref('etfs') }}
),

portfolio_total as (
    select sum(book_value) as total_book_value
    from current_holdings
),

rebalance_config as (
    select cast(value as real) as drift_threshold
    from {{ ref('rebalancing_config') }}
    where param = 'drift_threshold_pct'
)

select
    h.account,
    h.ticker,
    e.asset_class,
    h.total_units,
    h.avg_cost_per_unit,
    h.book_value,
    h.currency,
    h.snapshot_date,
    round(h.book_value / pt.total_book_value * 100, 1) as actual_pct,
    e.target_allocation as target_pct,
    round(h.book_value / pt.total_book_value * 100 - coalesce(e.target_allocation, 0), 1) as drift_pct,
    rc.drift_threshold,
    case
        when e.target_allocation is null then 'NO_TARGET'
        when abs(h.book_value / pt.total_book_value * 100 - e.target_allocation) > rc.drift_threshold
        then 'REBALANCE'
        else 'OK'
    end as status
from current_holdings h
left join etfs e on h.ticker = e.ticker
cross join portfolio_total pt
cross join rebalance_config rc
where pt.total_book_value > 0
order by h.ticker
