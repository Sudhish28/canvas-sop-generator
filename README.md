# 📋 AI-Powered Canvas SOP Generator & Workflow Analyzer

> **IT7039 — AI for SOPs and Process Documentation | Capstone Track B — Builder**  
> **Builder:** Sudhish Chitturi | **Process Owner:** Jhansi Pothula

---

## What This Does

This application converts a natural-language description of a Canvas LMS workflow into:

1. **Structured SOP** — Purpose, scope, roles, step-by-step instructions with exceptions, SLA, and improvement recommendations
2. **Process Diagram** — Auto-generated Mermaid flowchart with decision points and exception paths
3. **Workflow Intelligence** — Bottleneck detection, redundancy analysis, automation opportunities, and before/after metrics
4. **Export** — Download SOP as Markdown or full JSON; copy Mermaid diagram for mermaid.live

Built specifically around **Jhansi's real Canvas workflow** — including SSO login issues, inconsistent course navigation, unclear submission confirmation, and SpeedGrader feedback discovery. The partner acted as process owner and source of truth throughout.

---

## Live Demo

> **[▶ Open App on Streamlit Cloud](https://your-app-url.streamlit.app)**  
> *(Click "Load Sample Workflow" in the sidebar to try Jhansi's real workflow immediately)*

---

## Architecture

```
User Input (workflow text)
        │
        ▼
┌─────────────────────────────────────────────────────┐
│                    backend.py                       │
│                                                     │
│  generate_sop()  →  Claude API  →  Structured JSON  │
│  generate_mermaid_diagram()  →  Mermaid syntax      │
│  analyze_workflow()  →  Bottlenecks + Metrics       │
│  format_sop_as_markdown()  →  Export                │
│  log_prompt()  →  Full audit trail                  │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│                     app.py                          │
│                                                     │
│  Streamlit UI with 5 tabs:                          │
│  📄 SOP  |  📊 Diagram  |  🔍 Analysis             │
│  📤 Export  |  🔬 Prompt Log                        │
└─────────────────────────────────────────────────────┘
```

**Tech Stack:**
- Python 3.10+
- [Anthropic Claude API](https://docs.anthropic.com) — real LLM-powered processing
- [Streamlit](https://streamlit.io) — UI framework
- Mermaid.js — process diagram rendering
- GitHub — version control

---

## Running Locally

### 1. Clone the repo
```bash
git clone https://github.com/Sudhish28/canvas-sop-generator.git
cd canvas-sop-generator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
```bash
# Mac/Linux
export ANTHROPIC_API_KEY=your_api_key_here

# Windows
set ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## Deploying to Streamlit Community Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `ANTHROPIC_API_KEY` as a secret in the app settings
5. Deploy — you get a public URL in ~2 minutes

---

## Project Structure

```
canvas-sop-generator/
├── app.py              # Streamlit frontend (UI, tabs, export)
├── backend.py          # AI pipeline (Claude API calls, logging)
├── requirements.txt    # Python dependencies
├── sample_input.txt    # Jhansi's real workflow description
├── sample_output.md    # Example SOP output
└── README.md
```

---

## Key Features (Beyond Basic SOP)

| Feature | Description |
|---|---|
| **Real AI Integration** | Every generation calls Claude API — no hardcoded outputs |
| **Confidence Indicators** | Each SOP includes an AI confidence score with human review flag |
| **Prompt & Change Log** | Full audit trail of every API call (timestamp, model, output length) |
| **Before/After Metrics** | Quantifies time saved and error reduction from recommendations |
| **Exception-Aware SOPs** | Steps include real-world exceptions, not just ideal-path instructions |
| **Export** | Markdown + JSON download; Mermaid diagram for mermaid.live |

---

## Collaboration Model

This is a **Track B Builder** project with a dedicated process owner:

- **Sudhish (Builder)** — designed and built the application; responsible for all technical implementation
- **Jhansi (Process Owner)** — provided her real Canvas workflow as input; validated SOP outputs for accuracy; identified gaps between ideal and actual steps

The app was built specifically to document Jhansi's workflow, not a generic Canvas tutorial. All improvement recommendations trace back to friction points she identified.

---

## AI Usage

Claude API was used for:
- **SOP generation** — converting raw workflow text to structured JSON
- **Diagram generation** — producing Mermaid flowchart syntax from step descriptions  
- **Workflow analysis** — identifying bottlenecks, redundancies, and automation opportunities

Human validation was applied to every AI output. Where the AI generated generic language, steps were revised to reflect Jhansi's specific workflow. The prompt log (visible in the app's Prompt Log tab) provides full traceability.

---

## Sample Output

**Input:** Jhansi's Canvas workflow (SSO login → course navigation → assignment submission → grade check)

**SOP Generated:** 8-step SOP with 6 identified exceptions, 3 improvement recommendations, SLA of ~12 minutes  
**Diagram:** Flowchart with 4 decision nodes (login check, course favorited?, instructions location, submission confirmed?)  
**Analysis:** Efficiency score 5.5/10 → projected 7.8/10 after improvements; 3 automation opportunities identified

---

*Generated with Claude AI. All outputs validated by process owner. IT7039 Capstone — Spring 2026.*
