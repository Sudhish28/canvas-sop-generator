# VIDEO SCRIPT — IT7039 Capstone Final Demo
# Track B — Builder | Sudhish Chitturi
# Target: 8–10 minutes | Required coverage: all 5 rubric points

=======================================================================
BEFORE YOU RECORD — SETUP CHECKLIST
=======================================================================
□ App is running at localhost:8501 (or Streamlit Cloud URL)
□ Sidebar shows partner name "Jhansi"
□ Browser tab is visible and clean (close other tabs)
□ Sample workflow is NOT pre-loaded (you'll load it live)
□ Screen recording is capturing both screen AND microphone
□ Run once beforehand so results are cached for smooth demo
=======================================================================


-------------------------------------------------------------------
SECTION 1 — INTRO (0:00 – 0:45)
-------------------------------------------------------------------

[SHOW: App homepage, not yet loaded]

"Hi, I'm Sudhish Chitturi and this is my IT7039 capstone final 
submission for Track B — the Builder track.

The application I built is called the AI-Powered Canvas SOP Generator 
and Workflow Analyzer. Its purpose is to take a real person's messy, 
natural-language description of how they use Canvas — and convert it 
into a structured Standard Operating Procedure, a process diagram, 
and a workflow intelligence report.

My process owner is Jhansi Pothula. She's the student whose Canvas 
workflow I documented. She gave me her real workflow — not the ideal 
version, the actual one — with all the login failures, navigation 
confusion, and submission anxiety that real students experience. 
My job was to build an application that captures and structures that."


-------------------------------------------------------------------
SECTION 2 — LIVE DEMO (0:45 – 4:30)  ← CORE OF THE VIDEO
-------------------------------------------------------------------

[CLICK: "Load Sample Workflow" in the sidebar]

"I'll start by loading Jhansi's actual workflow description. This is 
what she told me verbatim — she described going through the university 
SSO portal with VPN issues, not finding her course favorited, checking 
Announcements first because she'd missed things before, the inconsistent 
navigation between Modules and Assignments, losing the Canvas page when 
she opens a PDF, the ambiguous submission confirmation — and that 
really frustrating grayed-out Submit button that gives you no reason why."

[SHOW: Workflow text loaded in the text area]

"This is real input. Not a clean textbook workflow. Now let me generate."

[CLICK: Generate button]

"The app calls the Claude API three times in parallel — once for the 
SOP, once for the Mermaid diagram, and once for the workflow analysis. 
Every call is logged — I'll show you that in a moment."

[WAIT for results — ~25 seconds]
[SHOW: Metrics row appears — SOP Steps, Confidence %, Efficiency Score, Bottlenecks]

"Already we can see the at-a-glance metrics. Let me walk through each tab."

[CLICK: SOP Tab]

"Here's the generated SOP. It has a title specific to Jhansi's workflow, 
not generic Canvas navigation. You can see the confidence score — 
[read the %, e.g. '91%'] — with a note on what was assumed. That's the 
AI transparency feature: every output flags its own confidence so the 
human reviewer knows where to look closer.

The steps are specific to what Jhansi described. Step [X] covers the 
SSO login with the VPN exception. Step [Y] covers checking Announcements 
before jumping to the assignment — because she specifically mentioned 
she learned that the hard way.

Each step has expected outcomes in green, exception tags in red — like 
the grayed-out submit button — and a tip pulled from real experience."

[SCROLL through a few steps, highlight one exception tag]

[CLICK: Diagram Tab]

"The diagram tab shows the Mermaid flowchart. Unlike a simple linear 
5-step diagram, this one has decision diamonds — for example, is the 
course favorited? Are the instructions in Canvas or externally linked? 
Did the submission confirm? — because those are the real branch points 
in Jhansi's actual workflow."

[SHOW: Mermaid code, point to a decision diamond]

"This renders live in the app. I can also copy this into mermaid.live 
for interactive editing or export as PNG."

[CLICK: Analysis Tab]

"The analysis tab is where the workflow intelligence lives. 

The before/after metrics dashboard shows the current workflow takes 
roughly [X] minutes with [Y] error-prone steps. After implementing 
the recommendations — things like bookmarking courses, using Canvas's 
'Open in new tab' for external links, and checking Submission History 
instead of a screenshot — it projects down to [Z] minutes.

The bottleneck section is specific: [read one bottleneck, e.g. 'Login 
friction at SSO — high severity, 3 minutes lost per occurrence, root 
cause is VPN conflict'].

The automation opportunities include Canvas bookmarklets, browser 
extensions for tab management, and a simple checklist approach for 
submission confirmation. Low effort, real impact."

[CLICK: Export Tab]

"Export — I can download the SOP as clean Markdown for sharing, or 
the full JSON for integration with other tools."

[CLICK: Prompt Log Tab]

"And here's the prompt log — every API call, timestamped, with the 
model used, output length, and a preview of the prompt. This is the 
full audit trail. Anyone can reproduce this exact output."


-------------------------------------------------------------------
SECTION 3 — COLLABORATION (4:30 – 6:00)
-------------------------------------------------------------------

[SHOW: Nothing specific — just talk to camera or screen]

"Let me talk about the collaboration.

Jhansi acted as my process owner. I was the builder documenting her 
process — she was not building with me, she was the source of truth 
about how a real Canvas user actually works.

The most valuable thing she gave me wasn't the ideal workflow — it was 
the exceptions. The SSO and VPN issue. The grayed-out button with no 
explanation. Losing the Canvas page when opening a PDF. Those didn't 
show up in any Canvas documentation. They came from her experience.

What that taught me: a good SOP isn't a best-case description. It's 
a description of what actually happens, including failure modes.

Early versions of this app produced generic output — things like 'click 
submit' as a step. Jhansi's feedback forced me to make the prompts 
more specific and to include exception handling in the SOP structure. 
That iteration cycle is where the real value came from."


-------------------------------------------------------------------
SECTION 4 — AI USAGE (6:00 – 7:30)
-------------------------------------------------------------------

"Now, how I used AI in this project — and I want to be specific 
rather than vague about this.

Claude was used for three things: SOP generation, diagram generation, 
and workflow analysis. In all three cases I designed the prompts to 
require JSON output in a specific schema I defined. That schema — the 
structure with confidence scores, exception tags, before/after metrics — 
that's my design, not the AI's.

Where AI wasn't enough on its own: the first version of the SOP 
generator would produce generic steps when given vague input. I had 
to iterate on the prompt — adding specific instructions like 'do NOT 
generate generic steps, base everything on the actual workflow described' 
and 'include real exceptions the user mentioned.' That prompt engineering 
is in the backend.py file, and you can see what was sent in the prompt log.

I also used AI to debug Mermaid syntax errors — the first few diagrams 
had invalid node IDs that broke rendering. AI helped me identify the 
pattern and fix the regex cleaning step.

What I had to validate myself: every SOP step was checked against 
Jhansi's actual description to make sure nothing was hallucinated. 
The improvement recommendations were cross-referenced with real Canvas 
features that actually exist. The confidence scores reflect genuine 
uncertainty — where the AI made assumptions, I flagged them."


-------------------------------------------------------------------
SECTION 5 — DESIGN DECISIONS & WHAT I'D IMPROVE (7:30 – 9:00)
-------------------------------------------------------------------

"A few design decisions worth explaining.

I chose to run three separate API calls — SOP, diagram, and analysis — 
rather than one large call. This gives better output quality for each 
task, and each result can be cached independently. The tradeoff is 
~25 second generation time. I documented that tradeoff in the code.

The confidence indicator was a deliberate addition to the original plan. 
The professor's materials stressed that AI outputs require human 
validation. The confidence score makes that visible in the UI — it's 
not decoration, it's a signal to the reviewer about where to look.

I chose Streamlit over FastAPI plus a separate frontend because for a 
single-user prototype, the development speed advantage was significant 
and the result is fully deployable on Streamlit Community Cloud with 
one click.

If I had more time, I'd add voice input — letting the user describe 
their workflow verbally rather than typing it. That's closer to how 
Jhansi actually described it to me. I'd also add a diff view between 
SOP versions so you can see exactly what changed when you regenerate."


-------------------------------------------------------------------
SECTION 6 — CLOSE (9:00 – 9:30)
-------------------------------------------------------------------

"To summarize what I'm submitting: a working AI-powered application 
that generates structured SOPs, process diagrams, and workflow 
intelligence from natural language input. Built around Jhansi's 
real Canvas workflow. Deployed and accessible at [URL]. Source code 
at github.com/Sudhish28/canvas-sop-generator.

The application works end to end. The collaboration was real. The AI 
usage is documented and traceable. And the output — when you run 
Jhansi's workflow through it — is something that would actually help 
a student navigate Canvas more effectively.

Thanks."

=======================================================================
END OF SCRIPT
=======================================================================


RECORDING TIPS:
- Don't read word-for-word. Use this as a guide, speak naturally.
- Demo sections: slow down and narrate what you're clicking.
- If the API call takes longer than 30s, say "the generation takes 
  about 25 seconds because we're making three real API calls" — 
  this actually HELPS your AI transparency score.
- Aim for 8-9 minutes. Under 10 is a hard requirement.
- Record in one take if possible. Small stumbles are fine — 
  professor cares about content, not production value.
