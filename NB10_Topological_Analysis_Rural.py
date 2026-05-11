import osmnx as ox
import networkx as nx
import folium
from folium import plugins
import random

# =====================================================================
# 1. ENVIRONMENT SETUP & GRAPH DOWNLOAD (RURAL AREA)
# =====================================================================
print("Initializing Rural Environment (Castelli Romani)...")
# Center point between Frascati and Grottaferrata (low density area)
center_point = (41.8000, 12.6700) 

print("Downloading street network from OpenStreetMap (drive)...")
# Using a 5.0km radius to capture the dispersion of rural deliveries
G = ox.graph_from_point(center_point, dist=5000, network_type='drive')

# Central Hub (Isolated peripheral warehouse)
hub_coords = (41.8150, 12.6600) 
hub_node = ox.distance.nearest_nodes(G, hub_coords[1], hub_coords[0])

print("✅ Rural Graph loaded successfully.")

# =====================================================================
# 2. DEMAND GENERATION (Reproducible)
# =====================================================================
random.seed(42) # Ensuring reproducibility for thesis results
all_nodes = list(G.nodes())
daily_orders = random.sample(all_nodes, 20) # 20 random delivery drops

print(f"📦 Generated {len(daily_orders)} random daily orders in the rural area.")

# =====================================================================
# 3. ROUTING FUNCTIONS
# =====================================================================
def get_trip_km(sequence, graph):
    """Calculates total distance of a node sequence in km."""
    km = 0
    for u, v in zip(sequence[:-1], sequence[1:]):
        try:
            d = nx.shortest_path_length(graph, u, v, weight='length')
            km += d
        except nx.NetworkXNoPath:
            km += 5000 # Penalty for unreachable nodes
    return km / 1000

def get_full_path_nodes(sequence, graph):
    """Retrieves full geometry for accurate map rendering."""
    full_path = []
    for u, v in zip(sequence[:-1], sequence[1:]):
        try:
            path_segment = nx.shortest_path(graph, u, v, weight='length')
            if full_path:
                full_path.extend(path_segment[1:]) 
            else:
                full_path.extend(path_segment)
        except nx.NetworkXNoPath:
            pass
    return full_path

# =====================================================================
# 4. SCENARIO A: STANDARD (Consolidated Milk-Run)
# =====================================================================
route_standard_stops = [hub_node]
unvisited = daily_orders.copy()
curr = hub_node

# Nearest Neighbor Heuristic
while unvisited:
    nearest = min(unvisited, key=lambda x: ((G.nodes[curr]['x']-G.nodes[x]['x'])**2 + (G.nodes[curr]['y']-G.nodes[x]['y'])**2))
    route_standard_stops.append(nearest)
    unvisited.remove(nearest)
    curr = nearest
route_standard_stops.append(hub_node) # Return to Hub

km_standard = get_trip_km(route_standard_stops, G)
path_standard_geom = get_full_path_nodes(route_standard_stops, G)

# =====================================================================
# 5. SCENARIO B: EXPRESS (Fragmented Same-Day)
# =====================================================================
# Batches of 5 orders max per trip to simulate urgency
batches = [daily_orders[i:i + 5] for i in range(0, len(daily_orders), 5)] 
km_express_total = 0
routes_express_stops = []      
paths_express_geom = []    

for batch in batches:
    mini_route = [hub_node]
    unvisited_batch = batch.copy()
    curr_b = hub_node
    while unvisited_batch:
        nearest = min(unvisited_batch, key=lambda x: ((G.nodes[curr_b]['x']-G.nodes[x]['x'])**2 + (G.nodes[curr_b]['y']-G.nodes[x]['y'])**2))
        mini_route.append(nearest)
        unvisited_batch.remove(nearest)
        curr_b = nearest
    mini_route.append(hub_node)
    
    routes_express_stops.append(mini_route)
    km_express_total += get_trip_km(mini_route, G)
    paths_express_geom.append(get_full_path_nodes(mini_route, G))

# =====================================================================
# 6. EMISSIONS CALCULATION (ALIGNED WITH THESIS CHAPTER 4)
# =====================================================================
print("\n--- EMISSIONS & TRAFFIC ANALYSIS ---")

# Base emissions derived from EcoFleet ML models (Chapter 4)
ICE_BASE_CO2_STANDARD = 0.1588  # kg CO2/km (158.8 g/km)
ICE_BASE_CO2_EXPRESS  = 0.2053  # kg CO2/km (205.3 g/km)

def get_traffic_penalty(hour):
    if (8 <= hour <= 9) or (17 <= hour <= 19): return 1.8 # Gridlock
    elif (10 <= hour <= 16): return 1.3 # Heavy
    else: return 1.0 # Moderate

