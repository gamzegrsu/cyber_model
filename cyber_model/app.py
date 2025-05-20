import os
import streamlit as st
import joblib
import numpy as np

# Streamlit ayarları
st.set_page_config(page_title="Siber Güvenlik Tahmin", layout="centered")
st.title("🛡️ Siber Güvenlik Saldırısı Tahmin Aracı")
st.markdown("🎯 Gerçek zamanlı olarak farklı modellerle siber saldırı tahmini yapın.")

# Model seçimi
model_option = st.selectbox(
    "🔍 Tahmin İçin Model Seç:",
    ("XGBoost", "KNN", "Logistic Regression")
)

# Model dosyasının yolu
model_map = {
    "XGBoost": "cyber_model/xgb_model.pkl",  # Eğer Streamlit bulut platformu veya başka bir ortamda çalışıyorsa tam yolu kullanın
    "KNN": "cyber_model/knn_model.pkl",
    "Logistic Regression": "cyber_model/lr_model.pkl"
}

# Modeli yükleme
try:
    if os.path.exists(model_map[model_option]):  # Dosyanın var olup olmadığını kontrol et
        model = joblib.load(model_map[model_option])
    else:
        st.error("Model dosyası bulunamadı.")
except Exception as e:
    st.error(f"Model yüklenirken bir hata oluştu: {e}")

st.subheader("📥 Girdi Verilerini Girin:")

# Özellikler: Kullanıcıdan veri alıyoruz
feature1 = st.slider("Paket Boyutu", 0, 1500, 500)
feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, 200)
feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, 300.0)
feature4 = st.slider("Kaynak Port", 0, 65535, 80)

# Özellikleri tek satır haline getir
features = np.array([[feature1, feature2, feature3, feature4]])

# Tahmin
if st.button("🔮 Tahmin Et"):
    try:
        prediction = model.predict(features)[0]
        prob = model.predict_proba(features)[0]
        
        # Tahmin Sonuçları
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
