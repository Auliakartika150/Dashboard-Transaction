from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# TRANSACTIONS DASHBOARD
# Sumber data: transactions.xlsx (sheet "transactions" + "customer")
# Kedua sheet dihubungkan lewat customer_id.
# Nilai uang hanya dihitung dari transaksi berstatus Success.
# ============================================================

st.set_page_config(
    page_title="Transactions Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY, BLUE, TEAL, ORANGE, GRAY = "#17324D", "#2563EB", "#0F9F8F", "#F59E0B", "#64748B"
SOFT = "#CBD5E1"

st.markdown(
    f"""
    <style>
      .stApp {{ background: #F6F8FC; }}
      [data-testid="stSidebar"] {{ background: #EEF3F9; }}
      .block-container {{ padding-top: 1.5rem; max-width: 1400px; }}
      h1, h2, h3 {{ color: {NAVY}; letter-spacing: -0.02em; }}
      div[data-testid="stMetric"] {{
          background: #FFFFFF; border: 1px solid #E3EAF3; border-radius: 12px;
          padding: 14px 16px; box-shadow: 0 2px 8px rgba(23,50,77,.04);
      }}
      div[data-testid="stMetricLabel"] p {{ color: {GRAY}; font-size: .82rem; }}
      div[data-testid="stMetricValue"] {{ color: {NAVY}; font-weight: 700; font-size: 1.45rem; }}
      div[data-testid="stPlotlyChart"] {{
          background: #FFFFFF; border: 1px solid #E6ECF3; border-radius: 12px; padding: 4px;
      }}
      .insight {{
          background: #EAF1FB; border-left: 4px solid {BLUE}; border-radius: 8px;
          padding: 12px 16px; color: #2B4560; font-size: .92rem; line-height: 1.6; margin: 1rem 0;
      }}
      .subtitle {{ color: {GRAY}; margin-top: -.5rem; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Fungsi bantu format ----------
def rupiah(value):
    return "Rp " + f"{value:,.0f}".replace(",", ".")


def rupiah_ringkas(value):
    """Format singkat agar angka besar mudah dibaca: Rp 1,25 miliar."""
    for batas, satuan in [(1e12, "triliun"), (1e9, "miliar"), (1e6, "juta")]:
        if abs(value) >= batas:
            return f"Rp {value / batas:.2f}".replace(".", ",") + f" {satuan}"
    return rupiah(value)


def number(value):
    return f"{int(value):,}".replace(",", ".")


def percent(value):
    return f"{value:.1f}%".replace(".", ",")


def style(fig, height=340):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=45, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#24364B"),
        title_font_size=15,
        coloraxis_showscale=False,
    )
    fig.update_yaxes(gridcolor="#E8EEF5")
    return fig


# ---------- Muat & bersihkan data ----------
def find_data_file():
    for folder in (Path(__file__).resolve().parent, Path.cwd()):
        path = folder / "transactions.xlsx"
        if path.exists():
            return path
    return None


@st.cache_data(show_spinner="Memuat data...")
def load_data(path_str):
    raw_tx = pd.read_excel(path_str, sheet_name="transactions")
    raw_cust = pd.read_excel(path_str, sheet_name="customer")

    need_tx = {"booking_id", "created_at", "customer_id", "quantity", "price",
               "payment_method", "payment_status", "promo_amount", "promo_code", "shipment_fee"}
    need_cust = {"customer_id", "gender", "birthdate", "home_location"}
    missing = (need_tx - set(raw_tx.columns)) | (need_cust - set(raw_cust.columns))
    if missing:
        raise ValueError(f"Kolom wajib tidak ditemukan: {sorted(missing)}")

    tx = raw_tx.copy()
    tx["created_at"] = pd.to_datetime(tx["created_at"], errors="coerce")
    for col in ["quantity", "price", "promo_amount", "shipment_fee", "customer_id"]:
        tx[col] = pd.to_numeric(tx[col], errors="coerce")
    for col in ["payment_status", "payment_method"]:
        tx[col] = tx[col].astype("string").str.strip().replace("", pd.NA).fillna("Tidak diketahui")
    tx["promo_code"] = tx["promo_code"].astype("string").str.strip().replace("", pd.NA)
    tx["promo_status"] = np.where(tx["promo_code"].isna(), "Non-Promo", "Promo")
    tx["promo_amount"] = tx["promo_amount"].fillna(0)
    tx["gross_amount"] = tx["quantity"] * tx["price"]
    tx["nmv"] = tx["gross_amount"] - tx["promo_amount"]
    tx["total_paid"] = tx["nmv"] + tx["shipment_fee"]
    tx["month_date"] = tx["created_at"].dt.to_period("M").dt.to_timestamp()

    cust = raw_cust.copy()
    cust["birthdate"] = pd.to_datetime(cust["birthdate"], errors="coerce")
    ref_date = tx["created_at"].max()
    cust["age"] = (ref_date - cust["birthdate"]).dt.days / 365.25
    cust.loc[cust["age"] < 0, "age"] = np.nan
    cust["age_group"] = pd.cut(
        cust["age"],
        bins=[0, 15, 25, 35, 45, np.inf],
        right=False,
        labels=["< 15", "15–24", "25–34", "35–44", "45+"],
    )
    cust = cust[["customer_id", "gender", "home_location", "age_group"]]

    merged = tx.merge(cust, on="customer_id", how="left", validate="many_to_one")
    merged["gender"] = merged["gender"].fillna("Tidak diketahui")
    merged["home_location"] = merged["home_location"].fillna("Tidak diketahui")
    return merged


data_file = find_data_file()
if data_file is None:
    st.title("Transactions Dashboard")
    st.warning("File transactions.xlsx belum ditemukan. Letakkan di folder yang sama dengan file dashboard ini, lalu jalankan ulang.")
    st.stop()

try:
    df = load_data(str(data_file))
except Exception as exc:
    st.error(f"Data gagal dibaca: {exc}")
    st.stop()

if df["created_at"].notna().sum() == 0:
    st.error("Kolom created_at tidak memiliki tanggal yang valid.")
    st.stop()

# ---------- Filter ----------
st.sidebar.title("Filter")
min_d, max_d = df["created_at"].min().date(), df["created_at"].max().date()
date_range = st.sidebar.date_input("Periode", value=(min_d, max_d), min_value=min_d, max_value=max_d)
start, end = (date_range if isinstance(date_range, (tuple, list)) and len(date_range) == 2
              else (date_range, date_range))

statuses = sorted(df["payment_status"].unique())
methods = sorted(df["payment_method"].unique())
sel_status = st.sidebar.multiselect("Status pembayaran", statuses, default=statuses)
sel_method = st.sidebar.multiselect("Metode pembayaran", methods, default=methods)
sel_promo = st.sidebar.multiselect("Jenis pembelian", ["Promo", "Non-Promo"], default=["Promo", "Non-Promo"])

mask = (
    df["created_at"].dt.date.between(start, end)
    & df["payment_status"].isin(sel_status)
    & df["payment_method"].isin(sel_method)
    & df["promo_status"].isin(sel_promo)
)
filtered = df[mask]
success = filtered[filtered["payment_status"].str.casefold() == "success"]

# ---------- Header ----------
st.title("Transactions Dashboard")
st.markdown(
    f'<p class="subtitle">Periode {start:%d %b %Y} – {end:%d %b %Y}. '
    "Nilai uang hanya dari transaksi berstatus Success.</p>",
    unsafe_allow_html=True,
)

if filtered.empty:
    st.warning("Tidak ada data yang sesuai dengan filter. Ubah pilihan filter di sidebar.")
    st.stop()

# ---------- KPI ----------
n_total = filtered["booking_id"].nunique()
n_success = success["booking_id"].nunique()
success_rate = n_success / n_total * 100 if n_total else 0
nmv = success["nmv"].sum()
n_customers = success["customer_id"].nunique()
avg_order = success.groupby("booking_id")["total_paid"].sum().mean() if n_success else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Nilai penjualan (NMV)", rupiah_ringkas(nmv), help=f"NMV = harga × jumlah − promo. Nilai lengkap: {rupiah(nmv)}")
k2.metric("Booking berhasil", number(n_success), help="Jumlah booking unik berstatus Success.")
k3.metric("Pelanggan aktif", number(n_customers), help="Pelanggan unik dengan transaksi berhasil.")
k4.metric("Rata-rata per booking", rupiah_ringkas(avg_order), help="Rata-rata total bayar (NMV + ongkir) per booking berhasil.")
k5.metric("Tingkat keberhasilan", percent(success_rate), help="Booking berhasil ÷ seluruh booking sesuai filter.")

# ---------- Data agregat ----------
monthly = (
    success.dropna(subset=["month_date"])
    .groupby("month_date", as_index=False)
    .agg(nmv=("nmv", "sum"), bookings=("booking_id", "nunique"),
         customers=("customer_id", "nunique"), units=("quantity", "sum"))
    .sort_values("month_date")
)

pay_all = filtered.groupby("payment_method").agg(total=("booking_id", "nunique"))
pay_ok = success.groupby("payment_method").agg(berhasil=("booking_id", "nunique"), nmv=("nmv", "sum"))
pay = pay_all.join(pay_ok).fillna(0).reset_index()
pay["rate"] = np.where(pay["total"] > 0, pay["berhasil"] / pay["total"] * 100, 0)

# ---------- Insight otomatis ----------
points = []
if not monthly.empty:
    best = monthly.loc[monthly["nmv"].idxmax()]
    points.append(f"Penjualan tertinggi terjadi pada <b>{best['month_date']:%B %Y}</b> ({rupiah_ringkas(best['nmv'])}).")
if not pay[pay["nmv"] > 0].empty:
    top_pay = pay.loc[pay["nmv"].idxmax()]
    points.append(f"Metode pembayaran dengan nilai terbesar: <b>{top_pay['payment_method']}</b>.")
if n_success:
    promo_share = success.loc[success["promo_status"] == "Promo", "booking_id"].nunique() / n_success * 100
    points.append(f"<b>{percent(promo_share)}</b> booking berhasil menggunakan promo.")
if points:
    st.markdown('<div class="insight"><b>Sorotan:</b> ' + " ".join(points) + "</div>", unsafe_allow_html=True)

# ---------- Tab ----------
tab1, tab2, tab3 = st.tabs(["Tren Penjualan", "Pembayaran & Promo", "Pelanggan"])

with tab1:
    metric_map = {
        "Nilai penjualan (NMV)": ("nmv", True),
        "Booking berhasil": ("bookings", False),
        "Pelanggan aktif": ("customers", False),
        "Unit terjual": ("units", False),
    }
    label = st.selectbox("Metrik", list(metric_map))
    col, is_money = metric_map[label]
    left, right = st.columns([2, 1])
    with left:
        if monthly.empty:
            st.info("Belum ada transaksi berhasil pada filter ini.")
        else:
            plot = monthly.copy()
            if is_money:
                plot[col] = plot[col] / 1e6
            fig = px.bar(plot, x="month_date", y=col, title=f"{label} per bulan",
                         labels={"month_date": "Bulan", col: "Juta Rp" if is_money else label})
            fig.update_traces(marker_color=BLUE)
            fig.update_xaxes(tickformat="%b %Y", dtick="M1" if len(plot) <= 12 else "M3")
            if is_money:
                fig.update_traces(hovertemplate="%{x|%B %Y}<br>Rp %{y:,.1f} juta<extra></extra>")
            st.plotly_chart(style(fig, 380), use_container_width=True)
    with right:
        status = filtered.groupby("payment_status")["booking_id"].nunique().reset_index(name="booking")
        fig = px.pie(status, names="payment_status", values="booking", hole=0.6,
                     title="Komposisi status pembayaran",
                     color_discrete_sequence=[TEAL, ORANGE, BLUE, SOFT])
        fig.update_traces(textinfo="percent+label", textposition="inside")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style(fig, 380), use_container_width=True)

    with st.expander("Lihat tabel ringkasan bulanan"):
        table = monthly.assign(Bulan=monthly["month_date"].dt.strftime("%B %Y"))
        table = table[["Bulan", "bookings", "customers", "units", "nmv"]]
        table.columns = ["Bulan", "Booking berhasil", "Pelanggan aktif", "Unit terjual", "NMV"]
        st.dataframe(table.style.format({"NMV": rupiah, "Booking berhasil": number,
                                         "Pelanggan aktif": number, "Unit terjual": number}),
                     use_container_width=True, hide_index=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        d = pay.sort_values("nmv")
        fig = px.bar(d, x="nmv", y="payment_method", orientation="h",
                     title="Nilai penjualan per metode pembayaran",
                     labels={"nmv": "NMV (Rp)", "payment_method": ""})
        fig.update_traces(marker_color=BLUE)
        fig.update_xaxes(tickformat="~s")
        st.plotly_chart(style(fig), use_container_width=True)
    with c2:
        d = pay.sort_values("rate")
        fig = px.bar(d, x="rate", y="payment_method", orientation="h",
                     title="Tingkat keberhasilan per metode (%)",
                     labels={"rate": "Berhasil (%)", "payment_method": ""})
        fig.update_traces(marker_color=TEAL)
        fig.update_xaxes(range=[0, 100])
        st.plotly_chart(style(fig), use_container_width=True)

    st.subheader("Promo vs non-promo")
    promo = (
        success.groupby("promo_status")
        .agg(bookings=("booking_id", "nunique"), nmv=("nmv", "sum"), potongan=("promo_amount", "sum"))
        .reset_index()
    )
    if promo.empty:
        st.info("Belum ada transaksi berhasil pada filter ini.")
    else:
        promo["avg"] = promo["nmv"] / promo["bookings"]
        view = promo.rename(columns={"promo_status": "Jenis", "bookings": "Booking berhasil", "nmv": "NMV",
                                     "potongan": "Total potongan", "avg": "Rata-rata NMV per booking"})
        st.dataframe(view.style.format({"Booking berhasil": number, "NMV": rupiah,
                                        "Total potongan": rupiah, "Rata-rata NMV per booking": rupiah}),
                     use_container_width=True, hide_index=True)

    codes = (
        success[success["promo_code"].notna()]
        .groupby("promo_code")
        .agg(bookings=("booking_id", "nunique"), potongan=("promo_amount", "sum"))
        .reset_index().sort_values("bookings", ascending=False).head(5)
    )
    if not codes.empty:
        st.subheader("5 kode promo terpopuler")
        codes.columns = ["Kode promo", "Booking berhasil", "Total potongan"]
        st.dataframe(codes.style.format({"Booking berhasil": number, "Total potongan": rupiah}),
                     use_container_width=True, hide_index=True)

with tab3:
    c1, c2, c3 = st.columns(3)
    with c1:
        g = success.groupby("gender")["customer_id"].nunique().reset_index(name="n")
        fig = px.pie(g, names="gender", values="n", hole=0.6, title="Gender pelanggan aktif",
                     color_discrete_sequence=[BLUE, TEAL, SOFT])
        fig.update_traces(textinfo="percent+label", textposition="inside")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style(fig), use_container_width=True)
    with c2:
        a = (success.dropna(subset=["age_group"]).groupby("age_group", observed=False)["customer_id"]
             .nunique().reset_index(name="n"))
        fig = px.bar(a, x="age_group", y="n", title="Kelompok usia (tahun)",
                     labels={"age_group": "", "n": "Pelanggan aktif"})
        fig.update_traces(marker_color=TEAL)
        st.plotly_chart(style(fig), use_container_width=True)
    with c3:
        loc = (success.groupby("home_location")["customer_id"].nunique().reset_index(name="n")
               .sort_values("n", ascending=False).head(8).sort_values("n"))
        fig = px.bar(loc, x="n", y="home_location", orientation="h", title="8 lokasi teratas",
                     labels={"n": "Pelanggan aktif", "home_location": ""})
        fig.update_traces(marker_color=BLUE)
        st.plotly_chart(style(fig), use_container_width=True)

    st.subheader("10 pelanggan dengan total pembayaran tertinggi")
    top = (
        success.groupby(["customer_id", "home_location"])
        .agg(bookings=("booking_id", "nunique"), total_paid=("total_paid", "sum"))
        .reset_index().sort_values("total_paid", ascending=False).head(10)
    )
    top.columns = ["ID pelanggan", "Lokasi", "Booking berhasil", "Total pembayaran"]
    st.dataframe(top.style.format({"ID pelanggan": "{:.0f}", "Booking berhasil": number,
                                   "Total pembayaran": rupiah}),
                 use_container_width=True, hide_index=True)

st.caption("NMV = harga × jumlah − promo. Total pembayaran = NMV + ongkir. Hanya transaksi berstatus Success yang dihitung sebagai nilai uang.")