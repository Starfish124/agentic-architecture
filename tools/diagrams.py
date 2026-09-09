"""Build every diagram in diagrams/ from one source of truth."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from skin import (ACCENT, MUTED, SOFT, arrow, band, caption, diamond, dot, drop,
                  elbow, node, note, oval, write, zone)

OUT = Path(__file__).resolve().parent.parent / "diagrams"
OUT.mkdir(exist_ok=True)
made = []


def emit(slug, **kw):
    write(OUT / f"{slug}.html", slug, **kw)
    made.append(slug)


def raw(d, colour=MUTED, w=1.2, dash="", marker="arrow"):
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{w}"{dd} '
            f'marker-end="url(#{marker})"/>')


# ---------------------------------------------------------------- 1. GT-Code
b = [
    zone(200, 96, 200, 264, "LOCAL INFERENCE"),
    zone(424, 80, 656, 288, "AGENT"),
    arrow(160, 160, 220, 160, label="PROMPT", ly=152),
    arrow(300, 192, 300, 244),
    arrow(376, 160, 444, 160, "accent", label="RUN", ly=152),
    arrow(624, 160, 676, 160, "accent"),
    arrow(816, 160, 868, 160, label="ALLOW", ly=152),
    arrow(536, 208, 536, 264),
    node(40, 128, 120, 64, "You", "any folder", "input"),
    node(224, 128, 152, 64, "Router", "resident 1.5B", "backend"),
    node(224, 248, 152, 88, "", kind="store", tag="MODELS",
         lines=["tiny  1.5b", "fast  8b", "brain 14b"]),
    node(448, 112, 176, 96, "Agent loop", "plan · execute · verify", "focal"),
    node(680, 112, 136, 96, "Permission", "yes / always / no", "security"),
    node(872, 112, 184, 96, "Tools", "files · shell · office", "backend", tag="LOCAL"),
    node(448, 272, 176, 72, "Memory", "sqlite + embeddings", "store"),
    caption(300, 354, "routes by cost, not size", "middle", SOFT, 8.5),
    caption(756, 228, "denied → nothing runs", "middle", ACCENT, 8.5),
    caption(636, 308, "recall · remember", size=8.5),
    note(40, 400, "Ollama on localhost is the only server. No API key, no telemetry, "
                  "no update check; web tools ship off, so the default is air-gapped."),
]
emit("gt-code-architecture", eyebrow="Architecture · GT-Code",
     heading="A coding agent that never leaves the machine",
     title="GT-Code architecture", width=1120, height=440, body="\n".join(b),
     desc="Prompt enters a router on a resident 1.5B model, which picks from a three-model "
          "local ladder and runs an agent loop; every tool call passes a permission gate.")

# ------------------------------------------------------- 2. GT-Code lifecycle
b = [
    arrow(480, 80, 480, 128),
    raw("M 340,184 H 164 Q 156,184 156,192 V 292"),
    arrow(480, 236, 480, 292),
    drop(620, 184, 804, 292),
    raw("M 156,360 V 392 Q 156,400 164,400 H 472"),
    arrow(480, 360, 480, 396),
    raw("M 804,360 V 392 Q 804,400 796,400 H 488"),
    arrow(480, 404, 480, 436),
    arrow(480, 504, 480, 528),
    arrow(620, 584, 700, 584, "accent", label="ALLOW", ly=576),
    arrow(480, 636, 480, 676, label="DENY", ly=664),
    arrow(280, 584, 336, 584, "accent"),
    raw("M 804,552 V 480 Q 804,472 796,472 H 600", MUTED, 1, "4,3"),
    caption(618, 460, "next step", colour=SOFT, size=8.5),
    caption(240, 176, "LOW", "end", MUTED, 8),
    caption(496, 268, "MEDIUM", colour=MUTED, size=8),
    caption(720, 176, "HIGH", colour=MUTED, size=8),
    oval(360, 32, 240, 48, "A new build request"),
    diamond(480, 184, 280, 104, "How many readings?", "confidence gate"),
    node(56, 296, 200, 64, "Ask one question", kind="backend"),
    node(380, 296, 200, 64, "Present the plan", kind="backend"),
    node(704, 296, 200, 64, "Build now", kind="backend"),
    dot(480, 400),
    node(368, 440, 224, 64, "Propose a tool call", kind="backend"),
    node(56, 552, 224, 64, "Destructive command", "rm -rf · format · push -f", "security"),
    diamond(480, 584, 280, 104, "Permission", "yes / always / no", "focal"),
    node(704, 552, 200, 64, "Run it, then verify", kind="backend"),
    oval(360, 680, 240, 48, "Nothing runs"),
    note(56, 780, "The gate is code, not instruction: a standing grant or /auto skips the "
                  "prompt, and the destructive-command check overrides both."),
]
emit("gt-code-lifecycle", eyebrow="Flowchart · GT-Code",
     heading="Where the agent is allowed to stop and ask",
     title="GT-Code request lifecycle", width=960, height=816, body="\n".join(b),
     desc="A build request is scored for confidence, routing to a question, a plan or an "
          "immediate build; every tool call then passes a permission decision.")

# -------------------------------------------------------------- 3. GT Assure
b = [
    zone(192, 32, 672, 336, "GT ASSURE · ONE PROCESS"),
    arrow(168, 208, 212, 208),
    drop(368, 208, 512, 168),
    drop(368, 208, 512, 240),
    arrow(608, 116, 660, 116, "accent", label="LLM", ly=108),
    arrow(608, 292, 660, 292, label="R/W", ly=284),
    arrow(840, 292, 884, 292),
    arrow(976, 336, 976, 380, "accent"),
    node(40, 176, 128, 64, "Browser", "no build step", "input"),
    node(216, 176, 152, 64, "FastAPI", "backend/main.py", "backend"),
    node(416, 64, 192, 104, "", kind="backend",
         lines=["control", "sample", "walkthrough", "pbc"]),
    node(416, 240, 192, 104, "", kind="backend",
         lines=["ingest · index", "sampling", "workpaper", "audit"]),
    node(664, 64, 176, 104, "Ollama", "generation + embeddings", "store"),
    node(664, 240, 176, 104, "engagements/<id>", "evidence · index · audit", "store"),
    node(888, 248, 176, 88, "Named reviewer", "approves, or it stays draft", "security"),
    node(888, 384, 176, 72, "Workpaper .xlsx", "CONCEPT until approved", "external"),
    caption(512, 56, "AGENTS", "middle", SOFT, 8),
    caption(512, 360, "SERVICES", "middle", SOFT, 8),
    node(0, 0, 0, 0, "", kind="external") if False else "",
    note(40, 440, "One folder holds everything about one client. The call to Ollama on "
                  "localhost is the only network call in the system."),
]
emit("gt-assure-architecture", eyebrow="Architecture · GT Assure",
     heading="Control testing with the judgement left in",
     title="GT Assure architecture", width=1120, height=480, body="\n".join(b),
     desc="A browser drives a local FastAPI app whose agents call Ollama and whose services "
          "read and write one per-engagement folder; a named reviewer gates every export.")

# ---------------------------------------------------- 4. GT Assure per-control
b = [
    arrow(480, 80, 480, 132),
    arrow(480, 200, 480, 244),
    arrow(480, 312, 480, 336),
    raw("M 344,384 H 192 Q 184,384 184,392 V 436"),
    arrow(480, 432, 480, 476),
    arrow(480, 544, 480, 588),
    arrow(480, 656, 480, 700),
    caption(264, 376, "NOTHING", "middle", ACCENT, 8),
    caption(496, 460, "EVIDENCE FOUND", colour=MUTED, size=8),
    oval(360, 32, 240, 48, "One control"),
    node(344, 136, 272, 64, "Expected-evidence profile", "criteria + probes", "backend", tag="MODEL"),
    node(344, 248, 272, 64, "Retrieve whole documents", "merge on best distance", "backend", tag="CODE"),
    diamond(480, 384, 272, 96, "Anything retrieved?"),
    node(48, 436, 272, 64, "Insufficient evidence", "second call never happens", "security"),
    node(344, 480, 272, 64, "Assess against criteria", "must cite the excerpts", "backend", tag="MODEL"),
    node(344, 592, 272, 64, "Drop citations out of range", "uncited → not evidenced", "focal", tag="CODE"),
    oval(336, 700, 288, 48, "Draft finding + audit entry"),
    note(56, 792, "A control with no evidence in front of the model is where fabrication "
                  "starts, so that branch never reaches the model at all."),
]
emit("gt-assure-control", eyebrow="Flowchart · GT Assure",
     heading="What the model decides, and what code decides",
     title="GT Assure per-control pipeline", width=960, height=816, body="\n".join(b),
     desc="Per control: a model drafts acceptance criteria, code retrieves documents, and "
          "an empty retrieval short-circuits before the second model call.")

# ------------------------------------------------------------ 5. GT Proposal
b = [
    zone(208, 88, 504, 144, "THE MODEL PROPOSES"),
    zone(208, 304, 760, 144, "CODE DECIDES"),
    drop(184, 264, 328, 208),
    arrow(328, 208, 328, 332, label="SELECTED", ly=300),
    elbow(424, 380, 504, 164),
    arrow(600, 208, 600, 332),
    arrow(696, 380, 756, 380, label="PASS", ly=372),
    arrow(852, 336, 852, 212, "accent"),
    node(40, 228, 144, 72, "The brief", "one opportunity", "input"),
    node(232, 120, 192, 88, "Select comparables", "no fee, no hours shown", "backend"),
    node(504, 120, 192, 88, "Draft six sections", "only from comparables", "backend"),
    node(232, 336, 192, 88, "Qualify + price", "median · range · rate", "backend"),
    node(504, 336, 192, 88, "Three interlocks", "names · citations · figures", "focal"),
    node(760, 336, 184, 88, "Approval", "refuses, never warns", "security"),
    node(760, 120, 184, 88, "Proposal + estimate", "with its provenance", "external"),
    caption(866, 276, "approved", colour=ACCENT, size=8.5),
    note(40, 492, "The model is never shown a fee or an hour count when it selects. Every "
                  "number in the estimate is computed by code from recorded actuals."),
]
emit("gt-proposal-architecture", eyebrow="Architecture · GT Proposal",
     heading="The model selects; the code counts",
     title="GT Proposal architecture", width=1008, height=520, body="\n".join(b),
     desc="A brief routes through model-side comparable selection and drafting, with "
          "qualification, pricing, interlocks and approval all computed in code.")

# -------------------------------------------- 6. GT Proposal confidentiality
b = [
    arrow(416, 80, 416, 124),
    arrow(416, 184, 416, 232),
    arrow(416, 328, 416, 392),
    arrow(416, 488, 416, 552),
    arrow(416, 648, 416, 700),
    raw("M 552,280 H 780 Q 788,280 788,288 V 388", ACCENT, 1.4, marker="arrow-accent"),
    caption(620, 272, "FOUND", "middle", ACCENT, 8),
    arrow(552, 440, 664, 440, "accent", label="NONE", ly=432),
    raw("M 552,600 H 780 Q 788,600 788,592 V 492", ACCENT, 1.4, marker="arrow-accent"),
    caption(620, 592, "FOUND", "middle", ACCENT, 8),
    caption(432, 372, "CLEAN", colour=MUTED, size=8),
    caption(432, 532, "CITED", colour=MUTED, size=8),
    caption(432, 692, "TRACEABLE", colour=MUTED, size=8),
    oval(304, 32, 224, 48, "A drafted section"),
    node(296, 128, 240, 56, "Strip citation tags", "they carry the old name", "backend", tag="CODE"),
    diamond(416, 280, 272, 96, "A past client name?", "full · legal · short form"),
    diamond(416, 440, 272, 96, "Any citation at all?", "attribution check"),
    diamond(416, 600, 272, 96, "A figure from nowhere?", "not in brief or extract"),
    node(664, 392, 248, 96, "Approval refused", "not a warning — refused", "security"),
    oval(304, 704, 224, 48, "Approvable"),
    note(56, 792, "Matching is exact on purpose. A similarity threshold is a dial for how "
                  "often a confidentiality check fails quietly."),
]
emit("gt-proposal-interlocks", eyebrow="Flowchart · GT Proposal",
     heading="Three things that stand between a draft and a filed proposal",
     title="GT Proposal interlocks", width=960, height=816, body="\n".join(b),
     desc="A drafted section passes a client-name check, an attribution check and a "
          "foreign-figure check; any hit refuses approval outright.")

# ---------------------------------------------------- 7. Glassbox layer stack
rows = [
    ("L1", "Models", "lane router — confidential cannot reach the cloud", False),
    ("L2", "Orchestration", "audited loop · pipeline · fan-out · evaluator · router", False),
    ("L3", "Tools", "JSON schema + capability-scoped permissions", False),
    ("L4", "Knowledge", "chunking · embedders · vector store · citations · memory", False),
    ("L5", "Guardrails", "injection scan in · BSN / IBAN / PII redaction out", False),
    ("L6", "Governance", "hash-chained audit · KYA registry · approval gates", True),
    ("L7", "Evals", "a case fails if the answer OR the chain fails", False),
]
b = [caption(112, 96, "nearest the model", "end", SOFT, 8.5),
     caption(112, 560, "nearest the auditor", "end", SOFT, 8.5),
     raw("M 104,112 V 540", SOFT, 1)]
y = 88
for i, (idx, name, sub, focal) in enumerate(rows):
    b.append(band(152, y, 808, 64, idx, name, sub, focal))
    y += 72
b.append(note(152, 624, "Every layer above is importable Python; the console is a window "
                        "onto the same objects, not a second implementation."))
emit("glassbox-layers", eyebrow="Layer stack · glassbox-agents",
     heading="Seven layers, and the governance plane is the product",
     title="Glassbox agents layer stack", width=1000, height=664, body="\n".join(b),
     desc="Seven platform layers from model routing up to the evaluation gate, with the "
          "governance layer highlighted.")

# ------------------------------------------------------------- 8. Two lanes
b = [
    arrow(184, 268, 228, 268),
    raw("M 280,216 V 104 Q 280,96 288,96 H 512"),
    arrow(416, 268, 512, 268, "accent", label="PINNED", ly=260),
    raw("M 368,320 V 368 Q 368,376 376,376 H 512"),
    raw("M 728,96 H 916 Q 924,96 924,104 V 208"),
    arrow(728, 268, 820, 268, label="LOGGED", ly=260),
    raw("M 728,376 H 916 Q 924,376 924,368 V 328"),
    caption(400, 88, "CONFIDENTIAL", "middle", MUTED, 8),
    caption(444, 368, "PUBLIC", "middle", MUTED, 8),
    node(40, 232, 144, 72, "A task", "+ sensitivity", "input"),
    node(232, 216, 184, 104, "LaneRouter", "sensitivity → lane", "focal"),
    node(520, 48, 208, 96, "Local lane", "vLLM · Ollama · your box", "backend"),
    node(520, 232, 208, 72, "LaneViolation", "raises — no fallback", "security"),
    node(520, 328, 208, 96, "Cloud lane", "PII redacted on the way out", "external"),
    node(824, 216, 200, 104, "Hash-chained audit", "verify() fails on any edit", "store"),
    note(40, 464, "A structural control, not a policy document: the router raises rather "
                  "than quietly downgrading a confidential task onto a cloud endpoint."),
]
emit("glassbox-lanes", eyebrow="Architecture · glassbox-agents",
     heading="Confidential work cannot reach the cloud lane",
     title="Glassbox two-lane routing", width=1064, height=496, body="\n".join(b),
     desc="A task carries a sensitivity label; the lane router sends it local, sends it "
          "cloud, or raises a LaneViolation, and every outcome is appended to the audit chain.")

# ---------------------------------------------------------- 9. Delivery stack
b = [
    zone(328, 8, 344, 264, "AUTHOR"),
    zone(40, 408, 272, 272, "MEASURE"),
    zone(688, 408, 272, 272, "SHIP"),
    arrow(500, 120, 500, 164),
    arrow(500, 248, 500, 292),
    raw("M 352,344 H 184 Q 176,344 176,352 V 436"),
    drop(648, 344, 824, 436),
    arrow(176, 564, 176, 532),
    arrow(824, 528, 824, 564, label="PULL", ly=556),
    raw("M 824,656 V 728 Q 824,736 816,736 H 652"),
    node(376, 40, 248, 80, "Claude Code sessions", "one per system", "backend"),
    node(376, 168, 248, 80, "Vibe Kanban", "parallel agent worktrees", "backend"),
    node(352, 296, 296, 96, "The repository", "code · tests · layers.json · ADRs", "focal"),
    node(64, 440, 224, 88, "Control room", "layers · boundaries · chains", "backend"),
    node(64, 568, 224, 88, "xyOps", "schedules · stores · alerts", "backend"),
    node(712, 440, 224, 88, "GitHub", "the only shared surface", "backend"),
    node(712, 568, 224, 88, "GT Windows laptop", "pac CLI, tenant auth", "backend"),
    node(352, 696, 296, 80, "Copilot Studio · Dataverse", "the tenant", "external"),
    caption(192, 552, "runs the checks", colour=SOFT, size=8.5),
    caption(200, 428, "reads the repo, not a slide", colour=SOFT, size=8.5),
    caption(672, 724, "push · publish", colour=SOFT, size=8.5),
    note(40, 812, "The Mac has no tenant access, so authoring and deployment are physically "
                  "separated and GitHub is the only thing that crosses."),
]
emit("delivery-stack", eyebrow="Architecture · how I ship",
     heading="How an agent gets from a prompt to a tenant",
     title="Agent delivery stack", width=1000, height=840, body="\n".join(b),
     desc="Claude Code sessions run in parallel Vibe Kanban worktrees onto one repository, "
          "which a control room measures on an xyOps schedule and which GitHub carries to a "
          "Windows laptop for deployment into the Microsoft tenant.")

# ------------------------------------------------------------ 10. Guardrails
rows = [
    ("00", "The system prompt", "the only layer that can be argued with", True),
    ("01", "Retrieval boundary", "approved sources only; nothing found → no call", False),
    ("02", "Capability scope", "which tools exist for this agent at all", False),
    ("03", "Deterministic interlocks", "uncited claim downgraded · invented reference dropped", False),
    ("04", "Human approval", "unapproved work cannot leave the tool", False),
    ("05", "Audit", "append-only, hash-chained, independently verifiable", False),
    ("06", "Evaluation gate", "answer and chain must both pass before release", False),
]
b = [caption(112, 96, "prompt", "end", ACCENT, 8.5),
     caption(112, 560, "code", "end", SOFT, 8.5),
     raw("M 104,112 V 540", SOFT, 1)]
y = 88
for idx, name, sub, focal in rows:
    b.append(band(152, y, 808, 64, idx, name, sub, focal))
    y += 72
b.append(note(152, 624, "A prompt can describe the behaviour I want. It cannot enforce a "
                        "permission, prove what happened, or refuse on my behalf."))
emit("guardrails", eyebrow="Layer stack · guardrails",
     heading="Prompt engineering is layer zero, not the guardrail",
     title="Guardrail layers", width=1000, height=664, body="\n".join(b),
     desc="Seven guardrail layers from the system prompt down to the evaluation gate, with "
          "the prompt layer marked as the only persuadable one.")

# ------------------------------------------------------- 11. Test levels
rows = [
    ("00", "No tenant, every PR", "interlocks · mocked connectors · frozen corpus", False),
    ("01", "No tenant, nightly", "golden set × N runs · pass rate · chain verifies", True),
    ("02", "Test environment", "connectors · permissions · one real path per agent", False),
    ("03", "Deployment environment", "smoke only — never where something is first discovered", False),
]
b = [caption(112, 96, "cheap, constant", "end", SOFT, 8.5),
     caption(112, 344, "costly, rare", "end", SOFT, 8.5),
     raw("M 104,112 V 324", SOFT, 1)]
y = 88
for idx, name, sub, focal in rows:
    b.append(band(152, y, 808, 64, idx, name, sub, focal))
    y += 72
b.append(note(152, 408, "Level 01 is the one that does not exist yet, and the one that decides "
                        "whether any of the rest is a gate or a ritual."))
emit("test-levels", eyebrow="Layer stack · evaluation",
     heading="Where an agent gets tested, and what each level catches",
     title="Agent test levels", width=1000, height=448, body="\n".join(b),
     desc="Four test levels from interlock unit tests with no tenant on every pull request, "
          "through a nightly golden-set run gated on pass rate, to smoke tests in the "
          "deployment environment.")

# ------------------------------------------------------ 12. Current stack
rows = [
    ("07", "Delivery", "GitHub → pac CLI on the tenant laptop → Copilot Studio · Dataverse", False),
    ("06", "Operations", "xyOps schedules · control room measures layers.json · Tailscale", False),
    ("05", "Governance", "hash-chained audit · capability scope · approval gates · boundaries", True),
    ("04", "Applications", "GT-Code · GT Assure · GT Proposal · IH Pilot · forensics agent", False),
    ("03", "Orchestration", "glassbox patterns · Copilot Studio topics · Power Automate · MCP", False),
    ("02", "Retrieval", "Chroma · SQLite + nomic-embed · literal lookup · per-engagement index", False),
    ("01", "Inference", "Ollama — qwen3 14b / 8b · qwen2.5 3b / 1.5b · nomic-embed, Apache-2.0", False),
    ("00", "Machines", "Mac mini, sovereign · Windows laptop, tenant · nothing shared but git", False),
]
b = [caption(112, 96, "abstraction", "end", SOFT, 8.5),
     caption(112, 640, "hardware", "end", SOFT, 8.5),
     raw("M 104,112 V 620", SOFT, 1)]
y = 88
for idx, name, sub, focal in rows:
    b.append(band(152, y, 808, 60, idx, name, sub, focal))
    y += 68
b.append(note(152, 700, "Layers 00–02 are deliberately boring and interchangeable. Layer 05 is "
                        "the one that is not bought in, and the one every agent inherits."))
emit("current-stack", eyebrow="Layer stack · what I run today",
     heading="The stack as it stands",
     title="Current stack", width=1000, height=744, body="\n".join(b),
     desc="Eight layers of the stack in use today, from the two machines at the bottom through "
          "local inference, retrieval, orchestration and the applications, to the governance "
          "plane and the delivery path into the Microsoft tenant.")

# ------------------------------------------------------- 13. Eval harness
b = [
    zone(296, 48, 272, 384, "RUNNERS"),
    elbow(240, 244, 316, 124, mid=280),
    arrow(240, 244, 316, 244),
    elbow(240, 244, 316, 364, mid=280),
    raw("M 544,124 H 580 Q 588,124 588,132 V 234"),
    arrow(544, 244, 584, 244),
    raw("M 544,364 H 580 Q 588,364 588,356 V 254"),
    dot(588, 244),
    arrow(592, 244, 628, 244),
    arrow(840, 244, 892, 244, label="RESULT", ly=236),
    arrow(736, 312, 736, 364),
    raw("M 840,412 H 980 Q 988,412 988,404 V 316"),
    node(40, 176, 200, 136, "", kind="focal", tag="GOLDEN SET",
         lines=["retrieval", "correctness", "refusal", "injection"]),
    node(320, 80, 224, 88, "pytest", "the interlocks", "backend"),
    node(320, 200, 224, 88, "deepeval", "component metrics", "backend"),
    node(320, 320, 224, 88, "promptfoo", "the gate matrix", "backend"),
    node(632, 176, 208, 136, "", kind="backend",
         lines=["interlock code", "the agent", "pinned + fixtures"]),
    node(632, 368, 208, 88, "Judge model", "local, calibrated", "security"),
    node(896, 176, 184, 136, "", kind="store",
         lines=["pass rate", "per release", "exit code"]),
    caption(752, 344, "LLM-graded metrics only", size=8.5),
    caption(736, 164, "SYSTEM UNDER TEST", "middle", SOFT, 8),
    caption(988, 164, "RESULTS", "middle", SOFT, 8),
    note(40, 496, "The golden set is data in the repo, not configuration inside a tool — so the "
                  "same cases feed all three runners. xyOps schedules the run and keeps the trend."),
]
emit("eval-harness", eyebrow="Architecture · evaluation",
     heading="One golden set, three runners, one judge",
     title="Eval harness", width=1120, height=536, body="\n".join(b),
     desc="A golden set of cases in the repository drives pytest for interlocks, deepeval for "
          "component metrics and promptfoo for the gate matrix, against a pinned system under "
          "test, with a local judge model grading only the LLM-graded metrics.")

print(f"{len(made)} diagrams -> {OUT}")
for m in made:
    print("  ", m)
