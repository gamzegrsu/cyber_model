import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Streamlit ayarları
st.set_page_config(page_title="Siber Güvenlik Tahmin", layout="centered")
st.title("🛡️ Siber Güvenlik Saldırısı Tahmin Aracı")
st.markdown("🎯 Gerçek zamanlı olarak farklı modellerle siber saldırı tahmini yapın.")

# Model seçimi
model_option = st.selectbox(
    "🔍 Tahmin İçin Model Seç:",
    ("XGBoost", "KNN", "Logistic Regression")
)

# Modeli yükle
model_map = {
    "XGBoost": "xgb_model.pkl",
    "KNN": "knn_model.pkl",
    "Logistic Regression": "lr_model.pkl"
}
model = joblib.load(model_map[model_option])

st.subheader("📥 Girdi Verilerini Girin:")

# Örnek özellikler (senin veri setine göre özelleştir!)
# Aşağıdakileri kendi veri sütunlarına göre güncelleyebilirsin
feature1 = st.slider("Paket Boyutu", 0, 1500, 500)
feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, 200)
feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, 300.0)
feature4 = st.slider("Kaynak Port", 0, 65535, 80)

# Özellikleri tek satır haline getir
features = np.array([[feature1, feature2, feature3, feature4]])

# Tahmin
if st.button("🔮 Tahmin Et"):
    prediction = model.predict(features)[0]
    prob = model.predict_proba(features)[0]

    st.success(f"📌 Model Tahmini: **{prediction}**")
    st.info(f"📊 Güven Skoru: %{np.max(prob)*100:.2f}")

    st.markdown("---")
    st.caption("🔁 Model: {}".format(model_option))

# Footer
st.markdown("""
---
🧠 Bu uygulama, dört farklı makine öğrenmesi modelini karşılaştırmalı olarak kullanarak canlı tahmin yapmanızı sağlar.
💡 Not: Tahminlerin doğruluğu modelin eğitim verisine bağlıdır.
""")
