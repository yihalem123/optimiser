from flask import Flask, request, jsonify
from optimizer import download_prices, optimize_min_volatility, max_sharpe_with_sector_constraints, get_expected_returns, perform_discrete_allocation, maximize_return_given_risk, minimize_risk_given_return, efficient_semivariance, efficient_cvar, optimize_hrp 
from flask_cors import CORS
from math import isnan
  

app = Flask(__name__)
CORS(app)


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

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/optimize_portfolio', methods=['POST'])
def optimize_portfolio():
    tickers = request.json.get('tickers')
    total_portfolio_value = request.json.get('total_portfolio_value')
    
    prices = download_prices(tickers)
    weights, _ = optimize_min_volatility(prices)
    allocations, leftover = perform_discrete_allocation(weights, prices, total_portfolio_value=total_portfolio_value)
    
    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover
    }
    return jsonify(response)

@app.route('/optimize_min_volatility', methods=['POST'])
def optimize_min_volatility_endpoint():
    tickers = request.json.get('tickers')
    total_portfolio_value = request.json.get('total_portfolio_value')
    
    prices = download_prices(tickers)
    weights, performance_data = optimize_min_volatility(prices)
    allocations, leftover = perform_discrete_allocation(weights, prices, total_portfolio_value=total_portfolio_value)
    performance_data = performance_data['MVO']
    performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}
    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "performance": performance_data
 
    }
    print(performance_data)
    return jsonify(response)

@app.route('/max_sharpe_with_sector_constraints', methods=['POST'])
def max_sharpe_with_sector_constraints_endpoint():
    tickers = request.json.get('tickers')
    total_portfolio_value = request.json.get('total_portfolio_value', 10000)
    
    prices = download_prices(tickers)
    weights, performance_data = max_sharpe_with_sector_constraints(prices, sector_mapper, sector_lower, sector_upper)
    allocations, leftover = perform_discrete_allocation(weights, prices, total_portfolio_value=total_portfolio_value)
    performance_data = performance_data['MVO']
    performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}

    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "performance": performance_data
    }
    return jsonify(response)

@app.route('/maximize_return_given_risk', methods=['POST'])
def maximize_return_given_risk_endpoint():
    tickers = request.json.get('tickers')
    target_volatility = request.json.get('target_volatility')
    total_portfolio_value = request.json.get('total_portfolio_value', 10000)
    prices = download_prices(tickers)
    weights, performance_data = maximize_return_given_risk(prices, target_volatility)
    allocations, leftover = perform_discrete_allocation(weights, prices, total_portfolio_value=total_portfolio_value)
    performance_data = performance_data['MVO']
    performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}

    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "performance": performance_data
    }
    return jsonify(response)

@app.route('/minimize_risk_given_return', methods=['POST'])
def minimize_risk_given_return_endpoint():
    tickers = request.json.get('tickers')
    target_return = request.json.get('target_return')
    total_portfolio_value = request.json.get('total_portfolio_value', 10000)

    prices = download_prices(tickers)
    weights, performance_data = minimize_risk_given_return(prices, target_return)
    allocations, leftover = perform_discrete_allocation(weights, prices, total_portfolio_value=total_portfolio_value)
    performance_data = performance_data['MVO']
    performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}

    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "performance":performance_data
    }
    return jsonify(response)

@app.route('/efficient_semivariance', methods=['POST'])
def efficient_semivariance_endpoint():
    tickers = request.json.get('tickers')
    target_return = request.json.get('target_return')
    total_portfolio_value = request.json.get('total_portfolio_value', 10000)
    
    prices = download_prices(tickers)
    mu = get_expected_returns(prices)

    weights, performance_data = efficient_semivariance(prices,mu,  benchmark=target_return)
    allocations, leftover = perform_discrete_allocation(weights, prices, total_portfolio_value=total_portfolio_value)
    performance_data = performance_data['MVO']
    performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}

    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "performance":performance_data
    }
    return jsonify(response)

@app.route('/efficient_cvar', methods=['POST'])
def efficient_cvar_endpoint():
    tickers = request.json.get('tickers')
    target_cvar = request.json.get('target_cvar')
    total_portfolio_value = request.json.get('total_portfolio_value', 10000)
   
    prices = download_prices(tickers)
    mu = get_expected_returns(prices)

    weights, performance_data = efficient_cvar(prices,mu,  target_cvar=target_cvar)
    allocations, leftover = perform_discrete_allocation(weights, prices,  total_portfolio_value=total_portfolio_value)
    performance_data = performance_data['MVO']
    performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}

    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "performance": performance_data
    }
    return jsonify(response)

@app.route('/optimize_hrp', methods=['POST'])
def optimize_hrp_endpoint():
    """
    Endpoint to optimize portfolio using Hierarchical Risk Parity (HRP).
    Expects a JSON request containing tickers and total_portfolio_value.
    Returns the optimized weights, allocations, and leftover funds.
    """
    # Get JSON data from request
    
    
    # Extract tickers and total portfolio value from JSON data
    tickers = request.json.get('tickers')
    total_portfolio_value = request.json.get('total_portfolio_value', 10000)
    
    # Download historical prices
    prices = download_prices(tickers)
    
    # Optimize portfolio using HRP
    weights = optimize_hrp(prices)
    
    # Perform discrete allocation
    allocations, leftover = perform_discrete_allocation(weights, prices, total_portfolio_value=total_portfolio_value)
    
    # Prepare response
    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover
    }
    
    # Return response as JSON
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)