import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Projek-PSBI App", layout="wide")

st.title("Projek-PSBI — Streamlit App")

st.markdown(
    "This Streamlit app renders the project's HTML templates so it can run directly on Streamlit Cloud or any Streamlit host. "
    "Note: dynamic Django functionality (views, context processors, auth) is not executed — templates are shown as static HTML."
)

st.sidebar.header("Navigation")
mode = st.sidebar.selectbox("Mode", ["Home", "Interactive", "Templates", "Static files"]) 

if mode == "Home":
    st.header("How to run")
    st.markdown("Run locally with `streamlit run app.py` or deploy to Streamlit Cloud (set main file to `app.py`).")

elif mode == "Interactive":
    import requests
    st.header("Interactive via Django API")
    
    # Try to read backend URL from Streamlit secrets (for Cloud deployment)
    default_backend = st.secrets.get("backend_url", "http://localhost:8000")
    backend = st.text_input('Backend base URL', default_backend)
    username = st.text_input('Username (existing Django user)')

    if backend and username:
        try:
            resp = requests.get(f"{backend}/api/missions/")
            resp.raise_for_status()
            missions = resp.json()
        except Exception as e:
            st.error(f"Cannot fetch missions: {e}")
            missions = []

        if missions:
            m_titles = [f"{m['id']}: {m['title']}" for m in missions]
            sel = st.selectbox('Mission', m_titles)
            mid = int(sel.split(':', 1)[0])
            try:
                mresp = requests.get(f"{backend}/api/missions/{mid}/")
                mresp.raise_for_status()
                mission = mresp.json()
                st.subheader(mission['title'])
                st.markdown(mission.get('content', ''))
                for q in mission.get('questions', []):
                    st.write(q['text'])
                    choice_map = {c['id']: c['text'] for c in q.get('choices', [])}
                    selected = st.radio(f"Question {q['id']}", list(choice_map.values()), key=f"q{q['id']}")
                    # map selected text back to id
                    selected_id = None
                    for cid, txt in choice_map.items():
                        if txt == selected:
                            selected_id = cid
                    if st.button('Submit answer', key=f"submit{q['id']}"):
                        try:
                            post = requests.post(f"{backend}/api/submit_answer/", json={
                                'username': username,
                                'question_id': q['id'],
                                'choice_id': selected_id
                            })
                            post.raise_for_status()
                            st.success(post.json())
                        except Exception as e:
                            st.error(f"Submit failed: {e}")
            except Exception as e:
                st.error(f"Cannot fetch mission detail: {e}")

    else:
        st.info('Provide backend URL and username to use interactive mode')

elif mode == "Templates":
    t_dir = ROOT / "dashboard" / "templates" / "dashboard"
    templates = sorted([p for p in t_dir.glob("**/*.html")]) if t_dir.exists() else []
    if not templates:
        st.warning(f"No templates found in {t_dir}")
    else:
        names = [str(p.relative_to(ROOT)) for p in templates]
        sel = st.selectbox("Select template to render", names)
        path = ROOT / sel
        if path.exists():
            html = path.read_text(encoding="utf-8")
            st.subheader(sel)
            # Render the HTML; this will not execute Django template tags but will display static HTML
            components.html(html, height=800, scrolling=True)

elif mode == "Static files":
    s_dir = ROOT / "dashboard" / "static" / "dashboard"
    files = sorted([p for p in s_dir.rglob("*") if p.is_file()]) if s_dir.exists() else []
    if not files:
        st.warning(f"No static files found in {s_dir}")
    else:
        names = [str(p.relative_to(ROOT)) for p in files]
        sel = st.selectbox("Select static file", names)
        path = ROOT / sel
        if path.exists():
            if path.suffix in {".html", ".css", ".js"}:
                st.code(path.read_text(encoding="utf-8"), language="html")
            else:
                st.text("Binary or unsupported file preview")
