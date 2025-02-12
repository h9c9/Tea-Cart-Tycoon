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
locations = ["Business District", "College Area", "Tourist Spot", "Residential Area", "Market Area"]

# **Location Selection for Business Hours**
st.subheader("📍 Select Locations for Business Hours (Morning & Evening)")
morning_location = st.selectbox("☀️ Morning Shift (8:00 AM - 2:00 PM)", locations, index=0)
evening_location = st.selectbox("🌙 Evening Shift (3:00 PM - 9:00 PM)", locations, index=1)

# **Item Cost & Price Information**
st.subheader("📦 Inventory Management (Price & Cost per Item)")

tea_types = {
    "Masala Chai": {"Price": 15, "Cost": 8},
    "Green Tea": {"Price": 20, "Cost": 12},
    "Herbal Tea": {"Price": 25, "Cost": 15},
    "Ginger Tea": {"Price": 18, "Cost": 10}
}

snack_types = {
    "Samosa": {"Price": 12, "Cost": 5},
    "Kachori": {"Price": 10, "Cost": 4},
    "Sandwich": {"Price": 30, "Cost": 18},
    "Pakora": {"Price": 15, "Cost": 7},
    "Patties": {"Price": 20, "Cost": 12}
}

# **Tea Selection**
st.write("**Tea Selection:**")
tea_inventory = {t: st.slider(f"{t} (₹{tea_types[t]['Price']}/₹{tea_types[t]['Cost']})", 0, 100, 0) for t in tea_types}

# **Snack Selection**
st.write("**Snack Selection:**")
snack_inventory = {s: st.slider(f"{s} (₹{snack_types[s]['Price']}/₹{snack_types[s]['Cost']})", 0, 80, 0) for s in snack_types}

# **Inventory Cost Calculation (But No Deduction Yet)**
inventory_cost = sum(tea_inventory[t] * tea_types[t]["Cost"] for t in tea_inventory) + sum(snack_inventory[s] * snack_types[s]["Cost"] for s in snack_inventory)
st.write(f"💰 **Total Inventory Cost (Not Deducted Yet): ₹{inventory_cost}**")

# **Forecast System: Generates for 2 random locations each day**
if st.session_state.day == 1 or st.button("📅 End Day & Generate Forecast"):
    st.session_state.forecast = random.sample(locations, 2)  # Pick 2 locations
    st.success("🔮 Tomorrow's Market Forecast:")
    for loc in st.session_state.forecast:
        forecast_event, _ = random.choice([
            ("Higher footfall expected.", (20, 50)),
            ("Lower traffic due to ongoing events.", (-30, -50))
        ])  
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
for loc in [morning_location, evening_location]:
    event = random.choice(["Higher customer flow.", "Lower demand due to nearby events."])
    event_results[loc] = event
    st.write(f"📌 **{loc}** → *{event}*")

# **Sales Calculation**
tea_sales = {t: min(tea_inventory[t], random.randint(5, 20)) for t in tea_inventory}
snack_sales = {s: min(snack_inventory[s], random.randint(5, 15)) for s in snack_inventory}

# **Wastage Calculation**
tea_waste = {t: tea_inventory[t] - tea_sales[t] for t in tea_inventory}
snack_waste = {s: snack_inventory[s] - snack_sales[s] for s in snack_inventory}

# **Revenue Calculation**
revenue = sum(tea_sales[t] * tea_types[t]["Price"] for t in tea_sales) + sum(snack_sales[s] * snack_types[s]["Price"] for s in snack_sales)

# **Cash in Hand Updates Only After Sales**
st.session_state.cash += revenue - inventory_cost

# **Day Summary**
st.subheader("📊 Day Summary")
st.write(f"💰 Revenue: ₹{revenue}")
st.write(f"💸 Cost: ₹{inventory_cost}")
st.write(f"💰 Cash in Hand: ₹{st.session_state.cash}")

# **Store Daily Summary in Table**
new_row = pd.DataFrame({
    "Day": [st.session_state.day],
    "Location 1": [morning_location],
    "Location 2": [evening_location],
    "Tea Sold": [sum(tea_sales.values())],
    "Snacks Sold": [sum(snack_sales.values())],
    "Revenue": [revenue],
    "Cost": [inventory_cost],
    "Wastage": [sum(tea_waste.values()) + sum(snack_waste.values())],
    "Event": [", ".join([f"{loc}: {ev}" for loc, ev in event_results.items()])]
})
st.session_state.sales_summary = pd.concat([st.session_state.sales_summary, new_row], ignore_index=True)

# **Display Sales Summary Table**
st.subheader("📊 Sales Summary (Day Wise)")
st.write(st.session_state.sales_summary)

# **Proceed to Next Day**
if st.button("➡️ Proceed to Next Day"):
    st.session_state.day += 1
    if st.session_state.day > total_days:
        st.success("🎉 Game Over! Thanks for playing!")












