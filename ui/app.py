import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Supply Chain Early Warning", layout="wide")

API_URL = "http://127.0.0.1:8000/api/v1"
MOCK_TOKEN = "mock-analyst-token-123"
HEADERS = {"Authorization": f"Bearer {MOCK_TOKEN}"}

st.title("🛡️ Supply Chain Early Warning Center")
st.markdown("### Analyst Dashboard")

# Fetch Alerts
try:
    response = requests.get(f"{API_URL}/alerts")
    if response.status_code == 200:
        alerts = response.json()
        
        if not alerts:
            st.success("No active supply chain threats at this time.")
        else:
            st.subheader(f"Active Alerts ({len(alerts)})")
            
            for idx, a in enumerate(alerts):
                with st.expander(f"🚨 Score: {a['exposure_score']} | Product: {a['affected_product_id']} (Supplier: {a['affected_supplier_id']}) - Status: {a['status'].upper()}"):
                    st.markdown(f"**Explanation Path:** `{a['explanation']}`")
                    
                    if a["status"] == "pending":
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("✅ Accept", key=f"acc_{a['alert_id']}"):
                                requests.post(f"{API_URL}/alerts/{a['alert_id']}/feedback", json={"action": "accept"}, headers=HEADERS)
                                st.rerun()
                        with col2:
                            if st.button("❌ Reject (False Positive)", key=f"rej_{a['alert_id']}"):
                                requests.post(f"{API_URL}/alerts/{a['alert_id']}/feedback", json={"action": "reject"}, headers=HEADERS)
                                st.rerun()
                    else:
                        st.info(f"Alert was previously marked as: {a['status']}")

except Exception as e:
    st.error(f"Failed to connect to API backend. Is FastAPI running? Error: {e}")

st.sidebar.markdown("### Admin / Debug")
st.sidebar.markdown("This UI implements the Phase 6 analyst feedback loop, connecting directly to the `/feedback` FastAPI endpoint.")
