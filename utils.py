import streamlit as st

def load_css(file_name):
    """Charge un fichier CSS."""
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Fichier CSS {file_name} introuvable.")

def card_component(title, icon, description, key):
    """
    Affiche un composant carte.
    Retourne True si cliqué.
    """
    # Utilisation d'un conteneur avec un bouton à l'intérieur
    
    with st.container():
        st.markdown(f"""
        <div class="project-card">
            <div class="card-icon">{icon}</div>
            <div class="card-title">{title}</div>
            <div class="card-desc">{description}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Le bouton est le point d'interaction
        return st.button(f"Ouvrir {title}", key=key, use_container_width=True)


