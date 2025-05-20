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
    "XGBoost": "xgb_model.pkl",  
    "KNN": "knn_model.pkl",
    "Logistic Regression": "lr_model.pkl"
}

# Modeli yükleme
try:
    model = joblib.load(model_map[model_option])
    st.write(f"Modelin beklediği özellik sayısı: {model.n_features_in_}")
except Exception as e:
    st.error(f"Model yüklenirken bir hata oluştu: {e}")

# Kullanıcıdan alınacak özellikler
feature1 = st.slider("Paket Boyutu", 0, 1500, 500)
feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, 200)
feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, 300.0)
feature4 = st.slider("Kaynak Port", 0, 65535, 80)
# Diğer özellikler (5'ten 15'e kadar özellikleri de ekleyin)
feature5 = st.slider("Özellik 5", 0, 1000, 100)
feature6 = st.slider("Özellik 6", 0, 1000, 150)
feature7 = st.slider("Özellik 7", 0, 1000, 200)
feature8 = st.slider("Özellik 8", 0, 1000, 250)
feature9 = st.slider("Özellik 9", 0, 1000, 300)
feature10 = st.slider("Özellik 10", 0, 1000, 350)
feature11 = st.slider("Özellik 11", 0, 1000, 400)
feature12 = st.slider("Özellik 12", 0, 1000, 450)
feature13 = st.slider("Özellik 13", 0, 1000, 500)
feature14 = st.slider("Özellik 14", 0, 1000, 550)
feature15 = st.slider("Özellik 15", 0, 1000, 600)

# Özellikleri tek bir satırda birleştiriyoruz
features = np.array([[feature1, feature2, feature3, feature4, feature5, feature6, feature7, feature8, feature9, feature10,
                      feature11, feature12, feature13, feature14, feature15]])

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

