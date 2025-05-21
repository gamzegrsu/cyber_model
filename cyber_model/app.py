import streamlit as st
import numpy as np
import joblib

# Sayfa yapılandırması (EN ÖNEMLİ: set_page_config en üstte olmalı)
st.set_page_config(page_title="Siber Güvenlik Tahmin", layout="centered")

# Arka plan ve yazı rengi için CSS
st.markdown(
    """
    <style>
    body {
        background-image: url("https://media.giphy.com/media/XIqCQx02E1U9W/giphy.gif");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
        color: black;  /* Sayfa genel yazı rengi siyah */
    }

    .stApp {
        background-color: rgba(255, 255, 255, 0.5);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
        color: black; /* Kutudaki yazılar da siyah */
    }

    h1, h2, h3, h4, h5, h6, label, button, .st-bx {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛡️ Siber Güvenlik Saldırısı Tahmin Aracı")
st.markdown("🎯 Gerçek zamanlı olarak farklı modellerle siber saldırı tahmini yapın.")

# Yardımcı Bilgi Kutusu
with st.expander("ℹ️ Bu Uygulama Ne Yapar?"):
    st.write("""
    Bu araç, ağ trafiği verilerine göre bir bağlantının siber saldırı olup olmadığını **makine öğrenmesi modelleriyle tahmin eder**.
    
    **Nasıl Kullanılır?**
    1. Model seçin (XGBoost önerilir).
    2. Aşağıdaki değerleri ayarlayın.
    3. 'Tahmin Et' butonuna tıklayın.
    
    Sonuç olarak sistem, trafiğin normal mi yoksa saldırı içerikli mi olduğunu gösterir.
    """)

# Özellik açıklamaları
with st.expander("🧾 Özellik Detayları"):
    st.write("""
    - **Paket Boyutu**: Gönderilen veri paketlerinin büyüklüğü. (Byte cinsinden)
    - **Bağlantı Süresi**: İki nokta arasındaki bağlantının süresi. (Milisaniye)
    - **Bayt Hızı**: Birim zamanda aktarılan veri miktarı.
    - **Kaynak Port**: Paketin gönderildiği port numarası.
    """)

# Model seçimi
model_option = st.selectbox(
    "🔍 Tahmin İçin Model Seç:",
    ("XGBoost", "KNN", "Logistic Regression")
)

# Model dosya yolları
model_map = {
    "XGBoost": "./cyber_model/xgb_model.pkl",
    "KNN": "./cyber_model/knn_model.pkl",
    "Logistic Regression": "./cyber_model/lr_model.pkl"
}

# Model yükleme
try:
    model = joblib.load(model_map[model_option])
except Exception as e:
    st.error(f"Model yüklenirken bir hata oluştu: {e}")
    st.stop()

st.subheader("📥 Girdi Verilerini Girin:")

# Sliderlar ile 4 ana özellik alınıyor
feature1 = st.slider("Paket Boyutu", 0, 1500, 500)
feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, 200)
feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, 300.0)
feature4 = st.slider("Kaynak Port", 0, 65535, 80)

# Kalan 11 özellik (örnek ortalama değerler ile dolduruluyor)
# Burada gerçekçi varsayılan değerler kullanılmıştır.
extra_features = np.array([
    50,    # feature5
    0.5,   # feature6
    100,   # feature7
    0,     # feature8
    0,     # feature9
    0.1,   # feature10
    20,    # feature11
    1,     # feature12
    0,     # feature13
    0,     # feature14
    0.05   # feature15
])

# Tüm özellikleri birleştir
features = np.concatenate((np.array([feature1, feature2, feature3, feature4]), extra_features))
features = features.reshape(1, -1)

# Saldırı türü açıklamaları
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


