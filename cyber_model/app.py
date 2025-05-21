import streamlit as st
import numpy as np
import joblib

# Sayfa yapılandırması (en başta olmalı)
st.set_page_config(page_title="Siber Güvenlik Tahmin", layout="centered")

# CSS ile stil ayarları
st.markdown("""
<style>
    .stButton>button {
        background-color: white;
        color: red;
        font-weight: bold;
        border: 2px solid black;
    }
    .stSlider>div>div>div>input {
        accent-color: black;
    }
    .prediction-box {
        background-color: #a3d9a5; /* Daha koyu yeşil */
        color: black !important;    /* Yazı siyah */
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        border: 2px solid #4a7c4a; /* koyu yeşil çerçeve */
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Siber Güvenlik Saldırısı Tahmin Aracı")
st.markdown("🎯 Gerçek zamanlı olarak farklı modellerle siber saldırı tahmini yapın.")

# Model seçimi ve yükleme kısmı (örnek)
model_option = st.selectbox("🔍 Tahmin İçin Model Seç:", ("XGBoost", "KNN", "Logistic Regression"))

model_map = {
    "XGBoost": "./cyber_model/xgb_model.pkl",
    "KNN": "./cyber_model/knn_model.pkl",
    "Logistic Regression": "./cyber_model/lr_model.pkl"
}

try:
    model = joblib.load(model_map[model_option])
except Exception as e:
    st.error(f"Model yüklenirken hata oluştu: {e}")
    st.stop()

# Özellik girişleri (örnek 4 özellik)
feature1 = st.slider("Paket Boyutu", 0, 1500, 500)
feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, 200)
feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, 300.0)
feature4 = st.slider("Kaynak Port", 0, 65535, 80)

# Geri kalan 11 özellik ortalama değerlerle doldurulur
extra_features = [100, 500, 50, 5, 10, 0, 0, 2, 1, 1, 0]

features = np.array([[feature1, feature2, feature3, feature4] + extra_features])

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
            st.markdown(f"""
            <div class="prediction-box">
                📌 Model Tahmini: {prediction_text} (Kod: {prediction})<br>
                📊 Güven Skoru: %{np.max(prob) * 100:.2f}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="prediction-box">
                📌 Model Tahmini: {prediction_text} (Kod: {prediction})<br>
                ⚠️ Bu model güven skoru (olasılık) sağlamıyor.
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Tahmin yapılırken bir hata oluştu: {e}")


