# Model and System Card

## System Name
News-to-Risk Supply-Chain Early Warning System (v1.0.0)

## System Architecture
A composite pipeline consisting of:
1. **Language & Relevance Filter**: Keyword/Stopword heuristics (TRL-4 Baseline).
2. **Event Extraction (NLP)**: Named Entity Recognition via `spaCy` (`en_core_web_sm`) extracting Organizations (ORG) and Locations (GPE/LOC).
3. **Graph Scoring Engine**: A `NetworkX` directed graph calculating downstream exposure paths.

## Intended Use
- **Primary Use Case**: Assisting supply chain analysts by flagging potential disruptions based on unstructured global news.
- **Out-of-Scope**: Automated re-routing of logistics. The system provides *decision support* (Human-in-the-loop), not automated remediation.

## Performance Metrics (Validation Set)
- **ORG Extraction F1**: 0.53
- **LOC Extraction F1**: 0.73
- **Deduplication Rate**: 40.0%
- **Alert Precision**: 0.82

## Limitations & Biases
- **Language Bias**: The NLP pipeline strictly filters for and operates on English text. Global supply chains require multi-lingual extraction (e.g., XLM-RoBERTa), which is planned for future phases.
- **False Positives**: The `en_core_web_sm` model frequently mislabels regulatory acronyms (e.g., 'CBAM') as Organizations.
- **Geospatial Resolution**: Location matching relies on string overlap rather than true geospatial polygons, which may cause mapping errors for cities with duplicate names.

## Privacy & Security
- Raw news text is passed through a PII scrubber (`tests/test_load_security.py`) to redact emails and standard phone patterns before hitting the database or NLP extractor.
