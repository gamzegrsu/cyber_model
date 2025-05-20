import streamlit as st
import numpy as np
import joblib

# 🌌 Arka plan resmi ekleme
page_bg_img = '''
<style>
body {
    background-image: url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1350&q=80");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: white;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Sayfa yapılandırması
st.set_page_config(page_title="Siber Güvenlik Tahmin", layout="centered")
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

# Girdi alanları
st.subheader("📥 Girdi Verilerini Girin:")

# Örnek verilerle doldur
if st.button("🎲 Örnek Veri ile Doldur"):
    st.session_state["feature1"] = 800
    st.session_state["feature2"] = 3500
    st.session_state["feature3"] = 450.0
    st.session_state["feature4"] = 443

feature1 = st.slider("Paket Boyutu", 0, 1500, st.session_state.get("feature1", 500))
feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, st.session_state.get("feature2", 200))
feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, st.session_state.get("feature3", 300.0))
feature4 = st.slider("Kaynak Port", 0, 65535, st.session_state.get("feature4", 80))

# Eksik kalan özellikleri ortalama değerlerle tamamla (örnek: 11 tane)
remaining_features = [350.0, 0.0, 0.5, 1000.0, 20.0, 50.0, 0.1, 500.0, 1.0, 200.0, 2.0]
all_features = np.array([[feature1, feature2, feature3, feature4] + remaining_features])

# Saldırı türü açıklamaları
attack_type_explanation = {
    0: "Normal trafik (saldırı yok)",
    1: "DoS saldırısı",
    2: "Port tarama",
    3: "MITM (Ortadaki Adam) saldırısı",
    4: "Veri sızdırma",
    5: "Botnet trafiği"
}

# Tahmin butonu
if st.button("🔮 Tahmin Et"):
    try:
        prediction = model.predict(all_features)[0]
        prediction_text = attack_type_explanation.get(prediction, "Bilinmeyen saldırı türü")

        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(all_features)[0]
            st.success(f"📌 Model Tahmini: **{prediction_text}** (Kod: {prediction})")
            st.info(f"📊 Güven Skoru: %{np.max(prob) * 100:.2f}")
        else:
            st.success(f"📌 Model Tahmini: **{prediction_text}** (Kod: {prediction})")
            st.warning("⚠️ Bu model güven skoru (olasılık) sağlamıyor.")
    except Exception as e:
        st.error(f"Tahmin yapılırken bir hata oluştu: {e}")

# Footer
st.markdown("""
---
🧠 Bu uygulama, üç farklı makine öğrenmesi modelini karşılaştırmalı olarak kullanarak canlı tahmin yapmanızı sağlar.  
💡 Not: Tahminlerin doğruluğu modelin eğitim verisine bağlıdır.
""")


