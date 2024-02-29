import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

with st.sidebar:
    st.markdown(
        "<div style='display: flex; justify-content: center;'><h1>Fanza Eldanendra</h1></div>",
        unsafe_allow_html=True
    )
    st.write('')
    # Menambahkan foto
    st.markdown(
        "<div style='display: flex; justify-content: center;'>"
        "<img src='/Image/muka saya.jpg' "
        "width='200' style='border-radius: 50%;'>"
        "</div>",
        unsafe_allow_html=True
    )
    st.write('')
    st.text("Email    : fanza2003@gmail.com")
    st.text("GitHub   : github.com/fanza2003")
    st.text("LinkedIn : linkedin.com/in/fanza eldanendra")


# Dataframe Function
def merge_cust_seller(orders,seller):
    cust = orders[["customer_city","customer_state","lama_pengiriman_hari","order_id","customer_id"]]
    seller = df_order_items[["order_id","seller_id","seller_city","seller_state"]]
    cust_seller = cust.merge(seller, left_on='order_id', right_on='order_id',how='left')
    return cust_seller

# Load the cleaned data
seller = pd.read_csv('./Dataset/olist_sellers_dataset.csv')
orders = pd.read_csv('./Dataset/orders.csv')
df_order_items = pd.read_csv('./Dataset/order_items.csv')

# Cleaning the data
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
cust_seller = merge_cust_seller(orders, seller)
# Title of the dashboard
st.title("E-commerce Data Analysis Dashboard")

# Sidebar for user input if needed
# You can add widgets like sliders, selectboxes, etc.

# Exploratory Data Analysis Section

## Section 1: Payment Analysis
st.header("Payment Analysis")

# Visualization 1.2: Persebaran Pembelian berdasarkan Bagian Hari
st.subheader("Persebaran Pembelian berdasarkan Bagian Hari")
df_bagian_hari = orders.groupby(by="waktu_hari_pembelian")["order_id"].nunique().reset_index()
df_bagian_hari.rename(columns={"order_id": "total_orders"}, inplace=True)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="waktu_hari_pembelian", y="total_orders", data=df_bagian_hari.sort_values(by="total_orders"), palette=["#102cd4"])
ax.set_title("Persebaran Pembelian berdasarkan Bagian Hari")
ax.set_ylabel("Total Order")
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)
## Section 1: Category Analysis
st.header("Category Analysis")

# Visualization 2: Category Terlaris dan Sedikit Peminat
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))

# Visual 2.1: Category Terlaris
df_category_terlaris = df_order_items.groupby("product_category_name_english")["product_id"].count().sort_values(ascending=False).head(5)
ax[0].barh(df_category_terlaris.index, df_category_terlaris, color="#102cd4")
ax[0].set_title("Category Terlaris")
ax[0].set_xlabel("Jumlah Pembelian")

# Visual 2.2: Category Sedikit Peminat
df_category_sedikit_peminat = df_order_items.groupby("product_category_name_english")["product_id"].count().sort_values().head(5)
ax[1].barh(df_category_sedikit_peminat.index, df_category_sedikit_peminat, color="#D3D3D3")
ax[1].set_title("Category Sedikit Peminat")
ax[1].set_xlabel("Jumlah Pembelian")

st.pyplot(fig)

## Section 3: Delivery Time Analysis
st.header("Delivery Time Analysis")

# Visualization 4: Pengiriman antar Kota
st.subheader("Pengiriman antar Kota")
df_pengiriman_city = cust_seller.groupby(['seller_city', 'customer_city'])['lama_pengiriman_hari'].mean().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x=df_pengiriman_city['lama_pengiriman_hari'], ax=ax)
ax.set_title("Boxplot Lama Pengiriman antar Kota")
ax.set_xlabel("Lama Pengiriman (Hari)")

st.pyplot(fig)

# Visualization 5: Pengiriman antar State
st.subheader("Pengiriman antar State")
df_pengiriman_state = cust_seller.groupby(['seller_state', 'customer_state'])['lama_pengiriman_hari'].mean().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x=df_pengiriman_state['lama_pengiriman_hari'], ax=ax)
ax.set_title("Boxplot Lama Pengiriman antar State")
ax.set_xlabel("Lama Pengiriman (Hari)")

st.pyplot(fig)



# Visualization 6: Payment Type Distribution
st.subheader("Payment Type Distribution")
df_payment = orders.groupby(by="payment_type")["order_id"].nunique().reset_index()

fig, ax = plt.subplots(figsize=(8, 8))
colors = sns.color_palette('Blues')
ax.pie(df_payment["order_id"], labels=df_payment["payment_type"], colors=colors, autopct='%.0f%%')
ax.set_title("Payment Type Distribution")

st.pyplot(fig)

"""penggunaan credit card adalah tipe transaksi yang paling sering digunakan dan digunankan untuk transaksi yang bernilai besar dibandingkan tipe transaksi lain.

## Perbandingan penjualan tahun 2017 dan 2018
karena tahun 2018 hanya terdata sampai bulan agustus maka dalam EDA ini,perbandingan dilakukan untuk bulan januari sampai agustus saja.
"""

orders['nomor_bulan'] = orders['order_purchase_timestamp'].dt.strftime('%m')
df_tanggal_penjualan = orders.groupby(by=["nomor_bulan","year"]).order_id.nunique().reset_index()
df_tanggal_penjualan["nomor_bulan"] = df_tanggal_penjualan["nomor_bulan"].astype(str).astype(int)
df_tanggal_penjualan = df_tanggal_penjualan[df_tanggal_penjualan["nomor_bulan"] < 9]

month_names = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'Mei',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug'
}
df_tanggal_penjualan['nama_bulan'] = df_tanggal_penjualan['nomor_bulan'].map(month_names)

custom_palette = ["#0DA6D1", "#102cd4"]
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='nama_bulan', y='order_id', hue='year', data=df_tanggal_penjualan, ax=ax, palette=custom_palette)
plt.ylabel("total order")
plt.xlabel(None)

# Menampilkan plot menggunakan Streamlit
st.pyplot(fig)

df_tanggal =  orders.groupby(by=["month","year"]).order_id.nunique().reset_index()
df_tanggal["month"] = pd.to_datetime(df_tanggal["month"], format='%m-%Y')
plt.figure(figsize=(20, 6))
ax = sns.lineplot(x='month', y='order_id', data=df_tanggal, estimator=None, linewidth=3)
ax.set(xticks=df_tanggal.month.values)


st.header('Trend peningkatan penjualan')

plt.title("Tren Pertumbuhan Penjualan", loc="center", fontsize=18)
plt.ylabel("total order")
plt.xlabel(None)
ax.grid(False)
for tick in ax.get_xticklabels():
    tick.set_rotation(45)

# Menampilkan plot menggunakan Streamlit
st.pyplot(plt)


# Section for Additional Analysis (if needed)

# Conclusion Section
st.header("Conclusion")
st.markdown("""
1. **Berapa rata-rata payment value dari tiap tipe transaksi? dan transaksi tipe apa yang paling sering digunakan?**
    - 75% konsumen menggunakan tipe transaksi creditkan dengan rata-rata payment value sebesar 163.022616.

2. **Bagian hari apa yang sering digunakan oleh pembeli untuk melakukan transaksi?**
    - Hari senin adalah hari yang paling banyak digunakan oleh konsumen untuk belanja dan waktu paling aktif untuk berbelanja ada di siang hari.

3. **Bulan apa yang terjadi peningkatan penjualan tertinggi?**
    - November 2017 adalah bulan dengan penjualan tertinggi, terutama di tanggal 24/11/2017.
""")

