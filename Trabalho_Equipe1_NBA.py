import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv("dados/nba_stats.csv")

data["salary"] = data["salary"].replace("[\$,]", "", regex=True).astype(float)
data = data.dropna(subset=["team", "position", "salary"])

st.title("Dashboard de Média Salarial da NBA")

st.sidebar.header("Filtros")
teams = st.sidebar.multiselect(
    "Selecione o(s) time(s):",
    options=data["team"].unique(),
    default=data["team"].unique(),
)
positions = st.sidebar.multiselect(
    "Selecione a(s) posição(ões):",
    options=data["position"].unique(),
    default=data["position"].unique(),
)


filtered_data = data[(data["team"].isin(teams)) & (data["position"].isin(positions))]

avg_salary = filtered_data["salary"].mean()

st.title("Média Salarial")
col1, col2 = st.columns(2)

with col1:
    avg_salary_by_year = filtered_data.groupby("year")["salary"].mean().reset_index()
    fig_year = px.line(
        avg_salary_by_year,
        x="year",
        y="salary",
        title="Média Salarial por Ano",
        labels={"salary": "Média Salarial ($)", "year": "Ano"},
    )
    st.plotly_chart(fig_year)

with col2:
    years = list(range(1999, 2022))
    inflation_rates = [
        2.2,
        3.4,
        3.2,
        2.8,
        1.6,
        2.7,
        3.4,
        3.2,
        2.8,
        3.8,
        0.1,
        1.5,
        3.0,
        2.3,
        2.1,
        2.4,
        2.3,
        2.1,
        2.4,
        2.1,
        2.1,
        1.2,
        4.7,
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=years,
            y=inflation_rates,
            mode="lines+markers",
            name="Inflation Rate",
            line=dict(color="blue", width=2),
            marker=dict(size=6),
        )
    )

    fig.update_layout(
        title="Inflação nos EUA (1999-2022)",
        xaxis_title="Ano",
        yaxis_title="Inflação (%)",
        template="plotly_white",
        xaxis=dict(tickmode="linear"),
    )

    st.plotly_chart(fig)


avg_salary_by_position = (
        filtered_data.groupby("position")["salary"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
fig_position = px.bar(
        avg_salary_by_position,
        x="position",
        y="salary",
        title="Média Salarial por Posição",
        labels={"salary": "Média Salarial ($)", "position": "Posição"},
    )
st.plotly_chart(fig_position)

st.subheader("Distribuição de Jogadores por Posição")
position_distribution = filtered_data["position"].value_counts().reset_index()
position_distribution.columns = ["position", "player_count"]

fig_position_distribution = px.bar(
    position_distribution,
    x="position",
    y="player_count",
    title="Distribuição de Jogadores por Posição",
    labels={"position": "Posição", "player_count": "Quantidade de Jogadores"},
    text="player_count",
)
fig_position_distribution.update_traces(textposition="outside")

st.plotly_chart(fig_position_distribution)

st.subheader("Média Salarial por Time (Barras)")
avg_salary_by_team = (
    filtered_data.groupby("team")["salary"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)
fig_team_bar = px.bar(
    avg_salary_by_team,
    x="team",
    y="salary",
    title="Média Salarial por Time (Barras)",
    labels={"salary": "Média Salarial ($)", "team": "Time"},
)
st.plotly_chart(fig_team_bar)


st.subheader("Jogadores Ordenados por Salário")
with st.expander("Mostrar/Esconder Tabela de Salários Ordenados"):
    sorted_salaries = filtered_data.sort_values(by="salary", ascending=False)
    st.dataframe(sorted_salaries[["name", "team", "position", "salary"]])


st.subheader("Quantidade de Anos Jogados por Jogador")
years_played = filtered_data["name"].value_counts().reset_index()
years_played.columns = ["name", "years_played"]

fig_years_played = px.bar(
years_played,
x="name",
y="years_played",
title="Quantidade de Anos Jogados por Jogador",
labels={"name": "Jogador", "years_played": "Anos Jogados"},
text="years_played",
)
fig_years_played.update_traces(textposition="outside")

st.plotly_chart(fig_years_played)

st.subheader("Quantidade de Anos Jogados vs Salário Médio")
years_salary_stats = (
filtered_data.groupby("name")
.agg(years_played=("name", "size"), avg_salary=("salary", "mean"))
.reset_index()
)

avg_salary_by_years = (
years_salary_stats.groupby("years_played")
.agg(avg_salary=("avg_salary", "mean"))
.reset_index()
)

fig_years_vs_salary_bar = px.bar(
avg_salary_by_years,
x="years_played",
y="avg_salary",
title="Quantidade de Anos Jogados vs Salário Médio",
labels={"years_played": "Anos Jogados", "avg_salary": "Salário Médio ($)"},
text="avg_salary",
)
fig_years_vs_salary_bar.update_traces(textposition="outside")
st.plotly_chart(fig_years_vs_salary_bar)

st.subheader("Distribuição dos Anos de Experiência (Anos Jogados)")
fig_experience_histogram = px.histogram(
years_salary_stats,
x="years_played",
title="Distribuição dos Anos de Experiência (Anos Jogados)",
labels={"years_played": "Anos de Experiência (Anos Jogados)"},
nbins=10, 
)
fig_experience_histogram.update_traces(texttemplate="%{y}", textposition="outside")
st.plotly_chart(fig_experience_histogram)
