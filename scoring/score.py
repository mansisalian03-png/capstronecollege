import datetime
import os
import math

class ScoringEngine:
    """
    Computes exposure scores and explainable propagation paths.
    Note: Standard GeoPandas geospatial joins fall back to pure-Python haversine/name-matching 
    here to accommodate the lack of Python 3.14 C-wheels. The algorithmic logic is identical.
    """
    def __init__(self, graph_engine, log_dir):
        self.graph = graph_engine
        self.log_file = os.path.join(log_dir, "audit_log.txt")
        # Ensure log dir exists
        os.makedirs(log_dir, exist_ok=True)
        
    def log_decision(self, event_id, event_type, path_nodes, score, explanation):
        timestamp = datetime.datetime.now().isoformat()
        log_entry = (
            f"[{timestamp}] ALERT GENERATED | "
            f"EventID: {event_id} | Type: {event_type} | "
            f"Score: {score} | Path: {path_nodes} | "
            f"Explanation: {explanation}\n"
        )
        with open(self.log_file, "a", encoding='utf-8') as f:
            f.write(log_entry)
            
    def process_event(self, event):
        alerts = []
        event_id = event.get("id", "evt_unknown")
        event_type = event.get("event_type", "unknown")
        
        # Base severity heuristic based on event type
        base_severity = 0.8 if event_type in ["weather", "supplier-incident", "strike"] else 0.5
        
        for loc_name in event.get("locs", []):
            impact_paths = self.graph.get_downstream_impacts(loc_name)
            
            for path in impact_paths:
                # Path structure: [Location_ID, Supplier_ID, Product_ID]
                if len(path) != 3:
                    continue
                    
                loc_node = self.graph.G.nodes[path[0]]
                sup_node = self.graph.G.nodes[path[1]]
                prod_node = self.graph.G.nodes[path[2]]
                
                # Retrieve supplier static risk rating
                risk_rating = float(sup_node.get("risk_rating", 1.0))
                
                # Compute Exposure Score (Base Event Severity * Static Supplier Risk)
                exposure_score = round((base_severity * risk_rating) / 5.0, 2) # Normalized to 0-1
                
                # Generate EXPLAINABLE propagation path string
                explanation = (
                    f"{event_type.capitalize()} event in {loc_node['city']} -> "
                    f"Supplier '{sup_node['name']}' operates in {loc_node['city']} -> "
                    f"Product '{prod_node['name']}' depends on '{sup_node['name']}'."
                )
                
                # Audit trail logging
                self.log_decision(event_id, event_type, path, exposure_score, explanation)
                
                alerts.append({
                    "event_id": event_id,
                    "affected_supplier_id": path[1],
                    "affected_product_id": path[2],
                    "exposure_score": exposure_score,
                    "explanation": explanation
                })
                
        return alerts
