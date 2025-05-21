import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
import numpy as np

# Sliders for user input
lumpsum_slider = widgets.IntSlider(value=100000, min=0, max=10000000, step=1000, description="Lumpsum (₹)")
monthly_sip_slider = widgets.IntSlider(value=10000, min=0, max=50000, step=1000, description="Monthly SIP (₹)")
step_up_pct_slider = widgets.IntSlider(value=5, min=0, max=100, step=1, description="Step-up % /yr")
step_up_amt_slider = widgets.IntSlider(value=1000, min=0, max=20000, step=100, description="Step-up Amt (₹)")
step_up_mode_slider = widgets.RadioButtons(options=['Percent', 'Fixed Amount'], description='Step-up mode')
return_slider = widgets.FloatSlider(value=0.12, min=0.05, max=0.20, step=0.01, description="Annual Return %")
years_slider = widgets.IntSlider(value=15, min=1, max=30, step=1, description="Years")

# Simulation function
def simulate_investment(lumpsum, monthly_sip, step_up_pct, step_up_amt, step_up_mode, annual_return, years):
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

        # Apply step-up
        if step_up_mode == 'Percent':
            sip *= (1 + step_up_pct / 100)
        elif step_up_mode == 'Fixed Amount':
            sip += step_up_amt

    # Plotting the growth
    years_range = list(range(0, years + 1))
    plt.figure(figsize=(10, 5))
    plt.plot(years_range, portfolio_values, label='Portfolio Value', linewidth=2)
    plt.plot(years_range, invested_values, label='Total Invested', linestyle='--', linewidth=2)

    plt.title("Investment Growth vs Total Invested")
    plt.xlabel("Years")
    plt.ylabel("Amount (₹)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
import numpy as np

# Sliders for user input
lumpsum_slider = widgets.IntSlider(value=100000, min=0, max=10000000, step=1000, description="Lumpsum (₹)")
monthly_sip_slider = widgets.IntSlider(value=10000, min=0, max=50000, step=1000, description="Monthly SIP (₹)")
step_up_pct_slider = widgets.IntSlider(value=5, min=0, max=100, step=1, description="Step-up % /yr")
step_up_amt_slider = widgets.IntSlider(value=1000, min=0, max=20000, step=100, description="Step-up Amt (₹)")
step_up_mode_slider = widgets.RadioButtons(options=['Percent', 'Fixed Amount'], description='Step-up mode')
return_slider = widgets.FloatSlider(value=0.12, min=0.05, max=0.20, step=0.01, description="Annual Return %")
years_slider = widgets.IntSlider(value=15, min=1, max=30, step=1, description="Years")

# Simulation function
def simulate_investment(lumpsum, monthly_sip, step_up_pct, step_up_amt, step_up_mode, annual_return, years):
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

        # Apply step-up
        if step_up_mode == 'Percent':
            sip *= (1 + step_up_pct / 100)
        elif step_up_mode == 'Fixed Amount':
            sip += step_up_amt

    # Plotting the growth
    years_range = list(range(0, years + 1))
    plt.figure(figsize=(10, 5))
    plt.plot(years_range, portfolio_values, label='Portfolio Value', linewidth=2)
    plt.plot(years_range, invested_values, label='Total Invested', linestyle='--', linewidth=2)

    plt.title("Investment Growth vs Total Invested")
    plt.xlabel("Years")
    plt.ylabel("Amount (₹)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print(f"\nFinal Portfolio Value after {years} years: ₹{round(portfolio_values[-1]):,}")
    print(f"Total Invested after {years} years: ₹{round(invested_values[-1]):,}")

# Link sliders to the simulation function
interactive_plot = widgets.interactive(simulate_investment,
                                       lumpsum=lumpsum_slider,
                                       monthly_sip=monthly_sip_slider,
                                       step_up_pct=step_up_pct_slider,
                                       step_up_amt=step_up_amt_slider,
                                       step_up_mode=step_up_mode_slider,
                                       annual_return=return_slider,
                                       years=years_slider)

# Display the sliders and the output
display(interactive_plot)
