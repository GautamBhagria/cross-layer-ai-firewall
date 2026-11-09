import asyncio
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from network_layer.gnn_anomaly import NetworkGraphEngine
from app_layer.semantic_filter import ApplicationPayloadEngine
from fusion_engine.decision_matrix import CrossLayerFusionEngine

app = FastAPI(title="Cross-Layer Intelligence Shield (CLIS)")

network_engine = NetworkGraphEngine()
app_engine = ApplicationPayloadEngine()
fusion_engine = CrossLayerFusionEngine()

class SecurityRequest(BaseModel):
    source_ip: str
    dest_ip: str
    port: int
    packet_size: int
    payload_text: str

@app.post("/filter")
async def filter_traffic(traffic: SecurityRequest):
    start_time = time.perf_counter()
    try:
        network_task = asyncio.to_thread(
            network_engine.evaluate_network_risk, 
            traffic.source_ip, traffic.dest_ip, traffic.port, traffic.packet_size
        )
        app_task = asyncio.to_thread(
            app_engine.evaluate_payload_risk, 
            traffic.payload_text
        )
        network_risk, app_risk = await asyncio.gather(network_task, app_task)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Processing Fault", "message": str(e)})

    decision = fusion_engine.evaluate_fusion_risk(network_risk, app_risk)
    latency = time.perf_counter() - start_time

    response_data = {
        "verdict": decision["verdict"],
        "status_summary": decision["status"],
        "telemetry": {
            "network_risk": round(network_risk, 4),
            "application_risk": round(app_risk, 4),
            "combined_risk": round(decision["combined_risk"], 4),
            "latency_seconds": round(latency, 6)
        }
    }

    if decision["verdict"] == "DROP":
        raise HTTPException(status_code=403, detail=response_data)
    return response_data

