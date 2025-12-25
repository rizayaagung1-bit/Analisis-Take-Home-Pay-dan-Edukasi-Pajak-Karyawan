def calculate_payroll(
    gaji_pokok,
    tunjangan,
    status_ptkp,
    bpjs_kesehatan=True,
    bpjs_ketenagakerjaan=True
):
    # PTKP (per tahun)
    PTKP = {
        "TK/0": 54000000,
        "K/0": 58500000,
        "K/1": 63000000,
        "K/2": 67500000,
        "K/3": 72000000,
    }

    bruto = gaji_pokok + tunjangan

    # BPJS
    pot_bpjs = 0
    if bpjs_kesehatan:
        pot_bpjs += 0.01 * bruto
    if bpjs_ketenagakerjaan:
        pot_bpjs += 0.02 * bruto

    neto_bulanan = bruto - pot_bpjs
    neto_tahunan = neto_bulanan * 12

    ptkp = PTKP.get(status_ptkp, 54000000)
    pkp = max(0, neto_tahunan - ptkp)

    # Tarif PPh 21 sederhana (lapis pertama)
    pph_tahunan = 0.05 * pkp
    pph_bulanan = pph_tahunan / 12

    take_home_pay = neto_bulanan - pph_bulanan

    return {
        "bruto": bruto,
        "bpjs": pot_bpjs,
        "neto_bulanan": neto_bulanan,
        "pkp": pkp,
        "pph_bulanan": pph_bulanan,
        "take_home_pay": take_home_pay
    }
