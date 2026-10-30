"""Pack d'entraînement : étude d'un circuit RLC série.

L'application est un support pédagogique. La rubrique de paiement reste une
maquette informative : aucun paiement ni déblocage d'accès n'est traité ici.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Pack Excellence | Circuit RLC",
    page_icon="🎓",
    layout="wide",
)

st.markdown(
    """
    <style>
      .main-header { color:#1e3a8a; text-align:center; margin-bottom:0.2rem; }
      .subtitle { text-align:center; color:#475569; margin-bottom:1.5rem; }
      .notice { background:#fff7ed; border-left:5px solid #f59e0b;
                padding:0.8rem 1rem; border-radius:0.4rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="main-header">🎓 Pack d’entraînement élite</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Lycée Seydina Limamou Laye · Guédiawaye · Physique-Chimie</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Choisir une rubrique",
        ["Accueil", "Sujet et repères", "Simulateur RLC", "Évaluation", "Boutique"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Valeurs du sujet : R = 47 Ω, r = 3 Ω, L = 25 mH, C = 100 nF.")


# Données de l'énoncé
R_DEFAULT = 47.0
r_DEFAULT = 3.0
L_DEFAULT = 25e-3
C_DEFAULT = 100e-9
E_STEP = 12.0
U_M = 5.0
MEASUREMENTS = pd.DataFrame(
    {
        "f (Hz)": [1000, 2500, 3000, 3183, 3500, 4000, 5000],
        "Im mesuré (mA)": [12.5, 45.2, 78.3, 84.9, 72.1, 48.6, 18.3],
    }
)


def circuit_values(R: float, r: float, L: float, C: float, Um: float):
    rt = R + r
    omega0 = 1.0 / np.sqrt(L * C)
    lambda_ = rt / (2.0 * L)
    alpha_sq = omega0**2 - lambda_**2
    q = omega0 * L / rt
    bandwidth = rt / L
    f0 = omega0 / (2.0 * np.pi)
    i_peak = Um / rt
    discriminant = lambda_**2 - omega0**2
    return {
        "RT": rt,
        "omega0": omega0,
        "T0": 2.0 * np.pi / omega0,
        "lambda": lambda_,
        "alpha_sq": alpha_sq,
        "alpha": np.sqrt(alpha_sq) if alpha_sq > 0 else np.nan,
        "discriminant": discriminant,
        "f0": f0,
        "Q": q,
        "bandwidth": bandwidth,
        "delta_f": bandwidth / (2.0 * np.pi),
        "Im_peak": i_peak,
    }


if page == "Accueil":
    st.header("Bienvenue dans votre espace d’entraînement")
    col1, col2, col3 = st.columns(3)
    col1.metric("Sujet", "Circuit RLC série")
    col2.metric("Niveau", "Concours")
    col3.metric("Durée conseillée", "3 h")
    st.markdown(
        """
        ### Objectifs
        Étudier l’établissement du courant, la résonance en intensité,
        l’énergie électromagnétique et l’exploitation de mesures expérimentales.

        Utilisez **Sujet et repères** pour retrouver l’énoncé et quelques résultats,
        **Simulateur RLC** pour visualiser les réponses, puis **Évaluation** pour
        vérifier les notions essentielles.
        """
    )
    st.info("Le quiz comporte 5 questions dans cette version de l’application.")


elif page == "Sujet et repères":
    st.header("Sujet : étude d’un circuit RLC série")
    st.write(
        "Le circuit comprend un générateur, une résistance R = 47 Ω, une bobine "
        "d’inductance L = 25,0 mH et de résistance interne r = 3,0 Ω, ainsi qu’un "
        "condensateur C = 100 nF. On note Rₜ = R + r et i(t) le courant du circuit."
    )
    with st.expander("Partie 1 — Régime transitoire", expanded=True):
        st.markdown(
            """
            À t = 0, on applique un échelon E = 12,0 V.

            1.1 Établir l’équation différentielle vérifiée par q(t), en posant Rₜ = R + r.
            1.2 En déduire l’équation vérifiée par i(t) = dq/dt.
            1.3 Montrer qu’elle s’écrit i″ + 2λi′ + ω₀²i = 0 et exprimer λ et ω₀.
            1.4 Calculer ω₀, T₀ et λ.
            1.5 Calculer le discriminant de l’équation caractéristique et préciser le régime.
            1.6 Résoudre l’équation avec i(0) = 0 et uC(0) = 0.
            1.7 Tracer i(t) et préciser le maximum ainsi que le temps d’établissement.
            """
        )
    with st.expander("Partie 2 — Régime sinusoïdal forcé et résonance"):
        st.markdown(
            """
            Pour ug(t) = Um cos(ωt), avec Um = 5,0 V :

            2.1 Établir l’impédance complexe Z(ω).
            2.2 En déduire l’amplitude Im(ω).
            2.3 Déterminer la pulsation qui maximise Im.
            2.4 Calculer ωᵣ, fᵣ et Im,max.
            2.5 Définir et calculer le facteur de qualité Q.
            2.6 Déterminer la bande passante à −3 dB, Δω et Δf.
            2.7 Tracer la courbe de résonance et ses points remarquables.
            """
        )
    with st.expander("Partie 3 — Analyse énergétique"):
        st.markdown(
            """
            3.1 Exprimer l’énergie stockée en fonction de L, C, i(t) et uC(t).
            3.2 Montrer qu’à la résonance, les énergies moyennes de la bobine et du
            condensateur sont égales.
            3.3 Établir le bilan de puissance instantanée et identifier les termes
            actifs et réactifs.
            3.4 Exprimer la puissance moyenne avec Um, Im et cos φ.
            3.5 Calculer la puissance moyenne à la résonance et pour ω = 0,8ωᵣ.
            """
        )
    with st.expander("Partie 4 — Mesures et incertitudes"):
        st.dataframe(MEASUREMENTS, hide_index=True, use_container_width=True)
        st.markdown(
            "4.1 Estimer graphiquement fᵣ,exp et Im,max,exp. 4.2 Comparer aux valeurs "
            "théoriques et calculer les écarts relatifs. 4.3 Pour u(Im) = 1,5 mA, "
            "exprimer Im,max avec une incertitude élargie à 95 %. 4.4 Faire de même "
            "pour u(f) = 10 Hz. 4.5 Estimer Qexp et le comparer à Q."
        )
        st.caption(
            "Les points mesurés sont repris tels que fournis dans l’énoncé. "
            "Ils ne suivent pas exactement la courbe théorique du circuit donné."
        )
    with st.expander("Partie 5 — Synthèse"):
        st.markdown(
            "5.1 Expliquer pourquoi la résonance est utile en radio et en filtrage, "
            "mais peut présenter un risque pour les installations électriques. "
            "5.2 Proposer un montage pour visualiser la courbe de résonance à "
            "l’oscilloscope. 5.3 Indiquer comment doubler Q tout en conservant la "
            "fréquence de résonance, avec une justification quantitative."
        )

    vals = circuit_values(R_DEFAULT, r_DEFAULT, L_DEFAULT, C_DEFAULT, U_M)
    st.subheader("Repères numériques")
    a, b, c = st.columns(3)
    a.metric("Rₜ", f"{vals['RT']:.1f} Ω")
    b.metric("ω₀", f"{vals['omega0']:.0f} rad·s⁻¹")
    c.metric("f₀", f"{vals['f0']:.1f} Hz")
    d, e, f = st.columns(3)
    d.metric("λ", f"{vals['lambda']:.0f} s⁻¹")
    e.metric("Q", f"{vals['Q']:.1f}")
    f.metric("Δf à −3 dB", f"{vals['delta_f']:.1f} Hz")
    st.latex(r"Lq'' + R_Tq' + \frac{q}{C}=E,\qquad Li''+R_Ti'+\frac{i}{C}=0")
    st.latex(r"\lambda=\frac{R_T}{2L},\qquad \omega_0=\frac{1}{\sqrt{LC}}")
    st.latex(r"Z=R_T+j\left(\omega L-\frac{1}{\omega C}\right),\qquad I_m=\frac{U_m}{|Z|}")
    st.latex(r"Q=\frac{\omega_0L}{R_T},\qquad \Delta\omega=\frac{R_T}{L},\qquad \Delta f=\frac{R_T}{2\pi L}")
    st.write(
        f"Pour les valeurs du sujet, le courant transitoire est pseudo-périodique "
        f"(α = {vals['alpha']:.1f} s⁻¹). Son premier maximum vaut environ "
        f"{(E_STEP / (L_DEFAULT * vals['alpha']) * np.exp(-vals['lambda'] * np.arctan2(vals['alpha'], vals['lambda']) / vals['alpha']) * np.sin(np.arctan2(vals['alpha'], vals['lambda'])) * 1e3):.2f} mA."
    )
    st.write(
        f"En régime forcé, Im,max = Um/Rₜ = {vals['Im_peak'] * 1e3:.1f} mA à "
        f"f₀ = {vals['f0']:.1f} Hz. Le maximum mesuré fourni (84,9 mA) est inférieur "
        f"de {(1.0 - 84.9 / (vals['Im_peak'] * 1e3)) * 100:.1f} % à cette valeur théorique."
    )
    st.info(
        "En série, l’amplitude du courant est maximale à ω₀ = 1/√(LC). "
        "La résistance modifie le maximum et la largeur du pic, mais pas sa fréquence."
    )


elif page == "Simulateur RLC":
    st.header("Simulateur du circuit RLC série")
    st.write("Modifiez les paramètres pour observer leur effet sur le transitoire et la résonance.")
    p1, p2, p3, p4 = st.columns(4)
    R = p1.number_input("R externe (Ω)", min_value=1.0, max_value=500.0, value=R_DEFAULT, step=1.0)
    r = p2.number_input("Résistance interne r (Ω)", min_value=0.0, max_value=100.0, value=r_DEFAULT, step=0.5)
    L_mH = p3.number_input("Inductance L (mH)", min_value=0.1, max_value=500.0, value=25.0, step=1.0)
    C_nF = p4.number_input("Capacité C (nF)", min_value=1.0, max_value=10000.0, value=100.0, step=10.0)
    L, C = L_mH * 1e-3, C_nF * 1e-9
    vals = circuit_values(R, r, L, C, U_M)
    rt = vals["RT"]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rₜ", f"{rt:.2f} Ω")
    m2.metric("f₀", f"{vals['f0']:.2f} Hz")
    m3.metric("Q", f"{vals['Q']:.2f}")
    m4.metric("Δf à −3 dB", f"{vals['delta_f']:.2f} Hz")

    if vals["alpha_sq"] > 0:
        alpha = vals["alpha"]
        lambda_ = vals["lambda"]
        t_peak = np.arctan2(alpha, lambda_) / alpha
        i_peak_step = E_STEP / (L * alpha) * np.exp(-lambda_ * t_peak) * np.sin(alpha * t_peak)
        t_settle = np.log(50.0) / lambda_  # enveloppe à 2 %
        t_end = max(6.0 * vals["T0"], 1.15 * t_settle)
        t = np.linspace(0.0, t_end, 2500)
        i_t = (E_STEP / (L * alpha)) * np.exp(-lambda_ * t) * np.sin(alpha * t)
        fig_t = go.Figure()
        fig_t.add_trace(go.Scatter(x=t * 1e3, y=i_t * 1e3, mode="lines", name="i(t)"))
        fig_t.add_vline(x=t_peak * 1e3, line_dash="dash", line_color="#dc2626")
        fig_t.update_layout(
            title="Réponse à l’échelon de 12 V",
            xaxis_title="Temps (ms)",
            yaxis_title="Courant (mA)",
            template="plotly_white",
        )
        st.plotly_chart(fig_t, use_container_width=True)
        st.caption(
            f"Premier maximum : {i_peak_step * 1e3:.2f} mA à {t_peak * 1e6:.2f} µs. "
            f"Temps d’établissement indicatif à 2 % : {t_settle * 1e3:.2f} ms."
        )
    else:
        st.warning("Le régime transitoire est apériodique ou critique pour ces paramètres.")

    st.subheader("Courbe de résonance en intensité")
    f = np.linspace(max(1.0, 0.15 * vals["f0"]), 2.2 * vals["f0"], 1800)
    omega = 2.0 * np.pi * f
    current = U_M / np.sqrt(rt**2 + (omega * L - 1.0 / (omega * C)) ** 2)
    fig_r = go.Figure()
    fig_r.add_trace(go.Scatter(x=f, y=current * 1e3, mode="lines", name="Modèle théorique"))
    fig_r.add_trace(
        go.Scatter(
            x=MEASUREMENTS["f (Hz)"],
            y=MEASUREMENTS["Im mesuré (mA)"],
            mode="markers",
            name="Mesures fournies dans le sujet",
            marker={"size": 9, "color": "#dc2626"},
        )
    )
    fig_r.add_vline(x=vals["f0"], line_dash="dash", line_color="#2563eb", annotation_text="f₀")
    fig_r.update_layout(
        title="Amplitude Im en fonction de la fréquence",
        xaxis_title="Fréquence (Hz)",
        yaxis_title="Im (mA)",
        template="plotly_white",
        legend={"orientation": "h", "y": 1.12},
    )
    st.plotly_chart(fig_r, use_container_width=True)
    st.caption(
        "Les mesures rouges sont celles de l’énoncé initial. Elles restent fixes lorsque "
        "vous modifiez les paramètres du modèle."
    )

    # Puissance moyenne pour le circuit paramétré, à la résonance et à 0,8 f0.
    def mean_power_at(omega_value: float) -> float:
        z_abs = np.sqrt(rt**2 + (omega_value * L - 1.0 / (omega_value * C)) ** 2)
        i_amp = U_M / z_abs
        cos_phi = rt / z_abs
        return 0.5 * U_M * i_amp * cos_phi

    with st.expander("Puissance moyenne — rappel"):
        st.write(f"À la résonance : **{mean_power_at(vals['omega0']):.4f} W**.")
        st.write(f"Pour ω = 0,8ω₀ : **{mean_power_at(0.8 * vals['omega0']):.4f} W**.")
        st.latex(r"P_{moy}=\frac{1}{2}U_m I_m\cos\varphi=\frac{1}{2}R_T I_m^2")


elif page == "Évaluation":
    st.header("Évaluation interactive — 5 questions")
    questions = [
        ("Quelle est la résistance totale Rₜ ?", ["47 Ω", "50 Ω", "53 Ω"], 1, "Rₜ = R + r = 47 + 3 = 50 Ω."),
        ("Quelle est la pulsation propre ω₀ ?", ["2 000 rad·s⁻¹", "20 000 rad·s⁻¹", "200 000 rad·s⁻¹"], 1, "ω₀ = 1/√(LC) = 20 000 rad·s⁻¹."),
        ("Quelle est la nature du régime transitoire ?", ["Apériodique", "Critique", "Pseudo-périodique"], 2, "λ² − ω₀² < 0 : le régime est pseudo-périodique amorti."),
        ("À quelle fréquence le courant est-il maximal ?", ["Environ 3 183 Hz", "Environ 31 830 Hz", "La fréquence dépend de Rₜ"], 0, "Pour le courant d’un RLC série, le maximum est à ω₀ = 1/√(LC)."),
        ("Quelle est la valeur théorique du facteur de qualité Q ?", ["0,1", "1", "10"], 2, "Q = ω₀L/Rₜ = (1/Rₜ)√(L/C) = 10."),
    ]
    with st.form("quiz_form"):
        answers = []
        for idx, (question, choices, correct, explanation) in enumerate(questions):
            answers.append(st.radio(question, choices, key=f"q{idx}"))
        submitted = st.form_submit_button("Corriger mes réponses", type="primary")
    if submitted:
        score = sum(answer == questions[i][1][questions[i][2]] for i, answer in enumerate(answers))
        st.session_state["rlc_last_score"] = score
        st.metric("Votre score", f"{score} / {len(questions)}")
        for idx, (_, choices, correct, explanation) in enumerate(questions):
            if answers[idx] == choices[correct]:
                st.success(f"Question {idx + 1} : correct. {explanation}")
            else:
                st.error(f"Question {idx + 1} : réponse attendue — {choices[correct]}. {explanation}")
    elif "rlc_last_score" in st.session_state:
        st.caption(f"Dernier score : {st.session_state['rlc_last_score']} / {len(questions)}")


elif page == "Boutique":
    st.header("Pack Électrocinétique avancée")
    st.subheader("Circuit RLC série — régime transitoire et forcé")
    st.write("Sujet de concours · durée conseillée : 3 heures · niveau concours")
    st.markdown("**Contenu présenté dans cette application :** sujet en cinq parties, repères de calcul, simulateur graphique et quiz de cinq questions.")
    st.metric("Prix indicatif du pack", "5 000 FCFA")
    st.markdown(
        '<div class="notice"><strong>Paiement mobile :</strong> Wave ou Orange Money au '
        '<strong>+221 77 513 63 49</strong>. Indiquez le nom du pack dans le motif et conservez '
        'votre reçu. La transaction doit être vérifiée manuellement ; cette application ne '
        'valide pas automatiquement les paiements.</div>',
        unsafe_allow_html=True,
    )


st.divider()
st.caption("© 2026 Lycée Seydina Limamou Laye · Guédiawaye · Support pédagogique de Physique-Chimie")
