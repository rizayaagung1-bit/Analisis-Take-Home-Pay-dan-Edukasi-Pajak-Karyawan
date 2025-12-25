import streamlit as st
from payroll import calculate_payroll
from groq_ai import payroll_analysis

st.set_page_config(page_title="AI Agent Payroll", layout="centered")

st.title("🤖 AI Agent Payroll")
st.subheader("Analisis Take Home Pay & Edukasi Pajak Karyawan")

st.markdown("Masukkan data gaji Anda untuk mengetahui **gaji bersih, analisis, dan penjelasan pajak**.")

with st.form("payroll_form"):
    gaji_pokok = st.number_input("Gaji Pokok (Rp)", min_value=0, step=500000)
    tunjangan = st.number_input("Total Tunjangan (Rp)", min_value=0, step=100000)

    status_ptkp = st.selectbox(
        "Status PTKP",
        ["TK/0", "K/0", "K/1", "K/2", "K/3"]
    )

    bpjs_kesehatan = st.checkbox("BPJS Kesehatan (1%)", value=True)
    bpjs_ketenagakerjaan = st.checkbox("BPJS Ketenagakerjaan (2%)", value=True)

    submitted = st.form_submit_button("Hitung & Analisis")

if submitted:
    hasil = calculate_payroll(
        gaji_pokok,
        tunjangan,
        status_ptkp,
        bpjs_kesehatan,
        bpjs_ketenagakerjaan
    )

    st.divider()
    st.subheader("📊 Ringkasan Gaji")

    st.write(f"**Gaji Bruto:** Rp{hasil['bruto']:,}")
    st.write(f"**BPJS:** Rp{hasil['bpjs']:,}")
    st.write(f"**PPh 21 Bulanan:** Rp{hasil['pph_bulanan']:,}")
    st.success(f"**Take Home Pay:** Rp{hasil['take_home_pay']:,}")

    st.divider()
    st.subheader("🧠 Analisis & Edukasi AI")

    with st.spinner("AI sedang menganalisis..."):
        analisis = payroll_analysis(hasil)

    st.info(analisis)
