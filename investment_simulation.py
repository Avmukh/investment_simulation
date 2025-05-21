import streamlit as st
import numpy as np
from babel.numbers import format_currency
import matplotlib.pyplot as plt

st.set_page_config(page_title="Investment Growth Simulator", layout="centered")
st.markdown("""
# 💰 Investment Growth Simulator

Visualize how your portfolio grows over time with:
- 📦 One-time **lumpsum**
- 💸 Monthly **SIP**
- ⏫ Annual **step-up** (percent or fixed)
- 📈 Customizable **return** & **duration**

---("Enjoy & remember!! Don't care what anyone says. Being rich is a good thing.")

""""")
st.markdown(
    """
    <div style='text-align: right;'>
       ---"Made with the effort of Sri Avimukh"
    </div>
    """,
    unsafe_allow_html=True
)


# Input sliders
st.write("")  # adds one blank line
st.text("")   # also adds one blank line

lumpsum = st.slider("Lumpsum (₹)", 0, 10_000_000, 100_000, step=1000)
monthly_sip = st.slider("Monthly SIP (₹)", 0, 100_000, 10_000, step=1000)
step_up_mode = st.radio("Step-up mode", ['Percent', 'Fixed Amount'])
step_up_pct = 0
step_up_amt = 0
if step_up_mode == 'Percent':
    step_up_pct = st.slider("Step-up % /yr", 0, 100, 5, step=1)
else:
    step_up_amt = st.slider("Step-up Amount /yr (₹)", 0, 20_000, 1000, step=100)

annual_return = st.slider("Annual Return %", 5, 20, 12, step=1) / 100
years = st.slider("Years", 1, 30, 15)

# Simulation logic
future_value = lumpsum
invested = lumpsum
sip = monthly_sip

portfolio_values = [future_value]
invested_values = [invested]

for year in range(1, years + 1):
    for month in range(12):
        future_value = future_value * (1 + annual_return / 12) + sip
        invested += sip
    portfolio_values.append(future_value)
    invested_values.append(invested)

    # Step-up adjustment
    if step_up_mode == 'Percent':
        sip *= (1 + step_up_pct / 100)
    else:
        sip += step_up_amt

# Plotting
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(0, years + 1), portfolio_values, label='Portfolio Value', linewidth=2)
ax.plot(range(0, years + 1), invested_values, label='Total Invested', linestyle='--', linewidth=2)
ax.set_title("Investment Growth vs Total Invested")
ax.set_xlabel("Years")
ax.set_ylabel("Amount (₹)")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Display final amounts with Indian formatting
final_val = round(portfolio_values[-1])
invested_val = round(invested_values[-1])

st.success(f"**Final Portfolio Value:** {format_currency(final_val, 'INR', locale='en_IN')}")
st.info(f"**Total Amount Invested:** {format_currency(invested_val, 'INR', locale='en_IN')}")

# Footer / Credit

st.markdown("---")
st.markdown("Made with ❤️ by Avik & Nandita")
