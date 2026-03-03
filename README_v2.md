# Linguistic Risk Measurement (LRM) — Version 2

## Start Here: Conceptual Proof Pack

**Conceptual Foundation:**  
ARTIFICE.pdf — Foundational Theorem and Definition of "Terminological Bad Faith"  
`/docs/Artifice.pdf`

**Linguistic Risk Framework and Audit Protocol** (How to Measure Linguistic Risk)  
`/docs/Linguistic Risk Modeling Framework.pdf`

**Tools and Instruments:**  
Risk Vector Analyser (Manual for this Code)  
Governance Instrument (Deployment Framework)

`/docs/LRM PDF Risk Vector Analyser.pdf`  
`/docs/LRM Governance Instrument.pdf`

All supporting papers and instruments are included in the `docs` folder so the full methodology can be reviewed and verified. This is a worked-through analytical framework — not a conceptual sketch.

---

## License

LRM (Linguistic Risk Measurement) © 2026 — John James Marshall CA(SA)  
Licensed under the Apache License 2.0 — see `LICENSE` and `NOTICE` for details.

---

# Overview

LRM is an operational framework for modeling linguistic risk in legal and financial governance environments.

It converts qualitative patterns of linguistic manipulation into quantifiable, auditable risk vectors.

The system:

- Does **not** determine truth  
- Does **not** determine legal correctness  
- Does **not** infer intent  

Instead, it detects structural linguistic risk signals commonly found in:

- Legal correspondence  
- Institutional communications  
- Adversarial exchanges  

The output is a structured, comparative risk profile.

---

# Version 2 — What Has Changed

Version 2 introduces significant architectural and analytical improvements:

## 1. Externalised Scoring Rules

All linguistic scoring dictionaries are now stored in:

## Scoring_rules.json (scoring_rules.json must be in the same folder as LRMv2.py)

This allows:

- Transparent rule auditing
- Versioned scoring models
- Controlled methodological evolution
- Reproducible analysis runs

Each analysis run records into an output as:

"Scoring_rules_version": "X.X" inside its JSON output folder.

---

## 2. Discourse-Level Expansion

Beyond lexical triggers, Version 2 incorporates discourse-informed signals, including:

- Hedges (mitigating language)
- Boosters (intensifying language)
- Presupposition triggers
- Expanded modal verb analysis
- Refined authority and burden markers

This strengthens sensitivity to procedural dominance and embedded framing.

---

## 3. Timestamped Auditable Output

Each run now produces:

- Timestamped output directory
- Structured `results.json`
- Optional CSV exports
- Reproducible run metadata

Output includes:

- Instrument version
- Scoring rules version
- Matter name
- Raw scores by document
- Z-scores (if applicable)
- Side summary statistics

This creates an audit trail suitable for governance environments.

---

## 4. Headless Engine Mode (App-Ready Architecture)

LRM is now available as a headless command-line engine:

### LRM_engine.py

It accepts structured arguments:
-matter
-side
-files
-output

This architecture:

- Separates analysis from UI
- Enables macOS app bundling
- Allows deterministic backend execution
- Supports future native app integration

A packaged engine release will be made available in due course.

---

# Core Risk Dimensions

The analyser evaluates documents across four distinct LRM categories.

---

## 1. Embedded Default / Verdicting (`embedded_default`)

Measures how strongly a sentence pre-loads a conclusion as established fact.

### Examples of Triggers:
- Absolutists: "clearly", "obviously", "plainly"
- Verdict labels: "baseless", "frivolous", "vexatious"
- Discount framing: "mere", "only", "so-called"

### Interpretation:
- 0.0 → Neutral description
- 0.5–1.0 → Mild verdicting pressure
- >1.0 → Repeated or layered embedded defaults

---

## 2. Burden Shift / Authority Substitution (`burden_shift`)

Identifies language that relocates responsibility or substitutes authority for argument.

### Examples:
- "must"
- "required to"
- "it is your responsibility"
- "failure to comply"
- "abuse of process"

### Interpretation:
- 0.0 → No burden manipulation
- 1.0–2.0 → Procedural pressure
- >2.0 → Coercive or authoritarian structure

---

## 3. Deflection / Premature Closure (`deflection`)

Detects attempts to terminate engagement without addressing substance.

### Examples:
- "this is final"
- "no further discussion"
- "matter is closed"
- "will not be entertained"

### Interpretation:
- 0.0 → Open engagement
- 1.0 → Soft closure
- ≥2.0 → Hard refusal / stonewalling

---

## 4. Interest Concealment (`interest_concealment`)

Flags language that obscures liability, commercial interest, or exposure.

### Examples:
- "no liability"
- "in line with policy"
- "for your protection"
- liability disclaimers
- passive voice constructions

### Interpretation:
- 0.0 → Transparent interest
- 1.0 → Standard disclaimers
- ≥2.0 → Active concealment

---

# Technical Methodology

## Unit of Analysis

Primary unit: **Sentence**

Why:
- Manipulative framing operates locally
- Risk accumulates incrementally
- Sentence-level aggregation preserves signal without exaggeration

---

## Processing Pipeline

PDF → Text Extraction
Text → Sentence Segmentation
Sentence → Feature Scoring
Sentence Scores → Document Risk Vector
Multiple Documents → Z-Score Normalisation

All steps are deterministic and auditable.

---

## Document-Level Risk Vector

Each document score is computed as:

### Mean(feature score per sentence)

This avoids:
- Length bias
- Emotional inflation
- Over-penalising verbose texts

### z = (value - corpus mean) / standard deviation

This enables:
- Comparative analysis
- Outlier detection
- Structural extremity assessment

