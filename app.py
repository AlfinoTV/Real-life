import time
import streamlit as st

st.set_page_config(
    page_title="School Life & Economy Simulator", page_icon="🏫", layout="wide"
)

# --- EXaktes HTML/CSS Design ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background-color: #1e1b4b;
        border-right: 1px solid #312e81;
    }
    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    .custom-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .clock-display {
        font-family: monospace;
        font-size: 1.8rem;
        font-weight: bold;
        color: #38bdf8;
        background: #0f172a;
        padding: 10px 20px;
        border-radius: 8px;
        border: 1px solid #334155;
        text-align: center;
        margin-bottom: 20px;
    }
    h1, h2, h3, h4 {
        color: #f8fafc !important;
        font-weight: 600;
    }
    div.stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: background-color 0.2s;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #2563eb;
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- 1. SESSION STATE INITIALISIEREN ---
if "money" not in st.session_state:
  st.session_state.money = 50.00
  st.session_state.pending_earnings = 0.0
  st.session_state.total_earnings = 0.0
  st.session_state.food = 80.0
  st.session_state.drink = 80.0
  st.session_state.sleep = 80.0
  st.session_state.loan = 0.0
  st.session_state.housing = {"name": "Keine", "rent": 0.0}

  # Erweiterte Verträge
  st.session_state.contracts = {
      "Handyvertrag": {"active": False, "cost": 1.2},
      "WLAN / Glasfaser": {"active": False, "cost": 1.5},
      "Netflix": {"active": False, "cost": 0.6},
      "Spotify": {"active": False, "cost": 0.4},
      "Amazon Prime": {"active": False, "cost": 0.5},
      "Disney+": {"active": False, "cost": 0.5},
      "Gym / Fitnessstudio": {"active": False, "cost": 1.5},
      "Cloud-Storage (2TB)": {"active": False, "cost": 0.3},
  }

  st.session_state.active_lesson = "Freistunde"
  st.session_state.current_rate = 0.0


def decay_stats():
  st.session_state.food = max(0.0, st.session_state.food - 0.2)
  st.session_state.drink = max(0.0, st.session_state.drink - 0.3)
  st.session_state.sleep = max(0.0, st.session_state.sleep - 0.1)


# --- 2. SIDEBAR STATUS ---
with st.sidebar:
  st.markdown("## 🏫 Lebensstatus")
  st.metric("Geld auf der Hand", f"{st.session_state.money:.2f} €")
  st.markdown("---")
  st.markdown("### 🔋 Vitalwerte")
  st.progress(
      int(st.session_state.food), text=f"Essen: {int(st.session_state.food)}%"
  )
  st.progress(
      int(st.session_state.drink),
      text=f"Trinken: {int(st.session_state.drink)}%",
  )
  st.progress(
      int(st.session_state.sleep),
      text=f"Schlaf / Energie: {int(st.session_state.sleep)}%",
  )

# --- 3. TABS (NAVIGATION) ---
tab_dash, tab_schedule, tab_shop, tab_housing, tab_bank, tab_contracts = st.tabs([
    "📊 Dashboard",
    "📚 Stundenplan",
    "🛒 Supermarkt",
    "🏠 Wohnung",
    "🏦 Bank",
    "📱 Verträge",
])

