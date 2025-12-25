import streamlit as st
import plotly.express as px
from groq import Groq

from payroll import calculate_payroll
from explanation import generate_payroll_explanation

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Agent Payroll",
    page_icon="💼",
    layout="centered"
)

st.title("💼 AI Agent Payroll")
st.caption("Analisis Take Home Pay & Edukasi Pajak Karyawan")

st.markdown(
    """
Aplikasi ini membantu karyawan memahami **gaji bersih (take home pay)**,
**potongan BPJS**, dan **pajak (PPh 21)** secara **transparan, visual, dan edukatif**.
"""
)

# =========================
# FORM INPUT
# =========================
with st.form("payroll_form"):
    st.subheader("📝 Input Data Gaji")

    gaji_pokok = st.number_input(
        "Gaji Pokok (Rp)",
        min_value=0,
        step=500_000,
        format="%d"
    )

    tunjangan = st.number_input(
        "Total Tunjangan (Rp)",
        min_value=0,
        step=100_000,
        format="%d"
    )

    status_ptkp = st.selectbox(
        "Status PTKP",
        ["TK/0", "K/0", "K/1", "K/2", "K/3"]
    )

    bpjs_kesehatan = st.checkbox("BPJS Kesehatan (1%)", value=True)
    bpjs_ketenagakerjaan = st.checkbox("BPJS Ketenagakerjaan (2%)", value=True)

    submitted = st.form_submit_button("🔍 Hitung & Analisis")

# =========================
# PROCESS & OUTPUT
# =========================
if submitted:
    # ---- HITUNG PAYROLL
    hasil = calculate_payroll(
        gaji_pokok=gaji_pokok,
        tunjangan=tunjangan,
        status_ptkp=status_ptkp,
        bpjs_kesehatan=bpjs_kesehatan,
        bpjs_ketenagakerjaan=bpjs_ketenagakerjaan
    )

    # =========================
    # RINGKASAN ANGKA
    # =========================
    st.divider()
    st.subheader("📊 Ringkasan Gaji")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Gaji Bruto:** Rp{hasil['bruto']:,}")
        st.write(f"**BPJS:** Rp{hasil['bpjs']:,}")
    with col2:
        st.write(f"**PPh 21 Bulanan:** Rp{hasil['pph_bulanan']:,}")
        st.success(f"**Take Home Pay:** Rp{hasil['take_home_pay']:,}")

    # =========================
    # PENJELASAN DETERMINISTIK
    # =========================
    st.divider()
    st.subheader("📘 Penjelasan Rincian Gaji")

    penjelasan = generate_payroll_explanation(hasil)
    st.markdown(penjelasan)

    # =========================
    # GRAFIK DONAT (PERSENTASE)
    # =========================
    st.divider()
    st.subheader("📈 Komposisi Gaji (Persentase)")

    labels = ["Take Home Pay", "BPJS", "Pajak (PPh 21)"]
    values = [
        hasil["take_home_pay"],
        hasil["bpjs"],
        hasil["pph_bulanan"]
    ]

    total = sum(values)
    percentages = [(v / total) * 100 if total > 0 else 0 for v in values]

    fig = px.pie(
        names=labels,
        values=percentages,
        hole=0.5
    )

    fig.update_traces(
        textinfo="label+percent",
        hovertemplate="%{label}: %{value:.2f}%<extra></extra>"
    )

    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # ANALISIS & EDUKASI AI (GROQ)
    # =========================
    st.divider()
    st.subheader("🧠 Analisis & Edukasi AI")

    prompt = f"""
Anda adalah AI Agent Payroll dan Edukasi Pajak Karyawan.

Data gaji karyawan:
- Gaji bruto: Rp{hasil['bruto']:,}
- Potongan BPJS: Rp{hasil['bpjs']:,}
- Pajak (PPh 21) bulanan: Rp{hasil['pph_bulanan']:,}
- Take home pay: Rp{hasil['take_home_pay']:,}

Tugas Anda:
1. Berikan ANALISIS singkat kondisi gaji karyawan.
2. Jelaskan pajak dan BPJS dengan bahasa awam.
3. Berikan insight ringan (bukan penghindaran pajak).

Gunakan bahasa Indonesia yang mudah dipahami.
"""

    models = [
        "llama-3.1-8b-instant",      # utama (stabil)
        "mixtral-8x7b-32768"         # fallback
    ]

    ai_output = None
    last_error = None

    with st.spinner("AI sedang menganalisis..."):
        for model in models:
            try:
                groq_client = Groq(
                    api_key=st.secrets["GROQ_API_KEY"]
                )
                response = groq_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4,
                )
                ai_output = response.choices[0].message.content
                break
            except Exception as e:
                last_error = e

    if ai_output:
        st.info(ai_output)
    else:
        st.warning(
            "AI tidak dapat memproses analisis saat ini.\n\n"
            f"Detail error: {last_error}"
        )

# =========================
# FOOTER
# =========================
st.divider()
st.caption(
    "⚠️ Aplikasi ini bersifat edukatif dan tidak menggantikan sistem resmi DJP."
)
