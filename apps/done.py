import streamlit as st

def app():
    st.markdown('<div class="gray-box"><h2>✅ Proses Selesai</h2></div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="gray-box">
            <h4>Terima kasih telah menggunakan aplikasi prediksi harga saham di indonesia menggunakan metode XGBoost yang dioptimasi dengan APSO.</h4>
            <p>Silakan kembali ke halaman sebelumnya untuk mengeksplorasi ulang atau memulai prediksi baru dengan dataset lain.</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Kembali ke Halaman Awal"):
        st.session_state.page = "🏠 **1. Home**"
