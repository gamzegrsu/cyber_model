import streamlit as st
import numpy as np
import joblib

# Sayfa yapılandırması - En başta olmalı
st.set_page_config(page_title="Siber Güvenlik Tahmin", layout="centered")

# CSS ile arka plan ve yazı renkleri
page_bg_img = '''
<style>
body {
    background-image: url("https://cdn.pixabay.com/photo/2017/05/10/15/20/hacker-2300772_960_720.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: black;
}
.stSlider > div > div > div > div {
    border: 2px solid black;
    border-radius: 5px;
}
.stButton>button {
    background-color: white;
    color: red;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #f0f0f0;
    color: darkred;
}
.stAlertSuccess {
    background-color: #1f4e18 !important;
    color: black !important;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

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

# Örnek veri ile doldurma butonu
if st.button("🎲 Örnek Veri ile Doldur"):
    st.session_state["feature1"] = 800
    st.session_state["feature2"] = 3500
    st.session_state["feature3"] = 450.0
    st.session_state["feature4"] = 443

# Özellik girişleri (sliderlar)
feature1 = st.slider("Paket Boyutu (Byte)", 0, 1500, st.session_state.get("feature1", 500))
feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, st.session_state.get("feature2", 200))
feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, st.session_state.get("feature3", 300.0))
feature4 = st.slider("Kaynak Port", 0, 65535, st.session_state.get("feature4", 80))

features = np.array([[feature1, feature2, feature3, feature4]])

# Özellik açıklama fonksiyonları
def paket_boyu_aciklama(deger):
    if deger <= 200:
        return "Küçük paket boyutu (genellikle normal trafik)"
    elif deger <= 1000:
        return "Orta boy paket"
    else:
        return "Büyük paket boyutu (şüpheli olabilir)"

def baglanti_suresi_aciklama(deger):
    if deger <= 100:
        return "Çok hızlı bağlantı (normal)"
    elif deger <= 500:
        return "Orta hız"
    else:
        return "Yavaş bağlantı (sorun olabilir)"

def bayt_hizi_aciklama(deger):
    if deger <= 200:
        return "Düşük hız"
    elif deger <= 700:
        return "Orta hız"
    else:
        return "Yüksek hız (şüpheli)"

def kaynak_port_aciklama(deger):
    if deger <= 1023:
        return "Sistem portu (HTTP, HTTPS gibi)"
    elif deger <= 49151:
        return "Kayıtlı port"
    else:
        return "Dinamik/Özel port"

# Özellik açıklamalarını göster
st.markdown("### 📊 Özellik Açıklamaları")
st.write(f"📦 Paket Boyutu: {paket_boyu_aciklama(feature1)}")
st.write(f"⏱ Bağlantı Süresi: {baglanti_suresi_aciklama(feature2)}")
st.write(f"📈 Bayt Hızı: {bayt_hizi_aciklama(feature3)}")
st.write(f"🔢 Kaynak Port: {kaynak_port_aciklama(feature4)}")

# Genel yorum
st.markdown("### 🧠 Genel Trafik Yorumu")
if feature1 > 1000 and feature2 < 200 and feature3 > 700:
    st.warning("⚠️ Bu parametreler DDoS saldırısı belirtisi olabilir!")
elif feature1 < 300 and feature2 > 500:
    st.info("ℹ️ Normal veya düşük trafik olabilir.")
else:
    st.success("✅ Trafik durumu net değil, dikkatle analiz edin.")

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
        prediction = model.predict(features)[0]
        prediction_text = attack_type_explanation.get(prediction, "Bilinmeyen saldırı türü")

        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(features)[0]
            st.success(f"📌 Model Tahmini: **{prediction_text}** (Kod: {prediction})", icon="✅")
            st.info(f"📊 Güven Skoru: %{np.max(prob) * 100:.2f}")
        else:
            st.success(f"📌 Model Tahmini: **{prediction_text}** (Kod: {prediction})", icon="✅")
            st.warning("⚠️ Bu model güven skoru (olasılık) sağlamıyor.")
    except Exception as e:
        st.error(f"Tahmin yapılırken bir hata oluştu: {e}")

# Footer
st.markdown("""
---
🧠 Bu uygulama, üç farklı makine öğrenmesi modelini karşılaştırmalı olarak kullanarak canlı tahmin yapmanızı sağlar.  
💡 Not: Tahminlerin doğruluğu modelin eğitim verisine bağlıdır.
""")

