import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="Minimarket Online Berkah", page_icon="🏪", layout="wide")

# CSS Styling tambahan (harus dibungkus dalam st.markdown dengan unsafe_allow_html=True)
st.markdown("""
    <style>
    .product-card {
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Judul Aplikasi
st.title("🏪 Minimarket Online Berkah")
st.write("Belanja kebutuhan harian lebih mudah dan cepat")
st.markdown("---")

# Data Produk Minimarket
products = [
    {"id": 1, "name": "Minyak Goreng 2L", "price": 35000},
    {"id": 2, "name": "Beras Premium 5kg", "price": 68000},
    {"id": 3, "name": "Gula Pasir 1kg", "price": 15500},
    {"id": 4, "name": "Telur Ayam 1kg", "price": 28000},
    {"id": 5, "name": "Mie Instan (1 Bungkus)", "price": 3000},
    {"id": 6, "name": "Susu UHT 1L", "price": 19000},
    {"id": 7, "name": "Teh Celup Kotak", "price": 9000},
    {"id": 8, "name": "Sabun Mandi Batang", "price": 4500}
]

# Inisialisasi Keranjang Belanja di Session State Streamlit
if "cart" not in st.session_state:
    st.session_state.cart = []

# Layout Kolom: Kiri untuk Produk, Kanan untuk Keranjang
col1, col2 = st.kol2 = st.columns([2, 1]) if hasattr(st, 'columns') else (st.container(), st.container())

# Jika menggunakan st.columns versi standar:
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Daftar Produk")
    
    # Menampilkan produk dalam grid 3 kolom
    grid_cols = st.columns(3)
    for index, product in enumerate(products):
        with grid_cols[index % 3]:
            st.markdown(f"""
                <div class="product-card">
                    <h4>{product['name']}</h4>
                    <p style="color: #e74c3c; font-weight: bold;">Rp {product['price']:,}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Tambah", key=f"add_{product['id']}"):
                # Cek apakah produk sudah ada di keranjang
                found = False
                for item in st.session_state.cart:
                    if item["id"] == product["id"]:
                        item["quantity"] += 1
                        found = True
                        break
                if not found:
                    st.session_state.cart.append({
                        "id": product["id"],
                        "name": product["name"],
                        "price": product["price"],
                        "quantity": 1
                    })
                st.success(f"{product['name']} ditambahkan!")
                st.rerun()

with col2:
    st.subheader("🛒 Keranjang Belanja")
    
    if not st.session_state.cart:
        st.info("Keranjang masih kosong.")
    else:
        total = 0
        for item in st.session_state.cart:
            item_total = item["price"] * item["quantity"]
            total += item_total
            
            st.write(f"**{item['name']}**")
            st.text(f"{item['quantity']} x Rp {item['price']:,} = Rp {item_total:,}")
            
            if st.button("Hapus", key=f"del_{item['id']}"):
                st.session_state.cart = [i for i in st.session_state.cart if i["id"] != item["id"]]
                st.rerun()
            st.markdown("---")
            
        st.markdown(f"### Total: Rp {total:,}")
        
        if st.button("Checkout Pesanan", type="primary"):
            st.success(f"Terima kasih! Pesanan senilai Rp {total:,} berhasil diproses.")
            st.session_state.cart = []
            st.rerun()
