import streamlit as st
import random
import time
import pandas as pd
import matplotlib.pyplot as plt

# Set the game title
st.title("Tea Cart Tycoon - Simulation")

# Initialize session state variables
if "day" not in st.session_state:
    st.session_state.day = 1
if "cash" not in st.session_state:
    st.session_state.cash = 15000  # Cash in Hand
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "weather" not in st.session_state:
    st.session_state.weather = "Sunny"  # Default weather
if "forecast" not in st.session_state:
    st.session_state.forecast = []  # Stores forecast for 2 locations
if "sales_summary" not in st.session_state:
    st.session_state.sales_summary = pd.DataFrame(columns=["Day", "Location 1", "Location 2", "Tea Sold", "Snacks Sold", "Revenue", "Cost", "Wastage", "Event"])
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Define game parameters
total_days = 15

# Locations Available
locations = ["Business District", "College Area", "Tourist Spot", "Residential Area", "Market Area"]

# **Location Selection for Business Hours**
st.subheader("📍 Select Locations for Business Hours (Morning & Evening)")
morning_location = st.selectbox("☀️ Morning Shift (8:00 AM - 2:00 PM)", locations, index=0)
evening_location = st.selectbox("🌙 Evening Shift (3:00 PM - 9:00 PM)", locations, index=1)

# Event Impact Data
event_impact = {
    "Business District": [
        ("Crowded - Office rush hour increased.", (20, 50)),
        ("Low footfall - Many employees working from home.", (-50, -30)),
        ("Trade fair happening - Increased visitors.", (30, 60))
    ],
    "College Area": [
        ("Full attendance - Exam season, students on campus.", (30, 60)),
        ("Preparation leave announced - Half the students are absent.", (-60, -40)),
        ("College festival today - Many visitors.", (50, 80))
    ],
    "Tourist Spot": [
        ("Peak tourist season - More footfall.", (40, 70)),
        ("Heavy rains - Fewer tourists visiting today.", (-60, -30)),
        ("Local attraction featured on social media.", (50, 80))
    ],
    "Residential Area": [
        ("Weekend - More people at home.", (15, 40)),
        ("Construction work nearby - Dust & noise reducing visitors.", (-50, -30))
    ],
    "Market Area": [
        ("Festival rush - Heavy shopping crowd.", (30, 60)),
        ("Month-end - People have less money left.", (-50, -20)),
        ("Vendor strike - Some shops closed.", (25, 50))
    ]
}

# **Forecast System: Generates for 2 random locations each day**
if st.session_state.day == 1 or st.button("📅 End Day & Generate Forecast"):
    st.session_state.forecast = random.sample(locations, 2)  # Pick 2 locations
    st.success("🔮 Tomorrow's Market Forecast:")
    for loc in st.session_state.forecast:
        forecast_event, _ = random.choice(event_impact[loc])  # Select random event
        st.write(f"📌 **{loc}** → *{forecast_event}*")

# **Weather Generation for Current Day**
if st.button("🎮 Play Day"):
    st.session_state.weather = random.choice(["Sunny", "Rainy", "Heavy Rains", "Cloudy", "Hot", "Cold", "Very Cold"])
    st.success(f"New Day Started! Weather: {st.session_state.weather}")

# **Display Current Day Weather**
st.subheader("☀️ Today's Weather")
st.write(f"🌤 **{st.session_state.weather}**")

# **Business Events for Today (Only for Selected Locations)**
st.subheader("📢 Event of the Day")
event_results = {}
for loc in [morning_location, evening_location]:  # Apply events only to selected locations
    event_tuple = random.choice(event_impact[loc])  
    if isinstance(event_tuple, tuple) and len(event_tuple) == 2:
        event, impact_range = event_tuple  
        min_impact, max_impact = sorted(impact_range)  
        impact = random.randint(min_impact, max_impact) if min_impact < max_impact else min_impact
        event_results[loc] = (event, impact)
        st.write(f"📌 **{loc}** → *{event}* → Impact: **{impact}%** sales change")

# **Inventory Selection**
st.subheader("📦 Inventory Management")
tea_types = {
    "Masala Chai": {"Price": 15, "Cost": 8},
    "Hot Coffee ": {"Price": 20, "Cost": 12},
    "COld Coffee": {"Price": 35, "Cost": 25},
    "Ice Tea": {"Price": 40, "Cost": 15}
}

snack_types = {
    "Samosa": {"Price": 20, "Cost": 9},
    "Kachori": {"Price": 20, "Cost": 9},
    "Sandwich": {"Price": 30, "Cost": 18},
    "Paneer Roll": {"Price": 45, "Cost": 27},
    "Patties": {"Price": 20, "Cost": 13}
}

tea_inventory = {t: st.slider(f"Replenish {t}", 0, 50, 0) for t in tea_types}
snack_inventory = {s: st.slider(f"Replenish {s}", 0, 50, 0) for s in snack_types}

# **Inventory Cost Deduction**
inventory_cost = sum(tea_inventory[t] * tea_types[t]["Cost"] for t in tea_inventory) + sum(snack_inventory[s] * snack_types[s]["Cost"] for s in snack_inventory)
if st.session_state.cash >= inventory_cost:
    st.session_state.cash -= inventory_cost
    st.success(f"💰 Inventory Purchased! ₹{inventory_cost} deducted.")
else:
    st.error("❌ Not enough cash! Reduce inventory.")

# **Sales Calculation**
total_impact = sum(impact for _, impact in event_results.values()) / len(event_results) if event_results else 0
tea_sales = {t: min(tea_inventory[t], int(random.randint(5, 20) * (1 + total_impact / 100))) for t in tea_inventory}
snack_sales = {s: min(snack_inventory[s], int(random.randint(5, 15) * (1 + total_impact / 100))) for s in snack_inventory}

# **Wastage Calculation**
tea_waste = {t: tea_inventory[t] - tea_sales[t] for t in tea_inventory}
snack_waste = {s: snack_inventory[s] - snack_sales[s] for s in snack_inventory}

# **Revenue Calculation**
revenue = sum(tea_sales[t] * tea_types[t]["Price"] for t in tea_sales) + sum(snack_sales[s] * snack_types[s]["Price"] for s in snack_sales)
st.session_state.cash += revenue

# **Day Summary**
st.subheader("📊 Day Summary")
st.write(f"💰 Revenue: ₹{revenue}")
st.write(f"💸 Cost: ₹{inventory_cost}")
st.write(f"💰 Cash in Hand: ₹{st.session_state.cash}")

# **Proceed to Next Day**
if st.button("➡️ Proceed to Next Day"):
    st.session_state.day += 1
    if st.session_state.day > total_days:
        st.success("🎉 Game Over! Thanks for playing!")











