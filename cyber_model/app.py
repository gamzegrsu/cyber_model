import streamlit as st
import numpy as np
import joblib
import pandas as pd

# Sayfa ayarları
st.set_page_config(page_title="Siber Güvenlik Tahmin", layout="centered")
st.title("🛡️ Siber Güvenlik Saldırısı Tahmin Aracı")
st.markdown("🎯 Gerçek zamanlı olarak farklı modellerle siber saldırı tahmini yapın.")

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

# Model yükle
try:
    model = joblib.load(model_map[model_option])
except Exception as e:
    st.error(f"Model yüklenirken bir hata oluştu: {e}")

st.subheader("📥 Girdi Verilerini Girin:")

# Kullanıcıdan 4 özellik alınır
feature1 = st.slider("Paket Boyutu", 0, 1500, 500)
feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, 200)
feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, 300.0)
feature4 = st.slider("Kaynak Port", 0, 65535, 80)

# Eğitim verisinden 15 özellik ortalamaları (bunu eğitim sırasında veya veri ön işleme yaparken hesaplamalısın)
feature_means = {
    0: 350,    # packet_count ortalaması
    1: 4500,   # duration ortalaması
    2: 250,    # avg_pkt_size ortalaması
    3: 2000,   # src_port ortalaması
    4: 123,    # Diğer özelliklerin ortalamaları (örnek değerler)
    5: 50,
    6: 10,
    7: 5,
    8: 0,
    9: 1,
    10: 0,
    11: 2,
    12: 7,
    13: 0,
    14: 1
}

# 15 boyutlu özellik vektörü oluştur
features_15 = np.zeros((1, 15))

# İlk 4 gerçek kullanıcı girdisi
features_15[0, 0] = feature1
features_15[0, 1] = feature2
features_15[0, 2] = feature3
features_15[0, 3] = feature4

# Geri kalan 11 özellik ortalama ile dolduruluyor
for i in range(4, 15):
    features_15[0, i] = feature_means.get(i, 0)  # Eğer ortalama yoksa 0

# Tahmin butonu
if st.button("🔮 Tahmin Et"):
    try:
        prediction = model.predict(features_15)[0]
        prob = model.predict_proba(features_15)[0]

        st.success(f"📌 Model Tahmini: **{prediction}**")
        st.info(f"📊 Güven Skoru: %{np.max(prob)*100:.2f}")

    except Exception as e:
        st.error(f"Tahmin yapılırken bir hata oluştu: {e}")

st.markdown("---")
st.caption(f"🔁 Model: {model_option}")

# Footer
st.markdown("""
---
🧠 Bu uygulama, üç farklı makine öğrenmesi modelini karşılaştırmalı olarak kullanarak canlı tahmin yapmanızı sağlar.  
💡 Not: Tahminlerin doğruluğu modelin eğitim verisine bağlıdır.
""")

