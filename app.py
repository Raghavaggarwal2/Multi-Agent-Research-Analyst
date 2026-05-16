import streamlit as st
import time
from pipeline import run_research_pipeline

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lumina Research",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=DM+Mono:wght@300;400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0a0c10;
    color: #e8e6e1;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 4rem; max-width: 1100px; }

/* ── Hero header ── */
.lumina-header {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.lumina-header::before {
    content: '';
    position: absolute;
    top: 0; left: 50%; transform: translateX(-50%);
    width: 1px; height: 40px;
    background: linear-gradient(to bottom, transparent, #c9a96e);
}
.lumina-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 4rem;
    font-weight: 300;
    letter-spacing: 0.12em;
    color: #f0ece4;
    margin: 0;
    line-height: 1;
}
.lumina-title span {
    color: #c9a96e;
    font-style: italic;
}
.lumina-tagline {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.3em;
    color: #6b7280;
    text-transform: uppercase;
    margin-top: 0.8rem;
}
.lumina-divider {
    width: 80px;
    height: 1px;
    background: linear-gradient(to right, transparent, #c9a96e, transparent);
    margin: 1.5rem auto 0;
}

/* ── Search bar ── */
.stTextInput > div > div {
    background: #12151c !important;
    border: 1px solid #2a2d35 !important;
    border-radius: 2px !important;
    color: #e8e6e1 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.8rem 1.2rem !important;
    transition: border-color 0.25s ease;
}
.stTextInput > div > div:focus-within {
    border-color: #c9a96e !important;
    box-shadow: 0 0 0 1px #c9a96e22 !important;
}
.stTextInput label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #6b7280 !important;
}

/* ── Button ── */
.stButton > button {
    background: #c9a96e !important;
    color: #0a0c10 !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
    font-weight: 400 !important;
    padding: 0.75rem 2.5rem !important;
    cursor: pointer !important;
    transition: background 0.2s ease, transform 0.1s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #e0be85 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Step pipeline ── */
.pipeline-track {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 2.5rem 0 2rem;
    padding: 0 1rem;
}
.step-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.45rem;
    flex: 1;
    position: relative;
}
.step-icon {
    width: 46px; height: 46px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    border: 1.5px solid #2a2d35;
    background: #12151c;
    color: #4b5563;
    transition: all 0.4s ease;
    position: relative;
    z-index: 2;
}
.step-icon.active {
    border-color: #c9a96e;
    color: #c9a96e;
    box-shadow: 0 0 18px #c9a96e33;
    background: #1a1710;
}
.step-icon.done {
    border-color: #4ade80;
    color: #4ade80;
    background: #0f1a12;
    box-shadow: 0 0 12px #4ade8022;
}
.step-icon.error {
    border-color: #f87171;
    color: #f87171;
    background: #1a0f0f;
}
.step-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #4b5563;
    text-align: center;
}
.step-label.active { color: #c9a96e; }
.step-label.done { color: #4ade80; }
.step-connector {
    flex: 0.6;
    height: 1px;
    background: #2a2d35;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.step-connector::after {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(to right, transparent, #c9a96e, transparent);
    animation: none;
}
.step-connector.flowing::after {
    animation: flow 1.5s ease-in-out infinite;
}
@keyframes flow {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* ── Loading card ── */
.loading-card {
    background: #0f1117;
    border: 1px solid #1e2128;
    border-left: 2px solid #c9a96e;
    border-radius: 2px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.loading-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #c9a96e;
    animation: pulse 1.2s ease-in-out infinite;
    flex-shrink: 0;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.3; transform: scale(0.7); }
}
.loading-text {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #9ca3af;
    letter-spacing: 0.05em;
}

/* ── Result cards ── */
.result-card {
    background: #0f1117;
    border: 1px solid #1e2128;
    border-radius: 2px;
    margin: 1.2rem 0;
    overflow: hidden;
}
.result-card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.85rem 1.3rem;
    background: #12151c;
    border-bottom: 1px solid #1e2128;
}
.result-card-icon { font-size: 0.9rem; }
.result-card-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #9ca3af;
    flex: 1;
}
.result-card-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    color: #4ade80;
    background: #0f1a12;
    border: 1px solid #1a3a1a;
    padding: 0.15rem 0.5rem;
    border-radius: 1px;
}
.result-card-body {
    padding: 1.3rem 1.5rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    line-height: 1.75;
    color: #c9c5be;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 380px;
    overflow-y: auto;
}
.result-card-body::-webkit-scrollbar { width: 4px; }
.result-card-body::-webkit-scrollbar-track { background: #0f1117; }
.result-card-body::-webkit-scrollbar-thumb { background: #2a2d35; border-radius: 2px; }

/* ── Final report ── */
.report-card {
    background: #0c0f14;
    border: 1px solid #c9a96e33;
    border-top: 2px solid #c9a96e;
    border-radius: 2px;
    margin: 1.5rem 0;
    overflow: hidden;
}
.report-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.5rem;
    background: #0f1117;
    border-bottom: 1px solid #c9a96e22;
}
.report-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #c9a96e;
    font-weight: 400;
}
.report-body {
    padding: 2rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.92rem;
    line-height: 1.85;
    color: #d6d2cb;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 520px;
    overflow-y: auto;
}
.report-body::-webkit-scrollbar { width: 4px; }
.report-body::-webkit-scrollbar-track { background: #0c0f14; }
.report-body::-webkit-scrollbar-thumb { background: #c9a96e44; border-radius: 2px; }

/* ── Critique card ── */
.critique-card {
    background: #0c0e14;
    border: 1px solid #6366f133;
    border-left: 2px solid #818cf8;
    border-radius: 2px;
    margin: 1.2rem 0;
    overflow: hidden;
}
.critique-header {
    padding: 0.85rem 1.3rem;
    background: #0f1117;
    border-bottom: 1px solid #6366f122;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #818cf8;
}
.critique-body {
    padding: 1.3rem 1.5rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    line-height: 1.75;
    color: #c9c5be;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 380px;
    overflow-y: auto;
}
.critique-body::-webkit-scrollbar { width: 4px; }
.critique-body::-webkit-scrollbar-track { background: #0c0e14; }
.critique-body::-webkit-scrollbar-thumb { background: #818cf844; border-radius: 2px; }

/* ── Complete banner ── */
.complete-banner {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, #0f1a12, #0c0f14, #0f1117);
    border: 1px solid #4ade8033;
    border-radius: 2px;
    margin: 1.5rem 0;
}
.complete-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.complete-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    font-weight: 300;
    color: #4ade80;
    letter-spacing: 0.1em;
    margin: 0.2rem 0;
}
.complete-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    color: #4b5563;
    text-transform: uppercase;
}

/* ── Error banner ── */
.error-banner {
    background: #1a0f0f;
    border: 1px solid #f8717133;
    border-left: 2px solid #f87171;
    border-radius: 2px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: #f87171;
    letter-spacing: 0.05em;
}

/* ── Footer ── */
.lumina-footer {
    text-align: center;
    padding: 3rem 0 1rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.25em;
    color: #374151;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ─── Helper: render HTML safely ─────────────────────────────────────────────
def html(content: str):
    st.markdown(content, unsafe_allow_html=True)


# ─── Pipeline wrapper that yields progress ──────────────────────────────────
def run_pipeline_with_ui(topic: str):
    """
    Runs the full pipeline and streams results back via
    Streamlit placeholders. Preserves all original logic.
    """
    steps = ["search", "reader", "writer", "critic"]
    icons = ["🔍", "📄", "✍️", "🔬"]
    labels = ["Search", "Read", "Write", "Critique"]
    status = {s: "idle" for s in steps}

    # ── Pipeline track ──────────────────────────────────────────────────────
    track_ph = st.empty()

    def render_track():
        nodes_html = ""
        for i, (s, icon, label) in enumerate(zip(steps, icons, labels)):
            st_cls = status[s]
            nodes_html += f'<div class="step-node"><div class="step-icon {st_cls}">{icon}</div><div class="step-label {st_cls}">{label}</div></div>'
            if i < len(steps) - 1:
                flowing = "flowing" if st_cls == "active" else ""
                nodes_html += f'<div class="step-connector {flowing}"></div>'
        track_ph.markdown(f'<div class="pipeline-track">{nodes_html}</div>', unsafe_allow_html=True)

    render_track()

    state = {}

    # ── SEARCH ──────────────────────────────────────────────────────────────
    status["search"] = "active"
    render_track()

    search_ph = st.empty()
    loading_msgs = [
        "Dispatching search agent across the web…",
        "Scanning scholarly sources and live feeds…",
        "Ranking credibility of retrieved documents…",
        "Assembling the intelligence snapshot…",
    ]
    for i, msg in enumerate(loading_msgs):
        search_ph.markdown(
            f'<div class="loading-card"><div class="loading-dot"></div>'
            f'<div class="loading-text">{msg}</div></div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.5)

    try:
        from agents import build_search_agent
        search_agent = build_search_agent()
        search_result_raw = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable, detailed and relevant information on the topic: {topic}")]
        })
        state["search_result"] = search_result_raw["messages"][-1].content
    except Exception as e:
        search_ph.markdown(f'<div class="error-banner">⚠ Search agent failed: {e}</div>', unsafe_allow_html=True)
        status["search"] = "error"
        render_track()
        return state

    search_ph.empty()
    status["search"] = "done"
    render_track()

    with st.expander("🔍 Search Intelligence (Click to expand)", expanded=False):
        st.markdown(f'```\n{state["search_result"]}\n```')

    # ── READER ──────────────────────────────────────────────────────────────
    status["reader"] = "active"
    render_track()

    reader_ph = st.empty()
    loading_msgs = [
        "Identifying the 2 most relevant URLs from results…",
        "Opening pages and extracting full content…",
        "Parsing and distilling key information…",
        "Synthesising deep reading notes…",
    ]
    for msg in loading_msgs:
        reader_ph.markdown(
            f'<div class="loading-card"><div class="loading-dot"></div>'
            f'<div class="loading-text">{msg}</div></div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.5)

    try:
        from agents import build_reader_agent
        reader_agent = build_reader_agent()
        reader_result_raw = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about: {topic}, "
                f"pick the 2 most relevant URLs from the search results and scrape both for deeper and detailed information.\n\n"
                f"Search Results:\n{state['search_result']}"
            )]
        })
        state["reader_result"] = reader_result_raw["messages"][-1].content
    except Exception as e:
        reader_ph.markdown(f'<div class="error-banner">⚠ Reader agent failed: {e}</div>', unsafe_allow_html=True)
        status["reader"] = "error"
        render_track()
        return state

    reader_ph.empty()
    status["reader"] = "done"
    render_track()

    with st.expander("📄 Deep Read Extraction (Click to expand)", expanded=False):
        st.markdown(f'```\n{state["reader_result"]}\n```')

    # ── WRITER ──────────────────────────────────────────────────────────────
    status["writer"] = "active"
    render_track()

    writer_ph = st.empty()
    loading_msgs = [
        "Merging search intelligence with deep reading…",
        "Structuring narrative flow and sections…",
        "Composing the research report…",
        "Refining prose and citations…",
    ]
    for msg in loading_msgs:
        writer_ph.markdown(
            f'<div class="loading-card"><div class="loading-dot"></div>'
            f'<div class="loading-text">{msg}</div></div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.5)

    try:
        from agents import writer_chain
        research_combined = (
            f"Search Results:\n{state['search_result']}\n\n"
            f"Deep Reading:\n{state['reader_result']}"
        )
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
        })
    except Exception as e:
        writer_ph.markdown(f'<div class="error-banner">⚠ Writer chain failed: {e}</div>', unsafe_allow_html=True)
        status["writer"] = "error"
        render_track()
        return state

    writer_ph.empty()
    status["writer"] = "done"
    render_track()

    html(
        f'<div class="report-card">'
        f'<div class="report-header"><span>📋</span>'
        f'<span class="report-title">Generated Research Report</span></div>'
        f'<div class="report-body">{state["report"]}</div>'
        f'</div>'
    )

    # Download button for the report
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download Report as Text",
            data=state["report"],
            file_name=f"research_report_{topic[:30].replace(' ', '_')}.txt",
            mime="text/plain",
        )

    # ── CRITIC ──────────────────────────────────────────────────────────────
    status["critic"] = "active"
    render_track()

    critic_ph = st.empty()
    loading_msgs = [
        "Engaging the critic lens on the report…",
        "Evaluating factual accuracy and gaps…",
        "Checking structure, depth, and objectivity…",
        "Formulating constructive critique…",
    ]
    for msg in loading_msgs:
        critic_ph.markdown(
            f'<div class="loading-card"><div class="loading-dot"></div>'
            f'<div class="loading-text">{msg}</div></div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.5)

    try:
        from agents import critic_chain
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
    except Exception as e:
        critic_ph.markdown(f'<div class="error-banner">⚠ Critic chain failed: {e}</div>', unsafe_allow_html=True)
        status["critic"] = "error"
        render_track()
        return state

    critic_ph.empty()
    status["critic"] = "done"
    render_track()

    html(
        f'<div class="critique-card">'
        f'<div class="critique-header">🔬 &nbsp; Expert Critique & Feedback</div>'
        f'<div class="critique-body">{state["feedback"]}</div>'
        f'</div>'
    )

    # ── Complete ─────────────────────────────────────────────────────────────
    html(
        '<div class="complete-banner">'
        '<div class="complete-icon">✦</div>'
        '<div class="complete-title">Research Complete</div>'
        '<div class="complete-sub">All pipeline stages executed successfully</div>'
        '</div>'
    )

    return state


# ─── App Layout ─────────────────────────────────────────────────────────────
html("""
<div class="lumina-header">
    <h1 class="lumina-title">LUMINA<span> Research</span></h1>
    <p class="lumina-tagline">AI-Powered Deep Research Intelligence</p>
    <div class="lumina-divider"></div>
</div>
""")

_, col, _ = st.columns([1, 2.5, 1])
with col:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025…",
        label_visibility="visible",
    )
    run_btn = st.button("Begin Research")

st.markdown("<br>", unsafe_allow_html=True)

if run_btn:
    if not topic.strip():
        html('<div class="error-banner">⚠ Please enter a research topic to continue.</div>')
    else:
        html(f"""
        <div style="text-align:center; margin: 0.5rem 0 1.5rem;">
            <span style="font-family:'DM Mono',monospace; font-size:0.68rem;
                         letter-spacing:0.2em; color:#6b7280; text-transform:uppercase;">
                Researching &nbsp;/&nbsp;
            </span>
            <span style="font-family:'Cormorant Garamond',serif; font-size:1.1rem;
                         color:#c9a96e; font-style:italic;">
                {topic}
            </span>
        </div>
        """)
        run_pipeline_with_ui(topic)

html('<div class="lumina-footer">Lumina Research &nbsp;·&nbsp; Powered by AI Agents</div>')