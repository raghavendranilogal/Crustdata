import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Crustdata Company Intelligence Explorer")


headers = {
    "Authorization": f"Token {94bebb0c37be086b15f004f5715f7507857db756}",
    "Content-Type": "application/json"
}

url = "https://api.crustdata.com/screener/companydb/search"

payload = {
    "filters": {
        "filter_type": "employee_metrics.latest_count",
        "type": ">",
        "value": 50
    },
    "limit": 20
}

headers = {
    "Authorization": f"Token {94bebb0c37be086b15f004f5715f7507857db756}",
    "Content-Type": "application/json"
}


# -------- CACHE API CALL --------

@st.cache_data(ttl=3600)
def fetch_companies():

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return []

    data = response.json()

    return data.get("companies", [])


companies = fetch_companies()

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

# -------- DATA TABLE --------

st.subheader("Company Dataset")
st.dataframe(df)

# -------- MOMENTUM CHART --------

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

# -------- SCATTER CHART --------

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

# -------- HIRING CHART --------

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
