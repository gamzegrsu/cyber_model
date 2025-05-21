import streamlit as st
import numpy as np
import joblib

# Sayfa ayarları
st.set_page_config(page_title="Siber Güvenlik Tahmin", layout="centered")

# Arka plan ve stil
st.markdown(
    """
    <style>
    body {
        background-image: url("https://media.giphy.com/media/XIqCQx02E1U9W/giphy.gif");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
        color: black;
    }
    .stApp {
        background-color: rgba(255, 255, 255, 0.5);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
        color: black;
        border: 3px solid black;
    }
    h1, h2, h3, h4, h5, h6, label, button, .st-bx {
        color: black !important;
    }
    div.stButton > button {
        background-color: white;
        color: red;
        font-weight: bold;
        border: 2px solid red;
        border-radius: 6px;
        padding: 8px 20px;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #ffcccc;
        color: darkred;
        border-color: darkred;
        cursor: pointer;
    }
    .stAlert > div[role="alert"] {
        border-left: 5px solid black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛡️ Siber Güvenlik Saldırısı Tahmin Aracı")
st.markdown("🎯 Gerçek zamanlı olarak KNN veya XGBoost modeliyle siber saldırı tahmini yapın.")

with st.expander("ℹ️ Bu Uygulama Ne Yapar?"):
    st.write("""
    Bu araç, ağ trafiği verilerine göre bir bağlantının siber saldırı olup olmadığını **seçtiğiniz makine öğrenmesi modeliyle** tahmin eder.

    **Nasıl Kullanılır?**
    1. Aşağıdaki değerleri ayarlayın.
    2. Kullanmak istediğiniz modeli seçin.
    3. 'Tahmin Et' butonuna tıklayın.
    """)

with st.expander("🧾 Özellik Detayları"):
    st.write("""
    - **Paket Boyutu**, **Bağlantı Süresi**, **Bayt Hızı**, **Portlar**, TCP bayrakları vb. toplam 15 özellik kullanılır.
    """)

# MODELLERİ YÜKLE
try:
    knn_model = joblib.load("knn_model.pkl")
    xgb_model = joblib.load("xgboost_model.pkl")
except Exception as e:
    st.error(f"Model(ler) yüklenemedi: {e}")
    st.stop()

# Kullanıcıdan özellik girişi
st.subheader("📥 Girdi Verilerini Girin:")

col1, col2 = st.columns(2)

with col1:
    feature1 = st.slider("Paket Boyutu (Byte)", 0, 1500, 500)
    feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, 200)
    feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, 300.0)
    feature4 = st.slider("Kaynak Port", 0, 65535, 80)
    feature5 = st.slider("Ortalama Paketler Arası Süre", 0, 1000, 15)
    feature6 = st.selectbox("Protokol Tipi", [1, 2, 3], format_func=lambda x: {1: "TCP", 2: "UDP", 3: "ICMP"}[x])
    feature7 = st.slider("Hedef Port", 0, 65535, 80)
    feature8 = st.slider("TCP SYN Flag Sayısı", 0, 10, 1)

with col2:
    feature9 = st.slider("TCP ACK Flag Sayısı", 0, 10, 1)
    feature10 = st.selectbox("Blacklist Durumu", [0, 1], format_func=lambda x: "Blacklistte" if x == 1 else "Normal")
    feature11 = st.slider("Aktif Bağlantı Sayısı", 0, 100, 5)
    feature12 = st.slider("Ortalama Paket Boyutu", 0, 1500, 500)
    feature13 = st.selectbox("Uygulama Tipi", [1, 2], format_func=lambda x: {1: "HTTP", 2: "FTP"}[x])
    feature14 = st.slider("TCP RST Flag Sayısı", 0, 10, 0)
    feature15 = st.slider("Yeniden Deneme Sayısı", 0, 10, 0)

features = np.array([
    feature1, feature2, feature3, feature4, feature5, feature6, feature7, feature8,
    feature9, feature10, feature11, feature12, feature13, feature14, feature15
]).reshape(1, -1)

# Model seçimi
model_choice = st.selectbox("🧠 Kullanmak İstediğiniz Modeli Seçin:", ["KNN", "XGBoost"])

# Saldırı açıklamaları
attack_type_explanation = {
    0: "Normal trafik (saldırı yok)",
    1: "DoS saldırısı",
    2: "Port tarama",
    3: "MITM (Ortadaki Adam) saldırısı",
    4: "Veri sızdırma",
    5: "Botnet trafiği"
}

# Tahmin
if st.button("🔮 Tahmin Et"):
    try:
        if model_choice == "KNN":
            prediction = knn_model.predict(features)[0]
            st.warning("⚠️ KNN modeli güven skoru (olasılık) sağlamaz.")
        else:
            prediction = xgb_model.predict(features)[0]
            probability = xgb_model.predict_proba(features)[0]
            st.info(f"🔎 Güven Skoru (XGBoost): {max(probability)*100:.2f}%")

        prediction_text = attack_type_explanation.get(prediction, "Bilinmeyen saldırı türü")
        st.success(f"📌 Model Tahmini: **{prediction_text}** (Kod: {prediction})")

    except Exception as e:
        st.error(f"Tahmin sırasında hata oluştu: {e}")

# Alt bilgi
st.markdown("""
---
🧠 Bu uygulama KNN ve XGBoost modelleriyle canlı tahmin yapar.  
📊 XGBoost modeli güven skoru verir, KNN vermez.  
💡 Not: Tahminlerin doğruluğu eğitim verisine ve özellik mühendisliğine bağlıdır.
""")


