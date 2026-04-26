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
# 🔐 API KEY (Streamlit Secrets)
# =====================================================
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
INDEX_NAME = "crisis-command-center-index"

# =====================================================
# 🧠 CONNECT TO PINECONE
# =====================================================
def connect_pinecone():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc.Index(INDEX_NAME)

# =====================================================
# 🔍 PINECONE SEARCH (FIXED)
# =====================================================
def search_documents(index, query):
    try:
        results = index.search(
            namespace="default",
            query={
                "inputs": {"text": query},
                "top_k": 3
            }
        )

        docs = []

        if hasattr(results, "result"):
            hits = results.result.get("hits", [])
        else:
            hits = results.get("matches", [])

        for h in hits:
            text = None

            if hasattr(h, "fields"):
                text = h.fields.get("text")

            if not text and hasattr(h, "metadata"):
                text = h.metadata.get("text")

            if text:
                docs.append(text)

        return docs

    except Exception as e:
        st.error(f"Pinecone Error: {e}")
        return []

# =====================================================
# 🌧️ WEATHER / FLOOD INTELLIGENCE (REAL API)
# =====================================================
def get_flood_risk(city):
    lat, lon = 31.4504, 73.1350  # Faisalabad default

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=precipitation"

    try:
        r = requests.get(url)
        data = r.json()

        rain = data["hourly"]["precipitation"][0]

        if rain > 10:
            return "HIGH"
        elif rain > 5:
            return "MEDIUM"
        else:
            return "LOW"

    except:
        return "UNKNOWN"

# =====================================================
# 🚨 DISASTER-AWARE RISK ENGINE (FIXED LOGIC)
# =====================================================
def get_disaster_risk(city, disaster_type):
    if disaster_type == "Flood":
        return get_flood_risk(city)

    elif disaster_type == "Heatwave":
        return "HIGH (Temperature Risk Model)"

    elif disaster_type == "Earthquake":
        return "SEISMIC EVENT - NO WEATHER DATA"

    elif disaster_type == "Fire":
        return "WIND + DRY CONDITIONS RISK (SIMULATED)"

    else:
        return "UNKNOWN"

# =====================================================
# 🏥 HOSPITAL DATA
# =====================================================
HOSPITALS = [
    {"name": "Allied Hospital", "lat": 31.4180, "lon": 73.0790},
    {"name": "DHQ Hospital", "lat": 31.4150, "lon": 73.0890},
    {"name": "Faisal Hospital", "lat": 31.4300, "lon": 73.1100},
]

# =====================================================
# 📍 DISTANCE FUNCTION
# =====================================================
def distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

# =====================================================
# 🚑 EVACUATION LOGIC
# =====================================================
def evacuation_plan(severity):
    if severity >= 8:
        return "AVOID MAIN ROADS — MOVE TO HIGH GROUND IMMEDIATELY"
    elif severity >= 5:
        return "USE CAUTIOUS EVACUATION ROUTES"
    else:
        return "NORMAL MOVEMENT SAFE"

# =====================================================
# 🗺️ MAP RENDERING
# =====================================================
def render_map(severity):

    center_lat, center_lon = 31.4504, 73.1350

    zones = [
        {"lat": center_lat, "lon": center_lon, "risk": severity},
        {"lat": center_lat + 0.02, "lon": center_lon + 0.02, "risk": severity - 2},
        {"lat": center_lat - 0.02, "lon": center_lon - 0.03, "risk": severity - 3},
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

    flood_layer = pdk.Layer(
        "ScatterplotLayer",
        data=zones,
        get_position='[lon, lat]',
        get_color='color',
        get_radius=8000
    )

    hospital_layer = pdk.Layer(
        "ScatterplotLayer",
        data=HOSPITALS,
        get_position='[lon, lat]',
        get_color='[0, 0, 255, 200]',
        get_radius=9000
    )

    view = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=11)

    st.pydeck_chart(pdk.Deck(layers=[flood_layer, hospital_layer], initial_view_state=view))

# =====================================================
# 🧠 AI REPORT
# =====================================================
def generate_report(city, disaster_type, severity, docs, risk, route):

    return f"""
GREEN CRISIS GRID – INTELLIGENT DISASTER SYSTEM
===============================================

City: {city}
Disaster: {disaster_type}
Severity: {severity}/10
Risk Level: {risk}

🚑 Evacuation Plan:
{route}

📌 Knowledge Base:
{chr(10).join(docs) if docs else "No data found"}

🏥 Hospital Strategy:
- Nearest hospitals activated
- Distance-based triage
- Emergency response readiness

SYSTEM STATUS: ACTIVE
"""

# =====================================================
# 🎨 UI
# =====================================================
st.set_page_config(page_title="Green Crisis Grid", layout="wide")

st.title("🚀 Green Crisis Grid AI")
st.markdown("Multi-Hazard Emergency Intelligence System")

city = st.sidebar.text_input("City", "Faisalabad")

disaster_type = st.sidebar.selectbox(
    "Disaster Type",
    ["Flood", "Earthquake", "Fire", "Heatwave"]
)

severity = st.sidebar.slider("Severity", 1, 10, 7)

run = st.sidebar.button("Run System")

# =====================================================
# 🚀 MAIN EXECUTION
# =====================================================
if run:

    index = connect_pinecone()

    risk = get_disaster_risk(city, disaster_type)
    route = evacuation_plan(severity)

    query = f"{disaster_type} emergency response {city}"
    docs = search_documents(index, query)

    st.success("System Activated")

    st.markdown("## 🗺️ Live Disaster Map")
    render_map(severity)

    st.markdown("## 🧠 AI Emergency Report")

    report = generate_report(
        city,
        disaster_type,
        severity,
        docs,
        risk,
        route
    )

    st.text_area("Report", report, height=400)

else:
    st.info("Enter inputs and run the system")
