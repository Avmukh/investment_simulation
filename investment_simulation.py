import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from babel.numbers import format_currency

# --- Page Setup ---
st.set_page_config(page_title="Investment Growth Simulator", layout="centered")
st.markdown("""
# 💰 Investment Planning Calculator


Visualize how your portfolio grows over time with:
- 📦 One-time **lumpsum**
- 💸 Monthly **SIP**
- ⬆️ Annual **step-up** (percent or fixed)
- 📈 Customizable **return** & **duration**

---("Enjoy & Remember!! Don't care what anyone says. Being rich is a good thing.")
""")

st.markdown(
     "<div style='text-align: right; margin-bottom: 40px;'>---\"Presented by Sri Avmukh & NM FinServ\"</div>",
    unsafe_allow_html=True
)

# --- Helper: Synced Slider + Number Input ---
def synced_slider(label, min_val, max_val, default, step, key_base):
    slider_key = f"{key_base}_slider"
    input_key = f"{key_base}_num"

    if key_base not in st.session_state:
        st.session_state[key_base] = default

    col1, col2 = st.columns([3, 1])
    with col1:
        slider_val = st.slider(label, min_val, max_val, st.session_state[key_base], step=step, key=slider_key)
    with col2:
        input_val = st.number_input("", min_val, max_val, st.session_state[key_base], step=step, key=input_key)

    # Sync logic
    if slider_val != st.session_state[key_base]:
        st.session_state[key_base] = slider_val
    elif input_val != st.session_state[key_base]:
        st.session_state[key_base] = input_val

    return st.session_state[key_base]

# --- Inputs ---
lumpsum = synced_slider("Lumpsum (₹)", 0, 10_000_000, 100_000, 1000, "lumpsum")
monthly_sip = synced_slider("Monthly SIP (₹)", 0, 100_000, 10_000, 1000, "sip")
step_up_mode = st.radio("Step-up mode", ['Percent', 'Fixed Amount'])
step_up_pct = synced_slider("Step-up % /yr", 0, 100, 5, 1, "stepup_pct") if step_up_mode == 'Percent' else 0
step_up_amt = synced_slider("Step-up Amount /yr (₹)", 0, 20_000, 1000, 100, "stepup_amt") if step_up_mode == 'Fixed Amount' else 0
annual_return = synced_slider("Annual Return %", 5, 100, 12, 1, "return") / 100
years = synced_slider("Years", 1, 50, 15, 1, "years")

# --- Control Buttons ---
col_run, col_anim = st.columns([1, 2])
run_simulation = col_run.button("▶️ Run Simulation")
animate = col_anim.checkbox("🔄 Animate Chart (Year + Month)", value=True)

if "run" not in st.session_state:
    st.session_state.run = False
if run_simulation:
    st.session_state.run = True

# --- Simulation & Animation ---
if st.session_state.run:
    future_value = lumpsum
    invested = lumpsum
    sip = monthly_sip

    portfolio_values = [future_value]
    invested_values = [invested]

    chart_placeholder = st.empty()
    progress_bar = st.progress(0, text="Starting simulation...")

    total_steps = years * 12
    step_count = 0

    for year in range(1, years + 1):
        for month in range(12):
            future_value = future_value * (1 + annual_return / 12) + sip
            invested += sip
            portfolio_values.append(future_value)
            invested_values.append(invested)
            step_count += 1

            if animate:
                fig, ax = plt.subplots(figsize=(10, 5))
                months_elapsed = range(step_count + 1)
                ax.plot(months_elapsed, portfolio_values, label='Portfolio Value', linewidth=2)
                ax.plot(months_elapsed, invested_values, label='Total Invested', linestyle='--', linewidth=2)
                ax.set_title("Investment Growth vs Total Invested")
                ax.set_xlabel("Months")
                ax.set_ylabel("Amount (₹)")
                ax.grid(True)
                ax.legend()
                chart_placeholder.pyplot(fig)
                progress_bar.progress(step_count / total_steps, text=f"Year {year}, Month {month + 1}")
                time.sleep(0.05)

        # Apply step-up after each year
        if step_up_mode == 'Percent':
            sip *= (1 + step_up_pct / 100)
        else:
            sip += step_up_amt

    # Final Static Chart
    fig, ax = plt.subplots(figsize=(10, 5))
    months_elapsed = range(len(portfolio_values))
    ax.plot(months_elapsed, portfolio_values, label='Portfolio Value', linewidth=2)
    ax.plot(months_elapsed, invested_values, label='Total Invested', linestyle='--', linewidth=2)
    ax.set_title("Investment Growth vs Total Invested")
    ax.set_xlabel("Months")
    ax.set_ylabel("Amount (₹)")
    ax.grid(True)
    ax.legend()
    chart_placeholder.pyplot(fig)
    progress_bar.empty()

    # --- Final Output ---
    final_val = round(portfolio_values[-1])
    invested_val = round(invested_values[-1])
    st.success(f"**Final Portfolio Value:** {format_currency(final_val, 'INR', locale='en_IN')}")
    st.info(f"**Total Amount Invested:** {format_currency(invested_val, 'INR', locale='en_IN')}")

    # CAGR Calculation
    cagr = ((portfolio_values[-1] / invested_values[-1]) ** (1 / years) - 1) * 100
    st.metric("CAGR (%)", f"{cagr:.2f}")

    # --- Inflation Input ---
    st.markdown("### 🧼 Additional Metrics")
    inflation_rate = st.slider("Assumed Inflation Rate (%)", 0.0, 15.0, 6.0, 0.1)

    # --- Real Return Calculation ---
    real_return = ((1 + annual_return) / (1 + inflation_rate / 100)) - 1
    real_cagr = ((portfolio_values[-1] / invested_values[-1]) ** (1 / years) - 1)
    real_cagr_adjusted = ((1 + real_cagr) / (1 + inflation_rate / 100)) - 1

    # --- Display ---
    st.metric("Inflation-Adjusted Annual Return", f"{real_return*100:.2f}%")

