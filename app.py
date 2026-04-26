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

# =====================================================
# 🌍 CITY DATABASE
# =====================================================

CITIES = {
    "Faisalabad": (31.4504, 73.1350),
    "Lahore": (31.5204, 74.3587),
    "Karachi": (24.8607, 67.0011),
    "Islamabad": (33.6844, 73.0479),
    "Multan": (30.1575, 71.5249)
}

# =====================================================
# 🏥 CITY HOSPITAL DATABASE
# =====================================================

HOSPITALS = {
    "Faisalabad": [
        {"name": "Allied Hospital", "lat": 31.4180, "lon": 73.0790},
        {"name": "DHQ Hospital", "lat": 31.4150, "lon": 73.0890},
        {"name": "Faisal Hospital", "lat": 31.4300, "lon": 73.1100},
    ],
    "Lahore": [
        {"name": "Mayo Hospital", "lat": 31.5651, "lon": 74.3142},
        {"name": "Jinnah Hospital", "lat": 31.4697, "lon": 74.2867},
        {"name": "Services Hospital", "lat": 31.5215, "lon": 74.3311},
    ],
    "Karachi": [
        {"name": "JPMC", "lat": 24.8600, "lon": 67.0100},
        {"name": "Civil Hospital", "lat": 24.8550, "lon": 67.0300},
        {"name": "Aga Khan Hospital", "lat": 24.8937, "lon": 67.0686},
    ],
    "Islamabad": [
        {"name": "PIMS", "lat": 33.7070, "lon": 73.0400},
        {"name": "Polyclinic Hospital", "lat": 33.7200, "lon": 73.0600},
    ],
    "Multan": [
        {"name": "Nishtar Hospital", "lat": 30.1570, "lon": 71.5240},
        {"name": "DHQ Hospital", "lat": 30.1900, "lon": 71.4700},
    ]
}

# =====================================================
# 🧠 PINECONE CONNECTION
# =====================================================

def connect_pinecone():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc.Index(INDEX_NAME)


# =====================================================
# 📡 PINECONE SEARCH
# =====================================================

def search_documents(index, query):
    try:
        results = index.search(
            namespace="default",
            query={
                "inputs": {
                    "text": query
                },
                "top_k": 3
            }
        )

        docs = []

        hits = results.get("result", {}).get("hits", [])

        for hit in hits:
            text = (
                hit.get("fields", {}).get("text")
                or hit.get("metadata", {}).get("text")
                or ""
            )

            if text:
                docs.append(text)

        return docs

    except Exception as e:
        st.error(f"Pinecone Search Error: {str(e)}")
        return []


# =====================================================
# 🌍 CITY COORDINATES
# =====================================================

def get_coords(city):
    return CITIES.get(city, (31.4504, 73.1350))


# =====================================================
# 🌡️ AUTONOMOUS DISASTER MODELS
# =====================================================

