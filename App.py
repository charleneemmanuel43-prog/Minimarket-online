import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# 1. Konfigurasi Halaman
st.set_page_config(page_title="FlashMart Store Pro", page_icon="⚡", layout="centered")

# 2. Custom CSS untuk Tampilan Modern
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 480px;
    }
    .main-header {
        background: linear-gradient(135deg, #00b050, #009943);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
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

# Header Aplikasi
st.markdown("""
    <div class="main-header">
        <h2 style="margin:0; font-size: 22px;">⚡ FlashMart Store Pro</h2>
    </div>
""", unsafe_allow_html=True)

search_query = st.text_input("", placeholder="🔍 Cari kebutuhan harian / pulsa...", label_visibility="collapsed")

# Kategori Pilihan
categories = ["Semua", "Sembako", "Minuman", "Perawatan"]
selected_category = st.selectbox("Pilih Kategori:", categories, label_visibility="collapsed")

st.markdown("""
    <div class="promo-banner">
        🔥 Gunakan Voucher <b>FLASHMARTINA</b> untuk Diskon Rp 10.000!
    </div>
""", unsafe_allow_html=True)

# Data Produk Katalog (Disesuaikan mirip minimarket)
products = [
    {"id": 1, "name": "S/ROTI KRIM KEJU 72G", "category": "Sembako", "stock": 25, "price": 4500, "icon": "🍞"},
    {"id": 2, "name": "CIMORY MIX BERRY 225", "category": "Minuman", "stock": 15, "price": 8500, "icon": "🧃"},
    {"id": 3, "name": "CAFELA EXPRESO 200ML", "category": "Minuman", "stock": 30, "price": 3500, "icon": "☕"},
    {"id": 4, "name": "FF LOW FAT VAN 225", "category": "Minuman", "stock": 12, "price": 5200, "icon": "🥛"},
    {"id": 5, "name": "PLASTIK SDG", "category": "Lainnya", "stock": 100, "price": 1000, "icon": "🛍️"}
]

# Inisialisasi State Keranjang & Checkout Terakhir
if "cart" not in st.session_state:
    st.session_state.cart = []
if "last_checkout" not in st.session_state:
    st.session_state.last_checkout = None

st.markdown("### 🛒 Katalog Produk - FlashMart Pusat")

filtered_products = [
    p for p in products 
    if (selected_category == "Semua" or p["category"] == selected_category) and 
       (search_query.lower() in p["name"].lower() if search_query else True)
]

# Grid Produk
grid_cols = st.columns(2)
for index, product in enumerate(filtered_products):
    with grid_cols[index % 2]:
        st.markdown(f"""
            <div class="product-card">
                <div style="font-size: 32px; margin-bottom: 5px;">{product['icon']}</div>
                <div style="font-weight: bold; font-size: 13px; height: 35px; color: #333;">{product['name']}</div>
                <div style="font-size: 11px; color: #777; margin-top: 3px;">Stok: {product['stock']}</div>
                <div style="color: #e74c3c; font-weight: bold; font-size: 14px; margin: 6px 0;">Rp {product['price']:,}</div>
            </div>
        """, unsafe_allow_html=True)
        
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
                st.rerun()
        with btn_col2:
            if st.button("⚡ Beli", key=f"buy_{product['id']}", type="primary", use_container_width=True):
                # Langsung masukkan ke keranjang & proses
                found = False
                for item in st.session_state.cart:
                    if item["id"] == product["id"]:
                        item["quantity"] += 1
                        found = True
                        break
                if not found:
                    st.session_state.cart.append({**product, "quantity": 1})
                st.rerun()

# Ringkasan Keranjang & Rumus Pembayaran
st.markdown("---")
st.subheader("🛍️ Ringkasan Keranjang Belanja")

if not st.session_state.cart:
    st.info("Keranjang belanja Anda masih kosong.")
else:
    subtotal_belanja = sum(item["price"] * item["quantity"] for item in st.session_state.cart)
    
    for item in st.session_state.cart:
        item_sub = item["price"] * item["quantity"]
        st.text(f"{item['name']} | {item['quantity']} x {item['price']:,} = Rp {item_sub:,}")
    
    st.markdown("---")
    
    # Input Simulasi Diskon & Pembayaran Tunai
    diskon_khusus = st.number_input("Diskon Promo (Rp)", min_value=0, value=0, step=500)
    harga_jual_bersih = max(0, subtotal_belanja - diskon_khusus)
    
    st.markdown(f"**Subtotal Harga Jual: Rp {subtotal_belanja:,}**")
    st.markdown(f"**Total Setelah Diskon: Rp {harga_jual_bersih:,}**")
    
    uang_tunai = st.number_input("Masukkan Uang Tunai (Rp)", min_value=0, value=int(harga_jual_bersih), step=5000)
    kembalian = uang_tunai - harga_jual_bersih
    
    if uang_tunai < harga_jual_bersih:
        st.warning("⚠️ Uang tunai kurang dari total belanja!")
    else:
        st.success(f"Uang Kembalian: **Rp {kembalian:,}**")

    if st.button("💳 Proses Checkout & Buat Struk", type="primary", use_container_width=True):
        # Simpan riwayat transaksi untuk dicetak struknya
        st.session_state.last_checkout = {
            "datetime": datetime.now().strftime("%d. %m. %y- %H:%M"),
            "items": list(st.session_state.cart),
            "subtotal": subtotal_belanja,
            "diskon": diskon_khusus,
            "total": harga_jual_bersih,
            "tunai": uang_tunai,
            "kembali": kembalian
        }
        st.session_state.cart = []
        st.success("Transaksi berhasil diproses!")
        st.rerun()

# Bagian Cetak Struk ala Indomaret
if st.session_state.last_checkout:
    st.markdown("---")
    st.subheader("🧾 Struk Belanja Resmi")
    
    tx = st.session_state.last_checkout
    
    receipt_items_html = ""
    for item in tx["items"]:
        sub = item["price"] * item["quantity"]
        receipt_items_html += f"""
            <div style="margin-bottom: 3px;">
                <div>{item['name']}</div>
                <div style="display: flex; justify-content: space-between;">
                    <span>&nbsp;&nbsp;{item['quantity']} &nbsp;&nbsp; {item['price']:,}</span>
                    <span>{sub:,}</span>
                </div>
            </div>
        """
    
    receipt_html = f"""
    <div id="print-area" style="font-family: 'Courier New', Courier, monospace; width: 300px; background: #fff; padding: 15px; border: 1px dashed #333; color: #000; font-size: 12px;">
        <div style="text-align: center;">
            <strong>PT FLASHMART STORE INDONESIA</strong><br>
            <span style="font-size: 10px;">JL. RAYA JATINANGOR - SUMEDANG</span><br>
            <span style="font-size: 10px;">NPWP: 21.151.107.6-446.001</span>
            <p style="margin: 5px 0;">--------------------------------</p>
            <strong>JATINANGOR KM. 20 - SUMEDANG</strong>
        </div>
        <div style="margin: 8px 0; font-size: 11px;">
            {tx['datetime']} &nbsp;&nbsp; 2. 0. 31 &nbsp;&nbsp; 914115/ALIA MU/01
        </div>
        <p style="margin: 5px 0;">--------------------------------</p>
        <div>
            {receipt_items_html}
        </div>
        <p style="margin: 5px 0;">--------------------------------</p>
        <div style="display: flex; justify-content: space-between;">
            <span>HARGA JUAL :</span>
            <span>{tx['subtotal']:,}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>DISKON PROMO :</span>
            <span>({tx['diskon']:,})</span>
        </div>
        <p style="margin: 5px 0;">--------------------------------</p>
        <div style="display: flex; justify-content: space-between; font-weight: bold;">
            <span>TOTAL :</span>
            <span>{tx['total']:,}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>TUNAI :</span>
            <span>{tx['tunai']:,}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>KEMBALI :</span>
            <span>{tx['kembali']:,}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>ANDA HEMAT :</span>
            <span>{tx['diskon']:,}</span>
        </div>
        <div style="text-align: center; margin-top: 15px; font-size: 10px;">
            <p>TERIMA KASIH. SELAMAT BELANJA KEMBALI</p>
            <p>====== LAYANAN KONSUMEN FLASHMART ======</p>
            <p>CALL 1500580 SMS : 0816 500 580</p>
            <p>EMAIL : KONTAK@FLASHMART.CO.ID</p>
            <p>======== INFO LENGKAP PROMOSI ========</p>
            <p>WWW. FLASHMART. CO. ID/PROMO</p>
        </div>
    </div>
    <br>
    <button onclick="printReceipt()" style="background-color: #27ae60; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%;">🖨️ Cetak Struk Belanja</button>

    <script>
    function printReceipt() {{
        var printContents = document.getElementById('print-area').innerHTML;
        var originalContents = document.body.innerHTML;
        document.body.innerHTML = printContents;
        window.print();
        document.body.innerHTML = originalContents;
        window.location.reload();
    }}
    </script>
    """
    
    components.html(receipt_html, height=450)
