# 🧠 ResumeIQ — AI Resume Matcher

## 📌 Problem Statement

Job seekers often apply blindly without knowing how well their resume matches a job description.

ResumeIQ solves this by analyzing resumes against job descriptions and giving:

* Match Score (0–100%)
* Strengths
* Gaps
* Keyword analysis
* Rewrite suggestions
* Competitor comparison (unique feature 🚀)

---

## ⚙️ Approach

1. Extract text from resume using **pdfplumber**
2. Use **Groq LLM (LLaMA 3.3 70B)** for:

   * Resume vs JD analysis
   * Score generation
   * Keyword gap detection
   * Rewrite suggestions
3. Parse structured LLM output into UI-friendly format
4. Display results using **Streamlit UI**
5. Generate **simulated competitors** for ranking comparison

---

## 🏗️ Architecture

User Input → Streamlit UI
→ Resume Parsing (pdfplumber)
→ LLM Processing (Groq API)
→ Response Parsing
→ UI Rendering (Scores + Insights + Comparison)

---

## 🚀 Features

✅ Resume vs JD Match Score
✅ Strength & Gap Analysis
✅ Keyword Presence & Missing Skills
✅ AI Rewrite Suggestions
✅ Competitor Ranking System 🏆
✅ Bulk Resume Ranking (Bonus Feature)

---

## 🛠️ Tech Stack

* Frontend: Streamlit
* Backend: Python
* AI Model: Groq (LLaMA 3.3 70B)
* Resume Parsing: pdfplumber
* Env Management: python-dotenv

---

## 🧪 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/ResumeIQ.git
cd ResumeIQ
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API key

Create `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

### 5. Run app

```bash
streamlit run app.py
```

---

## 📸 Screenshots
refer to the screenshots of the working of the app by clicking on the link below
https://drive.google.com/drive/folders/1jB8OYHTc0qsHonB24U1xts-XVWA0nwXx?usp=sharing

---

## 🎥 Video Walkthrough
refer to the video link below for detailed walkthrough .
https://drive.google.com/drive/folders/113QnXoFO_dM-UkCrqd016d-1Scp1OFI3?usp=sharing

---

## 🧠 Reflection

### Why this tech stack?

Streamlit was chosen for rapid prototyping and clean UI. Groq LLM was used for fast and powerful inference. pdfplumber ensures reliable text extraction from resumes.

### Biggest challenge

One of the biggest challenges I faced was working without any real dataset. Since I did not have actual candidate data, I designed the system to generate competitor profiles using AI itself. This helped simulate a realistic comparison and ranking system.

Another challenge was handling PDF parsing, especially for resumes where text extraction is not clean or the PDF is scanned. I handled basic cases, but improving this further would require better OCR support.

I also had to ensure that the AI responses were structured properly so that they could be parsed and displayed in the UI. Designing the prompt format and parsing logic was an important part of the implementation.


### What I would improve

-Support for scanned PDFs using better text extraction methods
-Enhance the login and history feature to store and track previous analyses
-Improve matching accuracy by using embeddings and similarity scoring instead of only prompt-based evaluation

---

## 📊 Evaluation Criteria Mapping

* ✅ Execution: Fully working app (single + bulk mode)
* ✅ AI Depth: Uses structured prompting + competitor simulation
* ✅ Problem Thinking: Handles empty inputs, bad PDFs
* ✅ Communication: Clear UI + insights
* ✅ Code Quality: Modular functions and parsing logic

---
