import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def app():
    st.markdown('<div class="gray-box"><h2>📈 Prediksi Harga Saham 7 Hari ke Depan</h2></div>', unsafe_allow_html=True)

    required_keys = ['final_model', 'df_lagged', 'df_hist']
    if not all(k in st.session_state for k in required_keys):
        st.warning("⚠️ Model belum dilatih atau data belum lengkap.")
        return

    model = st.session_state.final_model
    df_lagged = st.session_state.df_lagged.copy()
    df_hist = st.session_state.df_hist.copy()

    df_hist['Tanggal'] = pd.to_datetime(df_hist['Tanggal'])
    df_hist.set_index('Tanggal', inplace=True)
    df_lagged['Tanggal'] = pd.to_datetime(df_lagged['Tanggal'])

    last_date = df_hist.index.max()  # pastikan prediksi dimulai dari data terbaru
    last_input = df_lagged.drop(columns=['Tanggal', 'Terakhir']).iloc[-1:].copy()

    preds = []
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7, freq='B')

    for i in range(7):
        y_pred = model.predict(last_input)[0]
        preds.append(y_pred)
        new_row = last_input.values.flatten().tolist()
        new_row = [y_pred] + new_row[:-1]
        last_input = pd.DataFrame([new_row], columns=last_input.columns)

    future_df = pd.DataFrame({
        'Tanggal': future_dates,
        'Prediksi Harga': preds
    })

    # 🎯 Visualisasi hanya prediksi dengan zoom out dan label jelas
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(future_df['Tanggal'], future_df['Prediksi Harga'], marker='o', linestyle='-', color='green', label='Prediksi')

    for i, val in enumerate(future_df['Prediksi Harga']):
        ax.text(future_df['Tanggal'][i], val, f'{val:.2f}', ha='center', va='bottom', fontsize=9)

    ax.set_title('Prediksi Harga Saham 7 Hari ke Depan')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Harga Penutupan')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()  # Zoom out agar elemen terlihat

    st.pyplot(fig)

    # Tampilkan tabel
    st.markdown('<div class="gray-box"><h4>Tabel Prediksi 7 Hari Kedepan:</h4></div>', unsafe_allow_html=True)
    st.dataframe(future_df, use_container_width=True)

    st.session_state.pred_df = future_df

    if st.button("Next"):
        st.session_state.page = "📊 **7. Evaluasi Model**"
