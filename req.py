import requests

url = "http://127.0.0.1:5000/optimize_portfolio"
tickers = ["MSFT", "AMZN", "KO", "MA", "COST", "LUV", "XOM", "PFE", "JPM", "UNH", "ACN", "DIS", "GILD", "F", "TSLA"]
total_portfolio_value = 20000

payload = {
    "tickers": tickers,
    "total_portfolio_value": total_portfolio_value
}

response = requests.post(url, json=payload)
data = response.json()

print("Optimized Weights:", data["weights"])
print("Allocations:", data["allocations"])
print("Leftover:", data["leftover"])