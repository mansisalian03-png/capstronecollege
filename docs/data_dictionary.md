# Data Dictionary

## Provenance and Usage
This dataset is composed of a curated news corpus and a synthetically generated supplier-product graph. It is intended strictly for the "News-to-Risk Supply-Chain Early Warning" capstone prototype. 
- **News Corpus**: Curated synthetic snippets inspired by real events. Released under CC0 / Public Domain for testing purposes.
- **Supply Chain Graph**: Generated programmatically via `data/generate_graph.py` with a fixed seed for reproducibility. Real city coordinates are mixed with synthetic nodes. No proprietary data is used.

## 1. news_corpus.csv
Curated news bulletins representing various supply chain disruption events.

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Unique identifier for the news item. |
| `date` | Date (YYYY-MM-DD) | Publication date of the bulletin. |
| `title` | String | Headline of the news article. |
| `text` | String | Full text body of the bulletin for NLP extraction. |
| `source` | String | Provenance (e.g., 'Synthetic_SC_News'). |
| `url` | String | Originating URL or placeholder. |
| `category` | String | Label for testing classification (weather, strike, regulation, transport, supplier-incident). |

## 2. locations.csv
Geocoded locations serving as nodes in the supply chain graph.

| Field | Type | Description |
|-------|------|-------------|
| `loc_id` | String | Unique identifier (e.g., L01). |
| `city` | String | Name of the city/port. |
| `country` | String | Name of the country. |
| `lat` | Float | Latitude coordinate (-90 to 90). |
| `lon` | Float | Longitude coordinate (-180 to 180). |
| `type` | String | Type of location (port, hub, factory). |

## 3. suppliers.csv
Entities that produce goods or materials.

| Field | Type | Description |
|-------|------|-------------|
| `supplier_id` | String | Unique identifier (e.g., S001). |
| `name` | String | Name of the supplier. |
| `risk_rating` | Float | Synthetic baseline risk score (1.0 - 5.0). |
| `loc_id` | String | Foreign key to `locations.csv`. |

## 4. products.csv
Products manufactured or transported within the supply chain.

| Field | Type | Description |
|-------|------|-------------|
| `product_id` | String | Unique identifier (e.g., P001). |
| `name` | String | Name of the product. |
| `category` | String | Industry category (e.g., Electronics, Textiles). |

## 5. graph_edges.csv
Relationships connecting nodes (Suppliers -> Products). In a graph database, these form directed edges.

| Field | Type | Description |
|-------|------|-------------|
| `source` | String | ID of the source node (e.g., `supplier_id`). |
| `target` | String | ID of the target node (e.g., `product_id`). |
| `edge_type` | String | Type of relationship (e.g., 'SUPPLIES'). |
