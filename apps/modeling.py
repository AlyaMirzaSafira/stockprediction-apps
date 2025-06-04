import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb

def app():
    st.markdown('<div class="gray-box"><h2>Modeling XGBoost - APSO</h2></div>', unsafe_allow_html=True)

    if 'df_lagged' in st.session_state:
        df_lagged = st.session_state.df_lagged.copy()

        # Pemisahan fitur dan target
        X = df_lagged.drop(columns=['Tanggal', 'Terakhir'])
        y = df_lagged['Terakhir']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )

        # Form input hyperparameter
        st.markdown('<div class="gray-box"><h4>Input Hyperparameter XGBoost</h4></div>', unsafe_allow_html=True)
        n_estimators = st.number_input("n_estimators", min_value=100, max_value=200, value=150, step=10)
        max_depth = st.number_input("max_depth", min_value=3, max_value=5, value=4, step=1)
        learning_rate = st.number_input("learning_rate", min_value=0.01, max_value=1.0, value=0.1, step=0.01, format="%.3f")
        subsample = st.number_input("subsample", min_value=0.5, max_value=1.0, value=1.0, step=0.1, format="%.1f")
        colsample_bytree = st.number_input("colsample_bytree", min_value=0.5, max_value=1.0, value=0.7, step=0.1, format="%.1f")
        min_split_loss = st.number_input("min_split_loss", min_value=1.0, max_value=5.0, value=3.0, step=0.1)
        reg_alpha = st.number_input("reg_alpha", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
        reg_lambda = st.number_input("reg_lambda", min_value=0.0, max_value=10.0, value=5.0, step=0.1)

        if st.button("Train Model"):
            model = xgb.XGBRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                subsample=subsample,
                colsample_bytree=colsample_bytree,
                gamma=min_split_loss,
                reg_alpha=reg_alpha,
                reg_lambda=reg_lambda,
                objective='reg:squarederror'
            )
            model.fit(X_train, y_train)

            # Simpan model dan data untuk halaman berikutnya
            st.session_state.model = model
            st.session_state.final_model = model
            st.session_state.X_train = X_train
            st.session_state.X_test = X_test
            st.session_state.y_train = y_train
            st.session_state.y_test = y_test
            st.session_state.X = X
            st.session_state.y = y

            # Simpan data historis untuk prediksi
            df_hist = df_lagged[['Tanggal', 'Terakhir']].copy()
            st.session_state.df_hist = df_hist

            st.success("✅ Model berhasil dilatih.")

        if 'model' in st.session_state:
            if st.button("Next"):
                st.session_state.page = "🔮 **6. Prediksi Harga 7 Hari**"
    else:
        st.warning("⚠️ Silakan pilih lag terlebih dahulu pada halaman sebelumnya.")
