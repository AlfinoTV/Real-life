import time
import streamlit as st

st.set_page_config(
    page_title="School Life & Economy Simulator", page_icon="🏫", layout="wide"
)

# --- 1. SESSION STATE INITIALISIEREN ---
if "money" not in st.session_state:
  st.session_state.money = 50.00
  st.session_state.pending_earnings = 0.0
  st.session_state.total_earnings = 0.0
  st.session_state.total_taxes = 0.0
  st.session_state.food = 80.0
  st.session_state.drink = 80.0
  st.session_state.sleep = 80.0
  st.session_state.loan = 0.0
  st.session_state.housing = {"name": "Keine", "rent": 0}
  st.session_state.contracts = {
      "Handy": {"active": False, "cost": 1.2},
      "WLAN": {"active": False, "cost": 1.5},
      "Netflix": {"active": False, "cost": 0.6},
      "Spotify": {"active": False, "cost": 0.4},
  }
  st.session_state.active_lesson = "Freistunde"
  st.session_state.current_rate = 0.0


def decay_stats():
  st.session_state.food = max(0.0, st.session_state.food - 0.2)
  st.session_state.drink = max(0.0, st.session_state.drink - 0.3)
  st.session_state.sleep = max(0.0, st.session_state.sleep - 0.1)


# --- 2. SIDEBAR / STATUS ---
st.sidebar.title("🏫 Lebensstatus")
st.sidebar.metric("Geld", f"{st.session_state.money:.2f} €")

st.sidebar.write("---")
st.sidebar.progress(
    int(st.session_state.food), text=f"Essen: {int(st.session_state.food)}%"
)
st.sidebar.progress(
    int(st.session_state.drink), text=f"Trinken: {int(st.session_state.drink)}%"
)
st.sidebar.progress(
    int(st.session_state.sleep),
    text=f"Schlaf / Energie: {int(st.session_state.sleep)}%",
)

# --- 3. TABS ---
tab_dash, tab_schedule, tab_shop, tab_housing, tab_bank, tab_contracts = (
    st.tabs([
        "Dashboard",
        "Stundenplan",
        "Supermarkt",
        "Wohnung",
        "Bank",
        "Verträge",
    ])
)

# --- TAB 1: DASHBOARD ---
with tab_dash:
  st.subheader("⏱️ Live-Timer & Aktuelle Aktivität")

  col1, col2 = st.columns(2)

  with col1:
    st.info(f"Aktuelle Aktivität: **{st.session_state.active_lesson}**")
    st.metric("Verdienst-Rate", f"{st.session_state.current_rate:.2f} € / Min")
    st.metric(
        "Bereits verdient (nicht ausgezahlt)",
        f"{st.session_state.pending_earnings:.2f} €",
    )

    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
      if st.button("Auszahlen", use_container_width=True):
        st.session_state.money += st.session_state.pending_earnings
        st.success(
            f"{st.session_state.pending_earnings:.2f} € ausgezahlt! 💰"
        )
        st.session_state.pending_earnings = 0.0
        st.rerun()
    with c_btn2:
      if st.button("1 Min. arbeiten / lernen", use_container_width=True):
        st.session_state.pending_earnings += st.session_state.current_rate
        st.session_state.total_earnings += st.session_state.current_rate
        decay_stats()
        st.rerun()

  with col2:
    st.subheader("💤 Schlaf eintragen")
    # Korrigiert: min_value und max_value statt min_val/max_val
    sleep_hours = st.number_input(
        "Schlaf in Stunden:",
        min_value=1.0,
        max_value=16.0,
        value=8.0,
        step=0.5,
    )
    if st.button("Schlaf eintragen", use_container_width=True):
      recovered = min(100.0, sleep_hours * 12.5)
      st.session_state.sleep = min(100.0, st.session_state.sleep + recovered)
      st.success(f"{sleep_hours} Stunden Schlaf eingetragen! Energie aufgeladen.")
      st.rerun()

    contract_cost = sum(
        v["cost"] for v in st.session_state.contracts.values() if v["active"]
    )
    total_fixed = st.session_state.housing["rent"] + contract_cost
    st.write(f"Tägliche Fixkosten: **{total_fixed:.2f} €**")

    if st.button("Tag beenden & Abrechnung", use_container_width=True):
      tax = st.session_state.pending_earnings * 0.20
      net = st.session_state.pending_earnings - tax - total_fixed
      st.session_state.money += net
      st.session_state.total_taxes += tax
      st.session_state.pending_earnings = 0.0
      st.success(
          f"Tag beendet! Netto nach Steuern & Fixkosten: {net:.2f} € (Steuern:"
          f" {tax:.2f} €)"
      )
      st.rerun()

