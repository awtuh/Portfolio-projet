import streamlit as st
import os
import importlib.util
import sys

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Portfolio Projets Financiers",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import local modules
from utils import load_css, card_component

# Load Custom CSS
load_css("assets/styles.css")

def load_project_module(module_name):
    """Dynamically load a project module."""
    try:
        # Assuming projects are in the 'projects' folder
        # and the file name matches the module name
        file_path = os.path.join("projects", f"{module_name}.py")
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.error(f"Erreur lors du chargement du module {module_name}: {e}")
        return None

def main():
    # Session State for Navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'selected_project' not in st.session_state:
        st.session_state.selected_project = None

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Portfolio Projets Financiers</h1>
        <p style="text-align: center; font-size: 1.2em; margin-top: -10px;">
            Créé par <a href="https://www.linkedin.com/in/arthur-duval-9b627815b/" target="_blank" style="color: #00f2ff; text-decoration: none;">Arthur Duval</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Logic
    if st.session_state.current_page == 'home':
        render_dashboard()
    else:
        render_project_page()

def render_dashboard():
    st.markdown("""
    <div class="intro-text">
        <h3>Bienvenue sur mon Portfolio</h3>
        <p>Chaque semaine, je réunis ici un nouveau projet en lien avec la finance que j’ai développé et documenté pas à pas.</p>
        <p>Mon objectif : rendre accessibles des outils et modèles utiles en finance, en expliquant à chaque fois les concepts derrière le code, les choix techniques et les usages concrets.</p>
        <p>Chaque mini-projet est accompagné d’explications, de cas d’utilisation et de liens vers la théorie ou la pratique, pour apprendre, comprendre et expérimenter la finance autrement — que vous soyez débutant ou curieux.</p>
    </div>
    """, unsafe_allow_html=True)

    # Project Definitions - ONLY PROJECT 1 FOR WEEK 1
    projects = [
        {"id": "p01_option_pricer", "title": "Semaine 1 : Pricer d'Options", "icon": "📊", "desc": "Modèle Black-Scholes implémenté en Python & C++."}
    ]

    # Grid Layout for Cards
    cols = st.columns(3)
    for i, project in enumerate(projects):
        with cols[i % 3]:
            if card_component(project["title"], project["icon"], project["desc"], key=project["id"]):
                st.session_state.selected_project = project["id"]
                st.session_state.current_page = 'project'
                st.rerun()

def render_project_page():
    project_id = st.session_state.selected_project
    
    # Back Button
    if st.button("← Retour au Dashboard"):
        st.session_state.current_page = 'home'
        st.session_state.selected_project = None
        st.rerun()

    # Load and Render Project
    module = load_project_module(project_id)
    if module:
        try:
            module.render()
        except AttributeError:
            st.error(f"Le projet {project_id} n'a pas de fonction render().")
    else:
        st.info(f"Le projet {project_id} est en construction.")

if __name__ == "__main__":
    main()
