"""
LRM v3.7 — Linguistic Risk Measurement
Timestamped Auditable Metrics with Auditable Output
Discourse-Expanded Scoring (Hedges, Boosters, Presuppositions)
"""

import pdfplumber
import re
import pandas as pd
import os
import shutil
import json
from sklearn.preprocessing import StandardScaler
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

INSTRUMENT_NAME = "LRM v3.7 — Linguistic Risk Measurement"
INSTRUMENT_DESCRIPTOR = "Timestamped Auditable Metrics with Auditable Output (Discourse Expanded)"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATTERS_DIR = os.path.join(BASE_DIR, "Matters")
SCORING_CONFIG_PATH = os.path.join(BASE_DIR, "scoring_rules.json")

# ----------------------------
# LOAD SCORING RULES
# ----------------------------

if not os.path.exists(SCORING_CONFIG_PATH):
    raise FileNotFoundError("scoring_rules.json not found in project directory.")

with open(SCORING_CONFIG_PATH, "r") as f:
    scoring_config = json.load(f)

SCORING_RULES_VERSION = scoring_config.get("scoring_rules_version", "unknown")

VERDICT_MARKERS = scoring_config.get("verdict_markers", {})
BURDEN_MARKERS = scoring_config.get("burden_markers", {})
DEFLECTION_MARKERS = scoring_config.get("deflection_markers", {})
INTEREST_MARKERS = scoring_config.get("interest_markers", {})

# New optional discourse categories
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

    # Primary LRM dimensions
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

    # Passive voice heuristic
    if is_passive(text_low):
        scores["interest_concealment"] += 0.5

    # ----------------------------
    # Discourse Expansion (v2 rules)
    # ----------------------------

    # Presuppositions increase embedded_default
    for marker, weight in PRESUPPOSITION_MARKERS.items():
        if marker in text_low:
            scores["embedded_default"] += weight * multiplier

    # Boosters intensify embedded_default
    for marker, weight in BOOSTER_MARKERS.items():
        if marker in text_low:
            scores["embedded_default"] += weight * multiplier

    # Hedges dampen embedded_default and burden_shift
    for marker, weight in HEDGE_MARKERS.items():
        if marker in text_low:
            scores["embedded_default"] += weight * multiplier * 0.8
            scores["burden_shift"] += weight * multiplier * 0.6

    return scores

def document_risk_vector(pdf_path):
    try:
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

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def select_or_create_matter():
    existing = os.listdir(MATTERS_DIR)

    print("\nExisting Matters:")
    for i, m in enumerate(existing):
        print(f"{i+1}. {m}")

    print("\n0. Create New Matter")

    choice = input("Select Matter: ")

    if choice == "0":
        name = input("Enter new Matter name: ")
        matter_path = os.path.join(MATTERS_DIR, name)
        os.makedirs(os.path.join(matter_path, "Side_A"), exist_ok=True)
        os.makedirs(os.path.join(matter_path, "Side_B"), exist_ok=True)
        return matter_path
    else:
        return os.path.join(MATTERS_DIR, existing[int(choice)-1])

def copy_to_side(files, matter_path, side):
    side_path = os.path.join(matter_path, side)
    os.makedirs(side_path, exist_ok=True)
    for f in files:
        shutil.copy(f, side_path)

def analyze_matter(matter_path):

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_base = os.path.join(matter_path, "analysis_output")
    os.makedirs(output_base, exist_ok=True)

    run_output_dir = os.path.join(output_base, timestamp)
    os.makedirs(run_output_dir, exist_ok=True)

    raw_scores_by_document = {}
    side_data = {"Side_A": [], "Side_B": []}

    for side in ["Side_A", "Side_B"]:
        side_path = os.path.join(matter_path, side)
        if not os.path.exists(side_path):
            continue

        for file in os.listdir(side_path):
            if file.lower().endswith(".pdf"):
                full_path = os.path.join(side_path, file)
                vec = document_risk_vector(full_path)
                if vec is not None:
                    doc_key = f"{side} | {file}"
                    raw_scores_by_document[doc_key] = vec.to_dict()
                    side_data[side].append(vec)

    if not raw_scores_by_document:
        print("No PDFs found in this Matter.")
        return

    df = pd.DataFrame.from_dict(raw_scores_by_document, orient="index")
    df.to_csv(os.path.join(run_output_dir, "raw_scores.csv"))

    z_scores_dict = {}
    if len(df) > 1:
        scaler = StandardScaler()
        z = scaler.fit_transform(df)
        z_df = pd.DataFrame(z, index=df.index, columns=df.columns)
        z_df.to_csv(os.path.join(run_output_dir, "z_scores.csv"))
        z_scores_dict = z_df.to_dict(orient="index")

    side_summary_dict = {}
    for side in ["Side_A", "Side_B"]:
        if side_data[side]:
            side_df = pd.DataFrame(side_data[side])
            side_summary_dict[side] = side_df.mean().to_dict()

    results_json = {
        "instrument": INSTRUMENT_NAME,
        "descriptor": INSTRUMENT_DESCRIPTOR,
        "run_id": timestamp,
        "matter": os.path.basename(matter_path),
        "scoring_rules_version": SCORING_RULES_VERSION,
        "raw_scores_by_document": raw_scores_by_document,
        "z_scores_by_document": z_scores_dict,
        "side_summary": side_summary_dict
    }

    with open(os.path.join(run_output_dir, "results.json"), "w") as jf:
        json.dump(results_json, jf, indent=4)

    print("\n------------------------------------------")
    print("LRM RUN COMPLETE")
    print(f"Run ID: {timestamp}")
    print(f"Scoring Rules Version: {SCORING_RULES_VERSION}")
    print("Output saved to:")
    print(run_output_dir)
    print("------------------------------------------")

def main():
    os.makedirs(MATTERS_DIR, exist_ok=True)

    print(f"\n{INSTRUMENT_NAME}")
    print(INSTRUMENT_DESCRIPTOR)
    print(f"Scoring Rules Version: {SCORING_RULES_VERSION}\n")

    matter_path = select_or_create_matter()

    root = tk.Tk()
    root.withdraw()

    files = filedialog.askopenfilenames(
        title="Select PDFs",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not files:
        print("No files selected.")
        return

    side_choice = input("Assign to Side_A or Side_B? (A/B): ").upper()

    if side_choice == "A":
        copy_to_side(files, matter_path, "Side_A")
    elif side_choice == "B":
        copy_to_side(files, matter_path, "Side_B")
    else:
        print("Invalid choice.")
        return

    analyze_matter(matter_path)

if __name__ == "__main__":
    main()