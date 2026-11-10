import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(page_title="FlashMart Store Pro", page_icon="⚡", layout="centered")

# 2. Custom CSS untuk mempercantik tampilan mirip aplikasi modern
st.markdown("""
    <style>
    /* Hilangkan padding atas bawaan streamlit */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 480px; /* Tampilan ala mobile app */
    }
    
    /* Header Hijau */
    .main-header {
        background: linear-gradient(135deg, #00b050, #009943);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    
    /* Banner Voucher */
    .promo-banner {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 13px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    /* Kartu Produk */
    .product-card {
        background-color: #ffffff;
        border: 1px solid #eaeaea;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header & Search Bar
st.markdown("""
    <div class="main-header">
        <h2 style="margin:0; font-size: 22px;">⚡ FlashMart Store Pro</h2>
    </div>
""", unsafe_allow_html=True)

# Kotak Pencarian
search_query = st.text_input("", placeholder="🔍 Cari kebutuhan harian / pulsa...", label_visibility="collapsed")

# 4. Layanan PBB / Menu Cepat
st.markdown("##### 📱 Layanan Pulsa & PPOB")
ppob_cols = st.columns(4)
with ppob_cols[0]:
    if st.button("📶 Pulsa", use_container_width=True):
        st.toast("Fitur Pulsa dipilih")
with ppob_cols[1]:
    if st.button("🌐 Kuota", use_container_width=True):
        st.toast("Fitur Kuota Data dipilih")
with ppob_cols[2]:
    if st.button("⚡ PLN", use_container_width=True):
        st.toast("Fitur Token PLN dipilih")
with ppob_cols[3]:
    if st.button("💳 E-Money", use_container_width=True):
        st.toast("Fitur E-Money dipilih")

st.markdown("---")

# 5. Kategori Pilihan (Filter)
categories = ["Semua", "Sembako", "Minuman", "Perawatan"]
selected_category = st.selectbox("Pilih Kategori:", categories, label_visibility="collapsed")

# 6. Banner Promo Voucher
st.markdown("""
    <div class="promo-banner">
        🔥 Gunakan Voucher <b>FLASHMARTINA</b> untuk Diskon Rp 10.000!
    </div>
""", unsafe_allow_html=True)

# 7. Data Produk Katalog
products = [
    {"id": 1, "name": "Minyak Goreng 2L", "category": "Sembako", "stock": 25, "price": 38000, "icon": "🍳"},
    {"id": 2, "name": "Beras Premium 5kg", "category": "Sembako", "stock": 15, "price": 69000, "icon": "🌾"},
    {"id": 3, "name": "Susu UHT Ultra 1L", "category": "Minuman", "stock": 30, "price": 19500, "icon": "🥛"},
    {"id": 4, "name": "Mie Instan (1 Dus)", "category": "Sembako", "stock": 12, "price": 115000, "icon": "📦"}
]

# Inisialisasi Keranjang
if "cart" not in st.session_state:
    st.session_state.cart = []

st.markdown("### 🛒 Katalog Produk - FlashMart Pusat")

# Filter berdasarkan pencarian atau kategori
filtered_products = [
    p for p in products 
    if (selected_category == "Semua" or p["category"] == selected_category) and 
       (search_query.lower() in p["name"].lower() if search_query else True)
]

# 8. Menampilkan Produk dalam Grid 2 Kolom (Ala Mobile Apps)
grid_cols = st.columns(2)
for index, product in enumerate(filtered_products):
    with grid_cols[index % 2]:
        st.markdown(f"""
            <div class="product-card">
                <div style="font-size: 36px; margin-bottom: 5px;">{product['icon']}</div>
                <div style="font-weight: bold; font-size: 14px; height: 40px; color: #333;">{product['name']}</div>
                <div style="font-size: 11px; color: #777; margin-top: 5px;">Stok: {product['stock']}</div>
                <div style="color: #e74c3c; font-weight: bold; font-size: 15px; margin: 8px 0;">Rp {product['price']:,}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Tombol Aksi: Keranjang & Beli
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("➕ Keranjang", key=f"cart_{product['id']}", use_container_width=True):
                found = False
                for item in st.session_state.cart:
                    if item["id"] == product["id"]:
                        item["quantity"] += 1
                        found = True
                        break
                if not found:
                    st.session_state.cart.append({**product, "quantity": 1})
                st.toast(f"{product['name']} masuk keranjang!")
        with btn_col2:
            if st.button("⚡ Beli", key=f"buy_{product['id']}", type="primary", use_container_width=True):
                st.success(f"Berhasil membeli {product['name']} seharga Rp {product['price']:,}!")

# 9. Ringkasan Keranjang Belanja di Bagian Bawah
st.markdown("---")
st.subheader("🛍️ Ringkasan Keranjang Anda")
if not st.session_state.cart:
    st.info("Belum ada produk di keranjang.")
else:
    total_belanja = sum(item["price"] * item["quantity"] for item in st.session_state.cart)
    for item in st.session_state.cart:
        st.write(f"- {item['name']} ({item['quantity']}x) = Rp {item['price'] * item['quantity']:,}")
    
    st.markdown(f"**Total Pembayaran: Rp {total_belanja:,}**")
    if st.button("Proses Checkout Sekarang", type="primary", use_container_width=True):
        st.success("Checkout Berhasil! Terima kasih telah berbelanja di FlashMart.")
        st.session_state.cart = []
        st.rerun()
