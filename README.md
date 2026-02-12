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

# LRM Risk Vector Measurement - How it works:

## 1. Purpose of the Instrument

[span_0](start_span)This system operationalises elements of the Language Risk Model (LRM) by converting qualitative linguistic manipulation patterns into quantifiable risk vectors[span_0](end_span). [span_1](start_span)Its aim is not to determine truth or legal correctness, but to detect structural linguistic risk signals[span_1](end_span).

[span_2](start_span)The output is a comparative risk profile rather than a diagnosis[span_2](end_span). It is specifically designed to flag:
* **[span_3](start_span)Embedded verdicting**[span_3](end_span)
* **[span_4](start_span)Authority substitution**[span_4](end_span)
* **[span_5](start_span)Burden displacement**[span_5](end_span)
* **[span_6](start_span)Premature closure**[span_6](end_span)
* **[span_7](start_span)Interest concealment**[span_7](end_span)

---

## 2. Unit of Analysis

[span_8](start_span)The system uses the **sentence** as the primary unit of analysis[span_8](end_span). [span_9](start_span)This ensures that manipulative language is caught at a local level, risk is measured incrementally, and the final signal is not exaggerated by document length[span_9](end_span).

---

## 3. The Four Risk Dimensions
[span_10](start_span)The analyser evaluates text across four distinct LRM risk categories[span_10](end_span):

### 4.1 Embedded Default / Verdicting (`embedded_default`)
* **[span_11](start_span)Definition**: Measures how much a sentence pre-loads a conclusion as if it were established fact[span_11](end_span).
* **[span_12](start_span)Linguistic Indicators**: Categorical verbs (*is, are*), absolutist qualifiers (*always, never*), and discounting language (*mere, only*)[span_12](end_span).
* **[span_13](start_span)Interpretation**: Scores $>1.0$ indicate repeated or layered embedded defaults[span_13](end_span).

### 4.2 Burden Shift / Authority Substitution (`burden_shift`)
* **[span_14](start_span)Definition**: Language that relocates responsibility or substitutes argument with asserted authority[span_14](end_span).
* **[span_15](start_span)Linguistic Indicators**: Modal impositions (*must, required to*), conditional gating (*until you*), and authority claims (*clearly, self-evident*)[span_15](end_span).
* **[span_16](start_span)Interpretation**: Scores $>2.0$ suggest a coercive or authoritarian structure[span_16](end_span).

### 4.3 Deflection / Premature Closure (`deflection`)
* **[span_17](start_span)Definition**: Attempts to terminate engagement without addressing substance[span_17](end_span).
* **[span_18](start_span)Linguistic Indicators**: Closure phrases (*this is final*) and dismissive reframing[span_18](end_span).
* **[span_19](start_span)Interpretation**: Scores $\ge2.0$ indicate hard refusal or "stonewalling"[span_19](end_span).

### 4.4 Interest Concealment (`interest_concealment`)
* **[span_20](start_span)Definition**: Language that normalises or obscures self-interest, liability, or commercial exposure[span_20](end_span).
* **[span_21](start_span)Heuristic**: Empathy language (e.g., "we wish you well") co-occurring with commercial content (e.g., "invoice") increases this risk score[span_21](end_span).
* **[span_22](start_span)Interpretation**: Scores $\ge2.0$ suggest active concealment[span_22](end_span).

---

## 4. Scoring & Normalisation
### Document-Level Vector
[span_23](start_span)For each document, the system computes the mean feature score per sentence[span_23](end_span). [span_24](start_span)This avoids length bias and over-penalising verbose documents[span_24](end_span).

### Corpus Normalisation (Z-Scores)
When multiple PDFs are analysed together, raw scores are converted into z-scores:
[span_25](start_span)$$Z = \frac{\text{value} - \text{corpus mean}}{\text{standard deviation}}$$[span_25](end_span)

* **[span_26](start_span)0.0**: Average for the corpus[span_26](end_span).
* **[span_27](start_span)+2.0**: A structurally extreme document relative to the set[span_27](end_span).

---

## 5. Usage & Limitations

### Intended Contexts
* [span_28](start_span)Legal correspondence analysis[span_28](end_span).
* [span_29](start_span)Institutional power imbalance review[span_29](end_span).
* [span_30](start_span)Forensic linguistic support material[span_30](end_span).

### Explicit Non-Claims
[span_31](start_span)The tool **does not** assess legal correctness, infer intent, or label misconduct[span_31](end_span). [span_32](start_span)It serves as analytical scaffolding, not standalone evidence[span_32](end_span).

> **[span_33](start_span)Conceptual Summary**: The system measures how much a document tells you what to think, what to do, and when to stop talking—while pretending not to[span_33](end_span).

