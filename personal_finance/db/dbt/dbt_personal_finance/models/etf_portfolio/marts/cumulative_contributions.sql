with buys as (
    select * from {{ ref('stg_buys') }}
),

daily_totals as (
    select
        transaction_date,
        account,
        round(sum(cost), 2) as daily_total
    from buys
    group by transaction_date, account
)

select
    transaction_date,
    account,
    daily_total,
    round(sum(daily_total) over (
        partition by account
        order by transaction_date
        rows between unbounded preceding and current row
    ), 2) as cumulative_by_account,
    round(sum(daily_total) over (
        order by transaction_date
        rows between unbounded preceding and current row
    ), 2) as cumulative_total
from daily_totals
order by transaction_date desc, account
