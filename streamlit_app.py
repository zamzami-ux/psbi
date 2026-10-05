import streamlit as st
from pathlib import Path

ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Projek-PSBI Preview", layout="wide")

st.title("Projek-PSBI — Streamlit Preview")

st.markdown(
    "A quick Streamlit-based preview helper for the Projek-PSBI repository. "
    "This does not replace the Django app — it only helps inspect templates and static files."
)

st.sidebar.header("Actions")
mode = st.sidebar.selectbox("Mode", ["About", "Templates", "Static files"])

if mode == "About":
    st.header("How to run the Django app locally")
    st.code("python -m venv .venv\n.venv\\Scripts\\activate  # Windows\npip install -r requirements.txt\npython manage.py migrate\npython manage.py runserver", language="bash")
    st.markdown("Or run this Streamlit preview with: `streamlit run streamlit_app.py`")

elif mode == "Templates":
    t_dir = ROOT / "dashboard" / "templates" / "dashboard"
    templates = sorted([p.relative_to(ROOT) for p in t_dir.glob("**/*.html")]) if t_dir.exists() else []
    if not templates:
        st.warning(f"No templates found in {t_dir}")
    else:
        sel = st.selectbox("Select template to preview", templates)
        path = ROOT / sel
        if path.exists():
            st.subheader(str(sel))
            st.code(path.read_text(encoding="utf-8"), language="html")

elif mode == "Static files":
    s_dir = ROOT / "dashboard" / "static" / "dashboard"
    files = sorted([p.relative_to(ROOT) for p in s_dir.rglob("*") if p.is_file()]) if s_dir.exists() else []
    if not files:
        st.warning(f"No static files found in {s_dir}")
    else:
        sel = st.selectbox("Select static file", files)
        path = ROOT / sel
        if path.exists():
            st.subheader(str(sel))
            if path.suffix in {".css", ".js", ".html"}:
                st.code(path.read_text(encoding="utf-8"), language="html")
            else:
                st.text(f"Binary or unsupported preview for {sel}")
