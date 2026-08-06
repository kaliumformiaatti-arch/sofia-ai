import streamlit as st
import random
import requests
import json

# 1. Sivun asetukset ja upea neon-teema
st.set_page_config(page_title="AI Hahmot", page_icon="💖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0F0C1B; color: #FFFFFF; }
    .user-bubble {
        background-color: #FF2A7A; color: white; padding: 12px 16px;
        border-radius: 20px 20px 0px 20px; margin: 10px 0px;
        max-width: 85%; float: right; clear: both; font-family: sans-serif;
    }
    .bot-bubble {
        background-color: #1F1B2E; color: #F0E6FF; padding: 12px 16px;
        border-radius: 20px 20px 20px 0px; margin: 10px 0px;
        max-width: 85%; float: left; clear: both; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        font-family: sans-serif; border: 1px solid #3D3066;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Haetaan ilmainen Gemini-avain Secretsistä
gemini_key = st.secrets.get("GEMINI_KEY", None)

# Funktio: Pyydetään Geminiltä luonnollista suomen kieltä
def kysy_geminilta(ohje, historia):
    if not gemini_key:
        return "API-avain (GEMINI_KEY) puuttuu kokonaan Streamlit Secrets -asetuksista!"
        
    # TÄMÄ ON SE OIKEOPILLINEN JA TOIMIVA OSOITE KOKONAISUUDESSAAN:
    url = f"https://googleapis.com{gemini_key}"
    headers = {'Content-Type': 'application/json'}
    
    contents = []
    
    # Syötetään hahmon luonne "system-ohjeena" Geminille
    contents.append({"role": "user", "parts": [{"text": f"MÄÄRITELMÄ: {ohje}. Vastaa seuraaviin viesteihin täysin tämän roolin mukaisesti."}]})
    contents.append({"role": "model", "parts": [{"text": "Ymmärretty. Toimin tästä eteenpäin täysin tämän hahmon luonteen mukaisesti luonnollisella suomen kielellä."}]})
    
    for msg in historia:
        rooli = "user" if msg["role"] == "user" else "model"
        contents.append({"role": rooli, "parts": [{"text": msg["content"]}]})
        
    data = {"contents": contents}
    
    try:
        res = requests.post(url, headers=headers, data=json.dumps(data), timeout=15)
        vastaus_json = res.json()
        
        if 'error' in vastaus_json:
            return f"Googlen API-virhe: {vastaus_json['error']['message']} (Koodi: {vastaus_json['error']['code']})"
            
        return vastaus_json['candidates']['content']['parts']['text']
    except Exception as e:
        vastaus_teksti = res.text if 'res' in locals() else 'Ei vastausta palvelimelta'
        return f"Yhteysvirhe: {str(e)} | Palvelimen vastaus: {vastaus_teksti}"

# 3. Alustetaan oletushahmot muistiin
if "hahmot" not in st.session_state:
    st.session_state.hahmot = {
        "Sofia": {
            "ika": 22,
            "kuvaus": "DJ & Valokuvaaja. Suorapuheinen, energinen ja seikkailunhaluinen. Lyhyet platinanvaaleat hiukset.",
            "ohje": "Olet Sofia, 22-vuotias suomalainen DJ ja valokuvaaja. Luonteeltasi olet suorapuheinen, flirttaileva, energinen ja itsevarmasti seikkailunhaluinen. Puhu rentoa suomalaista puhekieltä, käytä nuorekkaita ilmauksia, slangiakin ja paljon emojeita. Älä puhu kirjakieltä tai robottimaisesti.",
            "tervehdys": "Moi! Se on Sofia tässä. Tulin just klubilta kotiin ja keitin kahvit. Mitäs sun päivään kuuluu? Puhutaanko vai tehäänkö jotain kreisiä? ⚡"
        },
        "Emilia": {
            "ika": 24,
            "kuvaus": "Pitkät tummat aaltoilevat hiukset. Suloinen, ujo ja syvällinen pohtija.",
            "ohje": "Olet Emilia, 24-vuotias suomalainen nainen. Olet suloinen, empaattinen, hieman ujo ja tykkäät syvällisistä keskusteluista. Puhu lämpimästi, lempeästi ja aidon oloisesti, kuin puhuisit läheiselle ystävälle.",
            "tervehdys": "Hei... Ihana kun laitoit viestiä. Olin just lukemassa kirjaa ja mietin sinua. Mitä sinulle kuuluu tänään? Kirjoitellaanko hetki? 🌸"
        },
        "Aino": {
            "ika": 27,
            "kuvaus": "Tummanruskeat kiharat hiukset. Itsevarma, salaperäinen ja itsenäinen nainen.",
            "ohje": "Olet Aino, 27-vuotias itsevarma, itsenäinen ja salaperäinen suomalainen nainen. Tykkäät älykkäästä flirttailusta ja haastamisesta. Puhu kiehtovasti, kypsästi ja sopivan itsevarmalla asenteella.",
            "tervehdys": "Iltaa. Mietinkin juuri, milloin mahtaisit ottaa yhteyttä. Toivottavasti päiväsi on ollut yhtä mielenkiintoinen kuin minun. Mitä sinulla on mielessä? ☕"
        }
    }

if "keskustelut" not in st.session_state:
    st.session_state.keskustelut = {}

# 4. SIVUPALKKI: Hahmon valinta ja luominen
st.sidebar.title("👥 Hahmot")
valittu_nimi = st.sidebar.radio("Valitse kenen kanssa keskustelemmat:", list(st.session_state.hahmot.keys()))

st.sidebar.markdown("---")
st.sidebar.subheader("➕ Luo uusi hahmo")
uusi_nimi = st.sidebar.text_input("Nimi:")
uusi_ika = st.sidebar.number_input("Ikä:", min_value=18, max_value=100, value=20)
uusi_kuvaus = st.sidebar.text_area("Kuvaus / Luonne:")

if st.sidebar.button("Luo hahmo"):
    if uusi_nimi and uusi_nimi not in st.session_state.hahmot:
        st.sidebar.success(f"Hahmo {uusi_nimi} luotu!")
        st.session_state.hahmot[uusi_nimi] = {
            "ika": uusi_ika,
            "kuvaus": uusi_kuvaus,
            "ohje": f"Olet {uusi_nimi}, {uusi_ika}-vuotias suomalainen. Luonteenkuvauksesi on: {uusi_kuvaus}. Puhu luonnollista suomea tämän luonteen mukaisesti.",
            "tervehdys": f"Moi! Mä oon {uusi_nimi}. Kiva tutustua suhun! Mitä tehään tänään? ✨"
        }
        st.rerun()

# 5. CHAT-IKKUNA
hahmo = st.session_state.hahmot[valittu_nimi]

if valittu_nimi not in st.session_state.keskustelut:
    st.session_state.keskustelut[valittu_nimi] = [
        {"role": "assistant", "content": hahmo["tervehdys"]}
    ]

st.title(f"🎧 {valittu_nimi} | {hahmo['ika']} v")
st.caption(hahmo["kuvaus"])

for msg in st.session_state.keskustelut[valittu_nimi]:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# 6. VIESTIN LÄHETYS
user_input = st.chat_input(f"Kirjoita hahmolle {valittu_nimi}...")

if user_input:
    st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)
    st.session_state.keskustelut[valittu_nimi].append({"role": "user", "content": user_input})
    
    historia_ilman_kuvia = [{"role": m["role"], "content": m["content"]} for m in st.session_state.keskustelut[valittu_nimi]]
    
    with st.spinner(f"{valittu_nimi} kirjoittaa..."):
        vastaus = kysy_geminilta(hahmo["ohje"], historia_ilman_kuvia)
        
        st.markdown(f'<div class="bot-bubble">{vastaus}</div>', unsafe_allow_html=True)
        st.session_state.keskustelut[valittu_nimi].append({"role": "assistant", "content": vastaus})
            
    st.rerun()
