function displayAllocations(data) {
    const allocations = data.allocations;
    const leftover = data.leftover;
    const weights = data.weights;

    let allocationList = "";
    for (const [ticker, allocation] of Object.entries(allocations)) {
        allocationList += `<li class="list-group-item">Buy ${allocation} shares of ${ticker}</li>`;
    }

    const cardHTML = `
        <div class="card">
            <div class="card-header">
                Allocations
            </div>
            <div class="card-body">
                <h5 class="card-title">Allocations Details</h5>
                <ul class="list-group">
                    ${allocationList}
                </ul>
                <p class="card-text">Leftover: $${leftover.toFixed(2)}</p>
            </div>
        </div>
    `;

    document.getElementById("allocationsCard").innerHTML = cardHTML;
}




function optimizeMinVolatility() {
    const formData = new FormData(document.getElementById("minVolatilityForm"));
    const tickers = formData.get("tickers").split(",");
    const totalPortfolioValue = parseInt(formData.get("totalPortfolioValue"));

    fetch("http://127.0.0.1:5000/optimize_min_volatility", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ tickers: tickers, total_portfolio_value: totalPortfolioValue })
    })
    .then(response => response.json())
    .then(data => {
        displayAllocations(data);

    });
}

function optimizeMaxSharpe() {
    const formData = new FormData(document.getElementById("maxSharpeForm"));
    const tickers = formData.get("tickers").split(",");

    fetch("http://127.0.0.1:5000/max_sharpe_with_sector_constraints", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ tickers: tickers })
    })
    .then(response => response.json())
    .then(data => {
        displayAllocations(data);

    });
}

function maximizeReturnGivenRisk() {
    const formData = new FormData(document.getElementById("maximizeReturnGivenRiskForm"));
    const tickers = formData.get("tickers").split(",");
    const targetVolatility = parseFloat(formData.get("targetVolatility"));

    fetch("http://127.0.0.1:5000/maximize_return_given_risk", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ tickers: tickers, target_volatility: targetVolatility })
    })
    .then(response => response.json())
    .then(data => {
        displayAllocations(data);

    });
}

function minimizeRiskGivenReturn() {
    const formData = new FormData(document.getElementById("minimizeRiskGivenReturnForm"));
    const tickers = formData.get("tickers").split(",");
    const targetReturn = parseFloat(formData.get("targetReturn"));

    fetch("http://127.0.0.1:5000/minimize_risk_given_return", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ tickers: tickers, target_return: targetReturn })
    })
    .then(response => response.json())
    .then(data => {
        displayAllocations(data);

    });
}

function efficientSemivariance() {
    const formData = new FormData(document.getElementById("efficientSemivarianceForm"));
    const tickers = formData.get("tickers").split(",");
    const targetReturn = parseFloat(formData.get("targetReturn"));

    fetch("http://127.0.0.1:5000/efficient_semivariance", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ tickers: tickers, target_return: targetReturn })
    })
    .then(response => response.json())
    .then(data => {
        displayAllocations(data);

    });
}

function efficientCVaR() {
    const formData = new FormData(document.getElementById("efficientCVaRForm"));
    const tickers = formData.get("tickers").split(",");
    const targetCVaR = parseFloat(formData.get("targetCVaR"));

    fetch("http://127.0.0.1:5000/efficient_cvar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ tickers: tickers, target_cvar: targetCVaR })
    })
    .then(response => response.json())
    .then(data => {
        displayAllocations(data);

    });
}

function optimizeHRP() {
    // Get form data
    var tickers = document.getElementById("hrpTickers").value;

    // Prepare payload
    var payload = {
        tickers: tickers.split(",").map(function(item) {
            return item.trim();
        })
    };

    // Send POST request to API endpoint
    fetch("http://127.0.0.1:5000/optimize_hrp", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        // Display allocations card
        displayAllocations(data);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

