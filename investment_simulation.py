import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Page Setup ---
st.set_page_config(page_title="Investment Growth Simulator", layout="centered")
st.markdown("""
# 💰 Investment Growth Simulator

Visualize how your portfolio grows over time with:
- 📦 One-time **lumpsum**
- 💸 Monthly **SIP**
- ⏫ Annual **step-up** (percent or fixed)
- 📈 Customizable **return** & **duration**

---
""")

# --- User Inputs ---
lumpsum = st.slider("Lumpsum Investment (₹)", min_value=0, max_value=10_000_000, value=100_000, step=10_000)
monthly_sip = st.slider("Monthly SIP (₹)", min_value=0, max_value=100_000, value=10_000, step=1_000)
step_up_mode = st.radio("Step-Up Mode", options=["Percent", "Fixed Amount"])
step_up_pct = st.slider("Step-Up % / Year", min_value=0, max_value=100, value=5, step=1) if step_up_mode == "Percent" else 0
step_up_amt = st.slider("Step-Up Amount (₹ / year)", min_value=0, max_value=50_000, value=1_000, step=500) if step_up_mode == "Fixed Amount" else 0
annual_return = st.slider("Expected Annual Return (%)", min_value=5.0, max_value=20.0, value=12.0, step=0.1) / 100
years = st.slider("Investment Duration (Years)", min_value=1, max_value=40, value=15, step=1)

# --- Simulation ---
def simulate(lumpsum, sip, step_up_pct, step_up_amt, step_mode, rate, years):
    portfolio = [lumpsum]
    invested = [lumpsum]
    current_sip = sip
    total_invested = lumpsum
    current_value = lumpsum

    for year in range(1, years + 1):
        for month in range(12):
            current_value = current_value * (1 + rate / 12) + current_sip
            total_invested += current_sip
        portfolio.append(current_value)
        invested.append(total_invested)

        if step_mode == "Percent":
            current_sip *= (1 + step_up_pct / 100)
        elif step_mode == "Fixed Amount":
            current_sip += step_up_amt

    return portfolio, invested

portfolio, invested = simulate(lumpsum, monthly_sip, step_up_pct, step_up_amt, step_up_mode, annual_return, years)

# --- Plot ---
st.subheader("📊 Investment Growth Chart")
fig, ax = plt.subplots(figsize=(10, 4))
years_range = np.arange(0, years + 1)

ax.plot(years_range, portfolio, label="Portfolio Value", linewidth=2)
ax.plot(years_range, invested, label="Total Invested", linestyle="--", linewidth=2)
ax.set_xlabel("Year")
ax.set_ylabel("Amount (₹)")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# --- Summary ---
st.markdown("---")
st.success(f"**Final Portfolio Value**: ₹{round(portfolio[-1]):,}")
st.info(f"**Total Amount Invested**: ₹{round(invested[-1]):,}")

st.markdown("---")
st.markdown("Made with ❤️ by Avik & Nandita")
