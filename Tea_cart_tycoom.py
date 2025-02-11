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
if "event" not in st.session_state:
    st.session_state.event = None
if "forecast" not in st.session_state:
    st.session_state.forecast = []  # Stores forecast for 2 locations
if "sales_summary" not in st.session_state:
    st.session_state.sales_summary = pd.DataFrame(columns=["Day", "Tea Sold", "Snacks Sold", "Revenue", "Cost", "Wastage", "Event"])
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Define game parameters
total_days = 15

# Location and Event Impact System
locations = ["Business District", "College Area", "Tourist Spot", "Residential Area", "Market Area"]

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
        forecast_event, impact_range = random.choice(event_impact[loc])  # Select random event
        st.write(f"📌 **{loc}** → *{forecast_event}*")

# **Weather Generation for Current Day**
if st.button("🎮 Play Day"):
    st.session_state.weather = random.choice(["Sunny", "Rainy", "Heavy Rains", "Cloudy", "Hot", "Cold", "Very Cold"])
    st.success(f"New Day Started! Weather: {st.session_state.weather}")

# **Display Current Day Weather**
st.subheader("☀️ Today's Weather")
st.write(f"🌤 **{st.session_state.weather}**")

# **Business Events for Today (Actual impact applied)**
st.subheader("📢 Event of the Day")
for loc in locations:
    event_tuple = random.choice(event_impact[loc])  # Select random event with impact range

    if isinstance(event_tuple, tuple) and len(event_tuple) == 2:
        event, impact_range = event_tuple  # Unpack event and impact range
        
        # **Ensure impact_range is valid**
        if isinstance(impact_range, tuple) and len(impact_range) == 2:
            min_impact, max_impact = impact_range
            
            if min_impact > max_impact:  # If reversed, swap values
                min_impact, max_impact = max_impact, min_impact
            
            if min_impact < max_impact:  # Ensure valid range before using randint
                impact = random.randint(min_impact, max_impact)
            else:
                impact = min_impact  # Use fixed value if range is the same
        else:
            impact = 0  # Default impact if range is invalid
        
        st.write(f"📌 **{loc}** → *{event}* → Impact: **{impact}%** sales change")
    else:
        st.warning(f"⚠️ No valid event found for {loc}. Skipping event.")

# Proceed with inventory selection, selling, and day-end summary...








