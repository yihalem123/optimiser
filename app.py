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
    
    
    response={}

    prices, errors = download_prices(tickers)

    valid_tickers = [ticker for ticker in tickers if ticker not in errors]
    if valid_tickers:
        valid_prices = prices[valid_tickers]
        weights, _ = optimize_min_volatility(valid_prices)
        allocations, leftover = perform_discrete_allocation(weights, valid_prices, total_portfolio_value=total_portfolio_value)
    else:
        weights, allocations, leftover = {}, {}, 0

    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "errors": errors
    }
    return jsonify(response)

@app.route('/optimize_min_volatility', methods=['POST'])
def optimize_min_volatility_endpoint():
    tickers = request.json.get('tickers')
    total_portfolio_value = request.json.get('total_portfolio_value')

    prices, valid_tickers, errors = download_prices(tickers)
#    valid_tickers = [ticker for ticker in tickers if ticker not in errors]
    response={}
    if valid_tickers:
        valid_prices = prices[valid_tickers]
        weights, performance_data = optimize_min_volatility(valid_prices)
        
        # Ensure weights only contain valid tickers
        weights = {ticker: weight for ticker, weight in weights.items() if ticker in valid_tickers}
        
        allocations, leftover = perform_discrete_allocation(weights, valid_prices, total_portfolio_value=total_portfolio_value)
        
        performance_data = performance_data['MVO']
        performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}
    else:
        weights, allocations, leftover, performance_data = {}, {}, 0, {}


    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "performance": performance_data,
        "errors": errors
    }
    

    return jsonify(response)

@app.route('/max_sharpe_with_sector_constraints', methods=['POST'])
def max_sharpe_with_sector_constraints_endpoint():
    tickers = request.json.get('tickers')
    total_portfolio_value = request.json.get('total_portfolio_value', 10000)
    
    prices, valid_tickers, errors = download_prices(tickers)
    
    if valid_tickers:
        valid_prices = prices[valid_tickers]
        weights, performance_data = max_sharpe_with_sector_constraints(valid_prices, sector_mapper, sector_lower, sector_upper)
        allocations, leftover = perform_discrete_allocation(weights, valid_prices, total_portfolio_value=total_portfolio_value)
        performance_data = performance_data['MVO']
        performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}
    else:
        weights, allocations, leftover, performance_data = {}, {}, 0, {}

    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "performance": performance_data,
        "errors": errors
    }
    return jsonify(response)

@app.route('/maximize_return_given_risk', methods=['POST'])
def maximize_return_given_risk_endpoint():
    tickers = request.json.get('tickers')
    target_volatility = request.json.get('target_volatility')
    total_portfolio_value = request.json.get('total_portfolio_value', 10000)

    prices, valid_tickers, errors = download_prices(tickers)
    
    if valid_tickers:
        valid_prices = prices[valid_tickers]
        weights, performance_data = maximize_return_given_risk(valid_prices, target_volatility)
        allocations, leftover = perform_discrete_allocation(weights, valid_prices, total_portfolio_value=total_portfolio_value)
        performance_data = performance_data['MVO']
        performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}
    else:
        weights, allocations, leftover, performance_data = {}, {}, 0, {}

    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "performance": performance_data,
        "errors": errors
    }
    return jsonify(response)

@app.route('/minimize_risk_given_return', methods=['POST'])
def minimize_risk_given_return_endpoint():
    tickers = request.json.get('tickers')
    target_return = request.json.get('target_return')
    total_portfolio_value = request.json.get('total_portfolio_value', 10000)

    prices, valid_tickers, errors = download_prices(tickers)
    
    if valid_tickers:
        valid_prices = prices[valid_tickers]
        weights, performance_data = minimize_risk_given_return(valid_prices, target_return)
        allocations, leftover = perform_discrete_allocation(weights, valid_prices, total_portfolio_value=total_portfolio_value)
        performance_data = performance_data['MVO']
        performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}
    else:
        weights, allocations, leftover, performance_data = {}, {}, 0, {}

    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "performance": performance_data,
        "errors": errors
    }
    return jsonify(response)

@app.route('/efficient_semivariance', methods=['POST'])
def efficient_semivariance_endpoint():
    tickers = request.json.get('tickers')
    target_return = request.json.get('target_return')
    total_portfolio_value = request.json.get('total_portfolio_value', 10000)
    
    prices, valid_tickers, errors = download_prices(tickers)
    
    if valid_tickers:
        valid_prices = prices[valid_tickers]
        mu = get_expected_returns(valid_prices)
        weights, performance_data = efficient_semivariance(valid_prices, mu, benchmark=target_return)
        allocations, leftover = perform_discrete_allocation(weights, valid_prices, total_portfolio_value=total_portfolio_value)
        performance_data = performance_data['MVO']
        performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}
    else:
        weights, allocations, leftover, performance_data = {}, {}, 0, {}

    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "performance": performance_data,
        "errors": errors
    }
    return jsonify(response)

@app.route('/efficient_cvar', methods=['POST'])
def efficient_cvar_endpoint():
    tickers = request.json.get('tickers')
    target_cvar = request.json.get('target_cvar')
    total_portfolio_value = request.json.get('total_portfolio_value', 10000)
   
    prices, valid_tickers, errors = download_prices(tickers)
    
    if valid_tickers:
        valid_prices = prices[valid_tickers]
        mu = get_expected_returns(valid_prices)
        weights, performance_data = efficient_cvar(valid_prices, mu, target_cvar=target_cvar)
        allocations, leftover = perform_discrete_allocation(weights, valid_prices, total_portfolio_value=total_portfolio_value)
        performance_data = performance_data['MVO']
        performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}
    else:
        weights, allocations, leftover, performance_data = {}, {}, 0, {}

    response = {
        "weights": weights,
        "allocations": allocations,
        "leftover": leftover,
        "performance": performance_data,
        "errors": errors
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
    prices, valid_tickers, errors = download_prices(tickers)
        
    if valid_tickers:
        valid_prices = prices[valid_tickers]
            
            # Optimize portfolio using HRP
        weights, performance_data = optimize_hrp(valid_prices)
            
            # Perform discrete allocation
        allocations, leftover = perform_discrete_allocation(weights, valid_prices, total_portfolio_value=total_portfolio_value)
        performance_data = performance_data['MVO']
        performance_data = {key: value if not isnan(value) else None for key, value in performance_data.items()}
    else:
        weights, allocations, leftover, performance_data = {}, {}, 0, {}

        # Prepare response
    response = {
            "weights": weights,
            "allocations": allocations,
            "leftover": leftover,
            "performance": performance_data,
            "errors": errors
        }
    
    # Return response as JSON
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)