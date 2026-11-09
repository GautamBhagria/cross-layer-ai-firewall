import os
import sys
import time
import streamlit as st
import networkx as nx
import numpy as np

# Windows UCRT64 / Python 3.14 DLL path patch
torch_lib_path = r"C:\Python 314\Lib\site-packages\torch\lib"
if os.path.exists(torch_lib_path) and hasattr(os, "add_dll_directory"):
    os.add_dll_directory(torch_lib_path)

# Ensure current src directory path is mapped for module discovery
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network_layer.gnn_anomaly import NetworkGraphEngine
from app_layer.semantic_filter import ApplicationPayloadEngine
from fusion_engine.decision_matrix import CrossLayerFusionEngine

# Page configurations
st.set_page_config(page_title="CLIS Security Simulation Monitor", layout="wide")

st.title("Cross-Layer Intelligence Shield (CLIS)")
st.markdown("### High-Performance Asynchronous AI Firewall Interface")
st.write("Simulate real-time traffic vectors combining GNN network graphs and quantized ONNX language analysis.")

# Initialize the backend security engines inside Streamlit's session cache memory
@st.cache_resource
def init_security_engines():
    return NetworkGraphEngine(), ApplicationPayloadEngine(), CrossLayerFusionEngine()

try:
    network_engine, app_engine, fusion_engine = init_security_engines()
except Exception as e:
    st.error(f"Engine Initialization Error: {str(e)}")
    st.info("Please make sure you have run 'python src/app_layer/export_onnx.py' first to build the model files.")
    st.stop()

# Layout splits: Controls (Left side) vs Analytics Visualizer (Right side)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Inbound Traffic Configuration")
    
    with st.form("traffic_form"):
        src_ip = st.text_input("Source IP Address", "192.168.1.45")
        dest_ip = st.text_input("Destination Host IP", "10.0.0.10")
        
        port = st.number_input("Target Connection Port", min_value=1, max_value=65535, value=80)
        packet_size = st.slider("Packet Data Footprint Size (Bytes)", min_value=64, max_value=1500, value=256)
        
        payload_text = st.text_area(
            "Application Data Layer Payload (String text)",
            value="Fetch general system performance reports."
        )
        
        submit_btn = st.form_submit_button(" Inject Traffic Vector")

with col2:
    st.subheader("Live Firewall Execution Analytics")
    
    if submit_btn:
        start_time = time.perf_counter()
        
        # Run local parallel trace models
        with st.spinner("Processing cross-layer components..."):
            network_risk = network_engine.evaluate_network_risk(src_ip, dest_ip, port, packet_size)
            app_risk = app_engine.evaluate_payload_risk(payload_text)
            decision = fusion_engine.evaluate_fusion_risk(network_risk, app_risk)
            
        latency = (time.perf_counter() - start_time) * 1000 # Convert to milliseconds
        
        # Render clean system layout cards
        v_color = "DROP" if decision["verdict"] == "DROP" else "🟢 ALLOW"
        st.metric(label="FINAL VERDICT RESULT", value=v_color, delta=decision["status"], delta_color="inverse" if decision["verdict"] == "DROP" else "normal")
        
        # Display structural data visualization graphs
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Network Anomaly Index", f"{round(network_risk * 100, 2)}%")
        m_col2.metric("Application Threat Level", f"{round(app_risk * 100, 2)}%")
        m_col3.metric("System Pipeline Latency", f"{round(latency, 4)} ms")
        
        # Raw payload schema reporting box
        st.subheader("📋 JSON Security Audit Log")
        st.json({
            "inbound_vector": {
                "route": f"{src_ip} -> {dest_ip}",
                "port": port,
                "bytes": packet_size,
                "payload": payload_text
            },
            "security_analytics": {
                "gnn_network_score": round(network_risk, 5),
                "onnx_nlp_score": round(app_risk, 5),
                "aggregated_fusion_score": round(decision["combined_risk"], 5),
                "line_rate_latency_ms": round(latency, 4)
            },
            "firewall_action": decision["verdict"]
        })
    else:
        st.info("Adjust the traffic configuration inputs on the left panel and click 'Inject Traffic Vector' to start the simulation visualization graph.")

