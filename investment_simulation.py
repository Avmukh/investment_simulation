import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from babel.numbers import format_currency

# --- Page Setup ---
st.set_page_config(page_title="Investment Growth Simulator", layout="centered")
st.markdown("""
# 💰 Investment Growth Simulator

Visualize how your portfolio grows over time with:
- 📦 One-time **lumpsum**
- 💸 Monthly **SIP**
- ⏫ Annual **step-up** (percent or fixed)
- 📈 Customizable **return** & **duration**

---("Enjoy & Remember!! Don't care what anyone says. Being rich is a good thing.")
""")

st.markdown(
    "<div style='text-align: right;'>---\"Made with the effort of Sri Avmukh\"</div>",
    unsafe_allow_html=True
)
"")

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
annual_return = synced_slider("Annual Return %", 5, 20, 12, 1, "return") / 100
years = synced_slider("Years", 1, 30, 15, 1, "years")

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

 

# --- Footer ---
st.markdown(
    "<hr style='margin-top:140px;'><div style='text-align:center;'>Made with ❤️ by <b>Avik & Nandita</b></div>",
    unsafe_allow_html=True
)
