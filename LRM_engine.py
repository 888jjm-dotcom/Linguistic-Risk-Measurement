"""
LRM v4.0 — Linguistic Risk Measurement Engine
Headless Command-Line Engine (App Ready)
"""

import pdfplumber
import re
import pandas as pd
import os
import json
import argparse
from sklearn.preprocessing import StandardScaler
from datetime import datetime

INSTRUMENT_NAME = "LRM v4.0 — Linguistic Risk Measurement Engine"
INSTRUMENT_DESCRIPTOR = "Headless App-Ready Engine (Discourse Expanded)"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORING_CONFIG_PATH = os.path.join(BASE_DIR, "scoring_rules.json")

# ----------------------------
# LOAD SCORING RULES
# ----------------------------

if not os.path.exists(SCORING_CONFIG_PATH):
    raise FileNotFoundError("scoring_rules.json not found.")

with open(SCORING_CONFIG_PATH, "r") as f:
    scoring_config = json.load(f)

SCORING_RULES_VERSION = scoring_config.get("scoring_rules_version", "unknown")

VERDICT_MARKERS = scoring_config.get("verdict_markers", {})
BURDEN_MARKERS = scoring_config.get("burden_markers", {})
DEFLECTION_MARKERS = scoring_config.get("deflection_markers", {})
INTEREST_MARKERS = scoring_config.get("interest_markers", {})
HEDGE_MARKERS = scoring_config.get("hedge_markers", {})
BOOSTER_MARKERS = scoring_config.get("booster_markers", {})
PRESUPPOSITION_MARKERS = scoring_config.get("presupposition_markers", {})

# ----------------------------

def is_passive(sentence):
    passive_pattern = r"\b(is|am|are|was|were|be|been|being)\b\s+([a-z]+ed)\b"
    return bool(re.search(passive_pattern, sentence.lower()))

def analyze_sentence(text, index, total):
    text_low = text.lower()

    scores = {
        "embedded_default": 0.0,
        "burden_shift": 0.0,
        "deflection": 0.0,
        "interest_concealment": 0.0
    }

    multiplier = 1.2 if (index < total * 0.1 or index > total * 0.9) else 1.0

    for marker, weight in VERDICT_MARKERS.items():
        if marker in text_low:
            scores["embedded_default"] += weight * multiplier

    for marker, weight in BURDEN_MARKERS.items():
        if marker in text_low:
            scores["burden_shift"] += weight * multiplier

    for marker, weight in DEFLECTION_MARKERS.items():
        if marker in text_low:
            scores["deflection"] += weight * multiplier

    for marker, weight in INTEREST_MARKERS.items():
        if marker in text_low:
            scores["interest_concealment"] += weight * multiplier

    if is_passive(text_low):
        scores["interest_concealment"] += 0.5

    for marker, weight in PRESUPPOSITION_MARKERS.items():
        if marker in text_low:
            scores["embedded_default"] += weight * multiplier

    for marker, weight in BOOSTER_MARKERS.items():
        if marker in text_low:
            scores["embedded_default"] += weight * multiplier

    for marker, weight in HEDGE_MARKERS.items():
        if marker in text_low:
            scores["embedded_default"] += weight * multiplier * 0.8
            scores["burden_shift"] += weight * multiplier * 0.6

    return scores

def document_risk_vector(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = " ".join([page.extract_text() or "" for page in pdf.pages])

    sentences = [
        s.strip()
        for s in re.split(r'(?<=[.!?])\s+', full_text)
        if len(s.strip()) > 10
    ]

    if not sentences:
        return pd.Series({
            "embedded_default": 0.0,
            "burden_shift": 0.0,
            "deflection": 0.0,
            "interest_concealment": 0.0
        })

    results = [analyze_sentence(s, i, len(sentences)) for i, s in enumerate(sentences)]
    df_results = pd.DataFrame(results)
    return df_results.mean()

# ----------------------------
# MAIN ENGINE ENTRY
# ----------------------------

def run_engine(matter_name, side, file_paths, output_dir):

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    raw_scores_by_document = {}
    side_vectors = []

    for file_path in file_paths:
        if not file_path.lower().endswith(".pdf"):
            continue

        vec = document_risk_vector(file_path)
        if vec is not None:
            filename = os.path.basename(file_path)
            doc_key = f"{side} | {filename}"
            raw_scores_by_document[doc_key] = vec.to_dict()
            side_vectors.append(vec)

    if not raw_scores_by_document:
        raise ValueError("No valid PDFs provided.")

    df = pd.DataFrame.from_dict(raw_scores_by_document, orient="index")

    z_scores_dict = {}
    if len(df) > 1:
        scaler = StandardScaler()
        z = scaler.fit_transform(df)
        z_df = pd.DataFrame(z, index=df.index, columns=df.columns)
        z_scores_dict = z_df.to_dict(orient="index")

    side_summary = {}
    if side_vectors:
        side_df = pd.DataFrame(side_vectors)
        side_summary[side] = side_df.mean().to_dict()

    results_json = {
        "instrument": INSTRUMENT_NAME,
        "descriptor": INSTRUMENT_DESCRIPTOR,
        "run_id": timestamp,
        "matter": matter_name,
        "scoring_rules_version": SCORING_RULES_VERSION,
        "raw_scores_by_document": raw_scores_by_document,
        "z_scores_by_document": z_scores_dict,
        "side_summary": side_summary
    }

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"results_{timestamp}.json")

    with open(output_path, "w") as jf:
        json.dump(results_json, jf, indent=4)

    print(output_path)


def main():
    parser = argparse.ArgumentParser(description="LRM Engine")
    parser.add_argument("--matter", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--files", nargs="+", required=True)

    args = parser.parse_args()

    run_engine(
        matter_name=args.matter,
        side=args.side,
        file_paths=args.files,
        output_dir=args.output
    )


if __name__ == "__main__":
    main()