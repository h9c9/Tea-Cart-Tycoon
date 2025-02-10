import streamlit as st
import random
import time
import pandas as pd

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
if "tea_inventory" not in st.session_state:
    st.session_state.tea_inventory = pd.DataFrame(columns=["Tea Type", "Price", "Cost", "Replenish Quantity", "Wastage"])
if "snack_inventory" not in st.session_state:
    st.session_state.snack_inventory = pd.DataFrame(columns=["Snack Type", "Price", "Cost", "Replenish Quantity", "Wastage"])

# Define game parameters
total_days = 15
tea_limit = 100
snack_limit = 80

# Real-time Countdown Timer (45 minutes)
st.subheader("⏳ Time Remaining")
elapsed_time = int(time.time() - st.session_state.get("start_time", time.time()))
remaining_time = max(0, (45 * 60) - elapsed_time)

if remaining_time == 0:
    st.session_state.game_over = True
    st.warning("⏳ Time is up! The game has ended.")

st.write(f"**{remaining_time // 60} minutes {remaining_time % 60} seconds left**")

# Weather conditions & impact on business
weather_effects = {
    "Sunny": "Normal business day, regular demand.",
    "Rainy": "Increased demand for hot beverages, slightly reduced footfall.",
    "Cold": "Higher demand for hot snacks and teas.",
    "Festive": "Massive increase in customer footfall, but higher competition."
}

weather_options = list(weather_effects.keys())
if st.session_state.weather is None:
    st.session_state.weather = random.choice(weather_options)

# Display Today's Weather Condition
st.subheader("☀️ Today's Weather Condition")
st.write(f"🌤 **{st.session_state.weather}** - {weather_effects[st.session_state.weather]}")

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
    quantity = st.slider(f"Select quantity for {tea}", 0, tea_limit, 0)
    tea_data.append([tea, details["Price"], details["Cost"], quantity, 0])

tea_df = pd.DataFrame(tea_data, columns=["Tea Type", "Price", "Cost", "Replenish Quantity", "Wastage"])
st.session_state.tea_inventory = tea_df
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
    quantity = st.slider(f"Select quantity for {snack}", 0, snack_limit, 0)
    snack_data.append([snack, details["Price"], details["Cost"], quantity, 0])

snack_df = pd.DataFrame(snack_data, columns=["Snack Type", "Price", "Cost", "Replenish Quantity", "Wastage"])
st.session_state.snack_inventory = snack_df
st.write(snack_df)

# Calculate total cost for replenishing inventory
total_cost = (tea_df["Cost"] * tea_df["Replenish Quantity"]).sum() + (snack_df["Cost"] * snack_df["Replenish Quantity"]).sum()

# Deduct cost from cash in hand
if total_cost > 0:
    if st.session_state.cash >= total_cost:
        st.session_state.cash -= total_cost
        st.success(f"Inventory purchased successfully! ₹{total_cost} deducted.")
    else:
        st.error("Not enough cash to purchase this inventory! Reduce quantities.")

st.write(f"💰 **Updated Cash in Hand: ₹{st.session_state.cash}**")

# Start Selling Button
if st.button("Start Selling"):
    sales_revenue = random.randint(500, 2000)  # Simulated revenue
    profit = sales_revenue - total_cost
    st.session_state.cash += profit

    # Update Day & Reset Conditions
    st.session_state.day += 1
    if st.session_state.day > total_days or remaining_time == 0:
        st.session_state.game_over = True

    # Refresh conditions
    st.session_state.weather = random.choice(weather_options)
    st.session_state.event = random.choice(list(weather_effects.keys()))

    st.success(f"✅ Day {st.session_state.day - 1} Completed! Profit: ₹{profit}")
    st.write(f"💰 **Updated Cash: ₹{st.session_state.cash}**")

# Game End Handling
if st.session_state.game_over:
    st.header("🚨 Game Over!")
    st.write(f"🏁 **Total Cash at End: ₹{st.session_state.cash}**")
    st.write("📊 Thank you for playing Tea Cart Tycoon!")



        
   




   

   

