import streamlit as st
import requests
import pandas as pd

st.title("Crustdata Company Explorer")

API_TOKEN = "c3dd4a518023333598b8d8323f043de7b0fdc509"

url = "https://api.crustdata.com/screener/companydb/search"

headers = {
    "Authorization": f"Token {API_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "filters": {
        "filter_type": "employee_metrics.latest_count",
        "type": ">",
        "value": 50
    },
    "limit": 10
}

st.write("Calling Crustdata API...")

response = requests.post(url, headers=headers, json=payload)

if response.status_code != 200:
    st.error(f"API Error: {response.status_code}")
    st.stop()

data = response.json()

companies = data.get("companies", [])

rows = []

for company in companies:
    emp = company.get("employee_metrics", {})
    fol = company.get("follower_metrics", {})

    rows.append({
        "Company": company.get("company_name"),
        "Employees": emp.get("latest_count"),
        "Hiring Growth 6M (%)": emp.get("growth_6m_percent"),
        "Follower Growth 12M (%)": fol.get("growth_12m_percent")
    })

df = pd.DataFrame(rows)

st.subheader("Company Data")

st.dataframe(df)

st.subheader("Hiring Growth")

st.bar_chart(df.set_index("Company")["Hiring Growth 6M (%)"])
