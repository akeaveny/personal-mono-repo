with buys as (
    select year, account, sum(cost) as total_bought
    from {{ ref('stg_buys') }}
    group by year, account
),

sells as (
    select year, account, sum(proceeds) as total_sold, count(*) as num_sells
    from {{ ref('stg_sells') }}
    group by year, account
),

divs as (
    select year, account, sum(dividend_amount) as total_dividends, count(*) as num_distributions
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
    a.tax_deductible,
    a.tax_free_growth,
    a.tax_free_withdrawal,
    a.annual_limit,
    coalesce(b.total_bought, 0) as total_bought,
    coalesce(s.total_sold, 0) as total_sold,
    coalesce(d.total_dividends, 0) as total_dividends,
    coalesce(s.num_sells, 0) as num_sells,
    coalesce(d.num_distributions, 0) as num_distributions,
    case
        when a.tax_free_growth = 'yes' then 'Tax-free (registered account)'
        else 'Taxable — 50% inclusion rate on capital gains'
    end as tax_status
from combined c
left join buys b on c.year = b.year and c.account = b.account
left join sells s on c.year = s.year and c.account = s.account
left join divs d on c.year = d.year and c.account = d.account
left join accounts a on c.account = a.account
order by c.year desc, c.account
