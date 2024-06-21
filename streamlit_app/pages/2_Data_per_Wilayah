import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="ITY - Institut Teknologi Yogyakarta",
    layout="wide",
    page_icon=":school:",
)

st.logo("images/logo.png")

st.title("Data Sebaran Mahasiswa Institut Teknologi Yogyakarta (ITY) per Wilayah")

data_mahasiswa = pd.read_csv("data_mahasiswa_ity.csv")
data_select = data_mahasiswa[
    ["angkatan", "prodi", "nama", "jk", "kabupaten", "provinsi", "instansi_asal"]
]
data_select = data_select.fillna("")
data = data_select.replace(r"^\s*$", "UNKNOWN", regex=True)

st.sidebar.header("Filter:")
dt_provinsi = data["provinsi"].unique().tolist()
provinsi = st.sidebar.selectbox(
    "Wilayah", options=dt_provinsi, placeholder="Pilih Wilayah"
)
dt_prodi = data.loc[data["provinsi"] == provinsi]["prodi"].unique().tolist()
prodi = st.sidebar.multiselect(
    "Program Studi (Prodi)",
    options=dt_prodi,
    default=dt_prodi[0:3],
    placeholder="Pilih Program Studi (Prodi)",
)
dt_angkatan = data.loc[data["provinsi"] == provinsi]["angkatan"].unique().tolist()
angkatan = st.sidebar.multiselect(
    "Tahun Angkatan",
    options=dt_angkatan,
    default=dt_angkatan[0:3],
    placeholder="Pilih Tahun Angkatan",
)
st.header("Wilayah Provinsi: " + provinsi)
df = (
    data.loc[data["provinsi"] == provinsi]
    .loc[data["prodi"].isin(prodi)]
    .loc[data["angkatan"].isin(angkatan)]
)
rekap = (
    df.groupby(by=["prodi", "angkatan", "kabupaten"])
    .count()[["nama"]]
    .rename(columns={"nama": "mahasiswa"})
)
rekap = rekap.reset_index()


def grafik(data, prod, angkatan):
    d = data.loc[data["prodi"] == prod].loc[data["angkatan"].isin(angkatan)]
    d["angkatan"] = d["angkatan"].astype("object")
    fig = px.bar(
        d,
        x="mahasiswa",
        y="kabupaten",
        orientation="h",
        height=800,
        width=1000,
        color="angkatan",
        text_auto=True,
        template="plotly_white",
    )
    fig.update_layout(
        title="Sebaran Mahasiswa Prodi " + prod + " pada Setiap Kabupaten",
        title_x=0.3,
        title_y=0.95,
        xaxis_title="Jumlah Mahasiswa",
        barmode="stack",
        legend=dict(title="Angakatan", xanchor="right", yanchor="top"),
    )
    fig.update_xaxes(title="Jumlah Mahasiswa")
    fig.update_yaxes(title=None)
    return fig


for prod in prodi:
    fig = grafik(rekap, prod, angkatan)
    st.plotly_chart(fig)
