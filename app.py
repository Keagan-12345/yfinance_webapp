from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    ticker_symbol = "AAPL"  # default
    data = {}
    
    if request.method == "POST":
        ticker_symbol = request.form["ticker"].upper()
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # Fetch last 1 year historical data
        hist = ticker.history(period="1y")
        data["history"] = hist.tail(10).to_html(classes="table table-striped")
        
        # Company info
        info = ticker.info
        data["info"] = pd.DataFrame(list(info.items()), columns=["Attribute", "Value"]).to_html(classes="table table-bordered")
        
    except Exception as e:
        data["error"] = str(e)

    return render_template("index.html", ticker=ticker_symbol, data=data)

if __name__ == "__main__":
    app.run(debug=True)
