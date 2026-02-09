"""
LRM EARLY PROTOTYPE – PDF → RISK VECTORS

Requirements (in your venv):

python -m pip install pdfplumber pandas scikit-learn

Features:

- Command-line mode: analyse one or more PDFs without any GUI
- (Optional) GUI pickers left available but not used by default
- Computes per-document risk vector
- Computes corpus z-scored matrix

"""

import pdfplumber
import re
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Optional GUI imports (not used in CLI mode)
import tkinter as tk
from tkinter import filedialog

from datetime import datetime  # NEW

# ---------- LOGGING (LOCAL TEXT FILE) ----------

LOG_FILE = "lrm_log.txt"


def log_document_vector(pdf_path: str, vec: pd.Series):
    """
    Append document risk vector to a local text log file.
    Format:
      timestamp | filename | embedded_default=... | burden_shift=... | deflection=... | interest_concealment=...
    """
    timestamp = datetime.now().isoformat(timespec="seconds")
    line = (
        f"{timestamp} | {pdf_path} | "
        f"embedded_default={vec.get('embedded_default', 0):.6f}, "
        f"burden_shift={vec.get('burden_shift', 0):.6f}, "
        f"deflection={vec.get('deflection', 0):.6f}, "
        f"interest_concealment={vec.get('interest_concealment', 0):.6f}\n"
    )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)


# ---------- GUI FILE PICKERS (OPTIONAL) ----------

def select_single_pdf():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Select a PDF or text file",
        filetypes=[("Documents", "*.pdf *.txt"), ("PDF Files", "*.pdf"), ("Text Files", "*.txt")]
    )


def select_multiple_pdfs():
    root = tk.Tk()
    root.withdraw()
    return list(
        filedialog.askopenfilenames(
            title="Select one or more PDFs or text files",
            filetypes=[("Documents", "*.pdf *.txt"), ("PDF Files", "*.pdf"), ("Text Files", "*.txt")]
        )
    )


# ---------- 1. PDF → TEXT ----------

def extract_text_from_pdf(pdf_path: str) -> str:
    text_chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_chunks.append(page.extract_text() or "")
    return "\n".join(text_chunks)


# ---------- 2. TEXT → SENTENCES (OFFLINE, NO NLTK) ----------

_SENT_SPLIT_REGEX = re.compile(r"(?<=[.!?])\s+")


def split_into_sentences(text: str):
    """
    Naive, offline sentence splitter.

    This replaces the NLTK punkt dependency to avoid SSL/download issues,
    while preserving the sentence-level unit required by the LRM manual.
    """
    raw = _SENT_SPLIT_REGEX.split(text)
    return [re.sub(r"\s+", " ", s).strip() for s in raw if s.strip()]


# ---------- 3. FEATURE ENGINEERING ----------

# 4.1 Embedded Default / Verdicting

DISCOUNT_MARKERS = [
    "mere", "merely", "just", "only", "not really", "not truly",
    "not genuinely", "so-called", "as if", "pseudo", "quasi",
    "simulates", "mimics", "pretends", "appears to", "seems to",
]

# Evaluative / verdicting nouns and adjectives

VERDICT_MARKERS = [
    "meritless", "without merit", "baseless", "groundless", "frivolous",
    "vexatious", "unfounded", "unwarranted", "unreasonable",
    "unjustified", "misconceived", "inaccurate", "incorrect",
    "false allegation", "false allegations", "misrepresentation",
]

# NEW: high-severity verdicting phrases (Maritz-style)

HIGH_VERDICT_TERMS = [
    "baseless complaint",
    "spectacularly false",
    "utterly devoid of merit",
    "simply unconscionable",
    "plainly vexatious",
    "abuse of process",
    "completely defective",
    "patently defective",
    "abortive process",
    "on every conceivable basis",
]

# 4.2 Burden Shift / Authority Substitution

AUTHORITY_MARKERS = [
    "clearly", "obviously", "self-evident", "beyond doubt", "without question",
    "prudent and correct", "as we have said countless times",
]

# Broader obligation / responsibility phrases

OBLIGATION_MARKERS = [
    "obliged to", "obligated to", "expected to",
    "you are obliged to", "you are obligated to", "you are expected to",
    "it is your responsibility", "you are responsible for",
    "you will be held liable", "you will be liable for",
    "we will assume you agree", "we will proceed on the basis that you",
    "you are required", "you have failed to",
    "failure to", "if you do not", "unless you",
]

