# Linguistic Risk Measurement (LRM)
A tool for modeling linguistic risks in legal and financial governance.

LRM PDF Risk Vector Analyser
Conceptual & Technical Measurement Framework

# Overview
This repository contains the operational framework for the Language Risk Model (LRM). This system converts qualitative linguistic manipulation patterns into quantifiable, auditable risk vectors.

Rather than determining truth or legal correctness, this tool is designed to detect structural linguistic risk signals commonly associated with legal correspondence, institutional communications, and adversarial exchanges.

# Core Risk Dimensions

The analyser evaluates documents across four distinct LRM risk categories:

# Embedded Default / Verdicting (embedded_default): 

Measures the extent to which a sentence pre-loads a conclusion as established fact (e.g., "clearly," "is," or "so-called").

Burden Shift / Authority Substitution (burden_shift): Identifies language that relocates responsibility or demands compliance without reciprocal justification (e.g., "must," "required to," or "until you").

Deflection / Premature Closure (deflection): Detects attempts to terminate engagement or shut down dialogue without addressing substance.

Interest Concealment (interest_concealment): Flags language that obscures self-interest or liability, often using faux-neutral phrasing.

# Technical Methodology

Unit of Analysis: 
The system processes documents at the sentence level, capturing incremental risk signals to preserve the "signal" without exaggeration.

# Processing Pipeline:

PDF to Text: Extraction of raw content.

Segmentation: Decomposition into independent sentences.

Feature Scoring: Evaluating each sentence against the four dimensions.

Aggregation: Compiling sentence scores into a Document Risk Vector.

Normalisation: Using Z-scores across a corpus to reveal outliers and structural extremes.

# Usage & Interpretation
The output is a comparative risk profile.

0.0: Average for the corpus.

+1.0: One standard deviation above the norm.

+2.0: Indicates a structurally extreme document.

# Intended Use & Limitations
This instrument is designed for:
1. Legal correspondence analysis.
2. Institutional power imbalance reviews.
3. Forensic linguistic support and comparative auditing.

# Important: 
This tool flags structural linguistic risk; it does not assess legal correctness, infer human intent, or replace professional human judgment.

# Conceptual Summary
In simple terms: The system measures how much a document tells the reader what to think, what to do, and when to stop talking—while pretending not to.
