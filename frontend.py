import streamlit as st
import requests
import uuid
from datetime import datetime, timedelta

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(page_title="Arwa Think", layout="wide", initial_sidebar_state="expanded")

# ============================================================
#  PHASE 1 — Color Tokens, Typography, & Full CSS
#  PHASE 2 — Convergence Spine + Badge
#  PHASE 3 — Gathering Animation
#  PHASE 5 — Constellation Welcome Screen
#  PHASE 6 — Glass, Grain, Gold Focus, Pill Selector
# ============================================================
st.markdown("""
<style>
/* ─── Fonts ─── */
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ─── Color Tokens: Signal & Void ─── */
:root {
    --void: #07070c;
    --deep-current: #0f0d1c;
    --ash: #1c1a2b;
    --mist: #e7e5ef;
    --fog: #7d7a94;
    --signal-gold: #e8c468;

    --hue-violet: #9b7ede;
    --hue-cyan: #5eb8c9;
    --hue-coral: #ef8354;
    --hue-rose: #e37fa0;
    --hue-sage: #8fbf8a;
    --hue-amber: #e0b04f;
}

/* ─── Global Reset ─── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
    background-color: var(--void) !important;
    color: var(--mist) !important;
}
.stApp {
    background-color: var(--void) !important;
}

/* ─── Noise Grain Overlay ─── */
.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    opacity: 0.03;
    pointer-events: none;
    z-index: 1;
    mix-blend-mode: overlay;
}

/* ─── Hide Default UI ─── */
header[data-testid="stHeader"] { background: transparent !important; }
footer, #MainMenu, .stDeployButton, [data-testid="collapsedControl"] { display: none !important; }

/* ════════════════════════════════════════════════════════════
   SIDEBAR — Frosted Glass Pane
   ════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: rgba(15, 13, 28, 0.78) !important;
    backdrop-filter: blur(24px) saturate(140%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(140%) !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

/* Sidebar branding */
.sidebar-brand {
    font-family: 'Fraunces', serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--signal-gold);
    padding: 1.2rem 1rem 0.3rem;
    letter-spacing: -0.5px;
}
.sidebar-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: var(--fog);
    text-transform: uppercase;
    letter-spacing: 2px;
    padding: 0 1rem 1.2rem;
}

/* New Chat button */
[data-testid="stSidebar"] button[kind="primary"] {
    background: var(--ash) !important;
    color: var(--mist) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    transition: background 0.15s, border-color 0.15s !important;
}
[data-testid="stSidebar"] button[kind="primary"]:hover {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.15) !important;
}

/* History labels */
.history-group {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--fog);
    padding: 20px 16px 6px;
    opacity: 0.7;
}

/* History items (styled via Streamlit buttons) */
[data-testid="stSidebar"] button[kind="secondary"] {
    background: transparent !important;
    color: var(--fog) !important;
    border: none !important;
    border-radius: 6px !important;
    text-align: left !important;
    font-size: 0.82rem !important;
    padding: 6px 12px !important;
    transition: all 0.15s !important;
    font-weight: 400 !important;
    justify-content: flex-start !important;
}
[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.04) !important;
    color: var(--mist) !important;
}

/* ════════════════════════════════════════════════════════════
   MODEL SELECTOR — Pill Segmented Toggle
   ════════════════════════════════════════════════════════════ */
.model-selector-row {
    max-width: 780px;
    margin: 0 auto;
    padding: 0.8rem 1rem 0.4rem;
}

/* Style st.radio as pills */
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 3px !important;
    background: var(--ash) !important;
    border-radius: 10px !important;
    padding: 3px !important;
    width: fit-content !important;
}
div[data-testid="stRadio"] > div > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    color: var(--fog) !important;
    border-radius: 7px !important;
    padding: 6px 18px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    margin: 0 !important;
    white-space: nowrap !important;
    border: none !important;
    background: transparent !important;
}
div[data-testid="stRadio"] > div > label:hover {
    color: var(--mist) !important;
    background: rgba(255,255,255,0.03) !important;
}
div[data-testid="stRadio"] > div > label[data-checked="true"],
div[data-testid="stRadio"] > div label:has(input:checked) {
    background: var(--deep-current) !important;
    color: var(--mist) !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3) !important;
}
/* Hide radio circles */
div[data-testid="stRadio"] > div > label > div:first-child {
    display: none !important;
}

/* Custom model chips */
.model-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--fog);
    background: var(--ash);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 6px;
    padding: 3px 10px;
    margin: 2px 3px 2px 0;
}
.model-chip .chip-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* ════════════════════════════════════════════════════════════
   CHAT MESSAGES
   ════════════════════════════════════════════════════════════ */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 1.8rem 1rem !important;
    margin: 0 !important;
    max-width: 800px;
    margin-left: auto !important;
    margin-right: auto !important;
    position: relative !important;
}

/* Avatars */
[data-testid="stChatMessageAvatar"] {
    background: var(--deep-current) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.75rem !important;
    color: var(--fog) !important;
}

/* ─── CONVERGENCE SPINE ─── */
.spine {
    width: 3px;
    border-radius: 2px;
    min-height: 40px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
}
.spine::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, rgba(255,255,255,0.3), transparent, rgba(255,255,255,0.3));
    background-size: 100% 200%;
    animation: spine-shimmer 3s ease-in-out infinite;
    opacity: 0;
}
.spine.settled::after {
    opacity: 0;
    animation: none;
}
@keyframes spine-shimmer {
    0% { background-position: 0 0; }
    50% { background-position: 0 100%; }
    100% { background-position: 0 0; }
}

/* ─── SYNTH BADGE (colored dots + mono label) ─── */
.synth-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 10px;
}
.synth-badge .dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
}
.synth-badge .badge-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    color: var(--fog);
    letter-spacing: 0.3px;
}

/* ════════════════════════════════════════════════════════════
   GATHERING ANIMATION (replaces spinner)
   ════════════════════════════════════════════════════════════ */
.gathering {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 0;
}
.gather-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    animation: gather 1.6s ease-in-out infinite;
    animation-delay: var(--delay, 0s);
}
@keyframes gather {
    0% { transform: translateX(var(--offset, 0px)) scale(0.7); opacity: 0.3; }
    50% { transform: translateX(0) scale(1); opacity: 1; }
    100% { transform: translateX(var(--offset, 0px)) scale(0.7); opacity: 0.3; }
}
.gathering .gather-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--fog);
    letter-spacing: 0.5px;
    animation: gather-text 1.6s ease-in-out infinite;
}
@keyframes gather-text {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
}

/* prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
    .gather-dot, .gathering .gather-label { animation: none !important; opacity: 0.7; transform: none; }
    .constellation-node { animation: none !important; }
    .spine::after { animation: none !important; }
}

/* ════════════════════════════════════════════════════════════
   COUNCIL VIEW — Draft Cards (Phase 4)
   ════════════════════════════════════════════════════════════ */
[data-testid="stExpander"] {
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    background: transparent !important;
    margin-top: 1rem !important;
}
[data-testid="stExpander"] summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: var(--fog) !important;
    letter-spacing: 0.3px !important;
}
[data-testid="stExpander"] summary:hover {
    color: var(--mist) !important;
}
.draft-card {
    background: var(--deep-current);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 1rem 1rem 1rem 1rem;
    font-size: 0.84rem;
    color: var(--fog);
    line-height: 1.65;
    position: relative;
    overflow: hidden;
}
.draft-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--card-hue, var(--fog));
    border-radius: 8px 8px 0 0;
}
.draft-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--mist);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.7rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex;
    align-items: center;
    gap: 6px;
}
.draft-label .label-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* ════════════════════════════════════════════════════════════
   WELCOME SCREEN — The Constellation
   ════════════════════════════════════════════════════════════ */
.welcome-container {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 55vh;
    text-align: center;
    overflow: hidden;
}
.constellation-field {
    position: absolute;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
}
.constellation-node {
    position: absolute;
    border-radius: 50%;
    opacity: 0.06;
    filter: blur(1px);
    animation: drift var(--dur, 20s) ease-in-out infinite alternate;
}
@keyframes drift {
    0% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(var(--dx1, 15px), var(--dy1, -10px)) scale(1.1); }
    66% { transform: translate(var(--dx2, -10px), var(--dy2, 20px)) scale(0.95); }
    100% { transform: translate(var(--dx3, 5px), var(--dy3, -15px)) scale(1.05); }
}

.welcome-title {
    font-family: 'Fraunces', serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: var(--mist);
    margin-bottom: 0.6rem;
    position: relative;
    z-index: 2;
    letter-spacing: -1px;
}
.welcome-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: var(--fog);
    margin-bottom: 2.5rem;
    max-width: 460px;
    line-height: 1.6;
    position: relative;
    z-index: 2;
}
.prompt-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    max-width: 520px;
    width: 100%;
    position: relative;
    z-index: 2;
}
.prompt-card {
    background: var(--deep-current);
    border: 1px solid rgba(255,255,255,0.05);
    border-top: 2px solid var(--card-hue, var(--fog));
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 0.84rem;
    color: var(--fog);
    text-align: left;
    line-height: 1.5;
    transition: all 0.2s;
}
.prompt-card:hover {
    background: var(--ash);
    border-color: rgba(255,255,255,0.1);
    color: var(--mist);
}

/* ════════════════════════════════════════════════════════════
   CHAT INPUT — Frosted Glass, Gold Focus
   ════════════════════════════════════════════════════════════ */
[data-testid="stChatInput"] {
    background: transparent !important;
    padding-bottom: 1.5rem !important;
}
[data-testid="stChatInput"] > div {
    max-width: 800px;
    margin: 0 auto;
    background: rgba(28, 26, 43, 0.7) !important;
    backdrop-filter: blur(16px) saturate(120%) !important;
    -webkit-backdrop-filter: blur(16px) saturate(120%) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 16px !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--mist) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(232, 196, 104, 0.4) !important;
    box-shadow: 0 0 0 2px rgba(232, 196, 104, 0.15) !important;
    outline: none !important;
}

/* Focus ring on all interactive elements */
*:focus-visible {
    outline: 2px solid rgba(232, 196, 104, 0.4) !important;
    outline-offset: 2px !important;
}

/* ─── Selectbox / Multiselect theming ─── */
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label { display: none !important; }
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stMultiSelect"] > div > div {
    background-color: var(--ash) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 8px !important;
    color: var(--mist) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
#  MODEL CATALOG + HUE MAPPING
# ============================================================
MODELS = {
    "DeepSeek V4 Pro":    {"key": "fw-deepseek-v4-pro",   "tier": "think"},
    "Qwen 3.8 Max":       {"key": "fw-qwen3p8-max",       "tier": "think"},
    "Kimi K3":            {"key": "fw-kimi-k3",            "tier": "think"},
    "Muse Glimmer 30B":   {"key": "fw-muse-glimmer",       "tier": "think"},
    "GLM 5.2":            {"key": "fw-glm-5p2",            "tier": "medium"},
    "Kimi K2.7 Code":     {"key": "fw-kimi-k2p7-code",     "tier": "medium"},
    "Nemotron 3 Ultra":   {"key": "fw-nemotron-ultra",      "tier": "medium"},
    "Inkling":            {"key": "fw-inkling",             "tier": "medium"},
    "Qwen 3.7 Plus":      {"key": "fw-qwen3p7-plus",       "tier": "medium"},
    "DeepSeek V4 Flash":  {"key": "fw-deepseek-v4-flash",   "tier": "fast"},
    "Nemotron Lightning": {"key": "fw-nemotron-light",       "tier": "fast"},
    "Minimax M3":         {"key": "fw-minimax-m3",           "tier": "fast"},
    "GPT-OSS 120B":       {"key": "fw-gpt-oss-120b",        "tier": "fast"},
    "Gemini 3.6 Flash":   {"key": "gemini-3.6-flash",       "tier": "fast"},
}

# Each model gets a fixed hue — this IS the visual grammar
MODEL_HUES = {
    "DeepSeek V4 Pro":    "#9b7ede",  # Violet
    "Qwen 3.8 Max":       "#5eb8c9",  # Cyan
    "Kimi K3":            "#e37fa0",  # Rose
    "Muse Glimmer 30B":   "#e0b04f",  # Amber
    "GLM 5.2":            "#8fbf8a",  # Sage
    "Kimi K2.7 Code":     "#9b7ede",  # Violet
    "Nemotron 3 Ultra":   "#ef8354",  # Coral
    "Inkling":            "#8fbf8a",  # Sage
    "Qwen 3.7 Plus":      "#5eb8c9",  # Cyan
    "DeepSeek V4 Flash":  "#ef8354",  # Coral
    "Nemotron Lightning":  "#ef8354",  # Coral
    "Minimax M3":         "#e0b04f",  # Amber
    "GPT-OSS 120B":       "#8fbf8a",  # Sage
    "Gemini 3.6 Flash":   "#5eb8c9",  # Cyan
}

DEFAULT_HUE = "#7d7a94"
THINK_KEYS = [m["key"] for m in MODELS.values() if m["tier"] == "think"]


def get_hues_for_models(model_labels):
    """Return list of hex colors for the given model labels."""
    return [MODEL_HUES.get(m, DEFAULT_HUE) for m in model_labels]


def build_spine_gradient(hues):
    """Build a CSS gradient string from a list of hues."""
    if len(hues) == 0:
        return DEFAULT_HUE
    if len(hues) == 1:
        return hues[0]
    return f"linear-gradient(to bottom, {', '.join(hues)})"


def build_gathering_html(model_labels):
    """Build the animated Gathering dots HTML."""
    hues = get_hues_for_models(model_labels)
    if not hues:
        hues = ["#9b7ede", "#5eb8c9", "#ef8354"]
    offsets = [-30, -15, 0, 15, 30]
    dots = ""
    for i, h in enumerate(hues[:5]):
        offset = offsets[i % len(offsets)]
        delay = i * 0.15
        dots += f'<span class="gather-dot" style="background:{h}; --delay:{delay}s; --offset:{offset}px;"></span>'
    return f"""
    <div class="gathering">
        {dots}
        <span class="gather-label">Gathering</span>
    </div>
    """


# ============================================================
#  SESSION STATE
# ============================================================
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
if "active_id" not in st.session_state:
    st.session_state.active_id = None
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


def new_conversation():
    cid = str(uuid.uuid4())[:8]
    st.session_state.conversations[cid] = {
        "title": "New conversation",
        "messages": [],
        "created": datetime.now(),
    }
    st.session_state.active_id = cid
    st.session_state.pending_prompt = None
    return cid


def get_active_messages():
    cid = st.session_state.active_id
    if cid and cid in st.session_state.conversations:
        return st.session_state.conversations[cid]["messages"]
    return []


def group_conversations():
    now = datetime.now()
    today, yesterday = now.date(), now.date() - timedelta(days=1)
    week_ago = now.date() - timedelta(days=7)
    groups = {"Today": [], "Yesterday": [], "Previous 7 Days": [], "Older": []}
    for cid, conv in sorted(st.session_state.conversations.items(), key=lambda x: x[1]["created"], reverse=True):
        d = conv["created"].date()
        if d == today:
            groups["Today"].append((cid, conv))
        elif d == yesterday:
            groups["Yesterday"].append((cid, conv))
        elif d >= week_ago:
            groups["Previous 7 Days"].append((cid, conv))
        else:
            groups["Older"].append((cid, conv))
    return groups


# ============================================================
#  SIDEBAR — Conversations
# ============================================================
with st.sidebar:
    st.markdown("<div class='sidebar-brand'>Arwa Think</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-sub'>Multi-model convergence</div>", unsafe_allow_html=True)

    if st.button("+ New conversation", use_container_width=True, type="primary", key="new_chat"):
        new_conversation()
        st.rerun()

    groups = group_conversations()
    for group_name, items in groups.items():
        if not items:
            continue
        st.markdown(f"<div class='history-group'>{group_name}</div>", unsafe_allow_html=True)
        for cid, conv in items:
            if st.button(conv["title"], key=f"h_{cid}", use_container_width=True, type="secondary"):
                st.session_state.active_id = cid
                st.session_state.pending_prompt = None
                st.rerun()


# ============================================================
#  MODEL SELECTOR — Pill Segmented Toggle
# ============================================================
st.markdown("<div class='model-selector-row'>", unsafe_allow_html=True)

mode = st.radio(
    "Routing",
    ["Auto", "Think", "Fast", "Custom"],
    horizontal=True,
    label_visibility="collapsed",
    key="routing_mode",
)

manual_models = []

if mode == "Think":
    manual_models = THINK_KEYS
    think_names = [n for n, m in MODELS.items() if m["tier"] == "think"]
    chips = "".join(
        f'<span class="model-chip"><span class="chip-dot" style="background:{MODEL_HUES[n]}"></span>{n}</span>'
        for n in think_names
    )
    st.markdown(chips, unsafe_allow_html=True)

elif mode == "Fast":
    fast_names = [n for n, m in MODELS.items() if m["tier"] == "fast"]
    sel = st.selectbox("_", fast_names, label_visibility="collapsed", key="fast_sel")
    manual_models = [MODELS[sel]["key"]]

elif mode == "Custom":
    sel_names = st.multiselect("_", list(MODELS.keys()), label_visibility="collapsed", key="custom_sel", max_selections=8)
    manual_models = [MODELS[n]["key"] for n in sel_names]
    if sel_names:
        chips = "".join(
            f'<span class="model-chip"><span class="chip-dot" style="background:{MODEL_HUES[n]}"></span>{n}</span>'
            for n in sel_names
        )
        st.markdown(chips, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
#  MAIN CHAT AREA
# ============================================================
messages = get_active_messages()

# ── Welcome / Constellation ──
if not messages and st.session_state.pending_prompt is None:
    st.markdown("""
    <div class="welcome-container">
        <div class="constellation-field">
            <div class="constellation-node" style="width:90px;height:90px;background:#9b7ede;left:12%;top:20%;--dur:22s;--dx1:20px;--dy1:-15px;--dx2:-12px;--dy2:25px;--dx3:8px;--dy3:-10px;"></div>
            <div class="constellation-node" style="width:70px;height:70px;background:#5eb8c9;right:18%;top:15%;--dur:26s;--dx1:-15px;--dy1:12px;--dx2:18px;--dy2:-8px;--dx3:-5px;--dy3:20px;"></div>
            <div class="constellation-node" style="width:110px;height:110px;background:#ef8354;left:60%;bottom:25%;--dur:30s;--dx1:10px;--dy1:18px;--dx2:-20px;--dy2:-12px;--dx3:15px;--dy3:5px;"></div>
            <div class="constellation-node" style="width:60px;height:60px;background:#e37fa0;left:25%;bottom:30%;--dur:18s;--dx1:-8px;--dy1:-20px;--dx2:15px;--dy2:10px;--dx3:-12px;--dy3:-5px;"></div>
            <div class="constellation-node" style="width:80px;height:80px;background:#8fbf8a;right:30%;top:50%;--dur:24s;--dx1:12px;--dy1:8px;--dx2:-18px;--dy2:-15px;--dx3:5px;--dy3:12px;"></div>
            <div class="constellation-node" style="width:50px;height:50px;background:#e0b04f;left:45%;top:10%;--dur:20s;--dx1:-10px;--dy1:15px;--dx2:8px;--dy2:-18px;--dx3:-5px;--dy3:8px;"></div>
            <div class="constellation-node" style="width:100px;height:100px;background:#9b7ede;right:10%;bottom:15%;--dur:28s;--dx1:18px;--dy1:-12px;--dx2:-10px;--dy2:20px;--dx3:8px;--dy3:-8px;"></div>
            <div class="constellation-node" style="width:65px;height:65px;background:#5eb8c9;left:8%;top:55%;--dur:19s;--dx1:-12px;--dy1:10px;--dx2:15px;--dy2:-5px;--dx3:-8px;--dy3:18px;"></div>
        </div>
        <div class="welcome-title">What can I help with?</div>
        <div class="welcome-sub">
            Several minds, one voice. Select a routing mode and ask anything.
        </div>
        <div class="prompt-grid">
            <div class="prompt-card" style="--card-hue:#9b7ede;">Explain how transformers work in deep learning</div>
            <div class="prompt-card" style="--card-hue:#5eb8c9;">Write a Python function to merge two sorted lists</div>
            <div class="prompt-card" style="--card-hue:#ef8354;">Compare REST vs GraphQL for a new project</div>
            <div class="prompt-card" style="--card-hue:#e37fa0;">Summarize the key breakthroughs in AI this year</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Render Message History ──
for msg in messages:
    with st.chat_message(msg["role"]):

        if msg["role"] == "assistant" and msg.get("models_used"):
            hues = get_hues_for_models(msg["models_used"])
            spine_bg = build_spine_gradient(hues)

            # Spine
            if len(hues) == 1:
                st.markdown(f'<div class="spine settled" style="background:{spine_bg};"></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="spine settled" style="background:{spine_bg};"></div>', unsafe_allow_html=True)

            # Badge with colored dots
            dots = "".join(f'<span class="dot" style="background:{h}"></span>' for h in hues)
            count = len(msg["models_used"])
            label = f"Synthesized from {count} models" if count > 1 else msg["models_used"][0]
            st.markdown(f'<div class="synth-badge">{dots}<span class="badge-text">{label}</span></div>', unsafe_allow_html=True)

        # Content
        st.markdown(msg["content"])

        # Council View — Draft Cards with colored top edges
        drafts = msg.get("drafts", [])
        if len(drafts) > 1:
            with st.expander("View council  /  individual AI drafts"):
                cols = st.columns(min(len(drafts), 3))
                for i, d in enumerate(drafts):
                    with cols[i % min(len(drafts), 3)]:
                        hue = MODEL_HUES.get(d["label"], DEFAULT_HUE)
                        preview = d["text"][:600] + ("..." if len(d["text"]) > 600 else "")
                        st.markdown(
                            f'<div class="draft-card" style="--card-hue:{hue};">'
                            f'<div class="draft-label"><span class="label-dot" style="background:{hue}"></span>{d["label"]}</div>'
                            f'{preview}</div>',
                            unsafe_allow_html=True,
                        )


# ── Process Pending Prompt (Gathering → Response) ──
if st.session_state.pending_prompt is not None:
    prompt = st.session_state.pending_prompt
    cid = st.session_state.active_id

    with st.chat_message("assistant"):
        # Show Gathering animation
        if mode == "Auto":
            gathering_labels = ["DeepSeek V4 Pro", "Gemini 3.6 Flash", "Qwen 3.8 Max"]
        elif mode == "Think":
            gathering_labels = [n for n, m in MODELS.items() if m["tier"] == "think"]
        elif mode == "Custom":
            gathering_labels = [n for n in (st.session_state.get("custom_sel") or []) ]
        else:
            fast_name = st.session_state.get("fast_sel", "Gemini 3.6 Flash")
            gathering_labels = [fast_name]

        placeholder = st.empty()
        placeholder.markdown(build_gathering_html(gathering_labels), unsafe_allow_html=True)

        try:
            res = requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "prompt": prompt,
                    "auto_route": mode == "Auto",
                    "manual_models": manual_models,
                },
                timeout=120,
            )
            placeholder.empty()

            if res.status_code == 200:
                data = res.json()
                st.session_state.conversations[cid]["messages"].append({
                    "role": "assistant",
                    "content": data["final_answer"],
                    "drafts": data.get("drafts", []),
                    "models_used": data["models_used"],
                    "category": data["category"],
                })
            else:
                err = res.text
                try:
                    err = res.json().get("detail", err)
                except Exception:
                    pass
                st.session_state.conversations[cid]["messages"].append({
                    "role": "assistant", "content": f"Error: {err}",
                    "drafts": [], "models_used": [], "category": "",
                })

        except requests.exceptions.ConnectionError:
            placeholder.empty()
            st.session_state.conversations[cid]["messages"].append({
                "role": "assistant",
                "content": "Cannot reach the backend. Ensure Uvicorn is running on port 8000.",
                "drafts": [], "models_used": [], "category": "",
            })
        except requests.exceptions.Timeout:
            placeholder.empty()
            st.session_state.conversations[cid]["messages"].append({
                "role": "assistant",
                "content": "Request timed out. Try fewer models or a simpler prompt.",
                "drafts": [], "models_used": [], "category": "",
            })
        except Exception as e:
            placeholder.empty()
            st.session_state.conversations[cid]["messages"].append({
                "role": "assistant", "content": f"Error: {str(e)}",
                "drafts": [], "models_used": [], "category": "",
            })

    st.session_state.pending_prompt = None
    st.rerun()


# ============================================================
#  CHAT INPUT — Pinned Bottom (Top-Level Scope)
# ============================================================
if prompt := st.chat_input("Message Arwa Think..."):
    if st.session_state.active_id is None or st.session_state.active_id not in st.session_state.conversations:
        new_conversation()

    cid = st.session_state.active_id

    if not st.session_state.conversations[cid]["messages"]:
        st.session_state.conversations[cid]["title"] = prompt[:42] + ("..." if len(prompt) > 42 else "")

    st.session_state.conversations[cid]["messages"].append({
        "role": "user", "content": prompt,
        "drafts": [], "models_used": [], "category": "",
    })

    st.session_state.pending_prompt = prompt
    st.rerun()