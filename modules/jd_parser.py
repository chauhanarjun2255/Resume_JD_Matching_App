def parse_jd(jd_text):
    """
    Clean Job Description text.
    """

    jd_text = jd_text.lower()

    jd_text = jd_text.replace(",", " ")
    jd_text = jd_text.replace(".", " ")
    jd_text = jd_text.replace("/", " ")

    return jd_text