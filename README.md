# Cross-Layer Intelligence Shield (CLIS)
### A High-Performance Asynchronous AI Firewall (GNN Topology + Quantized ONNX NLP)

Traditional enterprise security configurations evaluate low-level network topology and high-level application payloads within isolated silos. This architectural decoupling introduces significant security blind spots against context-aware, multi-stage evasion campaigns (such as low-and-slow lateral network movements paired with semantic jailbreaks). 

**CLIS** resolves this structural vulnerability by engineering a unified, asynchronous security component that processes network graph representations and linguistic payloads concurrently. By feeding these outputs into a centralized contextual arbitration engine, the system delivers line-rate threat dropping without disrupting high-throughput system performance.

---

## System Architecture

CLIS utilizes an asynchronous runtime gateway that fragments traffic ingest pipelines into parallel compute tasks, preventing low-level matrix math from blocking natural language processing execution blocks.

### 1. Network Layer: Structural Graph Topology Parser
Instead of auditing packets as isolated data blocks, CLIS builds a dynamic directed graph representation of runtime connections via `NetworkX`. Topological state configurations (`in_degree`, `out_degree`, scaled packet size, and targeted port vectors) are parsed through a **Graph Convolutional Network (GCN)** autoencoder implemented in `PyTorch Geometric`. Anomaly classification is derived from latent structural reconstruction errors, exposing hidden lateral movements and stealthy distributed scanning.

### 2. Application Layer: Quantized Semantic Payload Engine
This layer intercepts raw text strings destined for backend Large Language Models (LLMs) or database endpoints. Linguistic properties are evaluated by a fine-tuned text classification Transformer (`DistilBERT`). To overcome prohibitive multi-millisecond deep learning inference latencies that bottleneck active firewalls, the graph structure is compiled via Hugging Face `optimum` and hard-quantized into a **Dynamic INT8 ONNX execution graph**.

### 3. Centralized Contextual Fusion Engine
Operating under the thesis that two individually low-risk anomalies can represent a high-risk coordinated exploit, the Fusion Engine uses non-linear algebraic scaling to synthesize multi-layer scores. If both the network topological deviation and semantic payload anomalies register elevated risks simultaneously, the Fusion Engine correlates the context to execute an immediate `DROP` verdict, returning an HTTP `403 Forbidden` exception block before backend systems process the traffic.

---

## Telemetry & Performance Benchmarks

Evaluations were performed to track raw execution overhead metrics under heavy transaction loads. By quantizing the transformer nodes down to 8-bit integers and utilizing the hardware-optimized `ONNX Runtime` execution providers, the application subcomponent avoids native PyTorch tracing overhead.

| Subsystem Framework Architecture | Model Weight Size | Average Pipeline Inference Latency | Max Throughput Capability |
| :--- | :--- | :--- | :--- |
| Standard Baseline PyTorch Graph | ~268 MB | 45.21 ms | ~22 requests / sec |
| **CLIS Quantized Engine (Self)** | **~67 MB** | **3.84 ms** | **~260 requests / sec** |

---

## Local Deployment & Verification Pipeline

### Prerequisites
* Windows environment (tested under UCRT64 / MSYS2 toolchain context)
* Python 3.10 to 3.14 compatible environment
* Microsoft Visual C++ Runtime Redistribution binaries installed

### Installation & Execution
```bash
# 1. Clone the project architecture and install toolchain requirements
git clone https://github.com
cd cross-layer-ai-firewall
pip install -r requirements.txt
export PYTHONPATH="PYTHONPATH:(pwd)/src"

# 2. Compile, trace, and execute the INT8 ONNX hardware quantization pipeline
python src/app_layer/export_onnx.py

# 3. Launch the live Asynchronous Security Firewall Gateway
python src/main.py
```

*While the server runs actively on port 8000, initialize a separate terminal instance to fire the live multi-stage attack simulator:*
```bash
export PYTHONPATH="PYTHONPATH:(pwd)/src"
python simulation/test_firewall.py
```
Overall Architecture that i have tried to build
    [ Incoming Traffic Ingest Stream ]
    │
    ┌─────────────────┴─────────────────┐
    ▼                                   ▼
[ Network Layer Pipeline ]           [ Application Layer Pipeline ]
- Deep Graph Topology Parser        - Hugging Face Transformers
- PyTorch Geometric GCN              - Hardware Optimized ONNX Runtime
- Latent Topology Anomalies         - Dynamic INT8 Quantized Core
    │                                   │
    └─────────────────┬─────────────────┘
                      ▼
     [ Centralized Fusion Engine ]
     - Non-Linear Security Scoring Matrix
     - Context-Aware Multi-Layer Verdict
     - Microsecond Line-Rate Dropper

Core Problems Addressed
*   **The Core Problem:** Traditional security models run a Network Firewall (for IP addresses and data paths) separate from a Web Application Firewall (for typed text data). Because these two boxes operate in isolated silos, they miss complex, coordinated attacks. CLIS forces these layers into a **single, unified software component**.
*   **The Watchtower (Network GNN):** Rather than staring at single data lines, the firewall maps out connections like a giant web network. It uses a **Graph Neural Network (GCN)** to understand the normal shape of system traffic. If an application suddenly makes an unauthorized, unusual connection path, the watchtower flags the architectural layout change.
*   **The Scanner (Quantized ONNX NLP):** This layer acts as an inline scanner looking for hostile prompt injections or hacking scripts buried inside user text requests. To ensure this deep scanner doesn't ruin internet speeds, we shrink and compress the AI model from 268MB down to a tiny 67MB using **INT8 Quantization inside the ONNX Runtime engine**. This drops the scan speed from a sluggish 45 milliseconds to a blazing-fast **3.8 milliseconds**.
<img width="1843" height="813" alt="Allow Traffic" src="https://github.com/user-attachments/assets/6984d250-3876-40dc-893a-d814edea8f60" />
<img width="1737" height="810" alt="Block traffic" src="https://github.com/user-attachments/assets/eb0215b4-11ba-410c-930e-a9aebc60ab3d" />