def heatwave_model(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
        data = requests.get(url).json()

        temp = data["hourly"]["temperature_2m"][0]

        if temp >= 45:
            return 9, f"Extreme heatwave detected ({temp}°C)"
        elif temp >= 40:
            return 7, f"Severe heat conditions ({temp}°C)"
        elif temp >= 35:
            return 5, f"Moderate heatwave ({temp}°C)"
        else:
            return 3, f"Normal temperature ({temp}°C)"

    except:
        return 5, "Temperature API unavailable"


def flood_model(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=precipitation"
        data = requests.get(url).json()

        rain = data["hourly"]["precipitation"][0]

        if rain > 20:
            return 9, f"Flash flood risk ({rain} mm rainfall)"
        elif rain > 10:
            return 7, f"Heavy rainfall ({rain} mm)"
        elif rain > 5:
            return 5, f"Moderate rainfall ({rain} mm)"
        else:
            return 3, f"Low rainfall ({rain} mm)"

    except:
        return 5, "Flood API unavailable"


def fire_model(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=wind_speed_10m"
        data = requests.get(url).json()

        wind = data["hourly"]["wind_speed_10m"][0]

        if wind >= 40:
            return 8, f"High fire spread risk ({wind} km/h wind)"
        elif wind >= 25:
            return 6, f"Moderate fire spread risk ({wind} km/h)"
        else:
            return 3, f"Low fire risk ({wind} km/h)"

    except:
        return 5, "Fire API unavailable"


def earthquake_model():
    try:
        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
        data = requests.get(url).json()

        if not data["features"]:
            return 3, "No recent seismic activity"

        mag = data["features"][0]["properties"]["mag"]

        if mag >= 6:
            return 9, f"Strong earthquake detected (M {mag})"
        elif mag >= 4:
            return 7, f"Moderate earthquake detected (M {mag})"
        else:
            return 4, f"Minor tremors detected (M {mag})"

    except:
        return 5, "Earthquake API unavailable"


# =====================================================
# 🧠 MASTER DETECTION ENGINE
# =====================================================

def detect_disaster(disaster, lat, lon):
    if disaster == "Heatwave":
        return heatwave_model(lat, lon)

    elif disaster == "Flood":
        return flood_model(lat, lon)

    elif disaster == "Fire":
        return fire_model(lat, lon)

    elif disaster == "Earthquake":
        return earthquake_model()

    return 5, "Unknown condition"


# =====================================================
# 🏥 DISTANCE CALCULATION (HAVERSINE)
# =====================================================

def distance(lat1, lon1, lat2, lon2):
    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def rank_hospitals(city, lat, lon):
    hospitals = HOSPITALS.get(city, [])

    ranked = []

    for hospital in hospitals:
        dist = distance(
            lat,
            lon,
            hospital["lat"],
            hospital["lon"]
        )

        ranked.append({
            "name": hospital["name"],
            "lat": hospital["lat"],
            "lon": hospital["lon"],
            "distance": round(dist, 2)
        })

    ranked.sort(key=lambda x: x["distance"])
    return ranked


# =====================================================
# 🚑 EVACUATION LOGIC
# =====================================================

def evacuation_plan(severity):
    if severity >= 8:
        return "CRITICAL EVACUATION — Immediate relocation required"

    elif severity >= 5:
        return "CONTROLLED EVACUATION — High alert mode"

    return "NORMAL MONITORING — Safe movement"


# =====================================================
# 🗺️ REAL GIS MAP SYSTEM
# =====================================================

def render_map(lat, lon, severity, hospitals):
    # ---------------------------------------------
    # REAL GIS HEATMAP DATA
    # ---------------------------------------------

    heat_data = [
        {"lat": lat, "lon": lon, "weight": severity},
        {"lat": lat + 0.01, "lon": lon + 0.01, "weight": severity * 0.8},
        {"lat": lat - 0.01, "lon": lon - 0.02, "weight": severity * 0.7},
        {"lat": lat + 0.02, "lon": lon - 0.015, "weight": severity * 0.6},
        {"lat": lat - 0.02, "lon": lon + 0.02, "weight": severity * 0.5},
    ]

    # ---------------------------------------------
    # HEATMAP LAYER
    # ---------------------------------------------

    heat_layer = pdk.Layer(
        "HeatmapLayer",
        data=heat_data,
        get_position='[lon, lat]',
        get_weight='weight',
        radiusPixels=80,
        intensity=1.5,
        threshold=0.2,
    )

    # ---------------------------------------------
    # HOSPITAL LAYER
    # ---------------------------------------------

    hospital_layer = pdk.Layer(
        "ScatterplotLayer",
        data=hospitals,
        get_position='[lon, lat]',
        get_color='[0, 0, 255, 200]',
        get_radius=10000,
        pickable=True,
    )

    # ---------------------------------------------
    # DISASTER CENTER LAYER
    # ---------------------------------------------

    center_layer = pdk.Layer(
        "ScatterplotLayer",
        data=[{"lat": lat, "lon": lon}],
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 255]',
        get_radius=15000,
    )

    # ---------------------------------------------
    # VIEW STATE
    # ---------------------------------------------

    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=10,
        pitch=40,
    )

    # ---------------------------------------------
    # FINAL MAP
    # ---------------------------------------------

    st.pydeck_chart(
        pdk.Deck(
            layers=[
                heat_layer,
                hospital_layer,
                center_layer
            ],
            initial_view_state=view_state,
            tooltip={
                "text": "{name}"
            }
        )
    )


# =====================================================
# 🧾 FINAL REPORT
# =====================================================

def generate_report(city, disaster, severity, reason, docs, hospitals):
    hospital_text = "\n".join([
        f"{i+1}. {h['name']} ({h['distance']} km)"
        for i, h in enumerate(hospitals)
    ])

    knowledge_text = "\n".join(docs) if docs else "No matching intelligence found."

    return f"""
GREEN CRISIS GRID — AUTONOMOUS EMERGENCY SYSTEM
===============================================

City: {city}
Disaster Type: {disaster}
Severity Score: {severity}/10

AI Analysis:
{reason}

Evacuation Strategy:
{evacuation_plan(severity)}

Hospital Priority Ranking:
{hospital_text}

Knowledge Intelligence:
{knowledge_text}

System Status:
AUTONOMOUS ACTIVE RESPONSE MODE
"""


# =====================================================
# 🎨 STREAMLIT UI
# =====================================================

st.set_page_config(
    page_title="Green Crisis Grid AI",
    layout="wide"
)

st.title("🚀 Green Crisis Grid AI")
st.subheader("Real GIS + Autonomous Disaster Intelligence System")

st.markdown("""
AI-powered emergency command system with:

- Real-time disaster severity detection
- Live GIS disaster heatmaps
- Hospital prioritization by distance
- Pinecone RAG intelligence retrieval
- Autonomous evacuation planning
""")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Emergency Input")

city = st.sidebar.selectbox(
    "Select City",
    list(CITIES.keys())
)

disaster = st.sidebar.selectbox(
    "Disaster Type",
    [
        "Heatwave",
        "Flood",
        "Fire",
        "Earthquake"
    ]
)

run = st.sidebar.button("Run Autonomous System")

# =====================================================
# MAIN EXECUTION
# =====================================================

if run:
    if not PINECONE_API_KEY:
        st.error("Missing Pinecone API Key in Streamlit secrets")
        st.stop()

    with st.spinner("Running autonomous disaster intelligence..."):
        lat, lon = get_coords(city)

        severity, reason = detect_disaster(
            disaster,
            lat,
            lon
        )

        index = connect_pinecone()

        query = f"{disaster} emergency response {city}"

        docs = search_documents(
            index,
            query
        )

        hospitals = rank_hospitals(
            city,
            lat,
            lon
        )

        st.success("System Activated")

        st.markdown("## 🗺️ Crisis Command GIS Map")
        render_map(
            lat,
            lon,
            severity,
            hospitals
        )

        st.markdown("## 🧠 AI Emergency Report")

        report = generate_report(
            city,
            disaster,
            severity,
            reason,
            docs,
            hospitals
        )

        st.text_area(
            "Generated Report",
            report,
            height=500
        )

else:
    st.info("Select city + disaster and click Run Autonomous System")