# --- TAB 1: DASHBOARD ---
with tab_dash:
  st.markdown("### ⏱️ Live-Timer & Dashboard")

  # Cleane Live-Uhr im UI
  current_time_str = time.strftime("%H:%M:%S")
  st.markdown(
      f'<div class="clock-display">🕒 System-Zeit: {current_time_str}</div>',
      unsafe_allow_html=True,
  )

  col1, col2 = st.columns(2, gap="large")

  with col1:
    st.markdown(
        f"""
        <div class="custom-card">
            <h4>Aktive Aktivität: <span style="color: #38bdf8;">{st.session_state.active_lesson}</span></h4>
            <p style="font-size: 1.1rem; margin-top: 10px;">Verdienst-Rate: <b>{st.session_state.current_rate:.2f} € / Min</b></p>
            <hr style="border-color: #334155;">
            <p style="font-size: 1.2rem;">Bereits verdient: <b>{st.session_state.pending_earnings:.2f} €</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
      if st.button("Auszahlen"):
        st.session_state.money += st.session_state.pending_earnings
        st.success(
            f"{st.session_state.pending_earnings:.2f} € ausgezahlt! 💰"
        )
        st.session_state.pending_earnings = 0.0
        st.rerun()
    with c_btn2:
      if st.button("1 Min. arbeiten"):
        st.session_state.pending_earnings += st.session_state.current_rate
        st.session_state.total_earnings += st.session_state.current_rate
        decay_stats()
        st.rerun()

  with col2:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader("💤 Schlaf eintragen")
    sleep_hours = st.number_input(
        "Schlaf in Stunden:", min_value=1.0, max_value=16.0, value=8.0, step=0.5
    )
    if st.button("Schlaf eintragen"):
      recovered = min(100.0, sleep_hours * 12.5)
      st.session_state.sleep = min(100.0, st.session_state.sleep + recovered)
      st.success(f"{sleep_hours} Stunden Schlaf eingetragen!")
      st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    contract_cost = sum(
        v["cost"] for v in st.session_state.contracts.values() if v["active"]
    )
    total_fixed = st.session_state.housing["rent"] + contract_cost

    st.markdown(
        f"""
        <div class="custom-card">
            <p>Tägliche Fixkosten: <b>{total_fixed:.2f} €</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Tag beenden & Abrechnung"):
      tax = st.session_state.pending_earnings * 0.20
      net = st.session_state.pending_earnings - tax - total_fixed
      st.session_state.money += net
      st.session_state.pending_earnings = 0.0
      st.success(
          f"Tag beendet! Netto nach Fixkosten & Steuern: {net:.2f} € (Steuern:"
          f" {tax:.2f} €)"
      )
      st.rerun()

# --- TAB 2: STUNDENPLAN ---
with tab_schedule:
  st.subheader("📚 Stundenplan & Fächer auswählen")
  st.write("Klicke auf ein Fach, um es als aktuelle Aktivität festzulegen:")

  fächer = [
      {"name": "Mathematik", "rate": 0.50},
      {"name": "Physik (LK)", "rate": 0.60},
      {"name": "Informatik", "rate": 0.55},
      {"name": "Geschichte", "rate": 0.40},
      {"name": "Chemie", "rate": 0.50},
      {"name": "Kunst", "rate": 0.35},
      {"name": "Freistunde", "rate": 0.00},
      {"name": "Eigenes Projekt (Zocken/Lernen)", "rate": 0.50},
  ]

  cols = st.columns(3)
  for i, f in enumerate(fächer):
    with cols[i % 3]:
      if st.button(f"{f['name']}\n({f['rate']:.2f} €/m)", key=f"fach_{i}"):
        st.session_state.active_lesson = f["name"]
        st.session_state.current_rate = f["rate"]
        st.success(f'Gewählt: {f["name"]}')
        st.rerun()

# --- TAB 3: SUPERMARKT (ERWEITERT) ---
with tab_shop:
  st.subheader("🛒 Supermarkt — Großes Sortiment")
  col_drink, col_food = st.columns(2)

  with col_drink:
    st.markdown("#### 🥤 Getränke & Energy")
    getränke = [
        {"name": "Red Bull", "price": 2.50, "val": 25},
        {"name": "Club Mate", "price": 1.80, "val": 20},
        {"name": "Monster Energy", "price": 2.20, "val": 30},
        {"name": "Wasser (0.5L)", "price": 0.80, "val": 15},
        {"name": "Eistee", "price": 1.50, "val": 18},
        {"name": "Kaffee to Go", "price": 2.80, "val": 22},
    ]
    for idx, item in enumerate(getränke):
      if st.button(
          f"{item['name']} ({item['price']:.2f} €) — +{item['val']}% Trinken",
          key=f"dr_{idx}",
      ):
        if st.session_state.money >= item["price"]:
          st.session_state.money -= item["price"]
          st.session_state.drink = min(
              100.0, st.session_state.drink + item["val"]
          )
          st.success(f"{item['name']} gekauft!")
          st.rerun()
        else:
          st.error("Nicht genug Geld!")

  with col_food:
    st.markdown("#### 🍔 Essen & Snacks")
    essen = [
        {"name": "Subway Menü", "price": 8.99, "val": 55},
        {"name": "Döner Kebab", "price": 7.50, "val": 45},
        {"name": "Pizza (Ganze)", "price": 6.50, "val": 40},
        {"name": "Schokolade", "price": 1.49, "val": 15},
        {"name": "Bananen (Bund)", "price": 2.10, "val": 20},
        {"name": "Instant Ramen", "price": 1.20, "val": 12},
    ]
    for idx, item in enumerate(essen):
      if st.button(
          f"{item['name']} ({item['price']:.2f} €) — +{item['val']}% Essen",
          key=f"fd_{idx}",
      ):
        if st.session_state.money >= item["price"]:
          st.session_state.money -= item["price"]
          st.session_state.food = min(
              100.0, st.session_state.food + item["val"]
          )
          st.success(f"{item['name']} gekauft!")
          st.rerun()
        else:
          st.error("Nicht genug Geld!")

# --- TAB 4: WOHNUNG ---
with tab_housing:
  st.subheader("🏠 Immobilien-Markt")
  st.info(f"Aktuelle Unterkunft: **{st.session_state.housing['name']}**")

  c_h1, c_h2, c_h3 = st.columns(3)
  with c_h1:
    if st.button("Eltern-Keller (0.00 €)"):
      st.session_state.housing = {"name": "Eltern-Keller", "rent": 0.0}
      st.success("Ins Elternhaus eingezogen!")
      st.rerun()
  with c_h2:
    if st.button("WG-Zimmer (10.00 € / Tag)"):
      st.session_state.housing = {"name": "WG-Zimmer", "rent": 10.0}
      st.success("WG-Zimmer gemietet!")
      st.rerun()
  with c_h3:
    if st.button("Moderne Wohnung (25.00 € / Tag)"):
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

# --- TAB 6: VERTRÄGE (ERWEITERT) ---
with tab_contracts:
  st.subheader("📱 Abos & Verträge verwalten")
  st.write("Verwalte deine täglichen Fixkosten durch Abos und Verträge:")

  for name, data in st.session_state.contracts.items():
    status_text = "🟢 Aktiv" if data["active"] else "🔴 Inaktiv"
    c1, c2 = st.columns([3, 1])
    with c1:
      st.write(
          f"**{name}** — Kosten: **{data['cost']:.2f} € / Tag** | Status:"
          f" {status_text}"
      )
    with c2:
      if data["active"]:
        if st.button(f"Kündigen", key=f"c_off_{name}"):
          st.session_state.contracts[name]["active"] = False
          st.rerun()
      else:
        if st.button(f"Buchen", key=f"c_on_{name}"):
          st.session_state.contracts[name]["active"] = True
          st.rerun()
