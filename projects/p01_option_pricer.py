import streamlit as st
import numpy as np
from scipy.stats import norm
import time
import plotly.graph_objects as go

def black_scholes(S, K, T, r, sigma, option_type="call"):
    """
    Calcule le prix Black-Scholes pour une option Européenne.
    
    Paramètres:
    S (float): Prix actuel de l'actif (Spot) - ex: 100€
    K (float): Prix d'exercice (Strike) - ex: 100€
    T (float): Temps jusqu'à maturité (en années) - ex: 1.0 pour 1 an
    r (float): Taux sans risque (décimal) - ex: 0.05 pour 5%
    sigma (float): Volatilité (décimal) - ex: 0.2 pour 20%
    option_type (str): "call" (droit d'achat) ou "put" (droit de vente)
    
    Retourne:
    float: Prix théorique de l'option
    """
    # d1 : Mesure la probabilité que l'option finisse "dans la monnaie" (ajustée par la volatilité)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    # d2 : Ajustement de d1 pour le calcul de l'espérance actualisée
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        # Formule Call : S * N(d1) - K * e^(-rT) * N(d2)
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        # Formule Put : K * e^(-rT) * N(-d2) - S * N(-d1)
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
    return price, d1, d2

def calculate_greeks(S, K, T, r, sigma, option_type="call"):
    """Calcul simplifié des Grecques pour l'éducation."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Delta : Sensibilité au prix du sous-jacent
    if option_type == "call":
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
        
    # Gamma : Sensibilité du Delta (accélération)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    # Theta : Sensibilité au temps (Time decay) - Approximation annuelle
    theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    if option_type == "put":
        theta += r * K * np.exp(-r * T)
        
    return delta, gamma, theta

def render():
    st.markdown("## 🗓️ Semaine 1 : Pricer une option avec le modèle Black-Scholes")
    
    # --- Introduction Storytelling ---
    st.info("""
    Avant 1973, le tarif des options, c’était le règne de l’instinct : chacun bidouillait une estimation, souvent à côté de la plaque.
