import streamlit as st
import matplotlib.pyplot as plt

# Sidebar inputs
st.sidebar.header("Investment Parameters")
lumpsum = st.sidebar.slider("Lumpsum (₹)", 0, 10000000, 100000, step=1000)
monthly_sip = st.sidebar.slider("Monthly SIP (₹)", 0, 50000, 10000, step=1000)
step_up_mode = st.sidebar.radio("Step-up Mode", ["Percent", "Fixed Amount"])
step_up_pct = st.sidebar.slider("Step-up % /yr", 0, 100, 5) if step_up_mode == "Percent" else 0
step_up_amt = st.sidebar.slider("Step-up Amount /yr (₹)", 0, 20000, 1000, step=100) if step_up_mode == "Fixed Amount" else 0
annual_return = st.sidebar.slider("Annual Return (%)", 5.0, 20.0, 12.0, step=0.5) / 100
years = st.sidebar.slider("Investment Duration (Years)", 1, 30, 15)

# Simulation
def simulate(lumpsum, sip, mode, pct, amt, rate, years):
    fv = lumpsum
    invested = lumpsum
    portfolio_values = [fv]
    invested_values = [invested]

    for year in range(1, years + 1):
        for month in range(12):
            fv = fv * (1 + rate / 12) + sip
            invested += sip
        portfolio_values.append(fv)
        invested_values.append(invested)

        # Apply step-up
        if mode == "Percent":
            sip *= (1 + pct / 100)
        elif mode == "Fixed Amount":
            sip += amt

    return portfolio_values, invested_values

portfolio, invested = simulate(lumpsum, monthly_sip, step_up_mode, step_up_pct, step_up_amt, annual_return, years)

# Plotting
st.title("📈 Investment Growth vs Total Invested")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(0, years + 1), portfolio, label="Portfolio Value", linewidth=2)
ax.plot(range(0, years + 1), invested, label="Total Invested", linestyle="--", linewidth=2)
ax.set_xlabel("Years")
ax.set_ylabel("Amount (₹)")
ax.set_title("Growth Over Time")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Final numbers
st.subheader("💰 Final Portfolio Summary")
st.markdown
