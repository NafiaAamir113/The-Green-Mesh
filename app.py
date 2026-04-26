# import streamlit as st
# import pydeck as pdk
# import requests
# import math
# from pinecone import Pinecone

# # =====================================================
# # 🔐 API KEY
# # =====================================================
# PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
# INDEX_NAME = "crisis-command-center-index"

# # =====================================================
# # 🧠 PINECONE CONNECT
# # =====================================================
# def connect_pinecone():
#     pc = Pinecone(api_key=PINECONE_API_KEY)
#     return pc.Index(INDEX_NAME)

# # =====================================================
# # 🔍 PINECONE SEARCH
# # =====================================================
# def search_documents(index, query):
#     try:
#         results = index.search(
#             namespace="default",
#             query={"inputs": {"text": query}, "top_k": 3}
#         )

#         docs = []

#         hits = getattr(results, "result", {}).get("hits", [])

#         for h in hits:
#             text = None
#             if hasattr(h, "fields"):
#                 text = h.fields.get("text")
#             elif hasattr(h, "metadata"):
#                 text = h.metadata.get("text")

#             if text:
#                 docs.append(text)

#         return docs

#     except Exception as e:
#         st.error(f"Pinecone Error: {e}")
#         return []

# # =====================================================
# # 🌍 REAL DATA SOURCES
# # =====================================================

# LAT, LON = 31.4504, 73.1350  # Faisalabad default

# # -------------------------
# # 🌡️ HEATWAVE SEVERITY
# # -------------------------
# def heatwave_severity():
#     url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m"

#     try:
#         data = requests.get(url).json()
#         temp = data["hourly"]["temperature_2m"][0]

#         if temp >= 45:
#             return 9, f"Extreme heat detected: {temp}°C"
#         elif temp >= 40:
#             return 7, f"Severe heat detected: {temp}°C"
#         elif temp >= 35:
#             return 5, f"Moderate heat: {temp}°C"
#         else:
#             return 3, f"Normal temperature: {temp}°C"

#     except:
#         return 5, "Heat data unavailable"

# # -------------------------
# # 🌧️ FLOOD SEVERITY
# # -------------------------
# def flood_severity():
#     url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=precipitation"

#     try:
#         data = requests.get(url).json()
#         rain = data["hourly"]["precipitation"][0]

#         if rain > 20:
#             return 9, f"Extreme rainfall: {rain}mm"
#         elif rain > 10:
#             return 7, f"Heavy rainfall: {rain}mm"
#         elif rain > 5:
#             return 5, f"Moderate rainfall: {rain}mm"
#         else:
#             return 3, f"Low rainfall: {rain}mm"

#     except:
#         return 5, "Rain data unavailable"

# # -------------------------
# # 🌬️ FIRE RISK (SIMULATED REAL DATA LOGIC)
# # -------------------------
# def fire_severity():
#     url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=wind_speed_10m"

#     try:
#         data = requests.get(url).json()
#         wind = data["hourly"]["wind_speed_10m"][0]

#         if wind >= 40:
#             return 8, f"High fire spread risk (wind {wind} km/h)"
#         elif wind >= 25:
#             return 6, f"Moderate fire risk (wind {wind} km/h)"
#         else:
#             return 3, f"Low fire spread risk (wind {wind} km/h)"

#     except:
#         return 5, "Fire data unavailable"

# # -------------------------
# # 🌍 EARTHQUAKE (USGS REAL API)
# # -------------------------
# def earthquake_severity():
#     url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

#     try:
#         data = requests.get(url).json()

#         if len(data["features"]) == 0:
#             return 3, "No recent seismic activity"

#         mag = data["features"][0]["properties"]["mag"]

#         if mag >= 6:
#             return 9, f"Strong earthquake detected: M{mag}"
#         elif mag >= 4:
#             return 7, f"Moderate earthquake: M{mag}"
#         else:
#             return 4, f"Minor seismic activity: M{mag}"

#     except:
#         return 5, "Earthquake data unavailable"

