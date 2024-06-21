import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="ITY - Institut Teknologi Yogyakarta",
    layout="wide",
    page_icon=":school:",
)

st.logo("images/logo.png", link="https://github.com/herubagush/rekap_data_mahasiswa/blob/main/streamlit_app/")

st.title(
    "Rekapitulasi Data Mahasiswa Institut Teknologi Yogyakarta (ITY) Periode 2019-2023"
)

data_mahasiswa = pd.read_csv("data_mahasiswa_ity.csv")
data_select = data_mahasiswa[
    ["angkatan", "prodi", "nama", "jk", "kabupaten", "provinsi", "instansi_asal"]
]
data_select = data_select.fillna("")
data = data_select.replace(r"^\s*$", "UNKNOWN", regex=True)

# 1. Rekap Jumlah Mahasiswa per Prodi
st.subheader("1. Jumlah Mahasiswa per Prodi")
rekap1 = (
    data.groupby(by=["prodi"]).count()[["nama"]].rename(columns={"nama": "mahasiswa"})
)
rekap1 = rekap1.reset_index()
fig = px.bar(
    rekap1,
    x="mahasiswa",
    y="prodi",
    orientation="h",
    color="prodi",
    text_auto=True,
    template="plotly_white",
)
fig.update_layout(
    title="Student Body ITY Periode 2019-2023",
    title_x=0.3,
    title_y=0.95,
    xaxis_title="Jumlah Mahasiswa",
    yaxis_title=None,
    legend_title="Prodi",
)
st.plotly_chart(fig)

# 2. Jumlah Mahasiswa Selama Kurun Waktu 2019-2023
st.subheader("2. Jumlah Mahasiswa Selama Kurun Waktu 2019-2023")
rekap2 = (
    data.groupby(by=["angkatan"])
    .count()[["nama"]]
    .rename(columns={"nama": "mahasiswa"})
)
rekap2 = rekap2.reset_index()
fig = px.line(
    rekap2,
    x="angkatan",
    y="mahasiswa",
    markers=True,
    text="mahasiswa",
    template="plotly_white",
)
fig.update_layout(
    title="Tren Jumlah Mahasiswa ITY Periode 2019-2023",
    title_x=0.3,
    title_y=0.95,
    xaxis_title="Tahun",
    yaxis_title="Jumlah Mahasiswa",
)
fig.update_xaxes(range=[2018.5, 2023.5])
fig.update_traces(textposition="bottom center")
st.plotly_chart(fig)

# 3. Jumlah Mahasiswa per Prodi per Angkatan
st.subheader("3. Jumlah Mahasiswa per Prodi per Angkatan")
rekap3 = (
    data.groupby(by=["prodi", "angkatan"])
    .count()[["nama"]]
    .rename(columns={"nama": "mahasiswa"})
)
rekap3["kampus"] = "Institut Teknologi Yogyakarta"
rekap3 = rekap3.reset_index()
fig = px.sunburst(
    rekap3,
    path=["kampus", "prodi", "angkatan"],
    values="mahasiswa",
    title="Jumlah mahasiswa per Prodi per Angkatan",
    width=800,
    height=800,
    color_continuous_scale="rainbow",
    color="mahasiswa",
)
fig.update_layout(
    title="Sebaran Jumlah Mahasiswa ITY Periode 2019-2023", title_x=0.5, title_y=0.95
)
st.plotly_chart(fig)

# 4. Tren Jumlah Mahasiswa per Prodi Kurun Waktu 2019-2023
st.subheader("4. Tren Jumlah Mahasiswa per Prodi Kurun Waktu 2019-2023")
fig = px.line(
    rekap3,
    x="angkatan",
    y="mahasiswa",
    color="prodi",
    symbol="prodi",
    markers=True,
    template="plotly_white",
)
fig.update_layout(
    title="Tren Jumlah Mahasiswa ITY Periode 2019-2023",
    title_x=0.3,
    title_y=0.95,
    xaxis_title="Tahun",
    yaxis_title="Jumlah Mahasiswa",
    legend_title="Prodi",
)
fig.update_xaxes(range=[2018.5, 2023.5])
st.plotly_chart(fig)

# 5. Jumlah Mahasiswa per Provinsi
st.subheader("5. Jumlah Mahasiswa per Provinsi")
rekap4 = (
    data.groupby(by=["provinsi"])
    .count()[["nama"]]
    .rename(columns={"nama": "mahasiswa"})
)
rekap4 = rekap4.reset_index()
fig = px.bar(
    rekap4,
    x="mahasiswa",
    y="provinsi",
    orientation="h",
    text_auto=True,
    height=900,
    width=1000,
    template="plotly_white",
)
fig.update_layout(
    title="Sebaran Mahasiswa ITY Setiap Provinsi",
    title_x=0.3,
    title_y=0.95,
    xaxis_title="Jumlah Mahasiswa",
)
fig.update_xaxes(title="Jumlah Mahasiswa")
fig.update_yaxes(title=None)
st.plotly_chart(fig)

