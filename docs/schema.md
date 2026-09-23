# Data Schemas

## PostgreSQL Schema (Relational Data)
This database stores the transactional application state: ingested events, generated alerts, and analyst feedback loops. The static supply chain topology is primarily loaded into the in-memory graph.

### `events` Table
Stores deduplicated events extracted from the NLP pipeline.
- `event_id` (UUID, Primary Key)
- `source_url` (Varchar)
- `published_date` (Timestamp)
- `event_type` (Enum: weather, strike, regulation, transport, supplier-incident)
- `severity_score` (Float)
- `raw_text` (Text)
- `extracted_locations` (JSONB)
- `extracted_orgs` (JSONB)
- `created_at` (Timestamp)

### `alerts` Table
Stores computed exposure alerts linked to the graph.
- `alert_id` (UUID, Primary Key)
- `event_id` (UUID, Foreign Key -> events.event_id)
- `affected_supplier_id` (Varchar)
- `affected_product_id` (Varchar)
- `exposure_score` (Float)
- `propagation_path` (JSONB) - Explainable path, e.g., ["Port X", "Supplier Y", "Product Z"]
- `status` (Enum: pending, accepted, rejected)
- `created_at` (Timestamp)

### `analyst_feedback` Table
Audit trail of analyst interactions.
- `feedback_id` (UUID, Primary Key)
- `alert_id` (UUID, Foreign Key -> alerts.alert_id)
- `analyst_user_id` (Varchar)
- `action` (Enum: accept, reject, re_rank)
- `comments` (Text)
- `timestamp` (Timestamp)

---

## Graph Schema (NetworkX)
The supply-chain topology loaded into NetworkX for traversal and scoring.

### Nodes
Nodes are heterogeneous and identified by a unique string ID. They contain the following attributes:

**Type: `Location`**
- `loc_id` (String)
- `type` (String: port, hub, factory)
- `lat` (Float)
- `lon` (Float)

**Type: `Supplier`**
- `supplier_id` (String)
- `name` (String)
- `risk_rating` (Float)

**Type: `Product`**
- `product_id` (String)
- `category` (String)

### Edges
Edges are directed `(Source -> Target)` to represent flow and dependencies.

- `Supplier -> Product` 
  - Type: `SUPPLIES`
  - Attributes: `weight` (Float, defaults to 1.0)
- `Location -> Supplier`
  - Type: `OPERATES_IN`
  - Attributes: `distance_km` (Float, computed via GeoPandas if needed)
