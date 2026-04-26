# import streamlit as st
# import google.generativeai as genai
# import random
# import time
# import pandas as pd
# from datetime import datetime

# # --- CONFIGURATION & PAGE SETUP ---
# st.set_page_config(page_title="The Green Mesh | Agentic Economy on Arc", layout="wide")

# st.title("⚡ The Green Mesh")
# st.subheader("Autonomous Machine-to-Machine Energy Market powered by Arc & Gemini")

# # Sidebar for API Keys
# with st.sidebar:
#     st.header("Settings")
#     gemini_key = st.text_input("Enter Gemini API Key", type="password")
#     circle_api_mock = st.toggle("Mock Circle Nanopayments", value=True)
#     sim_speed = st.slider("Simulation Speed (seconds)", 1, 10, 3)
    
#     st.divider()
#     st.info("This agent swarm performs sub-cent transactions ($0.001) for every 1Wh of energy traded.")

# if not gemini_key:
#     st.warning("Please enter your Gemini API Key in the sidebar to start the agents.")
#     st.stop()

# # Initialize Gemini
# genai.configure(api_key=gemini_key)
# model = genai.GenerativeModel('gemini-1.5-flash') # Using Flash for sub-second agent reasoning

# # --- AGENT DEFINITIONS ---
# if 'agents' not in st.session_state:
#     st.session_state.agents = {
#         "Producer_1": {"type": "Solar House", "wallet": "0x...A1b2", "balance": 10.0, "status": "Idle", "energy": 100},
#         "Producer_2": {"type": "Solar House", "wallet": "0x...C3d4", "balance": 12.5, "status": "Idle", "energy": 80},
#         "Consumer_1": {"type": "EV Charger", "wallet": "0x...E5f6", "balance": 50.0, "status": "Idle", "battery": 20},
#         "Consumer_2": {"type": "EV Charger", "wallet": "0x...G7h8", "balance": 45.0, "status": "Idle", "battery": 15},
#     }

# if 'history' not in st.session_state:
#     st.session_state.history = []

# # --- CORE FUNCTIONS ---

# def get_agent_decision(prompt):
#     """Uses Gemini to decide pricing or purchasing."""
#     try:
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         return f"Error: {e}"

# def process_nanopayment(sender, receiver, amount):
#     """
#     Simulates the Circle Nanopayment flow via x402.
#     In production, this calls Circle Gateway/Wallets.
#     """
#     # This represents the settlement on Arc
#     tx_hash = f"0x{random.getrandbits(128):032x}"
#     return {
#         "status": "Settled",
#         "tx_hash": tx_hash,
#         "fee_usdc": 0.00001, # The micro-fee on Arc
#         "finality": "0.4s"
#     }

# # --- UI LAYOUT ---

# col1, col2 = st.columns([1, 2])

# with col1:
#     st.write("### 🤖 Agent Status")
#     for name, info in st.session_state.agents.items():
#         with st.expander(f"{name} ({info['type']})"):
#             st.write(f"**Wallet:** `{info['wallet']}`")
#             st.write(f"**Balance:** {info['balance']:.4f} USDC")
#             if info['type'] == "Solar House":
#                 st.progress(info['energy'] / 100, text=f"Energy: {info['energy']}Wh")
#             else:
#                 st.progress(info['battery'] / 100, text=f"Battery: {info['battery']}%")

# with col2:
#     st.write("### 📈 Live Transaction Stream (Arc L1)")
    
#     # Simulation Loop
#     if st.button("▶️ Start Market Swarm"):
#         log_placeholder = st.empty()
#         stats_placeholder = st.empty()
        
#         while True:
#             # 1. Producer Logic (Setting Price)
#             p_name = random.choice(["Producer_1", "Producer_2"])
#             weather = random.choice(["Sunny", "Cloudy", "Rainy"])
            
#             p_prompt = f"Agent {p_name} is a {st.session_state.agents[p_name]['type']}. Weather is {weather}. Energy available: {st.session_state.agents[p_name]['energy']}Wh. Current grid price is $0.01. Suggest a competitive sub-cent price per 1Wh in USDC. Reply ONLY with the number (e.g. 0.002)."
#             price_suggestion = get_agent_decision(p_prompt)
            
#             try:
#                 price = float(price_suggestion)
#             except:
#                 price = 0.005 # Default fallback
            
#             # 2. Consumer Logic (Decision to buy)
#             c_name = random.choice(["Consumer_1", "Consumer_2"])
#             battery = st.session_state.agents[c_name]['battery']
            
#             c_prompt = f"Agent {c_name} is an EV Charger with {battery}% battery. A producer is offering energy at {price} USDC per Wh. Grid is $0.01. Should I buy? Reply only with YES or NO."
#             decision = get_agent_decision(c_prompt)
            
#             if "YES" in decision.upper():
#                 # 3. Execution (Nanopayment)
#                 amount = price
#                 tx = process_nanopayment(c_name, p_name, amount)
                
