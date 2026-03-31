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
(Add your Loom/YouTube link here)

---

## 🧠 Reflection

### Why this tech stack?

Streamlit was chosen for rapid prototyping and clean UI. Groq LLM was used for fast and powerful inference. pdfplumber ensures reliable text extraction from resumes.

### Biggest challenge

Parsing structured output from LLM reliably was challenging. This was solved by enforcing strict response formats and building custom parsers.

### What I would improve

* Add embeddings + similarity scoring instead of only LLM
* Improve PDF parsing for scanned resumes
* Add user authentication & history tracking

---

## 📊 Evaluation Criteria Mapping

* ✅ Execution: Fully working app (single + bulk mode)
* ✅ AI Depth: Uses structured prompting + competitor simulation
* ✅ Problem Thinking: Handles empty inputs, bad PDFs
* ✅ Communication: Clear UI + insights
* ✅ Code Quality: Modular functions and parsing logic

---
