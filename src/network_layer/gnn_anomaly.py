import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
import networkx as nx
import numpy as np

class GCNAnomalyDetector(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels):
        super(GCNAnomalyDetector, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, in_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        return x

class NetworkGraphEngine:
    def __init__(self):
        self.G = nx.DiGraph()
        self.ip_map = {}
        self.feature_dim = 4
        self.model = GCNAnomalyDetector(in_channels=self.feature_dim, hidden_channels=8)
        self.model.eval()

    def _map_ip_to_idx(self, ip: str) -> int:
        if ip not in self.ip_map:
            self.ip_map[ip] = len(self.ip_map)
        return self.ip_map[ip]

    def evaluate_network_risk(self, src: str, dest: str, port: int, packet_size: int) -> float:
        u = self._map_ip_to_idx(src)
        v = self._map_ip_to_idx(dest)
        
        self.G.add_edge(u, v, port=port, size=packet_size)
        num_nodes = len(self.ip_map)
        if num_nodes < 2:
            return 0.0

        edge_index = torch.tensor(list(self.G.edges)).t().contiguous()
        x_list = []
        for node in range(num_nodes):
            in_deg = self.G.in_degree(node) if node in self.G else 0
            out_deg = self.G.out_degree(node) if node in self.G else 0
            x_list.append([float(in_deg), float(out_deg), float(packet_size)/1500.0, float(port)/65535.0])
        
        x = torch.tensor(x_list, dtype=torch.float)
        
        with torch.no_grad():
            reconstructed_x = self.model(x, edge_index)
            loss = F.mse_loss(x[u], reconstructed_x[u]).item()
            
        return float(1.0 / (1.0 + np.exp(-loss * 10)))

