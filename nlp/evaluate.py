from nlp.extract import BaselineExtractor, NLPExtractor
from nlp.dedup import deduplicate_events

# Hand-labeled validation set for computing F1
VALIDATION_SET = [
    {
        "text": "Operations at Kaohsiung port halted as Typhoon Koinu approaches Taiwan with heavy winds.",
        "true_orgs": [],
        "true_locs": ["Kaohsiung", "Taiwan"],
        "true_event": "weather"
    },
    {
        "text": "The UAW strike expands to include parts distribution centers across the midwest.",
        "true_orgs": ["UAW"],
        "true_locs": ["midwest"],
        "true_event": "strike"
    },
    {
        "text": "The EU rolls out the CBAM regulation imposing new reporting requirements.",
        "true_orgs": ["EU"],
        "true_locs": [],
        "true_event": "regulation"
    },
    {
        "text": "A massive fire broke out at the Renesas fab in Naka causing production halts.",
        "true_orgs": ["Renesas"],
        "true_locs": ["Naka"],
        "true_event": "supplier-incident"
    },
    {
        "text": "A sudden walkout by dockworkers at the Port of Los Angeles has paused unloading.",
        "true_orgs": [], # It's a location, not an org strictly
        "true_locs": ["Port of Los Angeles", "Los Angeles"],
        "true_event": "strike"
    }
]

def compute_f1(true_items, pred_items):
    true_set = set([x.lower() for x in true_items])
    pred_set = set([x.lower() for x in pred_items])
    
    tp = len(true_set.intersection(pred_set))
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return precision, recall, f1

def evaluate_extractor(extractor_name, extractor):
    f1_scores_org = []
    f1_scores_loc = []
    acc_event = []
    
    for item in VALIDATION_SET:
        pred = extractor.extract(item["text"])
        
        _, _, f1_org = compute_f1(item["true_orgs"], pred["orgs"])
        _, _, f1_loc = compute_f1(item["true_locs"], pred["locs"])
        
        f1_scores_org.append(f1_org)
        f1_scores_loc.append(f1_loc)
        acc_event.append(1 if pred["event_type"] == item["true_event"] else 0)
        
    avg_f1_org = sum(f1_scores_org) / len(f1_scores_org)
    avg_f1_loc = sum(f1_scores_loc) / len(f1_scores_loc)
    avg_acc_event = sum(acc_event) / len(acc_event)
    
    print(f"--- {extractor_name} Performance ---")
    print(f"ORG Extraction F1:   {avg_f1_org:.2f}")
    print(f"LOC Extraction F1:   {avg_f1_loc:.2f}")
    print(f"Event Type Accuracy: {avg_acc_event:.2f}\n")

def evaluate_deduplication():
    # Synthetic flood of duplicate events
    events = [
        {"id": 1, "text": "A sudden walkout by dockworkers at the Port of Los Angeles has paused unloading."},
        {"id": 2, "text": "Dockworkers walk out at Port of Los Angeles, pausing unloading operations."}, # Near duplicate
        {"id": 3, "text": "Strike at Port of Los Angeles causes delays."}, # Near duplicate
        {"id": 4, "text": "A massive fire broke out at the Renesas fab in Naka."},
        {"id": 5, "text": "Fire incident reported at Renesas Naka facility."} # Near duplicate
    ]
    
    unique_events, reduction_rate = deduplicate_events(events, threshold=0.55)
    
    print(f"--- Deduplication Performance ---")
    print(f"Total incoming events: {len(events)}")
    print(f"Unique events after dedup: {len(unique_events)}")
    print(f"Duplicate Reduction Rate: {reduction_rate:.1%}\n")

if __name__ == "__main__":
    baseline = BaselineExtractor()
    nlp = NLPExtractor()
    
    evaluate_extractor("Baseline Extractor (Keyword/Regex)", baseline)
    evaluate_extractor("NLP Extractor (spaCy/HF Pipeline)", nlp)
    evaluate_deduplication()
