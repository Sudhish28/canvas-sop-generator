# AI-Powered Canvas SOP Generator & Workflow Analyzer (Prototype Backend)

# -----------------------------
# 1. SOP GENERATOR (BASIC)
# -----------------------------
def generate_sop(workflow_text):
    sop = f"""
    SOP: Canvas Workflow

    Purpose:
    Convert Canvas user actions into structured SOP

    Input Workflow:
    {workflow_text}

    Steps:
    1. Login to Canvas
    2. Navigate to dashboard
    3. Open course
    4. Access modules
    5. Submit assignment

    Output:
    Structured SOP generated successfully
    """
    return sop


# -----------------------------
# 2. DIAGRAM GENERATOR (MERMAID MOCK)
# -----------------------------
def generate_mermaid_diagram():
    diagram = """
    graph TD
    A[Login to Canvas] --> B[Dashboard]
    B --> C[Open Course]
    C --> D[Access Modules]
    D --> E[Submit Assignment]
    """
    return diagram


# -----------------------------
# 3. WORKFLOW ANALYSIS (DUMMY LOGIC)
# -----------------------------
def analyze_workflow(workflow_text):
    return {
        "bottlenecks": ["Too many manual navigation steps"],
        "redundancies": ["Repeated clicking between modules"],
        "suggestions": ["Automate navigation using shortcuts or links"]
    }


# -----------------------------
# 4. SAMPLE RUN (PROOF IT WORKS)
# -----------------------------
if __name__ == "__main__":
    input_text = "Student logs into Canvas and submits assignment"

    print("\n--- SOP OUTPUT ---")
    print(generate_sop(input_text))

    print("\n--- DIAGRAM OUTPUT ---")
    print(generate_mermaid_diagram())

    print("\n--- ANALYSIS OUTPUT ---")
    print(analyze_workflow(input_text))