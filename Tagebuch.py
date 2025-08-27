import streamlit as st
from datetime import datetime
import os
import json

# Login Bereich
st.title("📔 Dein Tagebuch")

username = st.text_input("Benutzername")
password = st.text_input("Passwort", type="password")

if username and password:
    filepath = f"{username}.json"

    # Falls Datei nicht existiert → Registrierung
    if not os.path.exists(filepath):
        if st.button("Registrieren"):
            with open(filepath, "w") as f:
                json.dump({"passwort": password, "eintraege": []}, f)
            st.success("✅ Registrierung erfolgreich! Bitte neu anmelden.")

    else:
        with open(filepath, "r") as f:
            data = json.load(f)

        if data.get("passwort") == password:
            st.success("✅ Anmeldung erfolgreich!")

            # Menü Auswahl
            option = st.radio("Was möchten Sie tun?", 
                              ["Neuen Eintrag erstellen", "Einträge anzeigen"])

            if option == "Neuen Eintrag erstellen":
                eintrag = st.text_area("Was haben Sie heute gemacht?")
                erlebnis = st.text_area("Gab es ein besonderes Erlebnis?")
                rating = st.slider("Wie würden Sie Ihren Tag bewerten? (1-10)", 1, 10, 5)

                if st.button("Eintrag speichern"):
                    datum = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    data["eintraege"].append({
                        "datum": datum,
                        "eintrag": eintrag,
                        "erlebnis": erlebnis,
                        "rating": rating
                    })
                    with open(filepath, "w") as f:
                        json.dump(data, f)
                    st.success("📌 Eintrag gespeichert!")

            elif option == "Einträge anzeigen":
                if data.get("eintraege"):
                    for e in reversed(data["eintraege"]):
                        st.write(f"**Datum:** {e['datum']}")
                        st.write(f"**Eintrag:** {e['eintrag']}")
                        st.write(f"**Erlebnis:** {e['erlebnis']}")
                        st.write(f"**Bewertung:** {e['rating']}/10")
                        st.markdown("---")
                else:
                    st.info("Noch keine Einträge vorhanden.")

        else:
            st.error("❌ Falsches Passwort!")
