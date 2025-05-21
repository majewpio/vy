# streamlit_crm_demo.py
import streamlit as st
import pandas as pd
from PIL import Image

# ------------------ TŁO LOGOWANIA ------------------
@st.cache_data
def load_login_bg():
    return Image.open("logowanie.JPG")

# ------------------ ZAŁADUJ ZDJĘCIA PRODUKTÓW ------------------
@st.cache_data
def load_product_images():
    return {
        "vet pro 70": Image.open("vet_pro_70.JPG"),
        "vet portable 15": Image.open("vet_portable_15.JPG"),
        "vet pro-key 75": Image.open("vet_pro_75.JPG")
    }

# ------------------ LOGOWANIE ------------------
def login():
    st.image(load_login_bg(), use_column_width=True)
    st.title("Vet-Eye CRM Assistant")
    st.subheader("Zaloguj się, aby uzyskać dostęp do panelu handlowca")
    login = st.text_input("Login")
    password = st.text_input("Hasło", type="password")
    if st.button("Zaloguj"):
        if login == "handlowiec" and password == "vet123":
            st.session_state.logged_in = True
        else:
            st.error("Niepoprawny login lub hasło")

# ------------------ STRATEGIE I SKRYPTY ------------------
def get_action(score, churn):
    if churn >= 0.8:
        return ("Skontaktuj się natychmiast: klient zagrożony odejściem",
                "Zadzwoń i zapytaj, czy czegoś nie brakuje, zaproponuj wsparcie techniczne lub darmowe szkolenie.")
    elif score >= 0.85:
        return ("Umów demo lub spotkanie",
                "Dzień dobry, zauważyliśmy Państwa wzmożoną aktywność i chcielibyśmy zaproponować prezentację nowego modelu aparatu USG.")
    elif score >= 0.65:
        return ("Wyślij e-mail z ofertą",
                "Cześć! Mamy nową ofertę dla klinik takich jak Państwa. Czy mogę przesłać szczegóły?")
    else:
        return ("Monitoruj lead",
                "Na ten moment klient nie wykazuje gotowości zakupowej.")

# ------------------ PRODUKT NA PODSTAWIE SEGMENTU ------------------
def get_product_recommendation(row):
    if row['segment'] == 'mobilny':
        return "vet portable 15"
    elif row['clinic_size'] >= 10:
        return "vet pro-key 75"
    else:
        return "vet pro 70"

# ------------------ PANEL GŁÓWNY ------------------
@st.cache_data
def load_data():
    scores = pd.read_csv("veteye_clients_with_scores.csv")
    churn = pd.read_csv("veteye_clients_with_churn_scores.csv")
    df = scores.merge(churn[['clinic_id', 'churn_score']], on='clinic_id')
    return df

def dashboard():
    st.title("Panel handlowca Vet-Eye")
    df = load_data()
    images = load_product_images()

    for i, row in df.sort_values(by='buy_score', ascending=False).head(10).iterrows():
        st.markdown("---")
        st.subheader(f"📅 {row['clinic_name']}")
        st.write(f"Segment: {row['segment']} | Lokalizacja: {row['country']}")
        st.write(f"**Scoring sprzedażowy:** {round(row['buy_score']*100,1)}% | **Ryzyko odejścia:** {round(row['churn_score']*100,1)}%")

        action, script = get_action(row['buy_score'], row['churn_score'])
        st.write(f"🔄 **Zalecane działanie:** {action}")
        st.info(script)

        product = get_product_recommendation(row)
        st.write(f"🚀 **Rekomendowany produkt:** {product}")
        st.image(images[product], width=300)

# ------------------ APLIKACJA ------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    dashboard()
