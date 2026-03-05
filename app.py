import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Crustdata Company Intelligence Explorer")

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
    "limit": 20
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

    hiring_growth = emp.get("growth_6m_percent", 0)
    follower_growth = fol.get("growth_12m_percent", 0)

    rows.append({
        "Company": company.get("company_name"),
        "Employees": emp.get("latest_count"),
        "Hiring Growth": hiring_growth,
        "Follower Growth": follower_growth,
        "Momentum Score": hiring_growth + follower_growth
    })

df = pd.DataFrame(rows)

# -------- Table --------

st.subheader("Company Dataset")

st.dataframe(df)

# -------- Insight 1: Top Momentum --------

st.subheader("Top Company Momentum")

df_sorted = df.sort_values("Momentum Score", ascending=False)

fig1, ax1 = plt.subplots()

sns.barplot(
    data=df_sorted,
    y="Company",
    x="Momentum Score",
    ax=ax1
)

ax1.set_title("Companies Accelerating Fastest")

st.pyplot(fig1)

# -------- Insight 2: Growth vs Attention --------

st.subheader("Hiring Growth vs Market Attention")

fig2, ax2 = plt.subplots()

sns.scatterplot(
    data=df,
    x="Hiring Growth",
    y="Follower Growth",
    size="Employees",
    sizes=(50, 500),
    ax=ax2
)

ax2.set_title("Company Growth vs Market Attention")

st.pyplot(fig2)

# -------- Insight 3: Hiring Growth Leaderboard --------

st.subheader("Fastest Hiring Companies")

top_hiring = df.sort_values("Hiring Growth", ascending=False)

fig3, ax3 = plt.subplots()

sns.barplot(
    data=top_hiring,
    y="Company",
    x="Hiring Growth",
    ax=ax3
)

ax3.set_title("Companies Expanding Hiring")

st.pyplot(fig3)
