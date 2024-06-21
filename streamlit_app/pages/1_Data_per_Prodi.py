
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="ITY - Institut Teknologi Yogyakarta",
    layout="wide",
    page_icon=":school:",
)

st.logo("https://github.com/herubagush/rekap_data_mahasiswa/blob/main/streamlit_app/images/logo.png")

st.title("Data Sebaran Mahasiswa Institut Teknologi Yogyakarta (ITY) per Prodi")

data_mahasiswa = pd.read_csv("data_mahasiswa_ity.csv")
data_select = data_mahasiswa[
    ["angkatan", "prodi", "nama", "jk", "kabupaten", "provinsi", "instansi_asal"]
]
data_select = data_select.fillna("")
data = data_select.replace(r"^\s*$", "UNKNOWN", regex=True)

st.sidebar.header("Filter:")
dt_prodi = data["prodi"].unique().tolist()
prodi = st.sidebar.selectbox(
    "Program Studi (Prodi)", options=dt_prodi, placeholder="Pilih Program Studi (Prodi)"
)
dt_angkatan = data.loc[data["prodi"] == prodi]["angkatan"].unique().tolist()
angkatan = st.sidebar.multiselect(
    "Tahun Angkatan",
    options=dt_angkatan,
    default=dt_angkatan[0:3],
    placeholder="Pilih Tahun Angkatan",
)
dt_provinsi = data.loc[data["prodi"] == prodi]["provinsi"].unique().tolist()
provinsi = st.sidebar.multiselect(
    "Wilayah",
    options=dt_provinsi,
    default=dt_provinsi[0:3],
    placeholder="Pilih Wilayah",
)
st.header("Prodi: " + prodi)
df = (
    data.loc[data["prodi"] == prodi]
    .loc[data["angkatan"].isin(angkatan)]
    .loc[data["provinsi"].isin(provinsi)]
)
rekap = (
    df.groupby(by=["angkatan", "provinsi"])
    .count()[["nama"]]
    .rename(columns={"nama": "mahasiswa"})
)
rekap = rekap.reset_index()
rekap["angkatan"] = rekap["angkatan"].astype("object")
fig = px.bar(
    rekap,
    x="mahasiswa",
    y="provinsi",
    orientation="h",
    height=800,
    width=1000,
    color="angkatan",
    text_auto=True,
    template="plotly_white",
)
fig.update_layout(
    title="Sebaran Mahasiswa Prodi " + prodi + " pada Setiap Provinsi",
    title_x=0.3,
    title_y=0.95,
    xaxis_title="Jumlah Mahasiswa",
    barmode="stack",
    legend=dict(title="Angakatan", xanchor="right", yanchor="top"),
)
fig.update_xaxes(title="Jumlah Mahasiswa")
fig.update_yaxes(title=None)
st.plotly_chart(fig)
