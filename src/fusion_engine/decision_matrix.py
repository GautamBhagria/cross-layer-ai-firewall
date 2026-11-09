class CrossLayerFusionEngine:
    def __init__(self, high_risk_threshold: float = 0.70, compound_threshold: float = 0.45):
        self.high_risk_threshold = high_risk_threshold
        self.compound_threshold = compound_threshold

    def evaluate_fusion_risk(self, network_risk: float, app_risk: float) -> dict:
        combined_risk = 1.0 - ((1.0 - network_risk) * (1.0 - app_risk))
        
        if network_risk >= self.high_risk_threshold or app_risk >= self.high_risk_threshold:
            return {"verdict": "DROP", "status": "Critical Threat Layer Intercepted", "combined_risk": combined_risk}
            
        if network_risk > self.compound_threshold and app_risk > self.compound_threshold:
            return {"verdict": "DROP", "status": "Cross-Layer Correlated Exploitation Detected", "combined_risk": combined_risk}
            
        if combined_risk >= 0.60:
            return {"verdict": "DROP", "status": "Aggregated Contextual Risk Limit Breached", "combined_risk": combined_risk}
            
        return {"verdict": "ALLOW", "status": "Traffic Approved", "combined_risk": combined_risk}