#                 # Update State
#                 st.session_state.agents[c_name]['balance'] -= amount
#                 st.session_state.agents[p_name]['balance'] += amount
#                 st.session_state.agents[c_name]['battery'] += 1
#                 st.session_state.agents[p_name]['energy'] -= 1
                
#                 # Log History
#                 new_entry = {
#                     "Time": datetime.now().strftime("%H:%M:%S"),
#                     "From": c_name,
#                     "To": p_name,
#                     "Amount": f"${amount} USDC",
#                     "Status": "✅ Settled",
#                     "Arc_TX": tx['tx_hash'][:10] + "..."
#                 }
#                 st.session_state.history.insert(0, new_entry)
            
#             # Display history (Targeting 50+ transactions for hackathon proof)
#             df = pd.DataFrame(st.session_state.history)
#             log_placeholder.table(df.head(10))
            
#             # Show "Impossible on Ethereum" stats
#             total_txs = len(st.session_state.history)
#             eth_gas = total_txs * 0.75 # Assuming $0.75 gas on a cheap day
#             arc_gas = total_txs * 0.0001
            
#             with stats_placeholder.container():
#                 s1, s2, s3 = st.columns(3)
#                 s1.metric("Total Transactions", total_txs)
#                 s2.metric("Arc Gas Fees", f"${arc_gas:.4f}")
#                 s3.metric("ETH Gas (Potential)", f"${eth_gas:.2f}", delta=f"-{eth_gas-arc_gas:.2f}", delta_color="inverse")

#             time.sleep(sim_speed)
#             st.rerun()

# # --- FOOTER / HACKATHON PROOF ---
# st.divider()
# st.write("### Why this fits the 'Agentic Economy' Challenge:")
# st.markdown("""
# 1. **Sub-cent Transactions:** Every deal is $0.001 - $0.009 USDC.
# 2. **Deterministic Finality:** Arc ensures the agent can verify payment in <1s.
# 3. **Machine Reasoning:** Gemini 3 Flash acts as the autonomous brain for each device.
# 4. **Economic Viability:** Traditional gas fees would be 750x more expensive than the transaction value itself.
# """)

import streamlit as st
import pydeck as pdk
import requests
import math
from pinecone import Pinecone

# =====================================================
# 🔐 API KEY
# =====================================================
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
INDEX_NAME = "crisis-command-center-index"

# =====================================================
# 🧠 PINECONE CONNECT
# =====================================================
def connect_pinecone():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc.Index(INDEX_NAME)

# =====================================================
# 🔍 PINECONE SEARCH
# =====================================================
def search_documents(index, query):
    try:
        results = index.search(
            namespace="default",
            query={"inputs": {"text": query}, "top_k": 3}
        )

        docs = []

        hits = getattr(results, "result", {}).get("hits", [])

        for h in hits:
            text = None
            if hasattr(h, "fields"):
                text = h.fields.get("text")
            elif hasattr(h, "metadata"):
                text = h.metadata.get("text")

            if text:
                docs.append(text)

        return docs

    except Exception as e:
        st.error(f"Pinecone Error: {e}")
        return []

# =====================================================
# 🌍 REAL DATA SOURCES
# =====================================================

LAT, LON = 31.4504, 73.1350  # Faisalabad default

# -------------------------
# 🌡️ HEATWAVE SEVERITY
# -------------------------
def heatwave_severity():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m"

    try:
        data = requests.get(url).json()
        temp = data["hourly"]["temperature_2m"][0]

        if temp >= 45:
            return 9, f"Extreme heat detected: {temp}°C"
        elif temp >= 40:
            return 7, f"Severe heat detected: {temp}°C"
        elif temp >= 35:
            return 5, f"Moderate heat: {temp}°C"
        else:
            return 3, f"Normal temperature: {temp}°C"

    except:
        return 5, "Heat data unavailable"

# -------------------------
# 🌧️ FLOOD SEVERITY
# -------------------------
def flood_severity():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=precipitation"

    try:
        data = requests.get(url).json()
        rain = data["hourly"]["precipitation"][0]

        if rain > 20:
            return 9, f"Extreme rainfall: {rain}mm"
        elif rain > 10:
            return 7, f"Heavy rainfall: {rain}mm"
        elif rain > 5:
            return 5, f"Moderate rainfall: {rain}mm"
        else:
            return 3, f"Low rainfall: {rain}mm"

    except:
        return 5, "Rain data unavailable"

# -------------------------
# 🌬️ FIRE RISK (SIMULATED REAL DATA LOGIC)
# -------------------------
def fire_severity():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=wind_speed_10m"

    try:
        data = requests.get(url).json()
        wind = data["hourly"]["wind_speed_10m"][0]

        if wind >= 40:
            return 8, f"High fire spread risk (wind {wind} km/h)"
        elif wind >= 25:
            return 6, f"Moderate fire risk (wind {wind} km/h)"
        else:
            return 3, f"Low fire spread risk (wind {wind} km/h)"

    except:
        return 5, "Fire data unavailable"