# NEW: implicit procedural burden-shift terms

BURDEN_TERMS = [
    "wrong forum",
    "abuse of process",
    "completely defective",
    "patently defective",
    "abortive process",
    "on every conceivable basis",
    "obvious next step",
]

# 4.3 Deflection / Premature Closure

CLOSURE_MARKERS = [
    "untenable", "cannot proceed", "no further discussion", "we will take no further steps",
    "this is final", "full and final",
]

# Softer closure / refusal to engage further

SOFT_CLOSURE_MARKERS = [
    "we consider this matter closed",
    "we regard this matter as closed",
    "we consider the matter closed",
    "we will not enter into further correspondence",
    "we do not propose to correspond further",
    "we will not engage further on this",
    "we see no value in further correspondence",
    "our position remains unchanged",
]

# NEW: dismissive complaint-labelling as de facto closure

DEFLECTION_TERMS = [
    "baseless complaint",
    "vague to the point of being meaningless",
    "spectacularly false",
    "utterly devoid of merit",
    "simply unconscionable",
    "plainly vexatious",
]

# 4.4 Interest Concealment

INTEREST_MARKERS = [
    "we cannot accept liability", "we are not responsible", "no liability of whatsoever nature",
    "all charges are reasonable", "in accordance with our mandate", "best efforts",
]

# Policy/neutrality framing around interest / exposure

INTEREST_NEUTRALITY_MARKERS = [
    "in line with our policies",
    "consistent with our policies",
    "in accordance with our policies",
    "standard practice",
    "industry standard",
    "in line with industry practice",
    "we are unable to comment",
    "we are not in a position to comment",
    "cannot comment further",
]

# NEW: empathy/benefaction + defensive content (motivational opacity)

EMPATHY_TERMS = [
    "to the benefit of mr marshall",
    "assist mr marshall",
    "best interests of the children",
]

DEFENSIVE_TERMS = [
    "reserve the right to pursue a claim",
    "unnecessary costs",
    "mala fide",
    "vindictive claims",
]


def count_markers(sentence: str, markers) -> int:
    s_lower = sentence.lower()
    return sum(1 for m in markers if m in s_lower)


def sentence_features(sentence: str) -> dict:
    s = sentence.lower()

    # 4.1 Embedded Default / Verdicting
    embedded_default = 0.0

    # categorical + absolutist
    if " is " in f" {s} " or " are " in f" {s} ":
        if any(w in s for w in ["always", "never", "impossible", "obvious", "clearly"]):
            embedded_default += 1.0

    embedded_default += count_markers(s, DISCOUNT_MARKERS)
    embedded_default += count_markers(s, VERDICT_MARKERS)

    # high-severity verdicting (stronger weight)
    for term in HIGH_VERDICT_TERMS:
        if term in s:
            embedded_default += 1.0  # was 0.5

    if embedded_default > 3.0:
        embedded_default = 3.0

    # 4.2 Burden Shift / Authority Substitution
    burden_shift = 0.0

    if "must" in s or "required to" in s or "until you" in s:
        burden_shift += 1.0
    if "unable to take your matter any further" in s:
        burden_shift += 2.0

    burden_shift += count_markers(s, OBLIGATION_MARKERS)
    burden_shift += count_markers(s, AUTHORITY_MARKERS)

    # implicit procedural burden-shift (stronger)
    for term in BURDEN_TERMS:
        if term in s:
            burden_shift += 1.0  # was 0.5

    if burden_shift > 3.0:
        burden_shift = 3.0

    # 4.3 Deflection / Premature Closure
    deflection = 0.0
    deflection += count_markers(s, CLOSURE_MARKERS)

    if "ignored the pertinent issues" in s or "refused to accept our considered legal advice" in s:
        deflection += 2.0

    deflection += count_markers(s, SOFT_CLOSURE_MARKERS)

    # dismissive complaint-labelling as de facto closure (stronger)
    for term in DEFLECTION_TERMS:
        if term in s:
            deflection += 1.0  # was 0.5

    if deflection > 3.0:
        deflection = 3.0

    # 4.4 Interest Concealment
    interest_concealment = 0.0
    interest_concealment += count_markers(s, INTEREST_MARKERS)
    interest_concealment += count_markers(s, INTEREST_NEUTRALITY_MARKERS)

    if "we wish you everything of the very best" in s and "invoice" in s:
        interest_concealment += 1.0

    # empathy + defensive threat → strong motivational opacity
    has_empathy = any(e in s for e in EMPATHY_TERMS)
    has_defensive = any(d in s for d in DEFENSIVE_TERMS)

    if has_empathy and has_defensive:
        interest_concealment += 1.0
    elif has_defensive:
        interest_concealment += 1.0  # was 0.5

    if interest_concealment > 3.0:
        interest_concealment = 3.0

    return {
        "embedded_default": embedded_default,
        "burden_shift": burden_shift,
        "deflection": deflection,
        "interest_concealment": interest_concealment,
    }