# 6. Jumlah Mahasiswa per Provinsi pada Setiap Prodi
st.subheader("6. Jumlah Mahasiswa per Provinsi pada Setiap Prodi")
rekap5 = (
    data.groupby(by=["provinsi", "prodi"])
    .count()[["nama"]]
    .rename(columns={"nama": "mahasiswa"})
)
rekap5 = rekap5.reset_index()
fig = px.bar(
    rekap5,
    x="mahasiswa",
    y="provinsi",
    orientation="h",
    height=800,
    width=1000,
    color="prodi",
    text_auto=True,
    template="plotly_white",
)
fig.update_layout(
    title="Sebaran Mahasiswa per Prodi ITY pada Setiap Provinsi",
    title_x=0.3,
    title_y=0.95,
    xaxis_title="Jumlah Mahasiswa",
    barmode="stack",
    legend=dict(title="Prodi", xanchor="right", yanchor="top"),
)
fig.update_xaxes(title="Jumlah Mahasiswa")
fig.update_yaxes(title=None)
st.plotly_chart(fig)

# 7. Provinsi dengan Perolehan Total Mahasiswa Minimal 50 orang
st.subheader("7. Provinsi dengan Perolehan Total Mahasiswa Minimal 50 orang")
rekap6 = rekap4.loc[rekap4["mahasiswa"] >= 50]
n = len(rekap6)
st.write(
    "Jumlah provinsi dengan perolehan total mahasiswa minimal 50 orang adalah sebanyak",
    str(n),
    "provinsi, yaitu:",
)
fig = px.bar(
    rekap6,
    x="mahasiswa",
    y="provinsi",
    text_auto=True,
    orientation="h",
    height=500,
    width=1000,
    color="provinsi",
    template="plotly_white",
)
fig.update_layout(
    title=(str(n) + " BesarProvinsi dengan Perolehan Total Mahasiswa Minimal 50 orang"),
    title_x=0.3,
    title_y=0.95,
    xaxis_title="Jumlah Mahasiswa",
    legend_title="Provinsi",
)
fig.update_xaxes(title="Jumlah Mahasiswa")
fig.update_yaxes(title=None)
st.plotly_chart(fig)

# 8. Jumlah Mahasiswa per Prodi pada Provinsi dengan Perolehan Total Mahasiswa Lebih Dari 50 orang
st.subheader(
    "8. Jumlah Mahasiswa per Prodi pada Provinsi dengan Perolehan Total Mahasiswa Lebih Dari 50 orang"
)
rekap7 = pd.DataFrame()
rekap7.fillna(0)
for x in rekap6["provinsi"]:
    rekap7 = rekap7._append(rekap5.loc[rekap5["provinsi"] == x], ignore_index=True)
fig = px.bar(
    rekap7,
    x="mahasiswa",
    y="provinsi",
    orientation="h",
    height=500,
    width=1000,
    color="prodi",
    text_auto=True,
    template="plotly_white",
)
fig.update_layout(
    title=("Sebaran Mahasiswa per Prodi ITY pada " + str(n) + " Besar Provinsi"),
    title_x=0.3,
    title_y=0.95,
    xaxis_title="Jumlah Mahasiswa",
    barmode="stack",
    legend_title="Prodi",
)
fig.update_xaxes(title="Jumlah Mahasiswa")
fig.update_yaxes(title=None)
fig.update_layout(barmode="stack", legend=dict(xanchor="right", yanchor="top"))
st.plotly_chart(fig)

# 9. Detail Kabupaten pada Provinsi dengan Perolehan Total Mahasiswa Minimal 50 orang
st.subheader(
    "9. Detail Kabupaten pada Provinsi dengan Perolehan Total Mahasiswa Minimal 50 orang"
)
rekap8 = pd.DataFrame()
rekap8.fillna(0)
for x in rekap6["provinsi"]:
    rekap8 = rekap8._append(data.loc[data["provinsi"] == x], ignore_index=True)
rekap8 = (
    rekap8.groupby(by=["provinsi", "prodi", "kabupaten"])
    .count()[["nama"]]
    .rename(columns={"nama": "mahasiswa"})
)
rekap8 = rekap8.reset_index()


def makebar(prov, data):
    fig = px.bar(
        data,
        x="mahasiswa",
        y="kabupaten",
        orientation="h",
        height=500,
        width=950,
        color="prodi",
        text_auto=True,
        template="plotly_white",
    )
    fig.update_xaxes(title="Jumlah Mahasiswa")
    fig.update_yaxes(title=None)
    fig.update_layout(
        title=("Provinsi " + prov),
        title_x=0.3,
        title_y=0.95,
        xaxis_title="Jumlah Mahasiswa",
        barmode="stack",
        legend_title="Prodi",
    )
    return fig


for prov in rekap6["provinsi"]:
    rekap9 = rekap8.loc[rekap8["provinsi"] == prov]
    fig = makebar(prov, rekap9)
    st.plotly_chart(fig)
