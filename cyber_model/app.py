import streamlit as st
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

# Model dosyalarını yükle
model_map = {
    "XGBoost": "./cyber_model/xgb_model.pkl",
    "KNN": "./cyber_model/knn_model.pkl",
    "Logistic Regression": "./cyber_model/lr_model.pkl"
}

# Modeli yükleme
try:
    model = joblib.load(model_map[model_option])
except Exception as e:
    st.error(f"Model yüklenirken bir hata oluştu: {e}")

st.subheader("📥 Girdi Verilerini Girin:")

# 4 Özellik: Kullanıcıdan veri alıyoruz
feature1 = st.slider("Paket Boyutu", 0, 1500, 500)
feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, 200)
feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, 300.0)
feature4 = st.slider("Kaynak Port", 0, 65535, 80)

# Kullanıcı girdilerini dizi olarak al
user_input = [feature1, feature2, feature3, feature4]

# Tahmin
if st.button("🔮 Tahmin Et"):
    try:
        # Modelin beklediği özellik sayısını kontrol et
        expected_features = model.n_features_in_  # sklearn ve xgboost uyumludur
        eksik_sayi = expected_features - len(user_input)

        # Eksik varsa, 0 ile tamamla
        if eksik_sayi > 0:
            user_input.extend([0] * eksik_sayi)

        # Numpy array'e çevir
        features = np.array(user_input).reshape(1, -1)

        # Tahmin yap
        prediction = model.predict(features)[0]

        # Olasılık varsa yaz
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(features)[0]
            st.success(f"📌 Model Tahmini: **{prediction}**")
            st.info(f"📊 Güven Skoru: %{np.max(prob)*100:.2f}")
        else:
            st.success(f"📌 Model Tahmini: **{prediction}**")
            st.info("⚠️ Bu model olasılık değeri sağlamıyor.")

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
