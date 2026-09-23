# News-to-Risk Supply-Chain Early Warning

## Project Overview
This project builds an industry-grade capstone prototype for an early warning system. It ingests unstructured news, extracts events (strikes, weather, etc.) using NLP, and links them to a synthetic geospatial supplier-product graph to compute exposure scores for the supply chain.

## Setup Instructions (Clean Machine)

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd capstone-risk-warning
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # Download the spaCy language model
   python -m spacy download en_core_web_sm
   ```

4. **Environment Variables:**
   Copy the example environment file and update the variables:
   ```bash
   cp .env.example .env
   ```

5. **Run Tests:**
   ```bash
   pytest
   ```
