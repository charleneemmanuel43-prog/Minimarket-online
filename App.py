<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minimarket Online Sederhana</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background-color: #f4f6f9;
            color: #333;
        }
        header {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            max-width: 1200px;
            margin: 20px auto;
            gap: 20px;
            padding: 0 15px;
        }
        .product-section {
            flex: 2;
            min-width: 300px;
        }
        .cart-section {
            flex: 1;
            min-width: 280px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            height: fit-content;
        }
        h2 {
            margin-bottom: 15px;
            color: #2c3e50;
        }
        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }
        .product-card {
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .product-card h3 {
            font-size: 16px;
            margin-bottom: 8px;
        }
        .product-card p {
            color: #e74c3c;
            font-weight: bold;
            margin-bottom: 12px;
        }
        .btn {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        .btn:hover {
            background-color: #219653;
        }
        .cart-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            border-bottom: 1px solid #eee;
            padding-bottom: 8px;
            font-size: 14px;
        }
        .cart-total {
            margin-top: 15px;
            font-size: 18px;
            font-weight: bold;
            border-top: 2px solid #ddd;
            padding-top: 10px;
            display: flex;
            justify-content: space-between;
        }
        .btn-checkout {
            display: block;
            width: 100%;
            background-color: #2980b9;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 4px;
            margin-top: 15px;
            cursor: pointer;
            font-weight: bold;
            text-align: center;
        }
        .btn-checkout:hover {
            background-color: #2471a3;
        }
    </style>
</head>
<body>

    <header>
        <h1>🏪 Minimarket Online Berkah</h1>
        <p>Belanja kebutuhan harian lebih mudah dan cepat</p>
    </header>

    <div class="container">
        <!-- Daftar Produk -->
        <div class="product-section">
            <h2>Daftar Produk</h2>
            <div class="product-grid" id="product-grid">
                <!-- Produk akan dimuat lewat JavaScript -->
            </div>
        </div>

        <!-- Keranjang Belanja -->
        <div class="cart-section">
            <h2>Keranjang Belanja</h2>
            <div id="cart-items">
                <p style="color: #777; font-size: 14px;">Keranjang masih kosong.</p>
            </div>
            <div class="cart-total">
                <span>Total:</span>
                <span id="cart-total-price">Rp 0</span>
            </div>
            <button class="btn-checkout" onclick="checkout()">Checkout Pesanan</button>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
