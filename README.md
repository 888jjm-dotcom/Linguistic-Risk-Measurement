## Start Here: Conceptual Proof Pack

1. Conceptual Foundation: ARTIFICE.pdf: Foundational Theorum and Definition of "Terminological Bad Faith" [/docs/Artifice.pdf]
2. Linguistic Risk Framework and Audit Protocol (how to measure Linguistic Risk) [/docs/Linguistic Risk Modeling Framweork.pdf]
3. Tools and Instruments: Risk Vector Analyser (the Manual for this code) + Governance Instrument (how to deploy this in practice) [/docs/LRM PDF Risk Vector Analyser.pdf] and [ /docs/LRM Governance Instrument.pdf]

All supporting papers and instruments are included in the docs folder so you can review the full methodology and verify that this is a worked‑through framework, not just a concept.

## License

- LRM (Linguistic Risk Measurement) © 2026 - John James Marshall CA(SA)
- Licensed under the Apache License 2.0 – see LICENSE and NOTICE for details. 

# Linguistic Risk Measurement (LRM)

A tool for modeling linguistic risks in legal and financial governance.

---

## Overview

This repository contains the operational framework for the Linguistic Risk Model (LRM). The system converts qualitative linguistic manipulation patterns into **quantifiable, auditable risk vectors**.

It does **not** determine truth or legal correctness. Instead, it detects **structural linguistic risk signals** commonly found in:

- Legal correspondence  
- Institutional communications  
- Adversarial exchanges  

---

## Core Risk Dimensions

The analyser evaluates documents across four distinct LRM risk categories.

### 1. Embedded Default / Verdicting (`embedded_default`)

Measures how strongly a sentence **pre‑loads a conclusion as fact**.

Examples of triggers:

- Categorical framing with “is / are” combined with absolutists: “clearly”, “never”, “obviously”.  
- Discounting terms: “mere”, “merely”, “just”, “only”, “so‑called”.  
- Verdict labels: “baseless”, “frivolous”, “without merit”, “vexatious”.

### 2. Burden Shift / Authority Substitution (`burden_shift`)

Identifies language that **relocates responsibility or demands compliance** without reciprocal justification.

Examples:

- Obligation phrases: “must”, “required to”, “failure to… will result in…”.  
- Authority framing: “it is your responsibility”, “we will assume you agree”.  
- Procedural verdicts: “abuse of process”, “completely defective”, “wrong forum”.

### 3. Deflection / Premature Closure (`deflection`)

Detects attempts to **terminate engagement or shut down dialogue** without addressing substance.

Examples:

- Closure statements: “this is final”, “no further discussion”, “we will take no further steps”.  
- Labelling instead of engaging: “baseless complaint”, “plainly vexatious”, “vague to the point of being meaningless”.  

### 4. Interest Concealment (`interest_concealment`)

Flags language that **obscures self‑interest or liability**, often behind neutral / benevolent phrasing.

Examples:

- Liability disclaimers and policy shields: “we cannot accept liability”, “no liability of whatsoever nature”, “in line with our policies”.  
- Empathy plus defence: warm, caring language combined with threats, costs, or mandates.

---

## Technical Methodology

### Unit of Analysis

The system operates at the **sentence level**, to capture incremental risk signals without exaggeration.

### Processing Pipeline

1. **PDF → Text**  
   Extract raw text from PDF using `pdfplumber`.

2. **Segmentation**  
   Split the text into individual sentences using a lightweight, offline splitter.

3. **Feature Scoring**  
   For each sentence, compute four scores:
   - `embedded_default`
   - `burden_shift`
   - `deflection`
   - `interest_concealment`

4. **Aggregation**  
   Average sentence scores per document to obtain a **Document Risk Vector**.

5. **Normalisation (optional)**  
   Across a corpus of documents, compute **Z‑scores** to reveal outliers and structurally extreme texts.

---

## Usage

### Requirements

Install once (in your system Python or a virtual environment):

```bash
python -m pip install pdfplumber pandas scikit-learn
