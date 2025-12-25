from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def payroll_analysis(data):
    prompt = f"""
Anda adalah AI Agent Payroll dan Edukasi Pajak Karyawan.

Data gaji karyawan:
- Gaji bruto: Rp{data['bruto']:,}
- BPJS: Rp{data['bpjs']:,}
- PKP tahunan: Rp{data['pkp']:,}
- PPh 21 bulanan: Rp{data['pph_bulanan']:,}
- Take home pay: Rp{data['take_home_pay']:,}

Tugas Anda:
1. Berikan ANALISIS singkat kondisi gaji karyawan.
2. Jelaskan PAJAK dan BPJS dengan bahasa awam.
3. Berikan INSIGHT ringan (tanpa penghindaran pajak).

Gunakan bahasa Indonesia yang mudah dipahami.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return response.choices[0].message.content
