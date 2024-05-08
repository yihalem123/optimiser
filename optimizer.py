import yfinance as yf
import pandas as pd
from pypfopt import risk_models, expected_returns, EfficientFrontier, DiscreteAllocation, objective_functions, EfficientSemivariance, EfficientCVaR

def download_prices(tickers, period="max"):
    """Download historical prices for the given tickers."""
    ohlc = yf.download(tickers, period=period)
    prices = ohlc["Adj Close"].dropna(how="all")
    return prices

def get_expected_returns(prices):
    """Compute expected returns using CAPM."""
    mu = expected_returns.capm_return(prices)
    return mu

def optimize_min_volatility(prices):
    """Construct a long/short portfolio to minimize variance."""
    S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
    ef = EfficientFrontier(None, S, weight_bounds=(None, None))
    ef.min_volatility()
    weights = ef.clean_weights()
    print('------performance for min_volatility_optimized_portfolio-----')
    ef.portfolio_performance(verbose=True)

    return  weights

def perform_discrete_allocation(weights, prices, total_portfolio_value:1000, short_ratio=0.3):
    """Perform discrete allocation based on optimized weights."""
    latest_prices = prices.iloc[-1]
    da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=total_portfolio_value, short_ratio=short_ratio)
    alloc, leftover = da.lp_portfolio()
    allocations = {}
    for asset, shares in alloc.items():
        if shares > 0:
            action = "buy"
        else:
            action = "sell"
            shares = abs(shares)  # Convert negative shares to positive for verbal output
        allocations[asset] = f"{action} {shares} shares of {asset}"
    print(f"leftover: {leftover}")
    return allocations, leftover

def max_sharpe_with_sector_constraints(prices, sector_mapper, sector_lower, sector_upper):
    """Maximize Sharpe ratio with sector constraints."""
    mu = expected_returns.capm_return(prices)
    S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
    
    ef = EfficientFrontier(mu, S)


    ef.max_sharpe()
    weights = ef.clean_weights()
    print('-----performance for Maximum Sharperatio optimised portfolios-----')
    print("")
    ef.portfolio_performance(verbose=True)
    return weights

def maximize_return_given_risk(prices, target_volatility):
    """Maximize return for a given risk, with L2 regularization."""
    mu = expected_returns.capm_return(prices)
    S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
    
    ef = EfficientFrontier(mu, S)
    ef.add_objective(objective_functions.L2_reg, gamma=0.1)  # gamma is the tuning parameter
    ef.efficient_risk(target_volatility)
    weights = ef.clean_weights()
    print("-----Performance for Maximised return for a given risk Optimised Portfolio-----")

    ef.portfolio_performance(verbose=True)
    return weights

def minimize_risk_given_return(prices, target_return, market_neutral=True):
    """Minimize risk for a given return, market-neutral."""
    mu = expected_returns.capm_return(prices)
    S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
    
    ef = EfficientFrontier(mu, S, weight_bounds=(None, None))
    ef.add_objective(objective_functions.L2_reg)
    ef.efficient_return(target_return=target_return, market_neutral=market_neutral)
    weights = ef.clean_weights()
    print('------Performance for minimised risk for given return optimised Portfolio-----')
    ef.portfolio_performance(verbose=True)
    return weights

def efficient_semivariance(prices, mu, benchmark=0, target_return=None):
    """Efficient semi-variance optimization."""
    semicov = risk_models.semicovariance(prices, benchmark=benchmark)
    returns = expected_returns.returns_from_prices(prices).dropna()
    
    es = EfficientSemivariance(mu, returns)
    if target_return:
        es.efficient_return(target_return)
    else:
        es.min_semivariance()
    weights = es.clean_weights()
    print('-----performance for efficient semivarience optimised portfolios------')
    es.portfolio_performance(verbose=True)
    return weights

def efficient_cvar(prices, mu, target_cvar):
    """Efficient CVaR optimization."""
    returns = expected_returns.returns_from_prices(prices).dropna()
    
    ec = EfficientCVaR(mu, returns)
    ec.efficient_risk(target_cvar=target_cvar)
    weights = ec.clean_weights()
    print('------performance for Efficient CVaR optimization-------')
    ec.portfolio_performance(verbose=True)
    return weights


# Download historical prices
#prices = download_prices(tickers)

# Compute expected returns
#mu = get_expected_returns(prices)

# Optimize for minimum volatility
#weights = optimize_min_volatility(prices)
#alloc = perform_discrete_allocation(weights, prices)

#print(weights)
#print(performance)
# Perform discrete allocation


