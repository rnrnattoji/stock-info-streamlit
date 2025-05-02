import yfinance as yf
from datetime import datetime
import pytz
import streamlit as st

def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        name = info.get("longName", "N/A")
        current_price = info.get("regularMarketPrice")
        previous_close = info.get("regularMarketPreviousClose")

        if current_price is None or previous_close is None:
            return {"error": f"Data not available for symbol: {symbol}"}

        change = current_price - previous_close
        percent_change = (change / previous_close) * 100
        sign = "+" if change >= 0 else "-"

        # Get current time in US/Pacific
        current_time = datetime.now(pytz.timezone('US/Pacific')).strftime("%a %b %d %H:%M:%S %Z %Y")

        return {
            "time": current_time,
            "name": name,
            "price": f"{current_price:.2f}",
            "change": f"{sign}{abs(change):.2f}",
            "percent": f"{sign}{abs(percent_change):.2f}%"
        }

    except Exception as e:
        return {"error": str(e)}

# Streamlit UI
st.title("📈 Stock Info Viewer")

symbol = st.text_input("Enter a stock symbol (e.g., AAPL, TSLA, ADBE):")

if symbol:
    result = get_stock_data(symbol.upper())
    if "error" in result:
        st.error(result["error"])
    else:
        st.write(f"🕒 **{result['time']}**")
        st.subheader(f"🏢 {result['name']} ({symbol.upper()})")
        st.markdown(f"💲 **{result['price']}**  {result['change']} ({result['percent']})")