Interpretation:

- 0.0 → Average
- +1.0 → 1 SD above norm
- +2.0 → Structurally extreme

---

## Corpus Normalisation (Z-Scores)

When multiple documents are analysed together:


---

# What the Instrument Does NOT Claim

LRM:

- Does not assess legal correctness
- Does not infer intent
- Does not determine misconduct
- Does not replace professional judgment

It flags structural linguistic risk — nothing more.

---

# Intended Use Contexts

- Legal correspondence review
- Institutional power imbalance assessment
- Governance risk auditing
- Forensic linguistic support
- Comparative dispute analysis
- Research into adversarial framing

It is analytical scaffolding, not standalone evidence.

---

# Conceptual Summary

In simple terms:

LRM measures how much a document tells you what to think, what to do, and when to stop talking — while appearing neutral.

That is the operational definition of linguistic risk.

---

# 1. Installation

Install dependencies once:

python -m pip install pdfplumber pandas scikit-learn

# Requirements for LRM v2

## Overview

LRM v2 is the interactive (GUI-driven) version of the Linguistic Risk Measurement instrument.

It allows users to:

- Create and manage “Matters”
- Upload PDFs
- Assign documents to Side_A or Side_B
- Analyse linguistic risk patterns
- Generate timestamped, auditable output

This version is intended for structured analytical review and research use.

# Run the tool: python LRM_v3.7.py

## 2. Core Concept: Matters

A Matter represents one correspondence context.

Examples:
A dispute
A regulatory exchange
A complaint cycle
A litigation correspondence chain

Each Matter is self-contained. All scoring and Z-score comparisons occur within that Matter only.

## 3. Matter Structure

When a new Matter is created, the system automatically creates:
Matters/
    Matter_Name/
        Side_A/
        Side_B/
        analysis_output/

Side_A contains documents from one party.
Side_B contains documents from the opposing party.

## 4. Running an Analysis

When you launch: python LRM_v3.7.py

analysis_output stores timestamped results.

You will see:
Existing Matters:
1. ExampleMatter
0. Create New Matter
Select Matter:

Enter "0" to crate new Matter, then provide a New Matter Name.

## 5. Uploading Documents

After selecting a Matter a file dialog opens.
Select one or more PDFs when you are prompted:

You will be asked to assign to Side_A or Side_B? (A/B). Ensure that the files selected were related to one side in the matter.

### The PDFs are copied into the appropriate folder.

## 6. Scoring Rules

Scoring is controlled by: scoring_rules.json
This file defines:

- verdict_markers
- burden_markers
- deflection_markers
- interest_markers
- hedge_markers
- booster_markers
- presupposition_markers

Each rule has a numeric weight. The output file also contains: "scoring_rules_version": "X.X" as a record.
This version is recorded in every output JSON file for audit traceability. 
You may edit scoring rules, but version control discipline is strongly recommended.

## 7. Risk Dimensions

Each document is scored across four dimensions:
1. Embedded Default (embedded_default) - Pre-loaded conclusions presented as fact.
2. Burden Shift (burden_shift) - Procedural dominance or imposed obligation language.
3. Deflection (deflection) - Attempts to prematurely close or terminate engagement.
4. Interest Concealment (interest_concealment) - Language obscuring liability or commercial exposure.

## 8. Output Structure

Each run generates a timestamped output folder:

Matters/
    Matter_Name/
        analysis_output/
            YYYY-MM-DD_HH-MM-SS/
                raw_scores.csv
                z_scores.csv (if multiple docs)
                results.json

### results.json Contains:
  Instrument name
  Descriptor
  Run ID
  Matter name
  Scoring rules version
  Raw scores by document
  Z-scores (if applicable)
  Side summary averages

### Example snippet:
{
  "matter": "Marshall_Dispute",
  "scoring_rules_version": "2.0",
  "raw_scores_by_document": {
    "Side_A | Letter1.pdf": {
      "embedded_default": 0.36,
      "burden_shift": 0.88,
      "deflection": 0.00,
      "interest_concealment": 0.13
    }
  }
}

## 9. Z-Scores (Comparative Mode)
If multiple documents exist within a Matter, then the system calculates: 
z = (value - corpus mean) / standard deviation

This identifies structurally extreme documents within that Matter.

### Z-scores are not cross-Matter comparable.

## 10. What LRM Does NOT Do

LRM:
Does not determine legal correctness
Does not assess truth
Does not infer intent
Does not label misconduct
Does not replace professional judgment
It flags structural linguistic risk patterns only.

## 11. Recommended Workflow

Create Matter
Upload Side_A documents
Upload Side_B documents
Run analysis
Parallel Review both Raw scores and Z-scores
Side summaries - Document findings in professional judgement

## 12. Best Practice Guidance

Keep Matters discrete. 
Avoid mixing unrelated correspondence.
Do not alter scoring rules mid-Matter.
Record scoring_rules_version when reporting results.
Treat outputs as analytical scaffolding, not conclusions.

## 13. Summary

LRM v2 allows structured, auditable linguistic risk assessment within defined correspondence contexts.

It measures how strongly documents:

Pre-load conclusions
Shift burden
Foreclose engagement
Conceal interest

All scoring is deterministic, versioned, and transparent.

---

# Requirements for engine

## Install once:

"python -m pip install pdfplumber pandas scikit-learn"

## Run via:
"python LRM_engine.py --matter "Example" --side "Side_A" --output ./output --files document.pdf"

---

# Forward Roadmap

- macOS App Store deployment (in progress)
- Packaged engine distribution
- Native application integration
- Continued methodological refinement via versioned scoring rules

---


