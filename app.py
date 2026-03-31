import streamlit as st
import pdfplumber
from groq import Groq
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Page config
st.set_page_config(page_title="ResumeIQ", page_icon="🧠", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .stApp { max-width: 850px; margin: auto; }
    .score-box {
        text-align: center;
        padding: 20px;
        border-radius: 16px;
        margin: 20px 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .keyword-chip {
        display: inline-block;
        padding: 4px 12px;
        margin: 4px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .missing { background-color: #ff4b4b33; color: #ff4b4b; border: 1px solid #ff4b4b; }
    .present { background-color: #00c85333; color: #00c853; border: 1px solid #00c853; }
    .rank-card {
        background: #1e2130;
        border-radius: 12px;
        padding: 16px;
        margin: 10px 0;
        border-left: 4px solid #4f8bf9;
    }
    .you-card {
        background: #1e2130;
        border-radius: 12px;
        padding: 16px;
        margin: 10px 0;
        border-left: 4px solid #00c853;
    }
    .competitor-card {
        background: #1e2130;
        border-radius: 12px;
        padding: 16px;
        margin: 10px 0;
        border-left: 4px solid #f9a825;
    }
    </style>
""", unsafe_allow_html=True)

# ── Session state ───────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

# ══════════════════════════════════════════════════════
# PAGE 1 — WELCOME
# ══════════════════════════════════════════════════════
if st.session_state.page == "welcome":

    st.markdown("<h1 style='text-align:center;'>🧠 ResumeIQ</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>AI-powered resume matcher — know your chances before you apply</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 👋 Let's get started — tell us about yourself")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
    with col2:
        email = st.text_input("Email Address", placeholder="e.g. rahul@gmail.com")

    col3, col4 = st.columns(2)
    with col3:
        role = st.text_input("Job Role you're applying for", placeholder="e.g. Data Analyst")
    with col4:
        experience = st.selectbox("Years of Experience", [
            "Fresher (0 years)", "0–1 years", "1–3 years", "3–5 years", "5+ years"
        ])

    mode = st.radio(
        "What would you like to do?",
        ["📄 Analyse a single resume", "📦 Bulk upload & rank multiple resumes"],
        horizontal=True
    )

    st.markdown(" ")
    if st.button("Continue →", use_container_width=True, type="primary"):
        if not name.strip():
            st.warning("⚠️ Please enter your name.")
        elif not email.strip():
            st.warning("⚠️ Please enter your email.")
        elif not role.strip():
            st.warning("⚠️ Please enter the job role.")
        else:
            st.session_state.user_info = {
                "name": name, "email": email,
                "role": role, "experience": experience, "mode": mode
            }
            st.session_state.page = "main"
            st.rerun()

# ══════════════════════════════════════════════════════
# PAGE 2 — MAIN APP
# ══════════════════════════════════════════════════════
elif st.session_state.page == "main":

    info = st.session_state.user_info

    st.markdown("<h2 style='text-align:center;'>🧠 ResumeIQ</h2>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align:center; color:gray;'>Welcome, <b>{info['name']}</b> &nbsp;|&nbsp; "
        f"Applying for: <b>{info['role']}</b> &nbsp;|&nbsp; "
        f"Experience: <b>{info['experience']}</b></p>",
        unsafe_allow_html=True
    )

    if st.button("← Back"):
        st.session_state.page = "welcome"
        st.rerun()

    st.markdown("---")

    # ── Extract PDF text ────────────────────────────────────
    def extract_text_from_pdf(file):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()

    # ── Analyse resume against JD ───────────────────────────
    def analyze_resume(resume_text, jd_text, user_role):
        prompt = f"""
You are an expert HR assistant and resume reviewer.
The candidate is applying for: {user_role}

Analyze the resume against the job description and respond in EXACTLY this format:

MATCH_SCORE: [number 0-100]

STRENGTHS:
- [strength 1]
- [strength 2]
- [strength 3]

GAPS:
- [gap 1]
- [gap 2]
- [gap 3]

KEYWORDS_PRESENT:
- [keyword found in both resume and JD]
- [keyword found in both resume and JD]
- [keyword found in both resume and JD]

KEYWORDS_MISSING:
- [important keyword in JD but missing from resume]
- [important keyword in JD but missing from resume]
- [important keyword in JD but missing from resume]

REWRITE_SUGGESTIONS:
- ORIGINAL: [weak bullet point from resume]
  IMPROVED: [rewritten to better match JD]
- ORIGINAL: [another weak bullet point]
  IMPROVED: [rewritten version]

---
RESUME:
{resume_text}

---
JOB DESCRIPTION:
{jd_text}
"""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content

    # ── Generate competitor profiles + comparison ───────────
    def competitor_comparison(resume_text, jd_text, user_role, user_score):
        prompt = f"""
You are an expert HR analyst.

A candidate is applying for: {user_role}
Their resume match score against the JD is: {user_score}/100

Generate 3 realistic competitor candidate profiles who are also applying for this same role.
Make them varied — one weak, one similar, one stronger than the candidate.

Then compare the candidate's resume against these competitors.

Respond in EXACTLY this format:

COMPETITOR_1_NAME: [realistic name]
COMPETITOR_1_SCORE: [number 0-100]
COMPETITOR_1_SUMMARY: [2 sentences about their profile and what makes them strong or weak]

COMPETITOR_2_NAME: [realistic name]
COMPETITOR_2_SCORE: [number 0-100]
COMPETITOR_2_SUMMARY: [2 sentences about their profile]

COMPETITOR_3_NAME: [realistic name]
COMPETITOR_3_SCORE: [number 0-100]
COMPETITOR_3_SUMMARY: [2 sentences about their profile]

CANDIDATE_RANK: [1, 2, 3, or 4 — where does the candidate rank among all 4 including themselves]

WHAT_OTHERS_HAVE:
- [skill or experience the stronger competitors have that candidate lacks]
- [skill or experience the stronger competitors have that candidate lacks]
- [skill or experience the stronger competitors have that candidate lacks]

HOW_TO_BEAT_THEM:
- [specific actionable tip to outrank competitor 1 or 2]
- [specific actionable tip]
- [specific actionable tip]

---
CANDIDATE RESUME:
{resume_text}

---
JOB DESCRIPTION:
{jd_text}
"""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        return response.choices[0].message.content

    # ── Parse main analysis ─────────────────────────────────
    def parse_response(text):
        result = {
            "score": 0, "strengths": [], "gaps": [],
            "keywords_present": [], "keywords_missing": [], "rewrites": []
        }
        current_section = None
        current_rewrite = {}

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("MATCH_SCORE:"):
                try:
                    result["score"] = int(''.join(filter(str.isdigit, line.split(":")[1])))
                except:
                    result["score"] = 0
            elif line == "STRENGTHS:":
                current_section = "strengths"
            elif line == "GAPS:":
                current_section = "gaps"
            elif line == "KEYWORDS_PRESENT:":
                current_section = "keywords_present"
            elif line == "KEYWORDS_MISSING:":
                current_section = "keywords_missing"
            elif line == "REWRITE_SUGGESTIONS:":
                current_section = "rewrites"
            elif current_section == "rewrites":
                if line.startswith("- ORIGINAL:"):
                    if current_rewrite.get("original") and current_rewrite.get("improved"):
                        result["rewrites"].append(current_rewrite)
                    current_rewrite = {"original": line.replace("- ORIGINAL:", "").strip(), "improved": ""}
                elif line.startswith("IMPROVED:"):
                    current_rewrite["improved"] = line.replace("IMPROVED:", "").strip()
            elif line.startswith("- ") and current_section and current_section != "rewrites":
                result[current_section].append(line[2:])

        if current_rewrite.get("original") and current_rewrite.get("improved"):
            result["rewrites"].append(current_rewrite)

        return result

    # ── Parse competitor response ───────────────────────────
    def parse_competitors(text):
        result = {
            "competitors": [],
            "candidate_rank": 0,
            "what_others_have": [],
            "how_to_beat": []
        }
        current_section = None

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            if line.startswith("COMPETITOR_1_NAME:"):
                result["competitors"].append({"name": line.split(":", 1)[1].strip(), "score": 0, "summary": ""})
            elif line.startswith("COMPETITOR_1_SCORE:"):
                try:
                    result["competitors"][0]["score"] = int(''.join(filter(str.isdigit, line.split(":")[1])))
                except: pass
            elif line.startswith("COMPETITOR_1_SUMMARY:"):
                result["competitors"][0]["summary"] = line.split(":", 1)[1].strip()

            elif line.startswith("COMPETITOR_2_NAME:"):
                result["competitors"].append({"name": line.split(":", 1)[1].strip(), "score": 0, "summary": ""})
            elif line.startswith("COMPETITOR_2_SCORE:"):
                try:
                    result["competitors"][1]["score"] = int(''.join(filter(str.isdigit, line.split(":")[1])))
                except: pass
            elif line.startswith("COMPETITOR_2_SUMMARY:"):
                result["competitors"][1]["summary"] = line.split(":", 1)[1].strip()

            elif line.startswith("COMPETITOR_3_NAME:"):
                result["competitors"].append({"name": line.split(":", 1)[1].strip(), "score": 0, "summary": ""})
            elif line.startswith("COMPETITOR_3_SCORE:"):
                try:
                    result["competitors"][2]["score"] = int(''.join(filter(str.isdigit, line.split(":")[1])))
                except: pass
            elif line.startswith("COMPETITOR_3_SUMMARY:"):
                result["competitors"][2]["summary"] = line.split(":", 1)[1].strip()

            elif line.startswith("CANDIDATE_RANK:"):
                try:
                    result["candidate_rank"] = int(''.join(filter(str.isdigit, line.split(":")[1])))
                except: pass
            elif line == "WHAT_OTHERS_HAVE:":
                current_section = "what_others_have"
            elif line == "HOW_TO_BEAT_THEM:":
                current_section = "how_to_beat"
            elif line.startswith("- ") and current_section:
                result[current_section].append(line[2:])

        return result

    # ── Display main results ────────────────────────────────
    def display_results(parsed, name=""):
        score = parsed["score"]
        color = "#ff4b4b" if score < 40 else "#f9a825" if score < 70 else "#00c853"
        label = "Low Match" if score < 40 else "Moderate Match" if score < 70 else "Strong Match"

        st.markdown(
            f"<div class='score-box' style='background:{color}22; border:2px solid {color}; color:{color};'>"
            f"{'📄 ' + name + ' — ' if name else ''}Match Score: {score}% — {label}</div>",
            unsafe_allow_html=True
        )
        st.progress(score / 100)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ✅ Strengths")
            for s in parsed["strengths"]:
                st.success(s)
        with col2:
            st.markdown("### ❌ Gaps")
            for g in parsed["gaps"]:
                st.error(g)

        st.markdown("### 🔍 Keyword Analysis")
        keyword_html = ""
        for kw in parsed["keywords_present"]:
            keyword_html += f"<span class='keyword-chip present'>✓ {kw}</span>"
        for kw in parsed["keywords_missing"]:
            keyword_html += f"<span class='keyword-chip missing'>✗ {kw}</span>"
        st.markdown(keyword_html if keyword_html else "No keywords extracted.", unsafe_allow_html=True)

        if parsed["rewrites"]:
            st.markdown("### ✍️ Rewrite Suggestions")
            for rw in parsed["rewrites"]:
                with st.expander(f"💬 '{rw['original'][:60]}...'"):
                    st.markdown(f"**❌ Original:** {rw['original']}")
                    st.markdown(f"**✅ Improved:** {rw['improved']}")

    # ── Display competitor results ──────────────────────────
    def display_competitors(comp_data, your_name, your_score):
        st.markdown("## 🏆 How You Compare to Other Applicants")

        rank = comp_data.get("candidate_rank", 0)
        rank_emoji = ["🥇", "🥈", "🥉", "4️⃣"]
        rank_label = rank_emoji[rank - 1] if 1 <= rank <= 4 else "—"

        st.markdown(
            f"<div style='text-align:center; font-size:1.5rem; padding:15px; "
            f"background:#1e2130; border-radius:12px; margin-bottom:20px;'>"
            f"You rank <b>{rank_label} #{rank} out of 4 candidates</b> for this role</div>",
            unsafe_allow_html=True
        )

        # Build all 4 candidates including the user
        all_candidates = list(comp_data["competitors"]) + [{"name": f"You ({your_name})", "score": your_score, "summary": "This is your resume."}]
        all_candidates.sort(key=lambda x: x["score"], reverse=True)

        st.markdown("### 📊 All Candidates Ranked")
        for i, c in enumerate(all_candidates):
            is_you = "You" in c["name"]
            card_class = "you-card" if is_you else "competitor-card"
            c_color = "#00c853" if is_you else "#f9a825"
            score_c = c["score"]
            st.markdown(
                f"<div class='{card_class}'>"
                f"<b>#{i+1} — {c['name']}</b> &nbsp;&nbsp;"
                f"<span style='color:{c_color}; font-size:1.1rem; font-weight:bold;'>{score_c}%</span>"
                f"<br><small style='color:gray;'>{c['summary']}</small>"
                f"</div>",
                unsafe_allow_html=True
            )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔑 What Stronger Candidates Have")
            for item in comp_data["what_others_have"]:
                st.warning(item)
        with col2:
            st.markdown("### 🚀 How to Beat Them")
            for tip in comp_data["how_to_beat"]:
                st.info(tip)

    # ════════════════════════════════════════════════════════
    # SINGLE RESUME MODE
    # ════════════════════════════════════════════════════════
    if info["mode"] == "📄 Analyse a single resume":

        uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])
        job_description = st.text_area("📋 Paste the Job Description", height=200)

        if st.button("🔍 Analyse My Resume", use_container_width=True, type="primary"):
            if not uploaded_file:
                st.warning("⚠️ Please upload your resume PDF.")
            elif not job_description.strip():
                st.warning("⚠️ Please paste a job description.")
            else:
                resume_text = extract_text_from_pdf(uploaded_file)
                if not resume_text:
                    st.error("❌ Could not extract text. Make sure it's not a scanned image.")
                else:
                    with st.spinner("Step 1/2 — Analysing your resume... ⏳"):
                        raw = analyze_resume(resume_text, job_description, info["role"])
                        parsed = parse_response(raw)

                    with st.spinner("Step 2/2 — Comparing against other applicants... 🔍"):
                        comp_raw = competitor_comparison(resume_text, job_description, info["role"], parsed["score"])
                        comp_data = parse_competitors(comp_raw)

                    st.markdown("---")
                    st.markdown(f"## 📊 Your Results, {info['name']}")
                    display_results(parsed)

                    st.markdown("---")
                    display_competitors(comp_data, info["name"], parsed["score"])

    # ════════════════════════════════════════════════════════
    # BULK RESUME MODE
    # ════════════════════════════════════════════════════════
    else:
        uploaded_files = st.file_uploader(
            "📦 Upload Multiple Resumes (PDF)", type=["pdf"],
            accept_multiple_files=True
        )
        job_description_bulk = st.text_area("📋 Paste the Job Description", height=200)

        if st.button("🚀 Rank All Resumes", use_container_width=True, type="primary"):
            if not uploaded_files:
                st.warning("⚠️ Please upload at least one resume.")
            elif not job_description_bulk.strip():
                st.warning("⚠️ Please paste a job description.")
            else:
                all_results = []
                progress = st.progress(0)
                status = st.empty()

                for i, file in enumerate(uploaded_files):
                    status.text(f"Analysing {file.name}... ({i+1}/{len(uploaded_files)})")
                    resume_text = extract_text_from_pdf(file)
                    if resume_text:
                        raw = analyze_resume(resume_text, job_description_bulk, info["role"])
                        parsed = parse_response(raw)
                        all_results.append({"name": file.name, "parsed": parsed})
                    progress.progress((i + 1) / len(uploaded_files))

                status.empty()
                progress.empty()

                all_results.sort(key=lambda x: x["parsed"]["score"], reverse=True)

                st.markdown("## 🏆 Ranked Shortlist")
                for rank, result in enumerate(all_results, 1):
                    score = result["parsed"]["score"]
                    color = "#ff4b4b" if score < 40 else "#f9a825" if score < 70 else "#00c853"
                    st.markdown(
                        f"<div class='rank-card'>"
                        f"<b>#{rank} — {result['name']}</b> &nbsp;&nbsp;"
                        f"<span style='color:{color}; font-size:1.2rem; font-weight:bold;'>{score}%</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    with st.expander(f"See full analysis for {result['name']}"):
                        display_results(result["parsed"], result["name"])