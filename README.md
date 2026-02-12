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
# Conceptual & Technical Measurement Manual

## 1. Purpose of the Instrument

The LRM PDF Risk Vector Analyser operationalises the Language Risk Model (LRM) by converting qualitative linguistic manipulation patterns into quantifiable risk vectors. Rather than determining truth or legal correctness, it detects structural signals associated with:

Its aim is not to determine truth or legal correctness, but to detect structural linguistic risk signals commonly associated with:

• Embedded verdicting
• Authority substitution
• Burden displacement
• Premature closure
• Interest concealment

These signals are especially prevalent in legal correspondence, institutional
letters, and adversarial communications.

The output is a comparative risk profile, **not a diagnosis**.

## 2. Unit of Analysis

Primary Unit: **Sentence**

Each PDF is decomposed into sentences, because:
• Manipulative language operates locally (sentence-level)
• Risk is often introduced incrementally
• Aggregation preserves signal without exaggeration
Every sentence is independently evaluated and then aggregated at document level.

## 3. Processing Pipeline (Conceptual)

1. PDF → Text
2. Text → Sentences
3. Sentence → Feature Scores
4. Sentence Scores → Document Risk Vector
5. Multiple Documents → Normalised Risk Matrix
Each step is deterministic and **auditable**.

## 4. The Four Risk Dimensions

Each dimension corresponds to a distinct LRM risk category.

### 4.1 Embedded Default / Verdicting

**Variable**: embedded_default

**What it measures:**
The extent to which a sentence pre-loads a conclusion as if it were already established fact.

**Linguistic indicators**
• Categorical verbs: is, are
• Absolutist qualifiers: always, never, obvious, clearly
• Discounting language: mere, just, only, so-called

**Theoretical basis**
This maps to pre-emptive framing, where disagreement is structurally discouraged by
embedding the verdict inside the description.

**Measurement logic**
• +1 if categorical structure + absolutist language appears
• +1 for each discount marker detected

**Interpretation**
• 0.0 → Neutral description
• 0.5–1.0 → Mild verdicting pressure
• >1.0 → Repeated or layered embedded defaults

### 4.2 Burden Shift / Authority Substitution

**Variable:** burden_shift

**What it measures:**
Language that relocates responsibility or substitutes argument with asserted authority.

**Linguistic indicators**
• Modal impositions: must, required to
• Conditional gating: until you
• Authority claims: clearly, beyond doubt, self-evident

**Theoretical Basis:**
LRM identifies this as procedural dominance, where compliance is demanded without reciprocal justification.

**Measurement Logic**
• +1 for obligation language
• +2 for explicit termination dependency
• +1 per authority marker

**Interpretation**
• 0.0 → No burden manipulation
• 1.0–2.0 → Procedural pressure
• >2.0 → Coercive or authoritarian structure

### 4.3 Deflection / Premature Closure

**Variable**: Deflection

**What it Measures:**
Attempts to **terminate engagement** without addressing **substance**.

**Linguistic Indicators:**
• Closure phrases: this is final, no further discussion
• Dismissive reframing: ignored the pertinent issues

**Theoretical Basis:**
This reflects **interation foreclosure** - a classic control mechanism in adversarial texts.

**Measurement logic:**
• +1 per closure marker
• +2 for explicit dismissal of engagement

**Interpretation**
• 0.0 → Open engagement
• 1.0 → Soft closure
• ≥2.0 → Hard refusal / stonewalling

### 4.4 Interest Concealment

**Variable:** interest_concealment

**What it Measures:**
Language that normalises or obscures self-interest, liability, or commercial exposure.

**Linguistic indicators:**
• Liability disclaimers
• Fee justifications
• Faux-neutral phrasing around commercial outcomes

**Special Heuristic:**
Empathy language co-occurring with commercial content (e.g., “we wish you well” + “invoice”) increases risk.

**Theoretical Basis:**
LRM treats this as motivational opacity — presenting interest-laden positions as neutral or inevitable.

**Interpretation:**
• 0.0 → Transparent interest
• 1.0 → Standard disclaimers
• ≥2.0 → Active concealment

## 5. Document-Level Risk Vector

For **each document**, the system computes:
*mean(feature score per sentence)*

This avoids: 
• Length bias; 
• Emotional Inflation and 
• Over-penalising verbose documents

### Example Output:

"embedded_default      0.83"
"burden_shift          1.25"
"deflection            0.42"
"interest_concealment  0.67"

*This Means:*
• Verdicting pressure present
• Strong procedural control
• Some engagement allowed
• Moderate interest masking

## 6. Corpus Normalisation (Z-Scores)

When multiple PDFs are analysed together, raw scores are converted into **z-scores**:
*(value - corpus mean) / standard deviation*

**Why this Matters**:
• Reveals outliers
• Enables comparative analysis
• Prevents absolute-score fallacy

**Interpretation:**
• 0.0 → Average for corpus
• +1.0 → 1 standard deviation above norm
• +2.0 → Structurally extreme document

This is particularly powerful in **legal correspondence chains**.

## 7. What the Instrument/Tool Does Not Claim

### Explicit non-claims (important):

• It Does not assess legal correctness
• It Does not infer intent
• It Does not label abuse or misconduct
• It Does not replace human judgment

It **flags structural linguistic risk**, *nothing more — nothing less*.

## 8. Intended Use Contexts

This instrument is suitable for:

• Legal correspondence analysis
• Institutional power imbalance review
• Comparative document auditing
• Forensic linguistic support material
• Research into manipulative framing

It is not intended as evidence on its own, **but as analytical scaffolding**.

## 9. Conceptual Summary

**In simple terms:**

The system measures *how much a document tells you* what to think, what to do,
and when to stop talking — while pretending not to.

That’s the LRM in **operational form.**

---


### Requirements

Install once (in your system Python or a virtual environment):
```bash
python -m pip install pdfplumber pandas scikit-learn
```bash

