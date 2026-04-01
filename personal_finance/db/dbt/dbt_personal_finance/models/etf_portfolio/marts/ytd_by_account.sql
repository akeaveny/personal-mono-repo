with buys as (
    select year, account, sum(cost) as total_bought
    from {{ ref('stg_buys') }}
    group by year, account
),

sells as (
    select year, account, sum(proceeds) as total_sold
    from {{ ref('stg_sells') }}
    group by year, account
),

divs as (
    select year, account, sum(dividend_amount) as total_dividends
    from {{ ref('stg_dividends') }}
    group by year, account
),

accounts as (
    select * from {{ ref('accounts') }}
),

combined as (
    select distinct year, account from {{ ref('stg_transactions') }}
)

select
    c.year,
    c.account,
    a.account_type,
    coalesce(b.total_bought, 0) as total_bought,
    coalesce(s.total_sold, 0) as total_sold,
    coalesce(d.total_dividends, 0) as total_dividends,
    round(coalesce(b.total_bought, 0) - coalesce(s.total_sold, 0), 2) as net_invested,
    a.annual_limit,
    case
        when a.annual_limit is not null and a.annual_limit > 0
        then round(a.annual_limit - coalesce(b.total_bought, 0), 2)
        else null
    end as remaining_room
from combined c
left join buys b on c.year = b.year and c.account = b.account
left join sells s on c.year = s.year and c.account = s.account
left join divs d on c.year = d.year and c.account = d.account
left join accounts a on c.account = a.account
order by c.year desc, c.account
