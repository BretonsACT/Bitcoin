import streamlit as st
import pandas as pd

def get_recommendation(risk, horizon, goal, knowledge, decentralization):
    """
    Analyzes user input to provide an investment recommendation.
    """
    etf_score = 0
    btc_score = 0

    # --- Scoring Logic ---

    # 1. Risk Tolerance
    if risk == "Low (Protect my capital)":
        etf_score += 3
    elif risk == "Medium (Balanced growth and safety)":
        etf_score += 2
        btc_score += 1
    elif risk == "High (Aggressive growth is the priority)":
        etf_score += 1
        btc_score += 2
    elif risk == "Very High (Willing to take significant risks for maximal returns)":
        btc_score += 3

    # 2. Investment Horizon
    if horizon <= 3: # Short term
        btc_score += 2
    elif 3 < horizon <= 10: # Medium term
        etf_score += 1
        btc_score += 1
    else: # Long term
        etf_score += 2

    # 3. Primary Goal
    if goal == "Wealth Preservation":
        etf_score += 3
    elif goal == "Steady, Compounded Growth":
        etf_score += 2
    elif goal == "Aggressive Growth":
        btc_score += 2
        etf_score += 1
    elif goal == "High-Risk Speculation":
        btc_score += 3

    # 4. Technical Knowledge / Management Style
    if knowledge == "I want a simple, hands-off investment.":
        etf_score += 2
    else:
        btc_score += 2

    # 5. View on Decentralization
    if decentralization == "I prefer regulated, traditional financial systems.":
        etf_score += 2
    elif decentralization == "It's interesting, but not a primary factor.":
        etf_score += 1
        btc_score += 1
    else:
        btc_score += 2

    # --- Generate Recommendation ---
    if etf_score > btc_score + 3:
        return (
            "Strongly Leans: ETF",
            "Your profile indicates a strong preference for stability, long-term growth, and regulated markets. "
            "A diversified ETF, such as one tracking a broad market index like the S&P 500, aligns very well with your goals. "
            "It offers a hands-off approach to investing with lower volatility compared to single assets.",
            "success"
        )
    elif btc_score > etf_score + 3:
        return (
            "Strongly Leans: Bitcoin",
            "Your profile suggests a high tolerance for risk and a focus on aggressive, potentially speculative growth. "
            "You value direct asset control and are comfortable with the technical aspects of digital assets. "
            "Directly holding Bitcoin aligns with your appetite for high returns and acceptance of volatility.",
            "success"
        )
    elif etf_score > btc_score:
        return (
            "Leans: ETF",
            "Your profile leans towards a preference for safety and diversification. While you might be open to some risk, "
            "the structured and diversified nature of an ETF seems to be a better fit for your primary goals. "
            "You could consider a smaller allocation to higher-risk assets if you wish, but the core of your strategy points towards ETFs.",
            "info"
        )
    elif btc_score > etf_score:
        return (
            "Leans: Bitcoin",
            "Your profile shows an interest in higher growth potential and you're not afraid of taking on risk. "
            "While you appreciate some traditional aspects, your goals align more with the high-growth nature of Bitcoin. "
            "Ensure you fully understand the volatility and security responsibilities before investing.",
            "info"
        )
    else:
        return (
            "Balanced View: Consider Both",
            "Your profile is well-balanced between seeking growth and managing risk. A hybrid approach could be suitable for you. "
            "This might involve a core holding in diversified ETFs for stability, complemented by a smaller, speculative position in Bitcoin "
            "to capture potential upside. This allows you to have a solid foundation while still participating in a high-growth asset class.",
            "warning"
        )


def display_market_indicators():
    """
    Displays fictional market indicators for educational purposes.
    """
    st.subheader("Simulated Market Indicators")
    st.markdown(
        "These are *for demonstration only* and do not represent live market data. They illustrate the types of indicators you might look at."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Broad Market ETF (e.g., S&P 500)")
        # --- ETF Indicators ---
        st.metric(label="Market Trend (50/200 Day MA)", value="Bullish", delta="Golden Cross")
        st.metric(label="Relative Strength Index (RSI)", value="62 (Neutral)", delta="0.5")
        st.metric(label="Volatility Index (VIX)", value="17.5 (Low)", delta="-1.2", delta_color="inverse")


    with col2:
        st.markdown("#### ₿ Bitcoin")
        # --- Bitcoin Indicators ---
        st.metric(label="Market Trend (MACD)", value="Bearish", delta="Negative Crossover", delta_color="inverse")
        st.metric(label="Relative Strength Index (RSI)", value="45 (Neutral)", delta="-2.1")
        st.metric(label="On-Chain Sentiment (Hash Rate)", value="Strong", delta="All-Time High")


# --- Streamlit App Layout ---

st.set_page_config(layout="wide", page_title="Investment Decision Helper")

st.title("Investment Helper: ETF or Bitcoin?")
st.markdown(
    "This tool helps you analyze your investment profile to see which asset might be a better fit for you. "
    "Answer the questions in the sidebar to get your personalized feedback."
)
st.markdown("---")


# --- Sidebar for User Input ---
st.sidebar.header("Your Investor Profile")

risk_tolerance = st.sidebar.selectbox(
    "1. What is your risk tolerance?",
    ("Low (Protect my capital)", "Medium (Balanced growth and safety)", "High (Aggressive growth is the priority)", "Very High (Willing to take significant risks for maximal returns)")
)

investment_horizon = st.sidebar.slider(
    "2. What is your investment time horizon (in years)?",
    min_value=1, max_value=30, value=10, step=1
)

investment_goal = st.sidebar.radio(
    "3. What is your primary investment goal?",
    ("Wealth Preservation", "Steady, Compounded Growth", "Aggressive Growth", "High-Risk Speculation")
)

technical_knowledge = st.sidebar.radio(
    "4. How involved do you want to be?",
    ("I want a simple, hands-off investment.", "I'm willing to learn and manage my own digital assets.")
)

decentralization_view = st.sidebar.radio(
    "5. What's your view on decentralization vs. regulation?",
    ("I prefer regulated, traditional financial systems.", "It's interesting, but not a primary factor.", "Decentralization and self-custody are important to me.")
)


# --- Main Panel for Results ---

# Get and display recommendation
recommendation, explanation, alert_type = get_recommendation(
    risk_tolerance, investment_horizon, investment_goal, technical_knowledge, decentralization_view
)

st.header("Your Personalized Recommendation")

if alert_type == "success":
    st.success(f"**{recommendation}**")
elif alert_type == "info":
    st.info(f"**{recommendation}**")
else:
    st.warning(f"**{recommendation}**")

st.write(explanation)

st.markdown("---")

# Display market indicators
display_market_indicators()

st.markdown("---")
st.warning("**Disclaimer:** This is a tool for educational purposes only and does not constitute financial advice. Always do your own research and consult with a qualified financial advisor before making any investment decisions.")