# # =====================================================
# # 🧠 AUTONOMOUS DISASTER ENGINE
# # =====================================================
# def detect_disaster(disaster_type):

#     if disaster_type == "Heatwave":
#         return heatwave_severity()

#     elif disaster_type == "Flood":
#         return flood_severity()

#     elif disaster_type == "Fire":
#         return fire_severity()

#     elif disaster_type == "Earthquake":
#         return earthquake_severity()

#     else:
#         return 5, "Default risk model"

# # =====================================================
# # 🚑 EVACUATION LOGIC
# # =====================================================
# def evacuation_plan(severity):
#     if severity >= 8:
#         return "IMMEDIATE EVACUATION - HIGH RISK ZONES"
#     elif severity >= 5:
#         return "CONTROLLED EVACUATION - CAUTION REQUIRED"
#     else:
#         return "MONITOR SITUATION - SAFE MOVEMENT"

# # =====================================================
# # 🏥 HOSPITAL DATA
# # =====================================================
# HOSPITALS = [
#     {"name": "Allied Hospital", "lat": 31.4180, "lon": 73.0790},
#     {"name": "DHQ Hospital", "lat": 31.4150, "lon": 73.0890},
#     {"name": "Faisal Hospital", "lat": 31.4300, "lon": 73.1100},
# ]

# # =====================================================
# # 🗺️ MAP
# # =====================================================
# def render_map(severity):

#     zones = [
#         {"lat": LAT, "lon": LON, "risk": severity},
#         {"lat": LAT+0.02, "lon": LON+0.02, "risk": severity-2},
#         {"lat": LAT-0.02, "lon": LON-0.03, "risk": severity-3},
#     ]

#     def color(r):
#         if r >= 8:
#             return [255, 0, 0, 180]
#         elif r >= 5:
#             return [255, 165, 0, 160]
#         else:
#             return [0, 255, 0, 120]

#     for z in zones:
#         z["color"] = color(z["risk"])

#     layer1 = pdk.Layer(
#         "ScatterplotLayer",
#         data=zones,
#         get_position='[lon, lat]',
#         get_color='color',
#         get_radius=8000
#     )

#     layer2 = pdk.Layer(
#         "ScatterplotLayer",
#         data=HOSPITALS,
#         get_position='[lon, lat]',
#         get_color='[0,0,255,200]',
#         get_radius=9000
#     )

#     view = pdk.ViewState(latitude=LAT, longitude=LON, zoom=11)

#     st.pydeck_chart(pdk.Deck(layers=[layer1, layer2], initial_view_state=view))

# # =====================================================
# # 🧠 REPORT
# # =====================================================
# def generate_report(city, disaster, severity, docs, reason):

#     return f"""
# GREEN CRISIS GRID – AUTONOMOUS SYSTEM
# =====================================

# City: {city}
# Disaster: {disaster}
# Severity: {severity}/10

# 📡 AI Reason:
# {reason}

# 🚑 Evacuation:
# {evacuation_plan(severity)}

# 📌 Knowledge Base:
# {chr(10).join(docs) if docs else "No data"}

# 🏥 Hospital Strategy:
# - Distance-based prioritization
# - Emergency readiness activated

# SYSTEM: FULLY AUTONOMOUS ACTIVE
# """

# # =====================================================
# # 🎨 UI
# # =====================================================
# st.set_page_config(page_title="Green Crisis Grid", layout="wide")

# st.title("🚀 Green Crisis Grid AI (FULLY AUTONOMOUS)")
# st.markdown("No manual input needed — AI detects disaster severity automatically")

# city = st.sidebar.text_input("City", "Faisalabad")

# disaster_type = st.sidebar.selectbox(
#     "Disaster Type",
#     ["Heatwave", "Flood", "Fire", "Earthquake"]
# )

# run = st.sidebar.button("Run Autonomous System")

# # =====================================================
# # 🚀 MAIN
# # =====================================================
# if run:

#     index = connect_pinecone()

#     severity, reason = detect_disaster(disaster_type)

#     query = f"{disaster_type} emergency {city}"
#     docs = search_documents(index, query)

#     st.success("Autonomous System Activated")

#     st.markdown("## 🗺️ Live Disaster Map")
#     render_map(severity)

#     st.markdown("## 🧠 AI Report")

#     report = generate_report(city, disaster_type, severity, docs, reason)

#     st.text_area("Report", report, height=450)

# else:
#     st.info("Click Run Autonomous System to start")


import streamlit as st
import pydeck as pdk
import requests
import math
from pinecone import Pinecone

# =====================================================
# 🔐 CONFIG
# =====================================================
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
INDEX_NAME = "crisis-command-center-index"

LAT, LON = 31.4504, 73.1350  # Faisalabad

# =====================================================
# 🧠 PINECONE
# =====================================================
def connect_pinecone():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc.Index(INDEX_NAME)

def search_documents(index, query):
    try:
        res = index.search(
            namespace="default",
            query={"inputs": {"text": query}, "top_k": 3}
        )

        docs = []
        hits = getattr(res, "result", {}).get("hits", [])

        for h in hits:
            text = None
            if hasattr(h, "fields"):
                text = h.fields.get("text")
            elif hasattr(h, "metadata"):
                text = h.metadata.get("text")

            if text:
                docs.append(text)

        return docs

    except:
        return []

# =====================================================
# 🌍 REAL DATA MODELS
# =====================================================

def heatwave_model():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m"
    data = requests.get(url).json()
    temp = data["hourly"]["temperature_2m"][0]

    if temp >= 45:
        return 9, temp, "Extreme heatwave detected"
    elif temp >= 40:
        return 7, temp, "Severe heat conditions"
    elif temp >= 35:
        return 5, temp, "Moderate heatwave"
    else:
        return 3, temp, "Normal temperature"

def flood_model():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=precipitation"
    data = requests.get(url).json()
    rain = data["hourly"]["precipitation"][0]

    if rain > 20:
        return 9, rain, "Flash flood risk"
    elif rain > 10:
        return 7, rain, "Heavy rainfall"
    elif rain > 5:
        return 5, rain, "Moderate rain"
    else:
        return 3, rain, "Low rainfall"

def fire_model():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=wind_speed_10m"
    data = requests.get(url).json()
    wind = data["hourly"]["wind_speed_10m"][0]

    if wind >= 40:
        return 8, wind, "High fire spread risk"
    elif wind >= 25:
        return 6, wind, "Moderate fire risk"
    else:
        return 3, wind, "Low fire risk"

def earthquake_model():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    data = requests.get(url).json()

    if not data["features"]:
        return 3, 0, "No seismic activity"

    mag = data["features"][0]["properties"]["mag"]

    if mag >= 6:
        return 9, mag, "Strong earthquake detected"
    elif mag >= 4:
        return 7, mag, "Moderate earthquake"
    else:
        return 4, mag, "Minor tremors"

# =====================================================
# 🧠 AUTONOMOUS ENGINE
# =====================================================
def detect(disaster):
    if disaster == "Heatwave":
        return heatwave_model()
    elif disaster == "Flood":
        return flood_model()
    elif disaster == "Fire":
        return fire_model()
    elif disaster == "Earthquake":
        return earthquake_model()
    else:
        return 5, 0, "Unknown condition"

# =====================================================
# 🏥 HOSPITAL INTELLIGENCE (WINNING FEATURE)
# =====================================================
HOSPITALS = [
    {"name": "Allied Hospital", "lat": 31.4180, "lon": 73.0790},
    {"name": "DHQ Hospital", "lat": 31.4150, "lon": 73.0890},
    {"name": "Faisal Hospital", "lat": 31.4300, "lon": 73.1100},
]

def distance(a, b, c, d):
    R = 6371
    dlat = math.radians(c - a)
    dlon = math.radians(d - b)
    x = math.sin(dlat/2)**2 + math.cos(math.radians(a)) * math.cos(math.radians(c)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(x), math.sqrt(1-x))

