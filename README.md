# 📊 Projet 1 : Pricer d'Options (Black-Scholes)

Bienvenue sur le premier projet de mon **Portfolio d'Ingénierie Financière**.
Chaque semaine, je publie un nouveau module explorant un concept clé de la finance, codé en Python.

## 📝 À propos de ce projet

Ce projet est une implémentation interactive du modèle **Black-Scholes**, la pierre angulaire de l'évaluation des options financières.

**Objectifs pédagogiques :**
*   Comprendre la formule mathématique de Black-Scholes.
*   Implémenter la logique de pricing en Python avec `numpy` et `scipy`.
*   Visualiser le "Payoff" (gain/perte) d'une option à maturité.
*   Observer l'impact des "Grecques" (sensibilité du prix) via la simulation.

## 🛠️ Stack Technique

*   **Python 3.9+**
*   **Streamlit** : Pour l'interface web interactive.
*   **Numpy & Scipy** : Pour les calculs mathématiques et statistiques (loi normale).
*   **Plotly** : Pour les graphiques interactifs.

## 🚀 Installation et Lancement

1.  **Cloner le dépôt :**
    ```bash
    git clone https://github.com/VOTRE_USERNAME/Portfolio-projet.git
    cd Portfolio-projet
    ```

2.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Lancer l'application :**
    ```bash
    streamlit run app.py
    ```

## 🧠 Aperçu du Code

Le cœur du pricing réside dans la fonction `black_scholes` :

```python
def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    # ... calcul du prix selon Call ou Put
```

---
*Développé avec passion pour apprendre et partager.*
