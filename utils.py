
import requests
import pandas as pd
from bs4 import BeautifulSoup
import finnhub
from config import FINNHUB_API_KEY

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

def get_top_gainers():
    url = "https://finviz.com/screener.ashx?v=111&s=ta_topgainers"
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    tickers = list(set([x.text for x in soup.select("a.screener-link-primary")]))
    return tickers

def screen_stocks():
    tickers = get_top_gainers()
    results = []
    for ticker in tickers[:25]:
        try:
            quote = finnhub_client.quote(ticker)
            profile = finnhub_client.company_profile2(symbol=ticker)
            news = finnhub_client.company_news(ticker, _from="2024-01-01", to="2025-12-31")

            price = quote['c']
            change_pct = ((quote['c'] - quote['pc']) / quote['pc']) * 100
            volume = quote['v']
            shs_float = profile.get("shareOutstanding", 1e9) * 1e6  # Convert to shares

            has_catalyst = any(any(term in n["headline"].lower() for term in ["fda", "merger", "earnings"]) for n in news)

            if 1 <= price <= 20 and change_pct > 4 and volume > 100000 and shs_float <= 100e6:
                results.append({
                    "Ticker": ticker,
                    "Price": price,
                    "% Change": round(change_pct, 2),
                    "Volume": volume,
                    "Float": f"{shs_float/1e6:.1f}M",
                    "Catalyst": has_catalyst
                })
        except:
            pass

    return pd.DataFrame(results)
