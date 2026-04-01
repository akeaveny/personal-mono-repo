with buys as (
    select year, ticker, currency,
           sum(shares) as shares_bought,
           sum(cost) as total_bought,
           round(avg(price_per_share), 2) as avg_buy_price
    from {{ ref('stg_buys') }}
    group by year, ticker, currency
),

sells as (
    select year, ticker, currency,
           sum(shares) as shares_sold,
           sum(proceeds) as total_sold,
           round(avg(price_per_share), 2) as avg_sell_price
    from {{ ref('stg_sells') }}
    group by year, ticker, currency
),

divs as (
    select year, ticker, currency,
           sum(dividend_amount) as total_dividends
    from {{ ref('stg_dividends') }}
    group by year, ticker, currency
),

all_tickers as (
    select distinct year, ticker, currency from {{ ref('stg_transactions') }}
    where ticker is not null
)

select
    t.year,
    t.ticker,
    t.currency,
    coalesce(b.shares_bought, 0) as shares_bought,
    coalesce(b.total_bought, 0) as total_bought,
    b.avg_buy_price,
    coalesce(s.shares_sold, 0) as shares_sold,
    coalesce(s.total_sold, 0) as total_sold,
    s.avg_sell_price,
    coalesce(d.total_dividends, 0) as total_dividends,
    round(coalesce(b.shares_bought, 0) - coalesce(s.shares_sold, 0), 4) as net_shares
from all_tickers t
left join buys b on t.year = b.year and t.ticker = b.ticker and t.currency = b.currency
left join sells s on t.year = s.year and t.ticker = s.ticker and t.currency = s.currency
left join divs d on t.year = d.year and t.ticker = d.ticker and t.currency = d.currency
order by t.year desc, t.ticker
