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
    st.session_state.cash = 15000
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "weather" not in st.session_state:
    st.session_state.weather = None
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
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

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

weather_options = list(weather_effects.keys())

# Change weather each new day
if st.session_state.day == 1 or "previous_day" not in st.session_state or st.session_state.day > st.session_state.previous_day:
    st.session_state.weather = random.choice(weather_options)
    st.session_state.previous_day = st.session_state.day

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

# Calculate total cost for replenishing inventory
total_cost = (tea_df["Cost"] * tea_df["Replenish Quantity"]).sum() + (snack_df["Cost"] * snack_df["Replenish Quantity"]).sum()

# Deduct cost from cash available
if total_cost > 0 and st.session_state.cash >= total_cost:
    st.session_state.cash -= total_cost
    st.success(f"Inventory purchased! ₹{total_cost} deducted.")
elif total_cost > st.session_state.cash:
    st.error("Not enough cash! Reduce inventory.")

st.subheader(f"💰 Cash Available: ₹{st.session_state.cash}")

# Start Business Button
if st.button("Start Business"):
    # Flash Random Event
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
if st.button("Close for the Day"):
    tea_sold = random.randint(30, 100)
    snack_sold = random.randint(20, 80)
    tea_wasted = max(0, sum(tea_df["Replenish Quantity"]) - tea_sold)
    snack_wasted = max(0, sum(snack_df["Replenish Quantity"]) - snack_sold)
    revenue = (tea_sold * 15) + (snack_sold * 12)

    st.session_state.cash += revenue
    st.session_state.tea_sales.append(tea_sold)
    st.session_state.snack_sales.append(snack_sold)
    st.session_state.revenue_history.append(revenue)
    st.session_state.wastage_history.append(tea_wasted + snack_wasted)

    st.subheader(f"📊 Day {st.session_state.day} Summary")
    st.write(f"🔹 **Morning Location:** {morning_location}")
    st.write(f"🔹 **Evening Location:** {evening_location}")
    st.write(f"🔹 **Tea Sold:** {tea_sold}, **Tea Wasted:** {tea_wasted}")
    st.write(f"🔹 **Snacks Sold:** {snack_sold}, **Snacks Wasted:** {snack_wasted}")
    st.write(f"🔹 **Total Revenue:** ₹{revenue}")

    st.session_state.day += 1

if st.session_state.day > total_days or remaining_time == 0:
    st.subheader("🏁 Game Over!")
    st.write(f"💰 **Final Cash:** ₹{st.session_state.cash}")
    st.write("🎉 Thank you for playing Tea Cart Tycoon!")






   



   

   
   