# ---------- 4. DOCUMENT RISK VECTOR ----------

def document_risk_vector(pdf_path: str) -> pd.Series:
    text = extract_text_from_pdf(pdf_path)
    sentences = split_into_sentences(text)
    rows = []
    for s in sentences:
        feats = sentence_features(s)
        feats["sentence"] = s
        rows.append(feats)

    df = pd.DataFrame(rows)

    if df.empty:
        print(f"[INFO] {pdf_path}: 0 sentences found.")
        return pd.Series(
            {
                "embedded_default": 0.0,
                "burden_shift": 0.0,
                "deflection": 0.0,
                "interest_concealment": 0.0,
            }
        )

    total_sentences = len(df)
    nonzero_rows = df[["embedded_default", "burden_shift", "deflection", "interest_concealment"]].any(axis=1).sum()
    print(f"[INFO] {pdf_path}: {total_sentences} sentences analysed, {nonzero_rows} with non-zero features.")
    proportion_nonzero = nonzero_rows / total_sentences if total_sentences else 0.0
    print(f"[INFO] {pdf_path}: proportion with non-zero features = {proportion_nonzero:.3f}")

    # mean per feature at document level
    agg = df[["embedded_default", "burden_shift", "deflection", "interest_concealment"]].mean()
    return agg


# ---------- 5. CORPUS NORMALISATION ----------

def corpus_risk_matrix(pdf_paths: list) -> pd.DataFrame:
    records = []
    for path in pdf_paths:
        vec = document_risk_vector(path)
        vec["doc"] = path
        records.append(vec)
    df = pd.DataFrame(records)
    raw = df.set_index("doc")

    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(raw)
    scaled = pd.DataFrame(scaled_values, index=raw.index, columns=raw.columns)
    return scaled


# ---------- MAIN (CLI ENTRY POINT) ----------

if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Case 1: filenames provided on the command line → pure CLI mode
    if len(sys.argv) > 1:
        pdf_paths = [str(Path(p).expanduser()) for p in sys.argv[1:]]
        if len(pdf_paths) == 1:
            pdf_file = pdf_paths[0]
            print("Analysing single document:")
            print(" ", pdf_file)
            vec = document_risk_vector(pdf_file)
            print("\nRaw risk vector:")
            print(vec)
            log_document_vector(pdf_file, vec)
        else:
            print("Analysing multiple documents:")
            for p in pdf_paths:
                print(" ", p)
                vec = document_risk_vector(p)
                print("\nRaw risk vector:")
                print(vec)
                log_document_vector(p, vec)

            # corpus z-scores for the same paths
            risk_matrix = corpus_risk_matrix(pdf_paths)
            print("\nZ-scored risk matrix:")
            print(risk_matrix)

    # Case 2: no args → fall back to GUI file picker
    else:
        print("No filenames provided on the command line.")
        print("Opening file chooser...")
        first = select_single_pdf()
        if not first:
            print("No file selected. Exiting.")
            sys.exit(0)

        # First file → single analysis
        print("Analysing single document:")
        print(" ", first)
        vec = document_risk_vector(first)
        print("\nRaw risk vector:")
        print(vec)
        log_document_vector(first, vec)

        # Optionally select more for corpus analysis
        more = select_multiple_pdfs()
        if more:
            print("\nAnalysing additional documents for corpus analysis:")
            for p in more:
                print(" ", p)
                v2 = document_risk_vector(p)
                print("\nRaw risk vector:")
                print(v2)
                log_document_vector(p, v2)

            risk_matrix = corpus_risk_matrix(more)
            print("\nZ-scored risk matrix:")
            print(risk_matrix)
