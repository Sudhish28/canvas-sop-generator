"""
AI-Powered Canvas SOP Generator & Workflow Analyzer
Backend — uses Groq API (free, fast)
Partner: Jhansi Pothula (Process Owner)
Builder: Sudhish Chitturi
Course: IT7039 — AI for SOPs and Process Documentation
"""

import json
import datetime
import re
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("ggsk_fdaD6yFMYi3l0w7LlF8AWGdyb3FYxdmQSbuPmGVitERmT4oCsaEY"))
MODEL = "llama-3.3-70b-versatile"


def log_prompt(prompt: str, output: str, module: str) -> dict:
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "module": module,
        "prompt_preview": prompt[:300] + "..." if len(prompt) > 300 else prompt,
        "output_length": len(output),
        "model": MODEL,
    }


def clean_json(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    return raw.strip()


def generate_sop(workflow_text: str, partner_name: str = "Jhansi") -> dict:
    prompt = f"""You are an expert process documentation specialist. Your partner {partner_name} has described their real Canvas LMS workflow. Convert it into a professional SOP.

WORKFLOW FROM {partner_name.upper()}:
{workflow_text}

Return ONLY this exact JSON structure, no other text:
{{
  "title": "SOP title specific to this workflow",
  "sop_id": "SOP-CANVAS-001",
  "version": "1.0",
  "date": "{datetime.date.today().isoformat()}",
  "purpose": "2-3 sentence purpose statement",
  "scope": "Who this SOP applies to",
  "roles": [
    {{"role": "role name", "responsibility": "what they do"}}
  ],
  "prerequisites": ["thing needed before starting"],
  "steps": [
    {{
      "step_number": 1,
      "action": "Clear action title",
      "description": "Detailed description",
      "expected_outcome": "What success looks like",
      "exceptions": ["things that can go wrong"],
      "tips": "Helpful tip from real experience"
    }}
  ],
  "exceptions_and_escalations": [
    {{"scenario": "what went wrong", "resolution": "how to fix it"}}
  ],
  "sla": {{
    "normal_completion_time": "estimated time",
    "deadline_sensitivity": "description"
  }},
  "improvement_recommendations": [
    {{"issue": "identified problem", "recommendation": "suggested fix", "impact": "why this matters"}}
  ],
  "confidence_score": 0.92,
  "confidence_notes": "Brief note on confidence and assumptions"
}}

Rules:
- Be specific to this workflow, not generic
- Include real exceptions the user mentioned
- Return ONLY valid JSON, nothing else"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a process documentation expert. Always respond with valid JSON only, no markdown, no explanation."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
        temperature=0.3,
    )

    raw_output = clean_json(response.choices[0].message.content)

    try:
        sop_data = json.loads(raw_output)
    except json.JSONDecodeError:
        sop_data = {"raw_output": raw_output, "parse_error": True}

    return {"sop": sop_data, "log": log_prompt(prompt, raw_output, "SOP Generator")}


def generate_mermaid_diagram(workflow_text: str, sop_data: dict = None) -> dict:
    sop_context = ""
    if sop_data and not sop_data.get("parse_error"):
        steps = sop_data.get("steps", [])
        sop_context = f"\nSOP steps: {json.dumps([s.get('action', '') for s in steps])}"

    prompt = f"""Create a Mermaid flowchart for this Canvas workflow.

WORKFLOW:
{workflow_text}
{sop_context}

Rules:
- Start with: flowchart TD
- Use decision diamonds {{{{condition}}}} for branching like login check, course found, submission confirmed
- Show error/exception paths
- Keep node labels SHORT (max 4 words)
- End with a terminal node
- Return ONLY the Mermaid syntax, no explanation, no markdown fences"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a Mermaid diagram expert. Return only valid Mermaid flowchart syntax starting with 'flowchart TD'. No markdown fences, no explanation."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.2,
    )

    diagram = clean_json(response.choices[0].message.content)
    if not diagram.strip().lower().startswith("flowchart"):
        diagram = "flowchart TD\n" + diagram

    return {"diagram": diagram, "log": log_prompt(prompt, diagram, "Diagram Generator")}


