import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Nährstoff-Tracker", layout="wide")

# === PASSWORTSCHUTZ ===
# Ändere "meinPasswort123" in dein persönliches Wunschpasswort!
PASSWORT = "meinPasswort123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Zugang geschützt")
    user_password = st.text_input("Bitte Passwort eingeben:", type="password")
    if st.button("Anmelden"):
        if user_password == PASSWORT:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Falsches Passwort!")
    st.stop()

# === NÄHRSTOFF-TRACKER (Nur nach Anmeldung sichtbar) ===
st.title("🥗 Mein Nährstoff-Tracker")

# 1. Datenbank der Lebensmittel (Basiswerte pro 100g oder 1 Portion)
if "food_db" not in st.session_state:
    st.session_state.food_db = pd.DataFrame([
        {"Lebensmittel": "Vollkorn-Haferflocken", "Einheit": "g", "Energie (kcal)": 361.0, "Eiweiß (g)": 14.0, "Magnesium (mg)": 130.0},
        {"Lebensmittel": "Kulturheidelbeeren", "Einheit": "g", "Energie (kcal)": 50.0, "Eiweiß (g)": 0.6, "Magnesium (mg)": 6.0},
        {"Lebensmittel": "Magnesium Komplex", "Einheit": "Kapsel", "Energie (kcal)": 0.0, "Eiweiß (g)": 0.0, "Magnesium (mg)": 400.0},
    ])

# 2. Tages-Logbuch
if "daily_log" not in st.session_state:
    st.session_state.daily_log = []

# Tabs für die Übersicht
tab1, tab2 = st.tabs(["📝 Tages-Tracker", "🍎 Lebensmittel-Datenbank"])

with tab2:
    st.subheader("Neues Lebensmittel hinzufügen")
    with st.form("add_food"):
        name = st.text_input("Name des Lebensmittels")
        unit = st.selectbox("Einheit der Basisangabe", ["g", "ml", "Stück/Kapsel/Tropfen"])
        kcal = st.number_input("Energie (kcal) pro 100g / 1 Stück", min_value=0.0)
        protein = st.number_input("Eiweiß (g) pro 100g / 1 Stück", min_value=0.0)
        mg = st.number_input("Magnesium (mg) pro 100g / 1 Stück", min_value=0.0)
        
        submitted = st.form_submit_button("Speichern")
        if submitted and name:
            new_row = {"Lebensmittel": name, "Einheit": unit, "Energie (kcal)": kcal, "Eiweiß (g)": protein, "Magnesium (mg)": mg}
            st.session_state.food_db = pd.concat([st.session_state.food_db, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"'{name}' wurde gespeichert!")

    st.subheader("Gespeicherte Lebensmittel")
    st.dataframe(st.session_state.food_db, use_container_width=True)

with tab1:
    st.subheader("Mahlzeit / Einnahme erfassen")
    selected_food = st.selectbox("Lebensmittel auswählen", st.session_state.food_db["Lebensmittel"].tolist())
    
    food_info = st.session_state.food_db[st.session_state.food_db["Lebensmittel"] == selected_food].iloc[0]
    unit_label = food_info["Einheit"]
    
    amount = st.number_input(f"Menge in {unit_label}", min_value=0.0, value=100.0 if unit_label in ["g", "ml"] else 1.0)
    
    if st.button("Hinzufügen"):
        factor = amount / 100.0 if unit_label in ["g", "ml"] else amount
        entry = {
            "Lebensmittel": selected_food,
            "Menge": f"{amount} {unit_label}",
            "Energie (kcal)": round(food_info["Energie (kcal)"] * factor, 2),
            "Eiweiß (g)": round(food_info["Eiweiß (g)"] * factor, 2),
            "Magnesium (mg)": round(food_info["Magnesium (mg)"] * factor, 2)
        }
        st.session_state.daily_log.append(entry)
        st.success("Hinzugefügt!")

    st.divider()
    st.subheader("Heute konsumiert")
    if st.session_state.daily_log:
        log_df = pd.DataFrame(st.session_state.daily_log)
        st.dataframe(log_df, use_container_width=True)
        
        # Totals
        st.subheader("Gesamtsumme Heute")
        col1, col2, col3 = st.columns(3)
        col1.metric("Gesamt Kalorien", f"{log_df['Energie (kcal)'].sum():.1f} kcal")
        col2.metric("Gesamt Eiweiß", f"{log_df['Eiweiß (g)'].sum():.1f} g")
        col3.metric("Gesamt Magnesium", f"{log_df['Magnesium (mg)'].sum():.1f} mg")
