def payroll_analysis(data):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI tidak dapat memproses analisis saat ini. Detail error: {e}"
