import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi halaman
st.set_page_config(page_title="Minimarket Online Berkah", page_icon="🏪", layout="wide")

# CSS Styling tambahan
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

# Inisialisasi State
if "cart" not in st.session_state:
    st.session_state.cart = []
if "last_checkout" not in st.session_state:
    st.session_state.last_checkout = None

# Layout Kolom
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Daftar Produk")
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
        
        if st.button("Checkout & Cetak Struk", type="primary"):
            # Simpan data transaksi terakhir untuk dicetak struknya
            st.session_state.last_checkout = {
                "items": list(st.session_state.cart),
                "total": total
            }
            st.session_state.cart = []
            st.success("Pesanan berhasil diproses!")
            st.rerun()

# Bagian Tampilan Struk Belanja Terakhir
if st.session_state.last_checkout:
    st.markdown("---")
    st.subheader("🧾 Struk Belanja Terakhir")
    
    # Buat format HTML untuk struk (gaya struk kasir thermal)
    receipt_items_html = ""
    for item in st.session_state.last_checkout["items"]:
        subtotal = item["price"] * item["quantity"]
        receipt_items_html += f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>{item['name']} ({item['quantity']}x)</span>
                <span>Rp {subtotal:,}</span>
            </div>
        """
    
    receipt_total = st.session_state.last_checkout["total"]
    
    receipt_html = f"""
    <div id="print-area" style="font-family: 'Courier New', Courier, monospace; width: 300px; background: #fff; padding: 15px; border: 1px dashed #333; color: #000;">
        <div style="text-align: center;">
            <h3>MINIMARKET BERKAH</h3>
            <p style="font-size: 12px;">Jl. Contoh No. 123, Kota Anda</p>
            <p style="font-size: 12px;">--------------------------------</p>
        </div>
        <div style="font-size: 13px; margin-bottom: 10px;">
            {receipt_items_html}
        </div>
        <div style="font-size: 13px; border-top: 1px dashed #333; padding-top: 5px;">
            <div style="display: flex; justify-content: space-between; font-weight: bold;">
                <span>TOTAL:</span>
                <span>Rp {receipt_total:,}</span>
            </div>
        </div>
        <div style="text-align: center; margin-top: 15px; font-size: 12px;">
            <p>Terima Kasih Telah Berbelanja</p>
            <p>Barang yang sudah dibeli tidak dapat ditukar</p>
        </div>
    </div>
    <br>
    <button onclick="printReceipt()" style="background-color: #27ae60; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; font-weight: bold;">🖨️ Cetak Struk</button>

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
    
    # Render komponen HTML & JavaScript untuk tombol cetak struk
    components.html(receipt_html, height=350)
