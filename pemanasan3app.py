import streamlit as st
import time

# Konfigurasi halaman
st.set_page_config(page_title="Simulasi Pangan", page_icon="🍽️", layout="centered")

# Tambahkan background dan perjelas teks
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1504674900247-0877df9cc836");
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }
    .block-container {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar menu
halaman = st.sidebar.selectbox("📚 Pilih Halaman:", ["Beranda", "Simulasi"])

# ========================== DATA ==========================
data_makanan = {
    "🥚 Telur": {
        "reaksi": [
            (30, {
                "chef": "Telur mulai terasa hangat, belum ada perubahan nyata.",
                "analis": "Molekul protein mulai bergerak lebih cepat namun belum terjadi denaturasi.",
                "tingkat_kematangan": "-"
            }),
            (62, {
                "chef": "Putih telur mulai mengeras – tekstur setengah matang.",
                "analis": "Albumin mulai menggumpal karena denaturasi protein dimulai.",
                "tingkat_kematangan": "Setengah Matang"
            }),
            (70, {
                "chef": "Kuning telur mulai mengeras – telur matang sempurna.",
                "analis": "Lipovitellenin mengalami denaturasi, menyebabkan kuning mengeras.",
                "tingkat_kematangan": "Matang"
            })
        ],
        "penjelasan_analis": "Protein dalam telur mengalami denaturasi akibat panas. Albumin (putih telur) menggumpal terlebih dahulu, lalu lipovitellenin (kuning telur).",
        "penjelasan_chef": "Untuk telur rebus sedang, rebus sekitar 6-8 menit pada suhu 70–80°C.",
        "fun_fact": "Memasak telur perlahan menghasilkan tekstur creamy sempurna!",
        "penyimpanan": {
            "suhu": "0-4°C",
            "masa_simpan": "3-5 minggu",
            "tips": "Simpan di karton asli, jangan di pintu kulkas."
        }
    },
    "🍬 Gula": {
        "reaksi": [
            (100, {
                "chef": "Gula mulai meleleh dan membentuk sirup.",
                "analis": "Pelelehan fisik gula sukrosa dimulai di atas 100°C.",
                "tingkat_kematangan": "-"
            }),
            (160, {
                "chef": "Gula berubah warna coklat – karamelisasi awal.",
                "analis": "Sukrosa mulai terurai dan membentuk senyawa aroma & warna baru.",
                "tingkat_kematangan": "Karamel"
            }),
            (180, {
                "chef": "Gula gosong – rasa pahit muncul.",
                "analis": "Pembakaran gula menghasilkan senyawa pahit dan asap.",
                "tingkat_kematangan": "Gosong"
            })
        ],
        "penjelasan_analis": "Karamelisasi terjadi saat sukrosa terurai karena panas, menghasilkan warna dan aroma khas.",
        "penjelasan_chef": "Untuk saus karamel, panaskan hingga 165–170°C tanpa diaduk terlalu banyak.",
        "fun_fact": "Karamelisasi menghasilkan rasa toffee khas kue dan permen!",
        "penyimpanan": {
            "suhu": "20-25°C",
            "masa_simpan": "18-24 bulan",
            "tips": "Simpan di wadah kedap udara agar tidak menggumpal."
        }
    }
}

# ======================== FUNGSI ==========================

def get_multi_reaksi(makanan, suhu, mode):
    hasil = []
    for batas, detail in data_makanan[makanan]["reaksi"]:
        if suhu >= batas:
            hasil.append(f"{batas}°C: {detail[mode.lower()]}")
    return hasil or ["Belum ada perubahan signifikan."]

def generate_table(makanan, mode):
    rows = []
    for suhu, detail in data_makanan[makanan]["reaksi"]:
        row = {
            "Suhu (°C)": suhu,
            "Penjelasan": detail[mode.lower()]
        }
        if mode == "Chef" and "tingkat_kematangan" in detail:
            row["Tingkat Kematangan"] = detail["tingkat_kematangan"]
        rows.append(row)
    return rows

# ========================= HALAMAN ========================

if halaman == "Beranda":
    st.title("🍽️ Simulasi Pemanasan Pada Pangan")
    st.markdown("Selamat datang di **aplikasi interaktif** untuk memahami bagaimana bahan pangan bereaksi terhadap panas.")
    st.markdown("👨‍🍳 Mode *Chef*: Fokus pada tingkat kematangan dan waktu memasak.")
    st.markdown("🔬 Mode *Analis*: Fokus pada penjelasan ilmiah dan reaksi molekuler.")
    st.image("https://cdn0-production-images-kly.akamaized.net/7ja7izhlU54w5VbkjPRxctPzwnw=/680x383/smart/filters:quality(75):strip_icc():format(webp)/kly-media-production/medias/3543870/original/067438200_1629277779-alex-lam-WOrdQ6Wgomw-unsplash.jpg",
             caption="Bolu Pandan Topping Keju & Choco Chip", use_container_width=True)
    st.markdown("➡️ Pilih menu **Simulasi** di sidebar untuk memulai.")

elif halaman == "Simulasi":
    st.title("🔥 Simulasi Pemanasan pada pangan")

    mode = st.radio("🎭 Simulasi Sebagai:", ("Chef", "Analis"))
    makanan = st.selectbox("🔍 Pilih Bahan Makanan:", list(data_makanan.keys()))
    pilihan_simulasi = st.radio("🔥 Mau set suhu manual atau simulasi pemanasan?", ("Set Suhu Manual", "Simulasi Pemanasan"))

    tampilkan_reaksi = []
    suhu = 0

    if pilihan_simulasi == "Set Suhu Manual":
        suhu = st.slider("🌡️ Atur Suhu (°C):", 0, 300, 25)
        tampilkan_reaksi = get_multi_reaksi(makanan, suhu, mode)
    else:
        progress = st.progress(0)
        for i in range(301):
            suhu = i
            tampilkan_reaksi = get_multi_reaksi(makanan, suhu, mode)
            progress.progress(i / 300)
            time.sleep(0.002)
        st.success("✅ Simulasi selesai!")

    # Output
    st.subheader(f"🔥 Pada suhu {suhu}°C:")
    for r in tampilkan_reaksi:
        st.info(r)

    st.divider()
    st.subheader("📘 Penjelasan:")
    st.write(data_makanan[makanan][f"penjelasan_{mode.lower()}"])

    st.subheader("✨ Fun Fact:")
    st.success(data_makanan[makanan]["fun_fact"])

    st.subheader("🧊 Penyimpanan:")
    ps = data_makanan[makanan]["penyimpanan"]
    st.write(f"- **Suhu:** {ps['suhu']}\n- **Masa Simpan:** {ps['masa_simpan']}\n- **Tips:** {ps['tips']}")

    # Tabel akhir
    if pilihan_simulasi == "Simulasi Pemanasan":
        st.divider()
        st.subheader("📊 Tabel Reaksi Selama Pemanasan:")
        tabel = generate_table(makanan, mode)
        st.table(tabel)
