
import streamlit as st
from supabase import create_client
from urllib.parse import urlparse

st.title("Supabase Connection Test")

try:
    url = st.secrets["SUPABASE_URL"].strip().rstrip("/")
    key = st.secrets["SUPABASE_KEY"].strip()

    parsed = urlparse(url)

    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or not parsed.hostname.endswith(".supabase.co")
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
    ):
        st.error("Invalid Project URL format.")
        st.stop()

    st.write("Project URL format: Valid")

    supabase = create_client(url, key)

    result = (
        supabase.table("expenses")
        .select("id")
        .limit(1)
        .execute()
    )

    st.success("Supabase connected successfully!")

except Exception as e:
    st.error("Connection failed")
    st.error(str(e))
