import streamlit as st
import pandas as pd

def create_lag_features(df, n_lag):
    df_lagged = df[['Tanggal', 'Terakhir']].copy()
    for i in range(1, n_lag + 1):
        df_lagged[f'lag_{i}'] = df_lagged['Terakhir'].shift(i)
    df_lagged = df_lagged.dropna().reset_index(drop=True)
    return df_lagged

def app():
    st.markdown('<div class="gray-box"><h2>Pilih Lag Terbaik</h2></div>', unsafe_allow_html=True)

    if 'df' in st.session_state:
        df = st.session_state.df.copy()

        n_lag = st.slider("Pilih jumlah lag (1-30):", min_value=1, max_value=30, value=0)

        df_lagged = create_lag_features(df, n_lag)
        st.session_state.df_lagged = df_lagged  # Simpan untuk modeling

        st.markdown('<div class="gray-box"><h4>Data Saham dengan Lag:</h4></div>', unsafe_allow_html=True)
        st.dataframe(df_lagged.head(20), use_container_width=True)

        if st.button("Next"):
            st.session_state.page = "⚙️ **5. Modeling XGBoost-APSO**"
    else:
        st.warning("Silakan unggah data terlebih dahulu pada halaman sebelumnya.")
