import streamlit as st
import random
from huggingface_hub import InferenceClient

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
    .sidebar .sidebar-content { background-color: #110E24; }
    </style>
""", unsafe_allow_html=True)

# 2. Alustetaan ilmainen tekoäly asiakasohjelma Secrets-avaimella
hf_token = st.secrets.get("HF_TOKEN", None)
client = InferenceClient(token=hf_token)

# 3. Alustetaan oletushahmot muistiin (Kuvasi mukaisesti)
if "hahmot" not in st.session_state:
    st.session_state.hahmot = {
        "Sofia": {
            "ika": 22,
            "kuvaus": "DJ & Valokuvaaja. Suorapuheinen, energinen ja seikkailunhaluinen. Lyhyet platinanvaaleat hiukset.",
            "ohje": "Olet Sofia, 22-vuotias suomalainen DJ ja valokuvaaja. Luonteeltasi olet suorapuheinen, flirttaileva, energinen ja seikkailunhaluinen. Käytä puhekieltä, rentoa suomea ja emojiita.",
            "tervehdys": "Moi! Se on Sofia tässä. Tulin just klubilta kotiin ja keitin kahvit. Mitäs sun päivään kuuluu? Puhutaanko vai tehäänkö jotain kreisiä? ⚡"
        },
        "Emilia": {
            "ika": 24,
            "kuvaus": "Pitkät tummat aaltoilevat hiukset, kirkkaat silmät. Suloinen, ujo ja syvällinen pohtija.",
            "ohje": "Olet Emilia, 24-vuotias suomalainen nainen. Sinulla on pitkät tummat aaltoilevat hiukset. Olet suloinen, hieman ujo, empaattinen ja tykkäät syvällisistä keskusteluista. Puhu ystävällisesti ja lämpimästi.",
            "tervehdys": "Hei... Ihana kun laitoit viestiä. Olin just lukemassa kirjaa ja mietin sinua. Mitä sinulle kuuluu tänään? Kirjoitellaanko hetki? 🌸"
        },
        "Aino": {
            "ika": 27,
            "kuvaus": "Tummanruskeat kiharat hiukset. Itsevarma, salaperäinen ja itsenäinen nainen.",
            "ohje": "Olet Aino, 27-vuotias itsevarma ja salaperäinen suomalainen nainen. Olet itsenäinen, hieman arvoituksellinen ja pidät älykkäästä haastamisesta. Puhu itsevarmasti ja kiehtovasti.",
            "tervehdys": "Iltaa. Mietinkin juuri, milloin mahtaisit ottaa yhteyttä. Toivottavasti päiväsi on ollut yhtä mielenkiintoinen kuin minun. Mitä sinulla on mielessä? ☕"
        }
    }

# 4. Alustetaan chat-historioiden säilytys jokaiselle hahmolle erikseen
if "keskustelut" not in st.session_state:
    st.session_state.keskustelut = {}

# 5. SIVUPALKKI: Hahmojen valinta ja uuden luominen (Kuten esimerkkikuvassasi)
st.sidebar.title("👥 Hahmot")
valittu_nimi = st.sidebar.radio("Valitse kenen kanssa keskustelemat:", list(st.session_state.hahmot.keys()))

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
            "ohje": f"Olet {uusi_nimi}, {uusi_ika}-vuotias suomalainen. Luonteenkuvauksesi on: {uusi_kuvaus}. Puhu suomeksi luonteesi mukaisesti.",
            "tervehdys": f"Moi! Mä oon {uusi_nimi}. Kiva tutustua suhun! Mitä tehään tänään? ✨"
        }
        st.rerun()

# 6. AKTIVISEN HAHMON ALUSTUS CHATTIIN
hahmo = st.session_state.hahmot[valittu_nimi]

if valittu_nimi not in st.session_state.keskustelut:
    st.session_state.keskustelut[valittu_nimi] = [
        {"role": "assistant", "content": hahmo["tervehdys"]}
    ]

# Näytetään valitun hahmon tiedot ylhäällä
st.title(f"🎧 {valittu_nimi} | {hahmo['ika']} v")
st.caption(hahmo["kuvaus"])

# Näytetään valitun hahmon keskusteluhistoria muistista
for msg in st.session_state.keskustelut[valittu_nimi]:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# 7. TEKSTINSYÖTTÖ JA TEKOÄLYN ÄLYKÄS VASTAUS
user_input = st.chat_input(f"Kirjoita hahmolle {valittu_nimi}...")

if user_input:
    st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)
    st.session_state.keskustelut[valittu_nimi].append({"role": "user", "content": user_input})
    
    with st.spinner(f"{valittu_nimi} miettii vastausta..."):
        try:
            # Luodaan tekoälyä varten viestijono, joka sisältää hahmon rooliohjeen (System prompt)
            api_messages = [{"role": "system", "content": hahmo["ohje"]}]
            
            # Lisätään mukaan aiemmat viestit muistista, jotta hahmo muistaa mistä puhuttiin
            for m in st.session_state.keskustelut[valittu_nimi]:
                api_messages.append({"role": m["role"], "content": m["content"]})
                
            # Pyydetään älykäs suomenkielinen vastaus Hugging Facelta
            response = client.chat_completion(
                model="Qwen/Qwen2.5-7B-Instruct",
                messages=api_messages,
                max_tokens=150,
                temperature=0.7
            )
            
            vastaus = response.choices[0].message.content
            
            st.markdown(f'<div class="bot-bubble">{vastaus}</div>', unsafe_allow_html=True)
            st.session_state.keskustelut[valittu_nimi].append({"role": "assistant", "content": vastaus})
            
        except Exception as e:
            virhe = f"Äh, mun ajatukset pätkii just nyt! Kokeile lähettää viesti uudestaan. 💕 (Virhe: {e})"
            st.markdown(f'<div class="bot-bubble">{virhe}</div>', unsafe_allow_html=True)
            st.session_state.keskustelut[valittu_nimi].append({"role": "assistant", "content": virhe})
            
    st.rerun()
