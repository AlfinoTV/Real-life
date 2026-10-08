import time
import streamlit as st

st.set_page_config(
    page_title="School Life Simulator", page_icon="🏫", layout="wide"
)

st.title("🏫 School Life & Economy Simulator")

# Session State initialisieren (für Geld, Stats etc.)
if "money" not in st.session_state:
  st.session_state.money = 50.00
  st.session_state.food = 80.0
  st.session_state.drink = 80.0
  st.session_state.sleep = 80.0
  st.session_state.pending_earnings = 0.0

# Sidebar für Status
st.sidebar.header("Lebensstatus")
st.sidebar.metric("Geld", f"{st.session_state.money:.2f} €")
st.sidebar.progress(int(st.session_state.food), text="Essen")
st.sidebar.progress(int(st.session_state.drink), text="Trinken")
st.sidebar.progress(int(st.session_state.sleep), text="Schlaf")

# Echten Schlaf eintragen
st.subheader("💤 Schlaf eintragen")
sleep_hours = st.number_input(
    "Schlaf in Stunden:", min_val=1.0, max_val=16.0, value=8.0
)
if st.button("Schlaf eintragen"):
  recovered = min(100.0, sleep_hours * 12.5)
  st.session_state.sleep = min(100.0, st.session_state.sleep + recovered)
  st.success(f"{sleep_hours} Stunden Schlaf eingetragen!")
  st.rerun()

# Timer / Verdienst Sektion
st.subheader("⏱️ Live-Timer & Verdienst")
col1, col2 = st.columns(2)

with col1:
  if st.button("Auszahlen"):
    st.session_state.money += st.session_state.pending_earnings
    st.success(
        f"{st.session_state.pending_earnings:.2f} € erfolgreich ausgezahlt!"
    )
    st.session_state.pending_earnings = 0.0
    st.rerun()

with col2:
  st.metric(
      "Bereits verdient (nicht ausgezahlt)",
      f"{st.session_state.pending_earnings:.2f} €",
  )

# Kleines Beispiel für den Stat-Abfall / Simulator
if st.button("1 Minute arbeiten (Test)"):
  st.session_state.pending_earnings += 0.50
  st.session_state.food = max(0.0, st.session_state.food - 0.2)
  st.session_state.drink = max(0.0, st.session_state.drink - 0.3)
  st.rerun()
