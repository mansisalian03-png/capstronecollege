# User Guide (Supply Chain Analyst)

## Overview
The News-to-Risk Early Warning System automatically monitors global news feeds, extracts disruption events (strikes, weather, fires), and maps them against our internal supply chain graph to warn you about downstream impacts.

## Navigating the Dashboard
1. Open your browser to `http://localhost:8501`.
2. The dashboard displays **Active Alerts**, ranked by their **Exposure Score** (a combination of event severity and supplier risk).
3. **Explanation Path**: Click on any alert to expand it. You will see the exact reason the alert fired (e.g., `Strike event in Los Angeles -> Supplier A operates in Los Angeles -> Product X depends on Supplier A`).

## Submitting Feedback
The system relies on a Human-in-the-Loop mechanism to learn. 
- **Accept**: If the alert is accurate and actionable, click Accept.
- **Reject (False Positive)**: If the NLP model extracted the wrong location, or the news is irrelevant, click Reject.

Your feedback is securely recorded in the audit trail and is used to compute the "Alert Precision" metric.
