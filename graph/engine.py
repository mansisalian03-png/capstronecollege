import csv
import os
import networkx as nx

class SupplyChainGraph:
    """
    Builds the NetworkX supply chain graph from synthetic data.
    """
    def __init__(self):
        self.G = nx.DiGraph()
        
    def load_from_csv(self, data_dir):
        loc_file = os.path.join(data_dir, 'locations.csv')
        sup_file = os.path.join(data_dir, 'suppliers.csv')
        prod_file = os.path.join(data_dir, 'products.csv')
        edge_file = os.path.join(data_dir, 'graph_edges.csv')
        
        # Load Locations
        with open(loc_file, 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                self.G.add_node(row["loc_id"], type="location", city=row["city"], lat=row["lat"], lon=row["lon"])
                
        # Load Suppliers and link to Locations (Location -> Supplier)
        with open(sup_file, 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                self.G.add_node(row["supplier_id"], type="supplier", name=row["name"], risk_rating=row["risk_rating"])
                # Implicit geospatial edge: the supplier operates in this location
                self.G.add_edge(row["loc_id"], row["supplier_id"], edge_type="OPERATES_IN")
                
        # Load Products
        with open(prod_file, 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                self.G.add_node(row["product_id"], type="product", name=row["name"], category=row["category"])
                
        # Load Supplier -> Product edges
        with open(edge_file, 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                self.G.add_edge(row["source"], row["target"], edge_type=row["edge_type"])

    def get_downstream_impacts(self, loc_name):
        """
        Traverses the graph to find all paths from a compromised location to downstream products.
        """
        # Find loc_id by city name (case-insensitive)
        start_nodes = [
            n for n, attr in self.G.nodes(data=True) 
            if attr.get("type") == "location" and attr.get("city", "").lower() == loc_name.lower()
        ]
        
        impacts = []
        for start in start_nodes:
            # Get all nodes reachable from the location
            for successor in nx.bfs_tree(self.G, start):
                node_data = self.G.nodes[successor]
                # If it's a product, we found a complete impact path
                if node_data.get("type") == "product":
                    paths = list(nx.all_simple_paths(self.G, start, successor))
                    for p in paths:
                        impacts.append(p)
                        
        return impacts
