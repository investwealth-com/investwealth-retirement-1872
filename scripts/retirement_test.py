#!/usr/bin/env python3
"""Every retirement since 1872: the 4% rule, the safe maximum withdrawal rate and "how long will my money last".

Reproduces the numbers on https://www.investwealth.com/tools/safe-withdrawal-rate and
https://www.investwealth.com/tools/how-long-will-my-money-last from the annual data in ../data.

Method: a portfolio of US stocks and 10-year US Treasuries, rebalanced once a year; the first-year withdrawal is a share of the
starting portfolio and is raised with each year's actual US inflation; one retirement starts in every year from 1872.
US data, before taxes; optional yearly cost in percent. Backtested results are hypothetical. Educational research, not investment advice.

Usage:
  python retirement_test.py                      # 60/40, 4%, 30 years + the tables
  python retirement_test.py --stocks 80 --rate 3.5 --years 40 --fee 0.2
"""
import argparse, csv, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data', 'us_annual_returns_1872.csv')


def load():
    years, S, B, I = [], [], [], []
    with open(DATA, newline='') as f:
        for r in csv.DictReader(f):
            years.append(int(r['year'])); S.append(float(r['us_stocks_total_return']))
            B.append(float(r['us_10y_treasury_total_return'])); I.append(float(r['us_cpi_inflation']))
    return years, S, B, I


def simulate(S, B, I, stocks, rate, years, fee, start):
    """Return (survived, years_lasted, final_value_real) for one start index."""
    v, wd, cpi = 1.0, rate, 1.0
    for t in range(years):
        if start + t >= len(S):
            return None, t, v / cpi                     # data ends before the horizon
        v -= wd
        if v <= 0:
            return False, t + 1, 0.0
        v *= (1 + stocks * S[start + t] + (1 - stocks) * B[start + t]) * (1 - fee)
        wd *= 1 + I[start + t]; cpi *= 1 + I[start + t]
    return True, years, v / cpi


def all_survive(S, B, I, stocks, rate, years, fee):
    return all(simulate(S, B, I, stocks, rate, years, fee, k)[0] for k in range(len(S) - years + 1))


def safe_max(S, B, I, stocks, years, fee):
    lo, hi = 0.0, 0.15
    for _ in range(22):
        mid = (lo + hi) / 2
        if all_survive(S, B, I, stocks, mid, years, fee): lo = mid
        else: hi = mid
    return lo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stocks', type=float, default=60, help='stock share in percent (rest: 10-year Treasuries)')
    ap.add_argument('--rate', type=float, default=4.0, help='first-year withdrawal, percent of the starting portfolio')
    ap.add_argument('--years', type=int, default=30)
    ap.add_argument('--fee', type=float, default=0.0, help='yearly cost in percent')
    a = ap.parse_args()
    years, S, B, I = load(); st, rate, fee = a.stocks / 100, a.rate / 100, a.fee / 100
    n = len(S) - a.years + 1
    res = [(years[k],) + simulate(S, B, I, st, rate, a.years, fee, k) for k in range(n)]
    ok = sum(1 for r in res if r[1]); fails = [r for r in res if r[1] is False]
    print(f"{a.rate:.2f}% withdrawal, {a.stocks:.0f}/{100 - a.stocks:.0f}, {a.years} years, costs {a.fee:.2f}%: "
          f"{ok} of {n} retirement starts ({years[0]}–{years[n - 1]}) survived")
    if fails:
        print("  failures:", ', '.join(f"{y} (ran out in year {t})" for y, _, t, _ in fails))
    worst = min(res, key=lambda r: (r[1] is not False, r[2] if r[1] is False else 99, r[3]))
    print(f"  worst start: {worst[0]}  ·  best start: {max(res, key=lambda r: r[3])[0]}")
    print(f"  highest rate that survived every start: {100 * safe_max(S, B, I, st, a.years, fee):.2f}%")

    print("\nSafe maximum withdrawal rate by mix and horizon (survived every start since 1872):")
    print("  stocks/bonds   20y    30y    40y    50y")
    for s in (1.0, .8, .6, .4, .2):
        print(f"  {s * 100:3.0f}/{100 - s * 100:<3.0f}     " + "  ".join(f"{100 * safe_max(S, B, I, s, Y, fee):4.1f}%" for Y in (20, 30, 40, 50)))

    # how long will my money last: follow each start up to 40 years
    H = 40; starts = len(S) - H + 1; lasted = []
    for k in range(starts):
        ok_, t, _ = simulate(S, B, I, st, rate, H, fee, k); lasted.append(H + 1 if ok_ else t)
    lasted_sorted = sorted(lasted); med = lasted_sorted[len(lasted) // 2]
    print(f"\nHow long the money lasted at {a.rate:.2f}% ({starts} starts followed up to {H} years):")
    print(f"  lasted 30+ years in {100 * sum(1 for x in lasted if x >= 30) / starts:.0f}% of starts, 40+ years in "
          f"{100 * sum(1 for x in lasted if x > H) / starts:.0f}%; median {'40+' if med > H else med} years; "
          f"shortest {min(lasted)} years (start {years[lasted.index(min(lasted))]})")


if __name__ == '__main__':
    main()
