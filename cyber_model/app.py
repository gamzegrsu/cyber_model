import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="Siber Güvenlik Tahmin", layout="centered")

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
st.markdown("🎯 Gerçek zamanlı olarak farklı modellerle siber saldırı tahmini yapın.")

with st.expander("ℹ️ Bu Uygulama Ne Yapar?"):
    st.write("""
    Bu araç, ağ trafiği verilerine göre bir bağlantının siber saldırı olup olmadığını **makine öğrenmesi modelleriyle tahmin eder**.

    **Nasıl Kullanılır?**
    1. Model seçin (KNN önerilir).
    2. Aşağıdaki değerleri ayarlayın.
    3. 'Tahmin Et' butonuna tıklayın.

    Sonuç olarak sistem, trafiğin normal mi yoksa saldırı içerikli mi olduğunu gösterir.
    """)

with st.expander("🧾 Özellik Detayları"):
    st.write("""
    - **Paket Boyutu**: Gönderilen veri paketlerinin büyüklüğü. (Byte cinsinden)
    - **Bağlantı Süresi**: İki nokta arasındaki bağlantının süresi. (Milisaniye)
    - **Bayt Hızı**: Birim zamanda aktarılan veri miktarı.
    - **Kaynak Port**: Paketin gönderildiği port numarası.
    - **Ortalama Paketler Arası Süre**: Paketlerin ortalama interarrival zamanı (ms).
    - **Protokol Tipi**: TCP=1, UDP=2, ICMP=3 gibi.
    - **Hedef Port**: Paketin hedef port numarası.
    - **TCP SYN Flag Sayısı**: TCP SYN bayrağı sayısı.
    - **TCP ACK Flag Sayısı**: TCP ACK bayrağı sayısı.
    - **Kaynak IP Blacklist Durumu**: 0 (değil) veya 1 (blacklistte).
    - **Aktif Bağlantı Sayısı**: Aynı IP ile aktif bağlantı sayısı.
    - **Ortalama Paket Boyutu**: Byte cinsinden.
    - **Uygulama Tipi**: HTTP=1, FTP=2 vb.
    - **TCP RST Flag Sayısı**: TCP RST bayrağı sayısı.
    - **Yeniden Deneme Sayısı**: Paket yeniden deneme sayısı.
    """)

model_option = st.selectbox(
    "🔍 Tahmin İçin Model Seç:",
    ("XGBoost", "KNN", "Logistic Regression")
)

model_map = {
    "XGBoost": "./cyber_model/xgb_model.pkl",
    "KNN": "./cyber_model/knn_model.pkl",
    "Logistic Regression": "./cyber_model/lr_model.pkl"
}

try:
    model = joblib.load(model_map[model_option])
except Exception as e:
    st.error(f"Model yüklenirken bir hata oluştu: {e}")
    st.stop()

st.subheader("📥 Girdi Verilerini Girin:")

# Temel 4 özellik
feature1 = st.slider("Paket Boyutu (Byte)", 0, 1500, 500)
feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, 200)
feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, 300.0)
feature4 = st.slider("Kaynak Port", 0, 65535, 80)

# Gelişmiş özellikler
with st.expander("🔧 Gelişmiş Özellikleri Ayarla"):
    feature5 = st.slider("Ortalama Paketler Arası Süre (ms)", 0, 1000, 15)
    feature6 = st.selectbox("Protokol Tipi", [1, 2, 3], format_func=lambda x: {1: "TCP", 2: "UDP", 3: "ICMP"}[x])
    feature7 = st.slider("Hedef Port", 0, 65535, 80)
    feature8 = st.slider("TCP SYN Flag Sayısı", 0, 10, 1)
    feature9 = st.slider("TCP ACK Flag Sayısı", 0, 10, 1)
    feature10 = st.selectbox("Kaynak IP Blacklist Durumu", [0, 1])
    feature11 = st.slider("Aktif Bağlantı Sayısı", 0, 100, 5)
    feature12 = st.slider("Ortalama Paket Boyutu (Byte)", 0, 1500, 500)
    feature13 = st.selectbox("Uygulama Tipi", [1, 2], format_func=lambda x: {1: "HTTP", 2: "FTP"}[x])
    feature14 = st.slider("TCP RST Flag Sayısı", 0, 10, 0)
    feature15 = st.slider("Yeniden Deneme Sayısı", 0, 10, 0)

# Tüm özellikleri birleştir
features = np.array([
    feature1, feature2, feature3, feature4,
    feature5, feature6, feature7, feature8, feature9,
    feature10, feature11, feature12, feature13,
    feature14, feature15
]).reshape(1, -1)

attack_type_explanation = {
    0: "Normal trafik (saldırı yok)",
    1: "DoS saldırısı",
    2: "Port tarama",
    3: "MITM (Ortadaki Adam) saldırısı",
    4: "Veri sızdırma",
    5: "Botnet trafiği"
}

if st.button("🔮 Tahmin Et"):
    try:
        prediction = model.predict(features)[0]
        prediction_text = attack_type_explanation.get(prediction, "Bilinmeyen saldırı türü")

        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(features)[0]
            st.success(f"📌 Model Tahmini: **{prediction_text}** (Kod: {prediction})")
            st.info(f"📊 Güven Skoru: %{np.max(prob) * 100:.2f}")
        else:
            st.success(f"📌 Model Tahmini: **{prediction_text}** (Kod: {prediction})")
            st.warning("⚠️ Bu model güven skoru (olasılık) sağlamıyor.")
    except Exception as e:
        st.error(f"Tahmin yapılırken bir hata oluştu: {e}")

st.markdown("""
---
🧠 Bu uygulama, üç farklı makine öğrenmesi modelini karşılaştırmalı olarak kullanarak canlı tahmin yapmanızı sağlar.  
💡 Not: Tahminlerin doğruluğu modelin eğitim verisine bağlıdır.
""")