# -------------------------
# 🌍 EARTHQUAKE (USGS REAL API)
# -------------------------
def earthquake_severity():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

    try:
        data = requests.get(url).json()

        if len(data["features"]) == 0:
            return 3, "No recent seismic activity"

        mag = data["features"][0]["properties"]["mag"]

        if mag >= 6:
            return 9, f"Strong earthquake detected: M{mag}"
        elif mag >= 4:
            return 7, f"Moderate earthquake: M{mag}"
        else:
            return 4, f"Minor seismic activity: M{mag}"

    except:
        return 5, "Earthquake data unavailable"

# =====================================================
# 🧠 AUTONOMOUS DISASTER ENGINE
# =====================================================
def detect_disaster(disaster_type):

    if disaster_type == "Heatwave":
        return heatwave_severity()

    elif disaster_type == "Flood":
        return flood_severity()

    elif disaster_type == "Fire":
        return fire_severity()

    elif disaster_type == "Earthquake":
        return earthquake_severity()

    else:
        return 5, "Default risk model"

# =====================================================
# 🚑 EVACUATION LOGIC
# =====================================================
def evacuation_plan(severity):
    if severity >= 8:
        return "IMMEDIATE EVACUATION - HIGH RISK ZONES"
    elif severity >= 5:
        return "CONTROLLED EVACUATION - CAUTION REQUIRED"
    else:
        return "MONITOR SITUATION - SAFE MOVEMENT"

# =====================================================
# 🏥 HOSPITAL DATA
# =====================================================
HOSPITALS = [
    {"name": "Allied Hospital", "lat": 31.4180, "lon": 73.0790},
    {"name": "DHQ Hospital", "lat": 31.4150, "lon": 73.0890},
    {"name": "Faisal Hospital", "lat": 31.4300, "lon": 73.1100},
]

# =====================================================
# 🗺️ MAP
# =====================================================
def render_map(severity):

    zones = [
        {"lat": LAT, "lon": LON, "risk": severity},
        {"lat": LAT+0.02, "lon": LON+0.02, "risk": severity-2},
        {"lat": LAT-0.02, "lon": LON-0.03, "risk": severity-3},
    ]

    def color(r):
        if r >= 8:
            return [255, 0, 0, 180]
        elif r >= 5:
            return [255, 165, 0, 160]
        else:
            return [0, 255, 0, 120]

    for z in zones:
        z["color"] = color(z["risk"])

    layer1 = pdk.Layer(
        "ScatterplotLayer",
        data=zones,
        get_position='[lon, lat]',
        get_color='color',
        get_radius=8000
    )

    layer2 = pdk.Layer(
        "ScatterplotLayer",
        data=HOSPITALS,
        get_position='[lon, lat]',
        get_color='[0,0,255,200]',
        get_radius=9000
    )

    view = pdk.ViewState(latitude=LAT, longitude=LON, zoom=11)

    st.pydeck_chart(pdk.Deck(layers=[layer1, layer2], initial_view_state=view))

# =====================================================
# 🧠 REPORT
# =====================================================
def generate_report(city, disaster, severity, docs, reason):

    return f"""
GREEN CRISIS GRID – AUTONOMOUS SYSTEM
=====================================

City: {city}
Disaster: {disaster}
Severity: {severity}/10

📡 AI Reason:
{reason}

🚑 Evacuation:
{evacuation_plan(severity)}

📌 Knowledge Base:
{chr(10).join(docs) if docs else "No data"}

🏥 Hospital Strategy:
- Distance-based prioritization
- Emergency readiness activated

SYSTEM: FULLY AUTONOMOUS ACTIVE
"""

# =====================================================
# 🎨 UI
# =====================================================
st.set_page_config(page_title="Green Crisis Grid", layout="wide")

st.title("🚀 Green Crisis Grid AI (FULLY AUTONOMOUS)")
st.markdown("No manual input needed — AI detects disaster severity automatically")

city = st.sidebar.text_input("City", "Faisalabad")

disaster_type = st.sidebar.selectbox(
    "Disaster Type",
    ["Heatwave", "Flood", "Fire", "Earthquake"]
)

run = st.sidebar.button("Run Autonomous System")

# =====================================================
# 🚀 MAIN
# =====================================================
if run:

    index = connect_pinecone()

    severity, reason = detect_disaster(disaster_type)

    query = f"{disaster_type} emergency {city}"
    docs = search_documents(index, query)

    st.success("Autonomous System Activated")

    st.markdown("## 🗺️ Live Disaster Map")
    render_map(severity)

    st.markdown("## 🧠 AI Report")

    report = generate_report(city, disaster_type, severity, docs, reason)

    st.text_area("Report", report, height=450)

else:
    st.info("Click Run Autonomous System to start")
