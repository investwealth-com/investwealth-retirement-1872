# Every retirement since 1872: the data behind InvestWealth's withdrawal calculators

Annual US data from 1872 to 2025 and a small Python script that reproduce the numbers on
[investwealth.com/tools/safe-withdrawal-rate](https://www.investwealth.com/tools/safe-withdrawal-rate) and
[investwealth.com/tools/how-long-will-my-money-last](https://www.investwealth.com/tools/how-long-will-my-money-last):

- At a 4% first-year withdrawal, raised with inflation every year, a 60/40 portfolio lasted 30 years in **124 of 125** retirement starts since 1872. The one failure started in 1966.
- The highest rate that survived **every** 30-year start was **3.9%** with 60% stocks (4.0% with 80%); for 40 years about 3.6%; the cautious 20/80 mix fell to 2.7% over 40 years and 2.3% over 50.
- The eight worst 30-year start years all lie between 1962 and 1973, when bonds stopped cushioning stocks; the best (for example 1921 and 1982) supported 9–10%.

Backtested results are hypothetical. Educational research, not investment advice.

## Data

`data/us_annual_returns_1872.csv` — one row per calendar year, 1872–2025:

| column | meaning |
|---|---|
| `us_stocks_total_return` | US stocks (S&P 500 and its predecessors), total return, decimal (0.10 = +10%) |
| `us_10y_treasury_total_return` | 10-year US Treasury, total return |
| `us_cpi_inflation` | US consumer price inflation |

Sources: Robert Shiller's long-run stock, interest-rate and CPI series (Yale, "Irrational Exuberance" data) and FRED (Federal Reserve Bank of St. Louis); InvestWealth calculations for the annual total returns. Use the data freely with attribution to the original sources and to InvestWealth.com.

## Script

```bash
python scripts/retirement_test.py                                   # 60/40, 4%, 30 years, plus the tables
python scripts/retirement_test.py --stocks 80 --rate 3.5 --years 40 --fee 0.2
```

No dependencies beyond the Python standard library. The method is the one the calculators use: stocks and 10-year Treasuries rebalanced
once a year, the withdrawal raised with each year's actual inflation, one retirement starting in every year from 1872, before taxes,
optional yearly cost in percent.

Sample output (defaults):

```
4.00% withdrawal, 60/40, 30 years, costs 0.00%: 124 of 125 retirement starts (1872–1996) survived
  failures: 1966 (ran out in year 29)
  highest rate that survived every start: 3.91%

Safe maximum withdrawal rate by mix and horizon (survived every start since 1872):
  stocks/bonds   20y    30y    40y    50y
  100/0        4.5%   3.9%   3.7%   3.6%
   80/20       4.7%   4.0%   3.8%   3.6%
   60/40       4.8%   3.9%   3.6%   3.5%
   40/60       4.7%   3.8%   3.5%   3.1%
   20/80       4.5%   3.4%   2.7%   2.3%
```

## More from InvestWealth

- [How long will my money last?](https://www.investwealth.com/tools/how-long-will-my-money-last) — the same test in years instead of a rate, with a cash comparison
- [The 60/40 portfolio: calendar-year returns since 1872](https://www.investwealth.com/learn/guides/60-40-portfolio)
- [White Paper No. 1: When bonds stop hedging](https://www.investwealth.com/when-bonds-stop-hedging) — 150 years of the stock–bond correlation
- [Free Research Terminal](https://www.investwealth.com/register) — 30 markets, drawdowns, correlations, Hedge Health

## Licence

Code: MIT (see `LICENSE`). Data: derived from the public Shiller and FRED series, free to use with attribution.

InvestWealth.com · Dr.-Ing. Harry Hamann · Educational research, not investment advice. Past returns do not guarantee future results. Backtested results are hypothetical.
