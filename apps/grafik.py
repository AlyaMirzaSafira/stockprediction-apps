import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def app():
    st.markdown('<div class="gray-box"><h2>Grafik Harga Penutupan Saham</h2></div>', unsafe_allow_html=True)

    if 'df' in st.session_state:
        df = st.session_state.df.copy()

        # Pastikan kolom 'Tanggal' dalam format datetime dan urut
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
        df = df.sort_values('Tanggal')

        # Plot grafik harga penutupan (Terakhir)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df['Tanggal'], df['Terakhir'], color='blue', linewidth=2)
        ax.set_title("Harga Penutupan Saham", fontsize=14)
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Harga Penutupan (Terakhir)")
        ax.grid(True)

        st.pyplot(fig)

        if st.button("Next"):
            st.session_state.page = "⏱ **4. Pilih Lag Terbaik**"
    else:
        st.warning("Silakan unggah data saham terlebih dahulu melalui halaman sebelumnya.")
