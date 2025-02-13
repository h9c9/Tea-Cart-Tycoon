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
    st.session_state.cash = 15000  # Initial Cash
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "weather" not in st.session_state:
    st.session_state.weather = "Sunny"  # Default weather to prevent errors
if "event" not in st.session_state:
    st.session_state.event = None
if "tea_sales" not in st.session_state:
    st.session_state.tea_sales = []
if "snack_sales" not in st.session_state:
    st.session_state.snack_sales = []
if "revenue_history" not in st.session_state:
    st.session_state.revenue_history = []
if "wastage_history" not in st.session_state:
    st.session_state.wastage_history = []
if "cost_history" not in st.session_state:
    st.session_state.cost_history = []
if "sales_summary" not in st.session_state:
    st.session_state.sales_summary = pd.DataFrame(columns=["Day", "Tea Sold", "Snacks Sold", "Revenue", "Cost", "Wastage"])
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Display Initial Cash
st.subheader(f"💰 Initial Cash: ₹{st.session_state.cash}")

# Define game parameters
total_days = 15

# Game Timer (45-minute countdown)
st.subheader("⏳ Time Remaining")
elapsed_time = int(time.time() - st.session_state.start_time)
remaining_time = max(0, (45 * 60) - elapsed_time)

if remaining_time == 0:
    st.session_state.game_over = True
    st.warning("⏳ Time is up! The game has ended.")

st.write(f"**{remaining_time // 60} minutes {remaining_time % 60} seconds left**")

# Weather conditions & business impact
weather_effects = {
    "Sunny": "Normal business day, regular demand.",
    "Rainy": "Increased demand for hot beverages, slightly reduced footfall.",
    "Heavy Rains": "Very few customers, high impact on sales.",
    "Cloudy": "Moderate demand, no major impact.",
    "Hot": "Higher demand for cold drinks, tea sales drop.",
    "Cold": "Increased demand for hot beverages and snacks.",
    "Very Cold": "Very high demand for hot teas and snacks."
}

# Play Day Button (Starts a New Day)
if st.button("🎮 Play Day"):
    st.session_state.weather = random.choice(list(weather_effects.keys()))  # Generate new weather
    st.session_state.event = None  # Reset event
    st.success(f"New Day Started! Weather: {st.session_state.weather}")

# Display Today's Weather Condition
st.subheader("☀️ Today's Weather")
st.write(f"🌤 **{st.session_state.weather}** - {weather_effects[st.session_state.weather]}")

# Location Selection for Business Hours
st.subheader(f"📍 Select Locations for Business Hours (Morning & Evening)")
locations = ["College Area", "Business District", "Tourist Spot", "Residential Area", "Market Area"]
morning_location = st.selectbox("☀️ Morning Shift (8:00 AM - 2:00 PM)", locations, index=0)
evening_location = st.selectbox("🌙 Evening Shift (3:00 PM - 9:00 PM)", locations, index=1)

# Tea Inventory Selection
st.subheader("☕ Tea Inventory Management")
tea_types = {
    "Masala Chai": {"Price": 15, "Cost": 8},
    "Green Tea": {"Price": 20, "Cost": 12},
    "Herbal Tea": {"Price": 25, "Cost": 15},
    "Ginger Tea": {"Price": 18, "Cost": 10}
}

tea_data = []
for tea, details in tea_types.items():
    quantity = st.slider(f"Select quantity for {tea}", 0, 100, 0)
    tea_data.append([tea, details["Price"], details["Cost"], quantity, 0])

tea_df = pd.DataFrame(tea_data, columns=["Tea Type", "Price", "Cost", "Replenish Quantity", "Wastage"])
st.write(tea_df)

# Snack Inventory Selection
st.subheader("🍪 Snack Inventory Management")
snack_types = {
    "Samosa": {"Price": 12, "Cost": 5},
    "Kachori": {"Price": 10, "Cost": 4},
    "Sandwich": {"Price": 30, "Cost": 18},
    "Pakora": {"Price": 15, "Cost": 7},
    "Patties": {"Price": 20, "Cost": 12}
}

snack_data = []
for snack, details in snack_types.items():
    quantity = st.slider(f"Select quantity for {snack}", 0, 80, 0)
    snack_data.append([snack, details["Price"], details["Cost"], quantity, 0])

snack_df = pd.DataFrame(snack_data, columns=["Snack Type", "Price", "Cost", "Replenish Quantity", "Wastage"])
st.write(snack_df)

# Generate Random Business Event after Business Starts
if st.button("🚀 Start Business"):
    event_options = [
        "Festival Nearby - High Footfall",
        "Supplier Delay - Some items unavailable",
        "Competitor Discount - Customers might switch",
        "Local News Feature - Boosted Sales",
        "Power Outage - Limited operations"
    ]
    st.session_state.event = random.choice(event_options)
    st.subheader("📢 Event of the Day")
    st.write(f"🎭 **{st.session_state.event}**")

# Close for the Day Button
if st.button("🔚 Close for the Day"):
    tea_sold = random.randint(30, 100)
    snack_sold = random.randint(20, 80)
    tea_wasted = max(0, sum(tea_df["Replenish Quantity"]) - tea_sold)
    snack_wasted = max(0, sum(snack_df["Replenish Quantity"]) - snack_sold)
    revenue = (tea_sold * 15) + (snack_sold * 12)
    cost = (tea_df["Cost"] * tea_df["Replenish Quantity"]).sum() + (snack_df["Cost"] * snack_df["Replenish Quantity"]).sum()

    st.session_state.cash += revenue
    st.session_state.revenue_history.append(revenue)
    st.session_state.wastage_history.append(tea_wasted + snack_wasted)
    st.session_state.cost_history.append(cost)

    # Update Summary Table
    new_row = pd.DataFrame({"Day": [st.session_state.day], "Tea Sold": [tea_sold], "Snacks Sold": [snack_sold], 
                            "Revenue": [revenue], "Cost": [cost], "Wastage": [tea_wasted + snack_wasted]})
    st.session_state.sales_summary = pd.concat([st.session_state.sales_summary, new_row], ignore_index=True)

    st.subheader("📊 Day-wise Sales Summary")
    st.write(st.session_state.sales_summary)

    st.session_state.day += 1

if st.session_state.day > total_days or remaining_time == 0:
    st.subheader("🏁 Game Over!")
    st.write(f"💰 **Final Cash:** ₹{st.session_state.cash}")
    st.write("🎉 Thank you for playing Tea Cart Tycoon!")










   



   

   
   