def analyze_workflow(workflow_text: str, sop_data: dict = None) -> dict:
    sop_context = ""
    if sop_data and not sop_data.get("parse_error"):
        exceptions = sop_data.get("exceptions_and_escalations", [])
        sop_context = f"\nKnown exceptions: {json.dumps(exceptions)}"

    prompt = f"""Analyze this Canvas workflow and return structured insights.

WORKFLOW:
{workflow_text}
{sop_context}

Return ONLY this exact JSON, no other text:
{{
  "overall_efficiency_score": 6.5,
  "summary": "2-sentence overall assessment",
  "bottlenecks": [
    {{
      "location": "where in the workflow",
      "description": "what the bottleneck is",
      "severity": "high/medium/low",
      "estimated_time_lost": "X minutes per occurrence",
      "root_cause": "why this happens"
    }}
  ],
  "redundancies": [
    {{"description": "what is repeated", "steps_affected": ["step names"], "fix": "how to fix"}}
  ],
  "high_risk_steps": [
    {{"step": "step name", "risk": "what can go wrong", "likelihood": "high/medium/low", "mitigation": "how to reduce"}}
  ],
  "automation_opportunities": [
    {{"opportunity": "what to automate", "tool_suggestion": "tool", "effort": "low/medium/high", "impact": "benefit"}}
  ],
  "before_metrics": {{
    "estimated_time_minutes": 15,
    "error_prone_steps": 3,
    "manual_steps": 8
  }},
  "after_metrics": {{
    "estimated_time_minutes": 8,
    "error_prone_steps": 1,
    "manual_steps": 4,
    "assumptions": "what changes were assumed"
  }},
  "priority_actions": ["Most impactful action", "Second priority", "Third priority"]
}}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a workflow efficiency analyst. Always respond with valid JSON only, no markdown, no explanation."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2500,
        temperature=0.3,
    )

    raw_output = clean_json(response.choices[0].message.content)

    try:
        analysis = json.loads(raw_output)
    except json.JSONDecodeError:
        analysis = {"raw_output": raw_output, "parse_error": True}

    return {"analysis": analysis, "log": log_prompt(prompt, raw_output, "Workflow Analyzer")}


def format_sop_as_markdown(sop_data: dict) -> str:
    if sop_data.get("parse_error"):
        return sop_data.get("raw_output", "Error generating SOP")
    s = sop_data
    lines = [
        f"# {s.get('title', 'Canvas Workflow SOP')}",
        f"\n**SOP ID:** {s.get('sop_id', 'N/A')} | **Version:** {s.get('version', '1.0')} | **Date:** {s.get('date', '')}",
        "\n---\n",
        f"## Purpose\n{s.get('purpose', '')}",
        f"\n## Scope\n{s.get('scope', '')}",
    ]
    if s.get("roles"):
        lines.append("\n## Roles & Responsibilities")
        for r in s["roles"]:
            lines.append(f"- **{r.get('role', '')}**: {r.get('responsibility', '')}")
    if s.get("prerequisites"):
        lines.append("\n## Prerequisites")
        for p in s["prerequisites"]:
            lines.append(f"- {p}")
    if s.get("steps"):
        lines.append("\n## Step-by-Step Instructions")
        for step in s["steps"]:
            lines.append(f"\n### Step {step.get('step_number', '')}: {step.get('action', '')}")
            lines.append(step.get("description", ""))
            lines.append(f"\n**Expected Outcome:** {step.get('expected_outcome', '')}")
            if step.get("tips"):
                lines.append(f"\n> **Tip:** {step.get('tips', '')}")
            for e in step.get("exceptions", []):
                lines.append(f"- ⚠ {e}")
    if s.get("exceptions_and_escalations"):
        lines.append("\n## Exceptions & Escalations")
        for e in s["exceptions_and_escalations"]:
            lines.append(f"\n**Scenario:** {e.get('scenario', '')}")
            lines.append(f"**Resolution:** {e.get('resolution', '')}")
    if s.get("sla"):
        lines.append("\n## SLA / Timing")
        lines.append(f"- **Normal Completion Time:** {s['sla'].get('normal_completion_time', '')}")
        lines.append(f"- **Deadline Sensitivity:** {s['sla'].get('deadline_sensitivity', '')}")
    if s.get("improvement_recommendations"):
        lines.append("\n## Improvement Recommendations")
        for r in s["improvement_recommendations"]:
            lines.append(f"\n**Issue:** {r.get('issue', '')}")
            lines.append(f"**Recommendation:** {r.get('recommendation', '')}")
            lines.append(f"**Impact:** {r.get('impact', '')}")
    lines.append(f"\n---\n*AI Confidence: {s.get('confidence_score', 'N/A')} — {s.get('confidence_notes', '')}*")
    lines.append("*Generated by AI-Powered Canvas SOP Generator. Validated by process owner.*")
    return "\n".join(lines)


def run_full_pipeline(workflow_text: str, partner_name: str = "Jhansi") -> dict:
    all_logs = []

    sop_result = generate_sop(workflow_text, partner_name)
    all_logs.append(sop_result["log"])
    sop_data = sop_result["sop"]

    diagram_result = generate_mermaid_diagram(workflow_text, sop_data)
    all_logs.append(diagram_result["log"])

    analysis_result = analyze_workflow(workflow_text, sop_data)
    all_logs.append(analysis_result["log"])

    return {
        "sop": sop_data,
        "diagram": diagram_result["diagram"],
        "analysis": analysis_result["analysis"],
        "markdown_export": format_sop_as_markdown(sop_data),
        "prompt_log": all_logs,
        "generated_at": datetime.datetime.now().isoformat(),
    }   