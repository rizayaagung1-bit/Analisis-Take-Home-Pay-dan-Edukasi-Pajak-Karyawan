def generate_payroll_explanation(data):
    bruto = data["bruto"]
    bpjs = data["bpjs"]
    pajak = data["pph_bulanan"]
    thp = data["take_home_pay"]

    total_potongan = bpjs + pajak

    explanation = f"""
📌 **Penjelasan Rincian Gaji dan Potongan**

1️⃣ **Gaji Bruto**
Gaji bruto adalah total penghasilan yang Anda terima sebelum adanya potongan apa pun.  
Pada perhitungan ini, gaji bruto Anda sebesar **Rp{bruto:,.0f}**.

2️⃣ **Potongan BPJS**
BPJS merupakan iuran jaminan sosial yang dipotong langsung dari gaji karyawan.  
Besarnya potongan BPJS dalam perhitungan ini adalah **Rp{bpjs:,.0f}**.  
Potongan ini **bukan pajak**, tetapi iuran perlindungan kesehatan dan ketenagakerjaan.

3️⃣ **Pajak Penghasilan (PPh 21) Bulanan**
Pajak penghasilan adalah kewajiban kepada negara yang dipotong dari penghasilan karyawan.  
Pajak bulanan Anda sebesar **Rp{pajak:,.0f}**, dihitung sesuai ketentuan pajak yang berlaku.

4️⃣ **Total Potongan**
Total potongan yang mengurangi gaji Anda adalah:
- BPJS: Rp{bpjs:,.0f}
- Pajak: Rp{pajak:,.0f}

➡️ **Total potongan: Rp{total_potongan:,.0f}**

5️⃣ **Take Home Pay (Gaji Bersih)**
Take home pay adalah gaji yang benar-benar Anda terima setelah dikurangi seluruh potongan.  
Dalam perhitungan ini, take home pay Anda sebesar:

✅ **Rp{thp:,.0f}**

📊 **Kesimpulan**
Dari gaji bruto sebesar **Rp{bruto:,.0f}**, terdapat potongan sebesar  
**Rp{total_potongan:,.0f}**, sehingga gaji bersih yang Anda terima adalah  
**Rp{thp:,.0f}** per bulan.
"""

    return explanation
