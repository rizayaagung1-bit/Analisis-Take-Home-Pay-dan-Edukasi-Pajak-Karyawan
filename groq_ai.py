import streamlit as st
from groq import Groq

# 1️⃣ Inisialisasi client Groq (WAJIB ADA)
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# 2️⃣ Fungsi analisis payroll
def payroll_analysis(data):
    prompt = f"""
Anda adalah AI Agent Payroll dan Edukasi Pajak Karyawan.

Data gaji:
- Gaji bruto: Rp{data['bruto']:,}
- Potongan BPJS: Rp{data['bpjs']:,}
- PKP tahunan: Rp{data['pkp']:,}
- Pajak bulanan: Rp{data['pph_bulanan']:,}
- Take home pay: Rp{data['take_home_pay']:,}

Tugas:
1. Berikan ANALISIS singkat kondisi gaji.
2. Jelaskan pajak dan BPJS dengan bahasa awam.
3. Berikan insight ringan (bukan penghindaran pajak).

Gunakan bahasa Indonesia yang mudah dipahami.
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI tidak dapat memproses analisis saat ini. Detail error: {e}"
