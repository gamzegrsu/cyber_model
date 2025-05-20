import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="Siber Güvenlik Tahmin Aracı", layout="centered")
st.title("🛡️ Siber Güvenlik Saldırısı Tahmin Aracı")
st.markdown("🎯 Gerçek zamanlı olarak farklı modellerle siber saldırı tahmini yapın.")

with st.expander("ℹ️ Bu Uygulama Ne Yapar?"):
    st.write("""
    Bu araç, ağ trafiği verilerine göre bir bağlantının siber saldırı olup olmadığını **üç farklı makine öğrenmesi modeliyle** tahmin eder.
    """)

with st.expander("🧾 Özellik Detayları"):
    st.write("""
    - **Paket Boyutu**: Gönderilen veri paketlerinin büyüklüğü. (Byte)
    - **Bağlantı Süresi**: İki nokta arasındaki bağlantının süresi. (ms)
    - **Bayt Hızı**: Birim zamanda aktarılan veri miktarı.
    - **Kaynak Port**: Paketin gönderildiği port numarası.
    """)

# Model yolları
model_paths = {
    "XGBoost": "./cyber_model/xgb_model.pkl",
    "Logistic Regression": "./cyber_model/lr_model.pkl",
    "KNN": "./cyber_model/knn_model.pkl"
}

# Modelleri yükle
models = {}
for name, path in model_paths.items():
    try:
        models[name] = joblib.load(path)
    except Exception as e:
        st.warning(f"{name} yüklenemedi: {e}")

# Giriş verileri
st.subheader("📥 Girdi Verilerini Girin:")

if st.button("🎲 Örnek Veri ile Doldur"):
    st.session_state["feature1"] = 800
    st.session_state["feature2"] = 3500
    st.session_state["feature3"] = 450.0
    st.session_state["feature4"] = 443

feature1 = st.slider("Paket Boyutu", 0, 1500, st.session_state.get("feature1", 500))
feature2 = st.slider("Bağlantı Süresi (ms)", 0, 10000, st.session_state.get("feature2", 200))
feature3 = st.slider("Bayt Hızı", 0.0, 1000.0, st.session_state.get("feature3", 300.0))
feature4 = st.slider("Kaynak Port", 0, 65535, st.session_state.get("feature4", 80))

# Geri kalan 11 özelliği ortalama değerlerle dolduralım
average_values = [60, 0, 0, 1, 1, 0, 0, 1, 100, 50, 10]  # örnek makul değerler
full_features = np.array([[feature1, feature2, feature3, feature4] + average_values])

attack_labels = {
    0: "Normal trafik (saldırı yok)",
    1: "DoS saldırısı",
    2: "Port tarama",
    3: "MITM (Ortadaki Adam) saldırısı",
    4: "Veri sızdırma",
    5: "Botnet trafiği"
}

# Tahmin karşılaştırması
if st.button("🔍 Modelleri Karşılaştır"):
    for model_name, model in models.items():
        try:
            pred = model.predict(full_features)[0]
            label = attack_labels.get(pred, "Bilinmeyen saldırı")

            st.markdown(f"### 🔎 {model_name}")
            st.success(f"📌 Tahmin: **{label}** (Kod: {pred})")
            if hasattr(model, "predict_proba"):
                prob = model.predict_proba(full_features)[0]
                st.info(f"📊 Güven Skoru: %{np.max(prob) * 100:.2f}")
            else:
                st.warning("⚠️ Bu model olasılık sağlamıyor.")
        except Exception as e:
            st.error(f"{model_name} için tahmin hatası: {e}")

st.markdown("---")
st.markdown("🧠 Bu uygulama, üç farklı modeli karşılaştırmalı olarak kullanır. En doğru sonucu genellikle **XGBoost** sağlar.")


