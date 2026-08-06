import streamlit as st
import random
import io
from huggingface_hub import InferenceClient

# 1. Sivun asetukset (Klubi- & DJ-henkinen tumma teema)
st.set_page_config(page_title="Sofia AI", page_icon="🎧", layout="centered")

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

st.title("🎧 Sofia | 22 v")
st.caption("DJ & Valokuvaaja. Suorapuheinen, energinen ja seikkailunhaluinen.")

# Liitä oma hf_... alkaen oleva avaimesi tähän lainausmerkkien sisään
client = InferenceClient(token="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")

# Alustetaan keskusteluhistoria
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Moi! Se on Sofia tässä. Tulin just klubilta kotiin ja keitin kahvit. Mitäs sun päivään kuuluu? Puhutaanko vai tehäänkö jotain kreisiä? ⚡"}
    ]

# Näytetään vanhat viestit
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        if "image_bytes" in msg:
            st.image(msg["image_bytes"], use_container_width=True)

# Viestin syöttö alakulmassa
user_input = st.chat_input("Kirjoita Sofialle...")

if user_input:
    st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    avainsanat = ["kuva", "kuvan", "piirrä", "näytä", "selfie", "photo", "kuvaaj", "kuvaasi"]
    pyysi_kuvaa = any(sana in user_input.lower() for sana in avainsanat)
    
    with st.spinner("Sofia kirjoittaa..."):
        if pyysi_kuvaa:
            vastaus = "Oota hetki, otan nopsaa selfien täältä klubin DJ-kopista! Tässä sä näät mun platinat hiukset ja illan tyylin 😉"
            st.markdown(f'<div class="bot-bubble">{vastaus}</div>', unsafe_allow_html=True)
            
            # Ohjeet kuvan luomiseen
            sofia_prompt = f"A realistic modern selfie of a beautiful 22-year-old Finnish girl, short platinum blonde hair, grey-blue eyes, athletic body, wearing earrings, bold club style clothing, bokeh neon lights background, night club, random={random.randint(1,9999)}"
            
            try:
                # Luodaan kuva käyttäen Flux-mallia virallisen kirjaston kautta
                image = client.text_to_image(sofia_prompt, model="stabilityai/stable-diffusion-xl-base-1.0")
                
                # Muutetaan kuva Streamlitille sopivaan muotoon
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()
                
                st.image(img_bytes, use_container_width=True)
                st.session_state.messages.append({"role": "bot", "content": vastaus, "image_bytes": img_bytes})
            except Exception as e:
                virhe_viesti = "Äh, mun kamera reistaa juuri nyt, palvelin taitaa olla varattu! Kokeile sekunnin päästä uudestaan. 📸"
                st.markdown(f'<div class="bot-bubble">{virhe_viesti}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "bot", "content": virhe_viesti})
        else:
            vastaukset = [
                "Mä oon aina suorapuheinen, joten sanon suoraan: toi sun viesti oli aika kiinnostava! Kerro lisää sun menoista.",
                "Haha, sä oot kyllä hauska! Pitäiskö sun tulla mun seuraavalle keikalle kattoo ku miksaan? 🎧",
                "Seikkailu ois kova sana just nyt. Mut kerro ensin, mikä sut saa syttymään? 🔥"
            ]
            vastaus = random.choice(vastaukset)
            st.markdown(f'<div class="bot-bubble">{vastaus}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "bot", "content": vastaus})
            
    st.rerun()