def rank_hospitals():
    ranked = []
    for h in HOSPITALS:
        dist = distance(LAT, LON, h["lat"], h["lon"])
        ranked.append((h["name"], round(dist, 2)))
    return sorted(ranked, key=lambda x: x[1])

# =====================================================
# 🚑 EVACUATION ENGINE (IMPROVED)
# =====================================================
def evacuation(severity):
    if severity >= 8:
        return "CRITICAL EVACUATION — IMMEDIATE ACTION REQUIRED"
    elif severity >= 5:
        return "CONTROLLED EVACUATION — HIGH ALERT"
    else:
        return "NORMAL MONITORING — SAFE"

# =====================================================
# 🗺️ MAP (IMPACT VERSION)
# =====================================================
def render_map(severity):

    zones = [
        {"lat": LAT, "lon": LON, "risk": severity},
        {"lat": LAT+0.02, "lon": LON+0.02, "risk": severity-2},
        {"lat": LAT-0.02, "lon": LON-0.03, "risk": severity-3},
    ]

    def color(r):
        if r >= 8:
            return [255, 0, 0, 200]
        elif r >= 5:
            return [255, 140, 0, 180]
        else:
            return [0, 255, 0, 140]

    for z in zones:
        z["color"] = color(z["risk"])

    layer1 = pdk.Layer(
        "ScatterplotLayer",
        data=zones,
        get_position='[lon, lat]',
        get_color='color',
        get_radius=9000
    )

    layer2 = pdk.Layer(
        "ScatterplotLayer",
        data=HOSPITALS,
        get_position='[lon, lat]',
        get_color='[0,0,255,200]',
        get_radius=10000
    )

    st.pydeck_chart(pdk.Deck(layers=[layer1, layer2],
        initial_view_state=pdk.ViewState(latitude=LAT, longitude=LON, zoom=11)))

# =====================================================
# 🧠 FINAL AI REPORT (WINNING FORMAT)
# =====================================================
def report(city, disaster, severity, reason, docs, hospitals):

    return f"""
🚨 GREEN CRISIS GRID — EMERGENCY COMMAND SYSTEM
================================================

📍 Location: {city}
⚠️ Disaster: {disaster}
📊 Severity Score: {severity}/10

🧠 AI ANALYSIS:
{reason}

🚑 EVACUATION STATUS:
{evacuation(severity)}

🏥 HOSPITAL PRIORITY LIST:
{chr(10).join([f"{i+1}. {h[0]} ({h[1]} km)" for i,h in enumerate(hospitals)])}

📡 INTELLIGENCE FEED:
{chr(10).join(docs) if docs else "No relevant data"}

🟢 SYSTEM STATUS: AUTONOMOUS ACTIVE
"""

# =====================================================
# 🎨 UI
# =====================================================
st.set_page_config(page_title="Green Crisis Grid", layout="wide")

st.title("🚀 Green Crisis Grid AI — WINNING VERSION")

city = st.sidebar.text_input("City", "Faisalabad")
disaster = st.sidebar.selectbox("Disaster", ["Heatwave","Flood","Fire","Earthquake"])
run = st.sidebar.button("RUN EMERGENCY SYSTEM")

# =====================================================
# 🚀 RUN
# =====================================================
if run:

    index = connect_pinecone()

    severity, value, reason = detect(disaster)

    query = f"{disaster} emergency {city}"
    docs = search_documents(index, query)

    hospitals = rank_hospitals()

    st.success("SYSTEM ACTIVE")

    st.markdown("## 🗺️ LIVE DISASTER MAP")
    render_map(severity)

    st.markdown("## 🧠 EMERGENCY REPORT")

    final_report = report(city, disaster, severity, reason, docs, hospitals)

    st.text_area("Report", final_report, height=500)

else:
    st.info("Click RUN EMERGENCY SYSTEM")
