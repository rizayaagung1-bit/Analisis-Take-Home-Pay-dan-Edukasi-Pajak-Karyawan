import streamlit as st
from groq import Groq

def payroll_analysis(data):
    prompt = f"""
Anda adalah AI Agent Payroll dan Edukasi Pajak Karyawan.

Data gaji:
- Gaji bruto: Rp{data['bruto']:,}
- BPJS: Rp{data['bpjs']:,}
- Pajak bulanan: Rp{data['pph_bulanan']:,}
- Take home pay: Rp{data['take_home_pay']:,}

Berikan analisis dan penjelasan singkat dengan bahasa awam.
"""

    models = [
        "llama-3.1-8b-instant",      # paling stabil
        "mixtral-8x7b-32768"         # fallback
    ]

    for model in models:
        try:
            groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            response = groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            return response.choices[0].message.content

        except Exception as e:
            last_error = e

    return f"AI tidak dapat memproses analisis saat ini. Detail error: {last_error}"
