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
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="Green Crisis Grid", layout="wide")

st.title("🚀 Green Crisis Grid")
st.subheader("AI Crisis Command Center + Agent-to-Agent Energy Trading")

st.markdown("""
This demo simulates:
- Disaster severity analysis
- Hospital emergency prioritization
- Solar panel → EV charger energy trading
- AI-generated response plan
- Micropayment transaction logs
""")

# -----------------------------
# Sidebar Inputs
# -----------------------------

st.sidebar.header("Disaster Input")
city = st.sidebar.text_input("City", "Faisalabad")
disaster_type = st.sidebar.selectbox(
    "Disaster Type",
    ["Flood", "Earthquake", "Fire", "Heatwave", "Power Outage"]
)
severity = st.sidebar.slider("Severity Level", 1, 10, 7)

hospital_need = st.sidebar.slider("Hospital Power Need (kWh)", 10, 500, 120)
solar_excess = st.sidebar.slider("Available Solar Energy (kWh)", 10, 500, 200)

run_button = st.sidebar.button("Run AI Simulation")


# -----------------------------
# Helper Functions
# -----------------------------

def generate_priority_plan(disaster, severity_score):
    if severity_score >= 8:
        level = "CRITICAL"
        action = "Immediate evacuation + hospital-first resource allocation"
    elif severity_score >= 5:
        level = "HIGH"
        action = "Emergency teams + medical support deployment"
    else:
        level = "MODERATE"
        action = "Monitoring + preventive preparation"

    return level, action


def simulate_transactions(total_energy):
    transactions = []
    remaining = total_energy

    while remaining > 0:
        trade = round(min(random.uniform(1, 8), remaining), 2)
        price = round(trade * 0.002, 4)
        remaining -= trade

        transactions.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Energy Traded (kWh)": trade,
            "USDC Payment": price,
            "Seller": "Solar Panel Agent",
            "Buyer": "Hospital Grid Agent"
        })

    return pd.DataFrame(transactions)


# -----------------------------
# Main Simulation
# -----------------------------

if run_button:
    st.success("AI Multi-Agent System Running...")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 🌍 Crisis Analysis")
        level, action = generate_priority_plan(disaster_type, severity)

        st.metric("Risk Level", level)
        st.write(f"**City:** {city}")
        st.write(f"**Disaster:** {disaster_type}")
        st.write(f"**Recommended Action:** {action}")

    with col2:
        st.markdown("## ⚡ Energy Allocation")

        allocated = min(hospital_need, solar_excess)
        shortage = max(hospital_need - solar_excess, 0)

        st.metric("Energy Allocated", f"{allocated} kWh")
        st.metric("Remaining Shortage", f"{shortage} kWh")

        if shortage > 0:
            st.warning("Additional backup source required")
        else:
            st.success("Hospital fully powered using smart grid")

    st.markdown("---")

    st.markdown("## 💸 Agent-to-Agent Micropayment Transactions")

    tx_df = simulate_transactions(allocated)
    st.dataframe(tx_df, use_container_width=True)

    total_payment = round(tx_df["USDC Payment"].sum(), 4)
    st.metric("Total Settlement", f"${total_payment} USDC")

    st.markdown("---")

    st.markdown("## 📄 AI Generated Emergency Report")

    report = f"""
Emergency Response Report
=========================

Location: {city}
Disaster Type: {disaster_type}
Severity Level: {severity}/10
Risk Status: {level}

Hospital Power Need: {hospital_need} kWh
Solar Grid Supply: {solar_excess} kWh
Allocated Energy: {allocated} kWh
Shortage: {shortage} kWh

Recommended Government Action:
{action}

Blockchain Settlement:
Total USDC settled between energy agents: ${total_payment}

Generated by: Green Crisis Grid AI
"""

    st.text_area("Generated Report", report, height=350)

else:
    st.info("Use the sidebar and click 'Run AI Simulation' to start.")