Black, Scholes et Merton sont arrivés avec une formule : ça a été le passage de la peinture au laser.
Prix, risque, modèles — d’un coup, le marché a changé de dimension. Aujourd’hui, la finance moderne, c’est grâce à leur équation.
     """)
    
    with st.expander("📚 En savoir plus sur l'histoire (Vidéo/Article)"):
        st.markdown("""
        *   [Black-Scholes : la formule qui a donné naissance à Wall Street](https://www.polytechnique-insights.com/tribunes/economie/black-scholes-la-formule-qui-a-donne-naissance-a-wall-street/)
        *   [La formule qui a radicalement transformé la finance mondiale [Black-Scholes]](https://www.youtube.com/watch?v=XE7FKLfZzBA)
        """)

    st.markdown("---")

    # --- Section Interactive ---
    st.markdown("### 🎛️ Le Simulateur")
    st.caption("Modifiez les paramètres ci-dessous pour voir comment le prix de l'option évolue.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        S = st.number_input("Prix Actuel de l'Action (S)", value=100.0, step=1.0, help="Le prix de l'actif sous-jacent aujourd'hui sur le marché.")
        K = st.number_input("Prix d'Exercice (Strike K)", value=100.0, step=1.0, help="Le prix auquel vous aurez le droit d'acheter/vendre l'action à la fin.")
    with col2:
        T = st.number_input("Temps restant (Années)", value=1.0, step=0.1, help="Durée jusqu'à l'expiration de l'option. 1.0 = 1 an, 0.5 = 6 mois.")
        r = st.number_input("Taux sans risque (r)", value=0.05, step=0.01, help="Le taux d'intérêt 'sûr' (ex: obligations d'État). 0.05 = 5%.")
    with col3:
        sigma = st.number_input("Volatilité (σ)", value=0.2, step=0.01, help="À quel point le prix de l'action bouge. Plus c'est haut, plus c'est risqué (et cher).")
        option_type = st.selectbox("Type d'Option", ["call", "put"], help="'Call' = Droit d'acheter (je parie à la hausse). 'Put' = Droit de vendre (je parie à la baisse).")
        
    if st.button("🚀 Calculer le Prix"):
        start_time = time.time()
        price, d1, d2 = black_scholes(S, K, T, r, sigma, option_type)
        delta, gamma, theta = calculate_greeks(S, K, T, r, sigma, option_type)
        end_time = time.time()
        
        # --- Résultat et Interprétation ---
        st.success(f"### 💎 Prix de l'Option : ${price:.2f}")
        
        interpretation = f"""
        **Ce que cela signifie :**
        Pour obtenir le droit (mais pas l'obligation) d'acheter l'action à **{K}€** dans **{T} an(s)** (alors qu'elle vaut **{S}€** aujourd'hui),
        le marché estime que ce contrat vaut **{price:.2f}€** aujourd'hui.
        """
        if option_type == "put":
            interpretation = interpretation.replace("d'acheter", "de vendre")
            
        st.markdown(interpretation)
        
        # --- Les Grecques (Nouveau) ---
        st.markdown("#### 🧠 Analyse des Sensibilités (Les Grecques)")
        g_col1, g_col2, g_col3 = st.columns(3)
        with g_col1:
            st.metric("Delta (Δ)", f"{delta:.2f}", help="Vitesse : De combien change le prix de l'option si l'action monte de 1€.")
        with g_col2:
            st.metric("Gamma (Γ)", f"{gamma:.3f}", help="Accélération : De combien change le Delta si l'action monte de 1€.")
        with g_col3:
            st.metric("Theta (Θ)", f"{theta:.2f}", help="Temps : Combien de valeur l'option perd chaque jour qui passe (Time Decay).")

        # --- Visualisation ---
        st.markdown("#### 📉 Diagramme de Payoff (Gains/Pertes à Maturité)")
        spot_range = np.linspace(S * 0.5, S * 1.5, 100)
        if option_type == "call":
            payoff = np.maximum(spot_range - K, 0) - price # On soustrait le prix payé pour voir le profit net
        else:
            payoff = np.maximum(K - spot_range, 0) - price
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=spot_range, y=payoff, mode='lines', name='Profit Net', line=dict(color='#00f2ff', width=3)))
        fig.add_hline(y=0, line_color="white", line_width=1)
        fig.add_vline(x=S, line_dash="dash", line_color="#bc13fe", annotation_text="Prix Actuel")
        
        # Zone de perte/profit
        fig.add_shape(type="rect", x0=min(spot_range), y0=min(payoff), x1=max(spot_range), y1=0, 
                      fillcolor="red", opacity=0.1, line_width=0)
        fig.add_shape(type="rect", x0=min(spot_range), y0=0, x1=max(spot_range), y1=max(payoff), 
                      fillcolor="green", opacity=0.1, line_width=0)

        fig.update_layout(
            title=f"Profit/Perte Net à l'expiration (Strike={K})", 
            xaxis_title="Prix de l'Actif à Maturité", 
            yaxis_title="Profit / Perte (€)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E0E0')
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- Section Éducative Détaillée ---
    st.markdown("---")
    st.markdown("### 💼 Cas d'Usage Concret : L'Agriculteur Prudent")
    
    # Calcul réel pour l'exemple
    # Paramètres : S=200, K=200, T=0.5, r=0.02, sigma=0.2
    # On utilise la fonction black_scholes définie plus haut
    example_price, _, _ = black_scholes(200, 200, 0.5, 0.02, 0.2, "put")
    
    st.info(f"""
    **Le Scénario :**
    Un agriculteur craint que le prix du blé ne chute avant sa récolte dans 6 mois.
    
    **Les Données :**
    *   Prix actuel du blé ($S$) : **200 €/tonne**
    *   Prix plancher souhaité ($K$) : **200 €/tonne**
    *   Durée ($T$) : **6 mois** (0.5 an)
    *   Volatilité ($σ$) : **20%** (le marché bouge normalement)
    *   Taux sans risque ($r$) : **2%**
    
    **Le Calcul Black-Scholes :**
    Pour se protéger, il achète une option de vente (**PUT**).
    D'après le modèle, cette assurance coûte aujourd'hui : **{example_price:.2f} €/tonne**.
    
    **Bilan à la récolte (dans 6 mois) :**
    1.  **Si le blé s'effondre à 150 €** :
        *   Il vend son blé au marché : 150 €
        *   Il exerce son option (droit de vendre à 200 €) : Gain de 50 €
        *   Coût de l'assurance : -{example_price:.2f} €
        *   **Total reçu : {150 + 50 - example_price:.2f} €** (au lieu de 150 € sans protection).
        
    2.  **Si le blé monte à 250 €** :
        *   Il vend son blé au marché : 250 €
        *   Il jette l'option (elle ne vaut rien) : 0 €
        *   Coût de l'assurance : -{example_price:.2f} €
        *   **Total reçu : {250 - example_price:.2f} €**.
        
    👉 *Il a sacrifié un peu de gain potentiel ({example_price:.2f} €) pour garantir un prix minimum.*
    """)

    with st.expander("📊 Comprendre le Diagramme de Payoff"):
        st.markdown("""
        Le graphique ci-dessus montre votre profit net (axe Y) en fonction du prix futur de l'action (axe X).
        *   **Ligne Bleue** : Votre résultat net.
        *   **Zone Rouge** : Vous perdez de l'argent (limité au prix de l'option).
        *   **Zone Verte** : Vous gagnez de l'argent (potentiellement illimité pour un Call).
        *   **Point de bascule (Breakeven)** : Le prix que l'action doit atteindre pour que vous commenciez à faire du profit.
        """)
    
    # --- Section Éducative Détaillée ---
    st.markdown("---")
    st.markdown("### 🎓 Comprendre la Mécanique")
    
    with st.expander("🔍 Voir l'explication mathématique détaillée"):
        st.markdown(r"""
        La formule repose sur l'idée de construire un portefeuille sans risque (Delta-Hedging).
        
        $$
        C(S, t) = S \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2)
        $$
        
        **Déchiffrons chaque lettre :**
        *   **$C(S, t)$** : Le **Prix du Call** (ce qu'on cherche).
        *   **$S$** : Le **Prix Actuel** de l'action (Spot). Plus il est haut, plus le Call est cher.
        *   **$K$** : Le **Prix d'Exercice** (Strike). C'est le prix fixé dans le contrat.
        *   **$e^{-rT}$** : Le **Facteur d'Actualisation**. Il sert à ramener la valeur future de l'argent à sa valeur d'aujourd'hui (car 100€ dans un an valent moins que 100€ aujourd'hui).
        *   **$N(d)$** : La **Probabilité cumulée**. C'est un terme statistique (loi normale) qui est toujours compris entre 0 et 1.
        
        **L'intuition de la formule :**
        $$ \text{Prix} = (\text{Ce que je reçois}) - (\text{Ce que je paie}) $$
        
        1.  **$S \cdot N(d_1)$** : C'est la valeur attendue de l'action si l'option est exercée.
        2.  **$K \cdot e^{-rT} \cdot N(d_2)$** : C'est le coût du Strike que je devrai payer, ajusté par la probabilité de devoir le payer.
        """)
    
    st.markdown("### 💻 Le Code Python Expliqué")
    st.markdown("Voici comment on traduit ces maths en Python. J'utilise `numpy` pour les calculs et `scipy.stats` pour la loi normale.")
    
    st.code("""
import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type="call"):
    # 1. Calcul des termes d1 et d2
    # d1 combine la "moneyness" (S/K) et l'effet du temps/volatilité
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        # Formule du Call
        # norm.cdf(x) est la fonction de répartition N(x)
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        # Formule du Put
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
    return price
    """, language="python")