# --- TAB 2: STUNDENPLAN ---
with tab_schedule:
  st.subheader("📚 Stundenplan & Fächer auswählen")
  st.write(
      "Klicke auf ein Fach, um es als aktuelle Aktivität für den Timer"
      " zu übernehmen:"
  )

  fächer = [
      {"name": "Mathematik", "rate": 0.50},
      {"name": "Physik (LK)", "rate": 0.60},
      {"name": "Informatik", "rate": 0.55},
      {"name": "Geschichte", "rate": 0.40},
      {"name": "Freistunde", "rate": 0.00},
      {"name": "Eigenes Projekt (Zocken/Lernen)", "rate": 0.50},
  ]

  cols = st.columns(3)
  for i, f in enumerate(fächer):
    with cols[i % 3]:
      if st.button(
          f"{f['name']} ({f['rate']:.2f} €/m)", use_container_width=True
      ):
        st.session_state.active_lesson = f["name"]
        st.session_state.current_rate = f["rate"]
        st.success(f'Aktivität auf "{f["name"]}" gesetzt!')
        st.rerun()

# --- TAB 3: SUPERMARKT ---
with tab_shop:
  st.subheader("🛒 Supermarkt")
  col_drink, col_food = st.columns(2)

  with col_drink:
    st.write("**Getränke**")
    if st.button("Red Bull (2.50 €) — +25% Trinken"):
      if st.session_state.money >= 2.5:
        st.session_state.money -= 2.5
        st.session_state.drink = min(100.0, st.session_state.drink + 25)
        st.success("Red Bull gekauft!")
        st.rerun()
      else:
        st.error("Nicht genug Geld!")

    if st.button("Club Mate (1.80 €) — +20% Trinken"):
      if st.session_state.money >= 1.8:
        st.session_state.money -= 1.8
        st.session_state.drink = min(100.0, st.session_state.drink + 20)
        st.success("Club Mate gekauft!")
        st.rerun()
      else:
        st.error("Nicht genug Geld!")

  with col_food:
    st.write("**Essen**")
    if st.button("Subway Menü (8.99 €) — +55% Essen"):
      if st.session_state.money >= 8.99:
        st.session_state.money -= 8.99
        st.session_state.food = min(100.0, st.session_state.food + 55)
        st.success("Subway Menü gekauft!")
        st.rerun()
      else:
        st.error("Nicht genug Geld!")

    if st.button("Schokolade (1.49 €) — +18% Essen"):
      if st.session_state.money >= 1.49:
        st.session_state.money -= 1.49
        st.session_state.food = min(100.0, st.session_state.food + 18)
        st.success("Schokolade gekauft!")
        st.rerun()
      else:
        st.error("Nicht genug Geld!")

# --- TAB 4: WOHNUNG ---
with tab_housing:
  st.subheader("🏠 Immobilien-Markt")
  st.write(
      f"Aktuelle Unterkunft: **{st.session_state.housing['name']}**"
  )

  c_h1, c_h2 = st.columns(2)
  with c_h1:
    if st.button("WG-Zimmer mieten (10.00 € / Tag)"):
      st.session_state.housing = {"name": "WG-Zimmer", "rent": 10.0}
      st.success("WG-Zimmer gemietet!")
      st.rerun()
  with c_h2:
    if st.button("Moderne Wohnung mieten (25.00 € / Tag)"):
      st.session_state.housing = {"name": "Moderne Wohnung", "rent": 25.0}
      st.success("Moderne Wohnung gemietet!")
      st.rerun()

# --- TAB 5: BANK ---
with tab_bank:
  st.subheader("🏦 Bank & Kredite")
  st.metric("Aktueller Kredit", f"{st.session_state.loan:.2f} €")

  cb1, cb2 = st.columns(2)
  with cb1:
    if st.button("100 € Kredit aufnehmen"):
      st.session_state.loan += 100.0
      st.session_state.money += 100.0
      st.success("100 € aufgenommen.")
      st.rerun()
  with cb2:
    if st.button("100 € Kredit tilgen"):
      if st.session_state.money >= 100 and st.session_state.loan >= 100:
        st.session_state.loan -= 100.0
        st.session_state.money -= 100.0
        st.success("100 € getilgt.")
        st.rerun()
      else:
        st.error("Nicht genug Geld oder kein Kredit offen!")

# --- TAB 6: VERTRÄGE ---
with tab_contracts:
  st.subheader("📱 Abos & Verträge verwalten")
  for name, data in st.session_state.contracts.items():
    status_text = "Aktiv" if data["active"] else "Inaktiv"
    c1, c2 = st.columns([3, 1])
    with c1:
      st.write(
          f"**{name}** ({data['cost']:.2f} € / Tag) — Status:"
          f" **{status_text}**"
      )
    with c2:
      if data["active"]:
        if st.button(f"{name} kündigen", key=f"c_{name}"):
          st.session_state.contracts[name]["active"] = False
          st.rerun()
      else:
        if st.button(f"{name} buchen", key=f"c_{name}"):
          st.session_state.contracts[name]["active"] = True
          st.rerun()
