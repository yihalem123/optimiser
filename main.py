from optimizer import download_prices, optimize_min_volatility, max_sharpe_with_sector_constraints, get_expected_returns, perform_discrete_allocation, maximize_return_given_risk, minimize_risk_given_return, efficient_semivariance, efficient_cvar

tickers = ["MSFT", "AMZN", "KO", "MA", "COST", 
           "LUV", "XOM", "PFE", "JPM", "UNH", 
           "ACN", "DIS", "GILD", "F", "TSLA"]
prices = download_prices(tickers)

mu = get_expected_returns(prices)

# Maximize Sharpe ratio with sector constraints
sector_mapper = {
    "MSFT": "Tech",
    "AMZN": "Consumer Discretionary",
    "KO": "Consumer Staples",
    "MA": "Financial Services",
    "COST": "Consumer Staples",
    "LUV": "Aerospace",
    "XOM": "Energy",
    "PFE": "Healthcare",
    "JPM": "Financial Services",
    "UNH": "Healthcare",
    "ACN": "Misc",
    "DIS": "Media",
    "GILD": "Healthcare",
    "F": "Auto",
    "TSLA": "Auto"
}

sector_lower = {
    "Consumer Staples": 0.1, # at least 10% to staples
    "Tech": 0.05 # at least 5% to tech
    # For all other sectors, it will be assumed there is no lower bound
}

sector_upper = {
    "Tech": 0.2,
    "Aerospace":0.1,
    "Energy": 0.1,
    "Auto":0.15
}


# Optimize for minimum volatility
print("#####################################################")
weights = optimize_min_volatility(prices)
alloc = perform_discrete_allocation(weights, prices)
print(alloc)
print("#####################################################")
print("")
print("#####################################################")
weights_max_sharpe = max_sharpe_with_sector_constraints(prices, sector_mapper, sector_lower, sector_upper)
allocation_max_sharpe = perform_discrete_allocation(weights_max_sharpe,prices)
print(allocation_max_sharpe)
print("#####################################################")
print("")
# Maximize return for a given risk
print("#####################################################")
target_volatility = 0.15
weights_maximize_return_given_risk = maximize_return_given_risk(prices, target_volatility)
allocation_max_return = perform_discrete_allocation(weights_maximize_return_given_risk, prices)
print(allocation_max_return)
print("#####################################################")
print("")

# Minimize risk for a given return
print("#####################################################")
target_return = 0.07
weights_minimize_risk_given_return = minimize_risk_given_return(prices, target_return)
allocation_minimized_risk = perform_discrete_allocation(weights_minimize_risk_given_return, prices)
print(allocation_minimized_risk)
print("#####################################################")
print("")

# Efficient semi-variance optimization
print("#####################################################")
weights_efficient_semivariance = efficient_semivariance(prices, mu,  benchmark=0.05)
allocation_efficient_semivariance = perform_discrete_allocation(weights_efficient_semivariance, prices)
print(allocation_efficient_semivariance)
print("#####################################################")
print("")
# Efficient CVaR optimization
print("#####################################################")
target_cvar = 0.025
weights_efficient_cvar = efficient_cvar(prices, mu, target_cvar)
allocation_efficient_cvar = perform_discrete_allocation(weights_efficient_cvar, prices)
print(allocation_efficient_cvar)
print("#####################################################")

