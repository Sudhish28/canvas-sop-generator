"""
AI-Powered Canvas SOP Generator & Workflow Analyzer
Streamlit Frontend — app.py
Partner: Jhansi Pothula (Process Owner)
Builder: Sudhish Chitturi
Course: IT7039
"""

import streamlit as st
import json
import datetime
from backend import run_full_pipeline, format_sop_as_markdown

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Canvas SOP Generator",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    .main { background-color: #f8f9fa; }

    .stApp {
        background: linear-gradient(135deg, #0f1117 0%, #1a1d2e 100%);
    }

    .hero-header {
        background: linear-gradient(135deg, #1a1d2e, #0d1117);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #58a6ff, #7c3aed, #ec4899);
    }

    .hero-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.5rem;
        font-weight: 500;
        color: #e6edf3;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
    }

    .hero-sub {
        color: #8b949e;
        font-size: 0.9rem;
        margin: 0;
    }

    .partner-tag {
        display: inline-block;
        background: rgba(88, 166, 255, 0.1);
        border: 1px solid rgba(88, 166, 255, 0.3);
        color: #58a6ff;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-family: 'IBM Plex Mono', monospace;
        margin-top: 0.75rem;
    }

    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 1.25rem;
        text-align: center;
    }

    .metric-val {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 2rem;
        font-weight: 500;
        color: #58a6ff;
        margin: 0;
    }

    .metric-label {
        color: #8b949e;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0.25rem 0 0 0;
    }

    .sop-step {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 3px solid #58a6ff;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
    }

    .step-num {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        color: #58a6ff;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.25rem;
    }

    .step-action {
        font-weight: 500;
        color: #e6edf3;
        font-size: 1rem;
        margin-bottom: 0.35rem;
    }

    .step-desc {
        color: #8b949e;
        font-size: 0.875rem;
        line-height: 1.6;
    }

    .exception-tag {
        display: inline-block;
        background: rgba(248, 81, 73, 0.1);
        border: 1px solid rgba(248, 81, 73, 0.3);
        color: #f85149;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        margin: 2px;
    }

    .tip-box {
        background: rgba(56, 139, 253, 0.05);
        border: 1px solid rgba(56, 139, 253, 0.2);
        border-radius: 6px;
        padding: 0.5rem 0.75rem;
        margin-top: 0.5rem;
        color: #79c0ff;
        font-size: 0.8rem;
    }

    .bottleneck-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 3px solid #f85149;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }

    .severity-high { color: #f85149; }
    .severity-medium { color: #e3b341; }
    .severity-low { color: #3fb950; }

    .confidence-bar {
        background: #21262d;
        border-radius: 4px;
        height: 6px;
        overflow: hidden;
        margin: 0.5rem 0;
    }

    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #3fb950, #58a6ff);
        border-radius: 4px;
        transition: width 0.8s ease;
    }

    .log-entry {
        background: #0d1117;
        border: 1px solid #21262d;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.75rem;
        color: #8b949e;
    }

    .log-module {
        color: #3fb950;
        font-weight: 500;
    }

    .section-header {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #8b949e;
        border-bottom: 1px solid #21262d;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #1f6feb, #388bfd) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-weight: 500 !important;
        padding: 0.6rem 1.5rem !important;
        font-size: 0.9rem !important;
        transition: all 0.2s !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(56, 139, 253, 0.4) !important;
    }

    .stTextArea textarea {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #e6edf3 !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        border-radius: 8px !important;
    }

    .stTextArea textarea:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.2) !important;
    }

    div[data-testid="stSidebar"] {
        background: #0d1117 !important;
        border-right: 1px solid #21262d !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")

    partner_name = st.text_input("Process Owner Name", value="Jhansi", help="The partner whose workflow you are documenting")

    st.markdown("---")
    st.markdown("### 📌 About This Project")
    st.markdown("""
    **Course:** IT7039  
    **Track:** B — Builder  
    **Builder:** Sudhish Chitturi  
    **Partner:** Jhansi Pothula  
    
    This app converts real Canvas workflow descriptions into structured SOPs, process diagrams, and workflow intelligence reports.
    """)

    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    st.markdown("[GitHub Repository](https://github.com/Sudhish28/canvas-sop-generator)")

    st.markdown("---")
    st.markdown("### 💡 Try Jhansi's Workflow")
    if st.button("Load Sample Workflow"):
        st.session_state["sample_loaded"] = True


# ── Hero Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <p class="hero-title">📋 Canvas SOP Generator</p>
    <p class="hero-sub">AI-powered conversion of real workflow descriptions into structured Standard Operating Procedures, process diagrams, and workflow intelligence.</p>
    <span class="partner-tag">Process Owner: Jhansi Pothula · IT7039 Capstone · Track B Builder</span>
</div>
""", unsafe_allow_html=True)


# ── Sample workflow (Jhansi's real workflow) ─────────────────────────────────
JHANSI_WORKFLOW = """I open Canvas in Chrome. Sometimes it remembers my login, but after weekends it usually logs me out and I have to go through the university SSO portal — which sometimes errors when my VPN is on, so I turn off VPN first.

Once I'm in, I land on the Dashboard. My course (IT7039) isn't always showing as a favorite so I have to scroll through All Courses to find it, especially since I have 6 active courses.

First thing I check is Announcements because professors sometimes post last-minute changes to assignments that I'd miss otherwise — I learned this the hard way.

Then I go to Modules to find the assignment. But not every professor organizes it the same way — sometimes I have to go to Assignments directly if Modules doesn't show what I need.

I click on the assignment to read the instructions. Sometimes the instructions are right there in Canvas, but sometimes they link out to a Google Doc or a PDF that I have to download. I've accidentally closed the Canvas assignment page while reading the PDF and had to navigate all the way back.

I work on the assignment in Google Docs or Word. When I'm done I go back to Canvas, find the assignment again, and hit Submit. I upload my file. Canvas doesn't always make it obvious that the submission actually went through — I look for a green checkmark or 'Submitted' label but it's not always clear, so I take a screenshot just in case.

Sometimes the Submit button is grayed out with no explanation. This has happened when the due date passed or when I was on the wrong attempt number. Canvas doesn't tell you why it's grayed out which is really frustrating.

After submitting I go to Grades to confirm the submission registered. Sometimes there's a delay. Later when grades are posted I check SpeedGrader feedback, but finding where the inline comments are is confusing because the interface is not intuitive."""


# ── Main input area ───────────────────────────────────────────────────────────
if st.session_state.get("sample_loaded"):
    default_text = JHANSI_WORKFLOW
else:
    default_text = ""

workflow_input = st.text_area(
    "📝 Describe the workflow",
    value=default_text,
    height=220,
    placeholder=f"Describe {partner_name}'s workflow in natural language — include real steps, pain points, exceptions, and anything that goes wrong. The more detail, the better the SOP.",
    help="Enter a detailed description of the workflow you want to document as an SOP."
)

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    generate_btn = st.button("🚀 Generate SOP + Diagram + Analysis", type="primary")
with col2:
    word_count = len(workflow_input.split()) if workflow_input else 0
    st.markdown(f"<p style='color:#8b949e;font-size:0.8rem;margin-top:0.7rem;'>{word_count} words</p>", unsafe_allow_html=True)


# ── Generation pipeline ───────────────────────────────────────────────────────
if generate_btn:
    if not workflow_input.strip():
        st.error("Please enter a workflow description first.")
    else:
        with st.spinner("🤖 AI is processing the workflow... (this takes ~20-30 seconds)"):
            try:
                results = run_full_pipeline(workflow_input, partner_name)
                st.session_state["results"] = results
                st.success("✅ Generation complete!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure your ANTHROPIC_API_KEY environment variable is set.")
                st.stop()


# ── Results display ───────────────────────────────────────────────────────────
if "results" in st.session_state:
    results = st.session_state["results"]
    sop = results.get("sop", {})
    diagram = results.get("diagram", "")
    analysis = results.get("analysis", {})
    prompt_log = results.get("prompt_log", [])

    # ── Metrics row ────────────────────────────────────────────────────────────
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)

    steps_count = len(sop.get("steps", [])) if not sop.get("parse_error") else "—"
    confidence = sop.get("confidence_score", "—") if not sop.get("parse_error") else "—"
    efficiency = analysis.get("overall_efficiency_score", "—") if not analysis.get("parse_error") else "—"
    bottlenecks = len(analysis.get("bottlenecks", [])) if not analysis.get("parse_error") else "—"

    with m1:
        st.markdown(f"""<div class="metric-card"><p class="metric-val">{steps_count}</p><p class="metric-label">SOP Steps</p></div>""", unsafe_allow_html=True)
    with m2:
        conf_pct = f"{int(float(confidence)*100)}%" if confidence != "—" else "—"
        st.markdown(f"""<div class="metric-card"><p class="metric-val">{conf_pct}</p><p class="metric-label">AI Confidence</p></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-card"><p class="metric-val">{efficiency}/10</p><p class="metric-label">Efficiency Score</p></div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class="metric-card"><p class="metric-val">{bottlenecks}</p><p class="metric-label">Bottlenecks Found</p></div>""", unsafe_allow_html=True)

    st.markdown("")

    # ── Tabs ───────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 SOP", "📊 Diagram", "🔍 Analysis", "📤 Export", "🔬 Prompt Log"])

    # ── Tab 1: SOP ─────────────────────────────────────────────────────────────
    with tab1:
        if sop.get("parse_error"):
            st.markdown(sop.get("raw_output", ""))
        else:
            col_a, col_b = st.columns([2, 1])

            with col_a:
                st.markdown(f"## {sop.get('title', 'SOP')}")
                st.markdown(f"**SOP ID:** `{sop.get('sop_id', 'N/A')}` | **Version:** `{sop.get('version', '1.0')}` | **Date:** `{sop.get('date', '')}`")
                st.markdown(f"_{sop.get('purpose', '')}_")

            with col_b:
                # Confidence indicator
                conf_val = float(sop.get("confidence_score", 0))
                st.markdown(f"**AI Confidence**")
                conf_pct_int = int(conf_val * 100)
                color = "#3fb950" if conf_val >= 0.85 else "#e3b341" if conf_val >= 0.7 else "#f85149"
                st.markdown(f"""
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width:{conf_pct_int}%; background: {color};"></div>
                </div>
                <p style="font-size:0.8rem;color:#8b949e;">{conf_pct_int}% — {sop.get('confidence_notes', '')}</p>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # Scope & Roles
            with st.expander("📌 Scope, Roles & Prerequisites", expanded=False):
                st.markdown(f"**Scope:** {sop.get('scope', '')}")
                roles = sop.get("roles", [])
                if roles:
                    st.markdown("**Roles:**")
                    for r in roles:
                        st.markdown(f"- **{r.get('role', '')}**: {r.get('responsibility', '')}")
                prereqs = sop.get("prerequisites", [])
                if prereqs:
                    st.markdown("**Prerequisites:**")
                    for p in prereqs:
                        st.markdown(f"- {p}")

            # Steps
            st.markdown('<p class="section-header">Step-by-Step Instructions</p>', unsafe_allow_html=True)
            steps = sop.get("steps", [])
            for step in steps:
                exceptions_html = "".join([f'<span class="exception-tag">⚠ {e}</span>' for e in step.get("exceptions", [])])
                tip_html = f'<div class="tip-box">💡 {step.get("tips", "")}</div>' if step.get("tips") else ""

                st.markdown(f"""
                <div class="sop-step">
                    <div class="step-num">Step {step.get('step_number', '')} of {len(steps)}</div>
                    <div class="step-action">{step.get('action', '')}</div>
                    <div class="step-desc">{step.get('description', '')}</div>
                    <div style="margin-top:0.5rem;color:#3fb950;font-size:0.8rem;">✓ {step.get('expected_outcome', '')}</div>
                    <div style="margin-top:0.5rem;">{exceptions_html}</div>
                    {tip_html}
                </div>
                """, unsafe_allow_html=True)

            # Exceptions & SLA
            col_e, col_s = st.columns(2)
            with col_e:
                escalations = sop.get("exceptions_and_escalations", [])
                if escalations:
                    st.markdown('<p class="section-header">Exceptions & Escalations</p>', unsafe_allow_html=True)
                    for e in escalations:
                        st.markdown(f"""
                        <div class="bottleneck-card">
                            <div style="color:#f85149;font-size:0.8rem;font-weight:500;">⚠ {e.get('scenario', '')}</div>
                            <div style="color:#8b949e;font-size:0.85rem;margin-top:0.25rem;">→ {e.get('resolution', '')}</div>
                        </div>
                        """, unsafe_allow_html=True)
            with col_s:
                sla = sop.get("sla", {})
                if sla:
                    st.markdown('<p class="section-header">SLA / Timing</p>', unsafe_allow_html=True)
                    st.metric("Estimated Completion", sla.get("normal_completion_time", "N/A"))
                    st.markdown(f"<p style='color:#8b949e;font-size:0.85rem;'>{sla.get('deadline_sensitivity', '')}</p>", unsafe_allow_html=True)

    # ── Tab 2: Diagram ──────────────────────────────────────────────────────────
    with tab2:
        st.markdown('<p class="section-header">Process Flow Diagram</p>', unsafe_allow_html=True)

        if diagram:
            # Display the raw Mermaid syntax for copy/paste
            st.markdown("**Mermaid Diagram Code** — copy this into [mermaid.live](https://mermaid.live) to view interactively:")
            st.code(diagram, language="text")

            st.markdown("---")
            st.markdown("**Live Preview** (rendered below):")

            # Render via mermaid.js in an HTML component
            mermaid_html = f"""
            <div id="mermaid-container" style="background:#161b22;border:1px solid #30363d;border-radius:10px;padding:1.5rem;min-height:200px;">
                <div class="mermaid" style="text-align:center;">
{diagram}
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: 'dark',
                    flowchart: {{ curve: 'basis', padding: 20 }},
                    themeVariables: {{
                        primaryColor: '#1f2937',
                        primaryTextColor: '#e6edf3',
                        primaryBorderColor: '#58a6ff',
                        lineColor: '#8b949e',
                        secondaryColor: '#161b22',
                        tertiaryColor: '#0d1117',
                        background: '#161b22',
                        mainBkg: '#1f2937',
                        nodeBorder: '#58a6ff',
                    }}
                }});
            </script>
            """
            st.components.v1.html(mermaid_html, height=600, scrolling=True)

    # ── Tab 3: Analysis ─────────────────────────────────────────────────────────
    with tab3:
        if analysis.get("parse_error"):
            st.markdown(analysis.get("raw_output", ""))
        else:
            st.markdown(f"### {analysis.get('summary', '')}")

            # Before / After Metrics Dashboard
            st.markdown('<p class="section-header">Before / After Metrics</p>', unsafe_allow_html=True)
            before = analysis.get("before_metrics", {})
            after = analysis.get("after_metrics", {})

            col_b, col_a = st.columns(2)
            with col_b:
                st.markdown("**Current State**")
                st.metric("Time to complete", f"{before.get('estimated_time_minutes', '?')} min")
                st.metric("Error-prone steps", before.get("error_prone_steps", "?"))
                st.metric("Manual steps", before.get("manual_steps", "?"))
            with col_a:
                st.markdown("**After Improvements**")
                t_before = before.get("estimated_time_minutes", 0)
                t_after = after.get("estimated_time_minutes", 0)
                delta = f"-{t_before - t_after} min" if t_before and t_after else None
                st.metric("Time to complete", f"{t_after} min", delta=delta, delta_color="inverse")
                e_before = before.get("error_prone_steps", 0)
                e_after = after.get("error_prone_steps", 0)
                st.metric("Error-prone steps", e_after, delta=f"{e_after - e_before}" if e_before and e_after else None, delta_color="inverse")
                st.metric("Manual steps", after.get("manual_steps", "?"))

            if after.get("assumptions"):
                st.caption(f"*Assumptions: {after['assumptions']}*")

            # Bottlenecks
            bottlenecks = analysis.get("bottlenecks", [])
            if bottlenecks:
                st.markdown('<p class="section-header">Bottlenecks Identified</p>', unsafe_allow_html=True)
                for b in bottlenecks:
                    sev = b.get("severity", "medium").lower()
                    sev_color = "#f85149" if sev == "high" else "#e3b341" if sev == "medium" else "#3fb950"
                    st.markdown(f"""
                    <div class="bottleneck-card">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="color:#e6edf3;font-weight:500;">{b.get('location', '')}</span>
                            <span style="color:{sev_color};font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;">{sev} severity</span>
                        </div>
                        <div style="color:#8b949e;font-size:0.875rem;margin-top:0.35rem;">{b.get('description', '')}</div>
                        <div style="color:#58a6ff;font-size:0.8rem;margin-top:0.35rem;">⏱ {b.get('estimated_time_lost', '')} lost · Root cause: {b.get('root_cause', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Automation Opportunities
            autos = analysis.get("automation_opportunities", [])
            if autos:
                st.markdown('<p class="section-header">Automation Opportunities</p>', unsafe_allow_html=True)
                for a in autos:
                    effort = a.get("effort", "medium").lower()
                    effort_color = "#3fb950" if effort == "low" else "#e3b341" if effort == "medium" else "#f85149"
                    st.markdown(f"""
                    <div style="background:#161b22;border:1px solid #30363d;border-left:3px solid #3fb950;border-radius:8px;padding:1rem;margin-bottom:0.5rem;">
                        <div style="color:#e6edf3;font-weight:500;">{a.get('opportunity', '')}</div>
                        <div style="color:#8b949e;font-size:0.85rem;margin-top:0.25rem;">Tool: {a.get('tool_suggestion', '')} · Impact: {a.get('impact', '')}</div>
                        <div style="color:{effort_color};font-size:0.75rem;margin-top:0.25rem;">Effort: {effort}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Priority Actions
            priorities = analysis.get("priority_actions", [])
            if priorities:
                st.markdown('<p class="section-header">Priority Actions</p>', unsafe_allow_html=True)
                for i, p in enumerate(priorities, 1):
                    st.markdown(f"""
                    <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:0.75rem 1rem;margin-bottom:0.5rem;display:flex;gap:12px;align-items:flex-start;">
                        <span style="background:#1f6feb;color:white;border-radius:50%;width:22px;height:22px;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:600;flex-shrink:0;">{i}</span>
                        <span style="color:#e6edf3;font-size:0.875rem;">{p}</span>
                    </div>
                    """, unsafe_allow_html=True)

    # ── Tab 4: Export ───────────────────────────────────────────────────────────
    with tab4:
        st.markdown('<p class="section-header">Export Options</p>', unsafe_allow_html=True)
        st.markdown("Download your SOP in different formats for use outside Canvas.")

        col_x1, col_x2 = st.columns(2)

        with col_x1:
            markdown_content = results.get("markdown_export", "")
            if markdown_content:
                st.download_button(
                    label="📄 Download SOP as Markdown",
                    data=markdown_content,
                    file_name=f"SOP_{datetime.date.today()}.md",
                    mime="text/markdown",
                )

        with col_x2:
            full_json = json.dumps({
                "sop": sop,
                "analysis": analysis,
                "diagram": diagram,
                "prompt_log": prompt_log,
            }, indent=2)
            st.download_button(
                label="🔧 Download Full JSON (SOP + Analysis)",
                data=full_json,
                file_name=f"sop_full_{datetime.date.today()}.json",
                mime="application/json",
            )

        st.markdown("---")
        st.markdown("**Mermaid Diagram** — Copy and paste into [mermaid.live](https://mermaid.live) for interactive editing or export as PNG/SVG:")
        st.code(diagram, language="text")

    # ── Tab 5: Prompt Log ───────────────────────────────────────────────────────
    with tab5:
        st.markdown('<p class="section-header">Prompt & Change Log</p>', unsafe_allow_html=True)
        st.markdown("Full traceability of every AI call made during this generation.")

        for i, entry in enumerate(prompt_log, 1):
            st.markdown(f"""
            <div class="log-entry">
                <span class="log-module">[{entry.get('module', '')}]</span>
                &nbsp;&nbsp;
                <span>{entry.get('timestamp', '')}</span>
                &nbsp;&nbsp;|&nbsp;&nbsp;
                <span>Model: {entry.get('model', '')}</span>
                &nbsp;&nbsp;|&nbsp;&nbsp;
                <span>Output: {entry.get('output_length', 0):,} chars</span>
                <div style="color:#58a6ff;margin-top:0.4rem;font-size:0.7rem;">Prompt preview: {entry.get('prompt_preview', '')[:200]}...</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"**Generated at:** `{results.get('generated_at', '')}`")
        st.caption("All AI outputs were validated by the builder before inclusion. This log supports full reproducibility of results.")
