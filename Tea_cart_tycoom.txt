import streamlit as st
import random
import time

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
if "inventory" not in st.session_state:
    st.session_state.inventory = {"Tea": 0, "Snacks": 0}

# Define game parameters
total_days = 15
tea_limit = 100
snack_limit = 80

# Game Timer (Countdown)
if "timer" not in st.session_state:
    st.session_state.timer = 45 * 60  # 45 minutes in seconds

# Countdown function
def countdown():
    if st.session_state.timer > 0:
        st.session_state.timer -= 1
        time.sleep(1)

# Weather conditions
weather_options = ["Sunny", "Rainy", "Cold", "Festive"]
if st.session_state.weather is None:
    st.session_state.weather = random.choice(weather_options)

# Random Events
event_options = [
    "No Special Event",
    "Festival Nearby (Higher Demand)",
    "Supplier Delay (Stock Issue)",
    "Street Maintenance (Lower Footfall)",
    "Local News Feature (Boosted Sales)"
]
if st.session_state.event is None:
    st.session_state.event = random.choice(event_options)

# Location Selection
st.subheader(f"Day {st.session_state.day} - Select Locations")
locations = ["College Area", "Business District", "Tourist Spot", "Residential Area", "Market Area"]
selected_locations = st.multiselect("Choose up to 2 locations:", locations, max_selections=2)

# Display Weather and Event
st.subheader("Today's Market Conditions")
st.write(f"🌤 Weather: **{st.session_state.weather}**")
st.write(f"🎭 Random Event: **{st.session_state.event}**")

# Inventory Selection
st.subheader("Manage Inventory")
st.write("Choose how much tea and snacks to stock for the day.")

tea_stock = st.slider("Select Tea Stock (Max: 100)", 0, tea_limit, 50)
snack_stock = st.slider("Select Snack Stock (Max: 80)", 0, snack_limit, 40)

st.session_state.inventory["Tea"] = tea_stock
st.session_state.inventory["Snacks"] = snack_stock

# Start Selling Button
if st.button("Start Selling"):
    sales_revenue = random.randint(500, 2000)  # Simulated revenue
    expenses = (tea_stock * 8) + (snack_stock * 5)  # Basic cost estimation
    profit = sales_revenue - expenses
    st.session_state.cash += profit

    # Update Day & Reset Conditions
    st.session_state.day += 1
    if st.session_state.day > total_days:
        st.session_state.game_over = True

    # Refresh conditions
    st.session_state.weather = random.choice(weather_options)
    st.session_state.event = random.choice(event_options)

    st.success(f"Day {st.session_state.day - 1} Completed! Profit: ₹{profit}")
    st.write(f"💰 Updated Cash: ₹{st.session_state.cash}")

# Game End Handling
if st.session_state.game_over:
    st.header("Game Over!")
    st.write(f"Total Cash at End: ₹{st.session_state.cash}")
    st.write("Thank you for playing Tea Cart Tycoon!")
