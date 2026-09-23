import pytest
import os
from graph.engine import SupplyChainGraph
from scoring.score import ScoringEngine

def test_graph_and_scoring(tmp_path):
    # 1. Create Mock CSV Data
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    (data_dir / "locations.csv").write_text("loc_id,city,country,lat,lon,type\nL01,Kaohsiung,Taiwan,22.0,120.0,port\nL02,Mumbai,India,19.0,72.0,port\n")
    (data_dir / "suppliers.csv").write_text("supplier_id,name,risk_rating,loc_id\nS01,Supplier A,4.5,L01\nS02,Supplier B,2.0,L02\n")
    (data_dir / "products.csv").write_text("product_id,name,category\nP01,Widget X,Electronics\nP02,Widget Y,Textiles\n")
    (data_dir / "graph_edges.csv").write_text("source,target,edge_type\nS01,P01,SUPPLIES\nS02,P02,SUPPLIES\n")
    
    # 2. Build Graph
    graph_engine = SupplyChainGraph()
    graph_engine.load_from_csv(str(data_dir))
    
    # Assert NetworkX graph is built correctly
    assert graph_engine.G.number_of_nodes() == 6 # 2 locs, 2 sups, 2 prods
    
    # 3. Initialize Scoring Engine
    log_dir = tmp_path / "logs"
    scoring_engine = ScoringEngine(graph_engine, str(log_dir))
    
    # 4. Test Scenario: Event in Kaohsiung
    event_1 = {
        "id": "evt_100",
        "event_type": "weather",
        "locs": ["Kaohsiung"]
    }
    
    alerts_1 = scoring_engine.process_event(event_1)
    
    # Should alert for Supplier A and Product P01
    assert len(alerts_1) == 1
    assert alerts_1[0]["affected_supplier_id"] == "S01"
    assert alerts_1[0]["affected_product_id"] == "P01"
    assert alerts_1[0]["exposure_score"] > 0
    # Check Explainable Path
    assert "Weather event in Kaohsiung" in alerts_1[0]["explanation"]
    assert "Widget X' depends on 'Supplier A'" in alerts_1[0]["explanation"]
    
    # 5. Test Scenario: Event in isolated location
    event_2 = {
        "id": "evt_101",
        "event_type": "strike",
        "locs": ["Nowhere City"]
    }
    alerts_2 = scoring_engine.process_event(event_2)
    assert len(alerts_2) == 0 # No downstream impact
    
    # 6. Verify Audit Log
    log_file = log_dir / "audit_log.txt"
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "evt_100" in log_content
    assert "Kaohsiung" in log_content
