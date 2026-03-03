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

# Requirements

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

**LRM v2 formalises the transition from research prototype to structured analytical instrument.**