# Scenario A Emission (Standard routing, single departure at 07:00 AM)
co2_final_standard = km_standard * ICE_BASE_CO2_STANDARD * get_traffic_penalty(7)

# Scenario B Emission (Express routing, multiple departures)
departure_times = [10, 12, 15, 18]
co2_final_express = 0

print("Express Trips Breakdown:")
for i, route_stops in enumerate(routes_express_stops):
    km_trip = get_trip_km(route_stops, G) 
    factor = get_traffic_penalty(departure_times[i])
    
    partial_co2 = km_trip * ICE_BASE_CO2_EXPRESS * factor
    co2_final_express += partial_co2
    
    print(f"  - Trip {i+1} ({departure_times[i]}:00): {km_trip:.2f} km | Traffic Mult: {factor}x")

diff_perc = ((co2_final_express - co2_final_standard) / co2_final_standard) * 100

print("="*45)
print("FINAL RESULTS: ROUTING TOPOLOGY IMPACT (RURAL)")
print("="*45)
print(f"Total Distance Standard : {km_standard:.2f} km")
print(f"Total Distance Express  : {km_express_total:.2f} km (+{((km_express_total-km_standard)/km_standard)*100:.1f}%)")
print("-" * 45)
print(f"Scenario A (Standard)   : {co2_final_standard:.2f} kg CO₂")
print(f"Scenario B (Express)    : {co2_final_express:.2f} kg CO₂")
print("-" * 45)
print(f"TOTAL EMISSION PENALTY  : +{diff_perc:.1f}%")
print("="*45)

# =====================================================================
# 7. MAP GENERATION (FOLIUM)
# =====================================================================
colors_express = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231']
m_rural = folium.Map(location=hub_coords, zoom_start=12, tiles='cartodbpositron')
plugins.Fullscreen(position='topleft').add_to(m_rural)

fg_standard = folium.FeatureGroup(name="🟦 Scenario A: Standard (Consolidated)")
fg_express = folium.FeatureGroup(name="🟥 Scenario B: Express (Fragmented)")

# Render Standard Route
coords_sus_real = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in path_standard_geom]
plugins.AntPath(
    locations=coords_sus_real,
    color='#0056b3', pulse_color='#FFFFFF', delay=1000, weight=6, opacity=0.8,
    tooltip=f"Consolidated Loop ({km_standard:.1f} km)"
).add_to(fg_standard)

# Render Express Routes
for i, geometry_nodes in enumerate(paths_express_geom):
    coords_real = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in geometry_nodes]
    color = colors_express[i % len(colors_express)]
    plugins.AntPath(
        locations=coords_real,
        color=color, pulse_color='#FFFFFF', delay=600, weight=4, opacity=0.7, dash_array=[10, 20],
        tooltip=f"Express Trip #{i+1}"
    ).add_to(fg_express)

# Render Hub
folium.Marker(
    hub_coords, popup="<b>CENTRAL HUB (RURAL)</b>",
    icon=plugins.BeautifyIcon(icon='industry', prefix='fa', text_color='white', background_color='#222222', border_color='#222222', icon_shape='rectangle-dot', border_width=2),
    z_index_offset=1000
).add_to(m_rural)

fg_standard.add_to(m_rural)
fg_express.add_to(m_rural)
folium.LayerControl(collapsed=False).add_to(m_rural)

# Dashboard HTML Overlay (Specific for Rural context)
title_html_pro = f'''
     <div style="position: fixed; bottom: 30px; left: 30px; width: 350px; z-index:9999; font-family: 'Inter', sans-serif; background-color: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
     <h4 style="margin-top:0; color:#1B4332;"><b>SPEED vs SUSTAINABILITY</b></h4>
     <span style="font-size:13px; color:#52B788;">Rural Road Network (Castelli Romani)</span>
     <hr style="margin: 10px 0; border-top: 1px solid #eee;">
     <div style="display: flex; justify-content: space-between;"><span><i class="fa fa-circle" style="color:#0056b3"></i> <b>Standard:</b></span><span><b>{co2_final_standard:.2f} kg</b></span></div>
     <div style="display: flex; justify-content: space-between;"><span><i class="fa fa-circle" style="color:#e6194b"></i> <b>Express:</b></span><span><b>{co2_final_express:.2f} kg</b></span></div>
     <div style="margin-top: 15px; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #e6194b; border-radius: 4px;">
         <span style="font-size:12px; color:#666;">EMISSION GAP (RURAL PENALTY):</span><br>
         <span style="font-size:22px; color:#d32f2f; font-weight: 800;">+{diff_perc:.1f}% CO₂</span>
     </div>
     </div>
     '''
m_rural.get_root().html.add_child(folium.Element(title_html_pro))

m_rural.save("thesis_result_map_REAL_ROADS_rural.html")
print("✅ Map successfully generated as 'thesis_result_map_REAL_ROADS_rural.html'")