function displayAllocations(data) {
    const allocations = data.allocations;
    const leftover = data.leftover;
    const performance_data = data.performance;
    const errors = data.errors;

    let allocationList = "";
    for (const [asset, allocation] of Object.entries(allocations)) {
        allocationList += `<li class="list-group-item">${allocation}</li>`;
    }

    let performanceText = '';
    if (performance_data) {
        if ('Expected annual return' in performance_data && performance_data['Expected annual return'] !== null) {
            performanceText += `<p class="card-text">Expected Annual Return: ${performance_data['Expected annual return'].toFixed(2)* 100}%</p>`;
        }
        if ('Sharpe Ratio' in performance_data && performance_data['Sharpe Ratio'] !== null) {
            performanceText += `<p class="card-text">Sharpe Ratio: ${performance_data['Sharpe Ratio'].toFixed(2)}</p>`;
        }

        if ('Conditional Value at Risk' in performance_data && performance_data['Conditional Value at Risk'] !== null) {
            performanceText += `<p class="card-text">Conditional Value at Risk: ${performance_data['Conditional Value at Risk'].toFixed(2)* 100}%</p>`;
        }
        if ('Annual semi-deviation' in performance_data && performance_data['Annual semi-deviation'] !== null) {
            performanceText += `<p class="card-text">Annual Semi-Deviation: ${performance_data['Annual semi-deviation'].toFixed(2)* 100}%</p>`;
        }
        if ('Sortino Ratio' in performance_data && performance_data['Sortino Ratio'] !== null) {
            performanceText += `<p class="card-text">Sortino Ratio: ${performance_data['Sortino Ratio'].toFixed(2)}</p>`;
        }
        if ('Annual volatility' in performance_data && performance_data['Annual volatility'] !== null) {
            performanceText += `<p class="card-text">Annual Volatility: ${performance_data['Annual volatility'].toFixed(2)* 100}%</p>`;
        }
        // Add additional checks for other performance metrics here
    }
    let errorText = '';
    if (errors) {
        for (const [ticker, error] of Object.entries(errors)) {
            errorText += `<p class="text-danger">Error with ${ticker}: ${error}</p>`;
        }
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
                ${performanceText}
                ${errorText}
            </div>
        </div>
        <div id="donutChart"></div>
    `;

    document.getElementById("allocationsCard").innerHTML = cardHTML;
        // Extract weights from the data
        const weights = data.weights;
        const labels = Object.keys(weights);
        const series = Object.values(weights);
    
        // Generate the chart using ApexCharts
        new ApexCharts(document.querySelector("#donutChart"), {
            series: series,
            chart: {
                height: 350,
                type: 'donut',
                toolbar: {
                    show: true
                }
            },
            labels: labels,
        }).render();
    
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
        console.log(data)
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

    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to fetch data. Status: " + response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.message) {
            // Display error message on the frontend
            displayErrorMessage(data.message);
        } else {
            // Process and display data as usual
            displayAllocations(data);
            console.log(data);
        }
    })
    .catch(error => {
        // Handle generic error (e.g., network issues)
        displayErrorMessage("An error occurred: " + error.message);
    });
}

function displayErrorMessage(message) {
    // Display the error message on the frontend (e.g., in a div with id="error-message")
    document.getElementById("error-message").innerText = message;
    document.getElementById("error-message").style.display = "block";
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

document.addEventListener("DOMContentLoaded", () => {
    new ApexCharts(document.querySelector("#donutChart"), {
      series: [44, 55, 13, 43, 22],
      chart: {
        height: 350,
        type: 'donut',
        toolbar: {
          show: true
        }
      },
      labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
    }).render();
  });

