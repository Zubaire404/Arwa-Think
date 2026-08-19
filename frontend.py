import streamlit as st
import requests
import time

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Arwa Think",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
#  NEBULA GLASS THEME — Complete CSS Override
# ============================================================
st.markdown("""
<style>
/* ──────── Google Fonts ──────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ──────── Root Variables ──────── */
:root {
    --bg-void: #06080f;
    --bg-surface: #0d1117;
    --bg-card: rgba(255,255,255,0.03);
    --border-subtle: rgba(255,255,255,0.06);
    --border-glow: rgba(139,92,246,0.4);
    --text-primary: #f0f4f8;
    --text-secondary: #8b95a5;
    --accent-purple: #8b5cf6;
    --accent-cyan: #06b6d4;
    --accent-pink: #ec4899;
    --gradient-aurora: linear-gradient(135deg, #8b5cf6, #06b6d4, #8b5cf6);
    --glass-bg: rgba(13,17,23,0.7);
    --glass-border: rgba(255,255,255,0.08);
}

/* ──────── Global ──────── */
html, body, .stApp {
    background-color: var(--bg-void) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
}

/* Kill default Streamlit header/footer */
header[data-testid="stHeader"] { background: transparent !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
.stDeployButton { display: none !important; }

/* ──────── Sidebar (Model Settings) ──────── */
section[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem !important;
}

/* ──────── Chat Messages ──────── */
[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    backdrop-filter: blur(16px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    padding: 1.25rem 1.5rem !important;
    margin-bottom: 1rem !important;
    transition: border-color 0.4s ease, box-shadow 0.4s ease !important;
}
[data-testid="stChatMessage"]:hover {
    border-color: rgba(139,92,246,0.2) !important;
    box-shadow: 0 0 30px rgba(139,92,246,0.05) !important;
}

/* ──────── Chat Input ──────── */
[data-testid="stChatInput"] {
    border-top: 1px solid var(--border-subtle) !important;
    padding-top: 1rem !important;
}
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.8rem 1.2rem !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 3px rgba(6,182,212,0.15), 0 0 20px rgba(6,182,212,0.1) !important;
    outline: none !important;
}
[data-testid="stChatInput"] button {
    background: var(--gradient-aurora) !important;
    border: none !important;
    border-radius: 12px !important;
}

/* ──────── Radio buttons ──────── */
div[data-testid="stRadio"] label {
    color: var(--text-secondary) !important;
    font-size: 0.9rem !important;
}
div[data-testid="stRadio"] label[data-checked="true"],
div[data-testid="stRadio"] label:has(input:checked) {
    color: var(--accent-cyan) !important;
    font-weight: 600 !important;
}

/* ──────── Multiselect / Selectbox ──────── */
[data-testid="stMultiSelect"],
[data-testid="stSelectbox"] {
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stMultiSelect"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
}

/* ──────── Spinner ──────── */
.stSpinner > div > div {
    border-top-color: var(--accent-cyan) !important;
}

/* ──────── Dividers ──────── */
hr {
    border-color: var(--border-subtle) !important;
    opacity: 0.4 !important;
}

/* ──────── Custom Components ──────── */
.arwa-logo {
    font-size: 2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 50%, #ec4899 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin-bottom: 2px;
}
.arwa-subtitle {
    color: #64748b;
    font-size: 0.78rem;
    font-weight: 400;
    letter-spacing: 0.5px;
    margin-bottom: 1.2rem;
}

.model-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, rgba(139,92,246,0.12), rgba(6,182,212,0.12));
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 500;
    color: #c4b5fd;
    margin-bottom: 12px;
    backdrop-filter: blur(8px);
}
.model-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #06b6d4;
    display: inline-block;
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 0.4; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.2); }
}

.compare-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 16px;
    margin-top: 8px;
}
.compare-card-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--accent-cyan);
    margin-bottom: 8px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.sidebar-section-title {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #475569;
    margin-top: 1.2rem;
    margin-bottom: 0.5rem;
}

.warning-box {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.82rem;
    color: #fbbf24;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
#  MODEL CATALOG
# ============================================================
MODELS = {
    # ── THINK (Deep Reasoning) ──
    "DeepSeek V4 Pro":         {"key": "fw-deepseek-v4-pro", "tier": "think", "icon": "🧠", "ctx": "1M",  "desc": "Frontier reasoning model"},
    "Qwen 3.8 Max":            {"key": "fw-qwen3p8-max",     "tier": "think", "icon": "🧠", "ctx": "262k","desc": "Alibaba's most powerful"},
    "Kimi K3":                 {"key": "fw-kimi-k3",         "tier": "think", "icon": "🧠", "ctx": "1M",  "desc": "Moonshot's flagship"},
    "Muse Glimmer 30B":        {"key": "fw-muse-glimmer",    "tier": "think", "icon": "🧠", "ctx": "131k","desc": "Creative + Vision"},

    # ── MEDIUM (Balanced) ──
    "GLM 5.2":                 {"key": "fw-glm-5p2",         "tier": "medium","icon": "⚡", "ctx": "1M",  "desc": "Zhipu balanced LLM"},
    "Kimi K2.7 Code":          {"key": "fw-kimi-k2p7-code",  "tier": "medium","icon": "⚡", "ctx": "262k","desc": "Optimized for coding"},
    "Nemotron 3 Ultra":        {"key": "fw-nemotron-ultra",   "tier": "medium","icon": "⚡", "ctx": "262k","desc": "NVIDIA's balanced model"},
    "Inkling":                 {"key": "fw-inkling",          "tier": "medium","icon": "⚡", "ctx": "1M",  "desc": "Versatile all-rounder"},
    "Qwen 3.7 Plus":           {"key": "fw-qwen3p7-plus",    "tier": "medium","icon": "⚡", "ctx": "262k","desc": "Alibaba mid-tier + vision"},

    # ── FAST (Speed Priority) ──
    "DeepSeek V4 Flash":       {"key": "fw-deepseek-v4-flash","tier": "fast", "icon": "🚀", "ctx": "1M",  "desc": "Ultra-fast reasoning"},
    "Nemotron Lightning":      {"key": "fw-nemotron-light",   "tier": "fast", "icon": "🚀", "ctx": "262k","desc": "NVIDIA's fastest MoE"},
    "Minimax M3":              {"key": "fw-minimax-m3",       "tier": "fast", "icon": "🚀", "ctx": "512k","desc": "Lightweight & quick"},
    "GPT-OSS 120B":            {"key": "fw-gpt-oss-120b",    "tier": "fast", "icon": "🚀", "ctx": "131k","desc": "Open GPT architecture"},

    # ── GEMINI (Always available) ──
    "Gemini 3.6 Flash":        {"key": "gemini-3.6-flash",   "tier": "fast", "icon": "✨", "ctx": "1M",  "desc": "Google's fastest model"},
}

TIER_COLORS = {"think": "#8b5cf6", "medium": "#f59e0b", "fast": "#10b981"}
TIER_LABELS = {"think": "THINK", "medium": "MEDIUM", "fast": "FAST"}

# ============================================================
#  SIDEBAR — Model Settings
# ============================================================
with st.sidebar:
    st.markdown("<div class='arwa-logo'>Arwa Think</div>", unsafe_allow_html=True)
    st.markdown("<div class='arwa-subtitle'>MULTI-MODEL AI ENGINE</div>", unsafe_allow_html=True)
    st.divider()

    # Mode Selector
    st.markdown("<div class='sidebar-section-title'>Routing Mode</div>", unsafe_allow_html=True)
    routing_mode = st.radio(
        "mode_radio",
        ["Auto", "One Think", "One Fast", "Multi-Model"],
        label_visibility="collapsed",
        horizontal=False
    )

    manual_models = []

    if routing_mode == "One Think":
        st.markdown("<div class='sidebar-section-title'>Select Think Model</div>", unsafe_allow_html=True)
        think_names = [n for n, m in MODELS.items() if m["tier"] == "think"]
        selected = st.selectbox("think_select", think_names, label_visibility="collapsed")
        manual_models = [MODELS[selected]["key"]]

    elif routing_mode == "One Fast":
        st.markdown("<div class='sidebar-section-title'>Select Fast Model</div>", unsafe_allow_html=True)
        fast_names = [n for n, m in MODELS.items() if m["tier"] == "fast"]
        selected = st.selectbox("fast_select", fast_names, label_visibility="collapsed")
        manual_models = [MODELS[selected]["key"]]

    elif routing_mode == "Multi-Model":
        st.markdown("<div class='sidebar-section-title'>Select Models (max 8)</div>", unsafe_allow_html=True)

        # Group by tier with formatted labels
        for tier_key, tier_label in [("think", "🧠 Think"), ("medium", "⚡ Medium"), ("fast", "🚀 Fast")]:
            st.markdown(f"<div style='font-size:0.78rem;color:{TIER_COLORS[tier_key]};font-weight:700;margin:12px 0 4px;'>{tier_label}</div>", unsafe_allow_html=True)
            tier_models = {n: m for n, m in MODELS.items() if m["tier"] == tier_key}
            for name, info in tier_models.items():
                checked = st.checkbox(
                    f"{name}  ·  {info['ctx']}",
                    key=f"cb_{info['key']}",
                    value=(name in ["DeepSeek V4 Flash", "Gemini 3.6 Flash"])
                )
                if checked:
                    manual_models.append(info["key"])

        if len(manual_models) > 8:
            manual_models = manual_models[:8]
            st.error("Maximum 8 models allowed.")
        elif len(manual_models) > 4:
            st.markdown(
                "<div class='warning-box'>⚠️ More than 4 models selected — responses may be slower as all run in parallel.</div>",
                unsafe_allow_html=True
            )

    st.divider()
    st.markdown(f"<div style='font-size:0.72rem;color:#475569;text-align:center;'>Mode: {routing_mode}  ·  {len(manual_models) if manual_models else 'Auto'} model(s)</div>", unsafe_allow_html=True)


# ============================================================
#  MAIN CHAT AREA
# ============================================================

# Initialize
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm **Arwa Think** — your multi-model AI assistant.\n\nChoose a routing mode from the sidebar, then ask me anything.",
        "drafts": [],
        "models_used": [],
        "category": ""
    }]

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg.get("models_used"):
            labels = [m.split("/")[-1] if "/" in m else m for m in msg["models_used"]]
            badge_text = " · ".join(labels)
            st.markdown(f"<div class='model-badge'><span class='dot'></span>{badge_text} — {msg.get('category','')}</div>", unsafe_allow_html=True)

        st.markdown(msg["content"])

        drafts = msg.get("drafts", [])
        if len(drafts) > 1 and "Multi" in routing_mode:
            st.markdown("---")
            st.markdown("**📊 Individual Model Outputs:**")
            cols = st.columns(min(len(drafts), 3))
            for i, d in enumerate(drafts):
                with cols[i % min(len(drafts), 3)]:
                    st.markdown(f"<div class='compare-card'><div class='compare-card-title'>{d['label']}</div></div>", unsafe_allow_html=True)
                    st.markdown(d["text"][:600] + ("..." if len(d.get("text","")) > 600 else ""))

# Chat input
if prompt := st.chat_input("Ask Arwa Think anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "drafts": [], "models_used": [], "category": ""})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking across models..."):
            try:
                res = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={
                        "prompt": prompt,
                        "auto_route": routing_mode == "Auto",
                        "manual_models": manual_models
                    },
                    timeout=90
                )

                if res.status_code == 200:
                    data = res.json()
                    answer = data["final_answer"]
                    drafts = data.get("drafts", [])
                    models_used = data["models_used"]
                    category = data["category"]

                    labels = models_used
                    badge_text = " · ".join(labels)
                    st.markdown(f"<div class='model-badge'><span class='dot'></span>{badge_text} — {category}</div>", unsafe_allow_html=True)

                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "drafts": drafts,
                        "models_used": models_used,
                        "category": category
                    })

                    if len(drafts) > 1 and "Multi" in routing_mode:
                        st.markdown("---")
                        st.markdown("**📊 Individual Model Outputs:**")
                        cols = st.columns(min(len(drafts), 3))
                        for i, d in enumerate(drafts):
                            with cols[i % min(len(drafts), 3)]:
                                st.markdown(f"<div class='compare-card'><div class='compare-card-title'>{d['label']}</div></div>", unsafe_allow_html=True)
                                st.markdown(d["text"][:600] + ("..." if len(d.get("text","")) > 600 else ""))
                else:
                    error_detail = res.json().get("detail", res.text) if res.headers.get("content-type","").startswith("application/json") else res.text
                    st.error(f"⚠️ {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("Cannot reach Arwa Think backend. Make sure the server is running on port 8000.")
            except requests.exceptions.Timeout:
                st.error("Request timed out. The models are taking too long — try selecting fewer models.")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")