# --- Explanatory Content ---
with st.expander("ℹ️ What's the difference between Annual Return and CAGR?"):
    st.markdown("""
    **Annual Return** is the expected return you enter for simulation – it’s a fixed growth assumption.

    **CAGR** (Compound Annual Growth Rate) reflects the actual average yearly growth based on your entire investment behavior (lumpsum, SIP, step-up) over the selected time period.

    Because money is added gradually (via SIPs and step-ups), the CAGR is usually **lower** than the Annual Return unless everything is invested upfront.
    """)

with st.expander("ℹ️ What's the difference between IRR and XIRR?"):
    st.markdown("""
**IRR** (Internal Rate of Return) is a metric used to evaluate the profitability of an investment. It assumes that all cash flows occur at regular intervals (e.g., monthly, yearly), which is not always the case in real life.

**XIRR** (Extended IRR) is a more accurate version of IRR. It allows for **irregular cash flows** – meaning it considers the actual dates when money is invested or withdrawn.

### 🔍 Key Difference:
- Use **IRR** when cash flows are **evenly spaced** (e.g., monthly SIPs).
- Use **XIRR** when cash flows are **irregular** (e.g., lumpsums added at random dates, redemptions).

In real-world mutual fund investing (especially with SIPs, redemptions, top-ups), **XIRR gives a more realistic return**.
""")

with st.expander("ℹ️ Understanding Returns: CAGR, Annualized Return & Inflation Adjustment"):
    st.markdown("""
### 📈 **Annualized Return**
This is the **constant yearly return** that would result in the same final value as your actual investment growth. It assumes **compounded growth**.

### ♻️ **CAGR (Compound Annual Growth Rate)**
- CAGR is a type of annualized return.
- It reflects the **smoothed yearly rate** at which your investment grew from **beginning to end**, ignoring intermediate ups and downs.
- Formula:  
  = (Final_Value / Total_Invested) ^ (1 / Years) - 1.

> **Use CAGR** to compare long-term investment performance across different options.

---

### 💸 **Inflation-Adjusted Return (Real Return)**
- Shows how much your investment actually **grew in purchasing power**.
- Adjusted for inflation to show **real wealth gain**.
- Formula:  
  =(1 + Nominal_Return_Cell) / (1 + Inflation_Rate_Cell) - 1


> Even if your investment grew at 12%, if inflation was 6%, your **real return is only ~5.66%**.

---

### 🧠 Summary
| Term                     | Adjusts for Inflation | Uses Compounding | Real-World Use Case |
|--------------------------|-----------------------|------------------|---------------------|
| Annual Return            | ❌                    | ✅               | Target or Assumption |
| CAGR                     | ❌                    | ✅               | Measuring actual growth |
| Inflation-Adjusted Return| ✅                    | ✅               | Real wealth growth |
| XIRR                    | ❌ (or ✅ if adjusted) | ✅               | Irregular cash flows |

Always evaluate investments in **real terms**, not just nominal numbers.
""")

with st.expander("ℹ️ What's Nominal vs Real Return?"):
    st.markdown("""
    - **Nominal Return** is the return you see before accounting for inflation.
    - **Real Return** shows how much your purchasing power actually increased.

    ### Example:
    If your portfolio grew 12% annually, but inflation was 6%:
    
     Real Return = (1 + 0.12) / (1 + 0.06) - 1 = 0.0566 = 5.66%


    > Always consider **real return** to know how much wealth you’re really building.
    """)
# --- Footer ---
st.markdown(
    "<hr style='margin-top:40px;'><div style='text-align:center;'>Made with ❤️ by <b>Avik & Nandita (Mukherjee) </b></div>",
    unsafe_allow_html=True
)
