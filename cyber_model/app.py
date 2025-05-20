import streamlit as st
import numpy as np
import joblib

# Streamlit başlık ayarları
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

model = None
expected_features = 4  # Varsayılan olarak 4 özelliğimiz var

try:
    model = joblib.load(model_map[model_option])

    # Modelin beklediği giriş boyutunu öğren
    if hasattr(model, 'n_features_in_'):
        expected_features = model.n_features_in_
except Exception as e:
    st.error(f"Model yüklenirken bir hata oluştu: {e}")

# Kullanıcıdan veri al
st.subheader("📥 Girdi Verilerini Girin:")

feature1 = st.slider("Paket Boyutu", 0, 1500, 500)
feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, 200)
feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, 300.0)
feature4 = st.slider("Kaynak Port", 0, 65535, 80)

user_input = [feature1, feature2, feature3, feature4]

if st.button("🔮 Tahmin Et"):
    try:
        # Eksik özellik varsa 0 ile tamamla
        if len(user_input) < expected_features:
            user_input.extend([0] * (expected_features - len(user_input)))

        # Fazlalık varsa kes
        elif len(user_input) > expected_features:
            user_input = user_input[:expected_features]

        features = np.array(user_input).reshape(1, -1)

        # Tahmin
        prediction = model.predict(features)[0]

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

