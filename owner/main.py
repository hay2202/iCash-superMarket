from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger("owner")

app = FastAPI(title="Owner Dashboard")

# Add CORS middleware for UI access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include controller routers
from owner.controllers.dashboard_controller import router as dashboard_router
app.include_router(dashboard_router)


@app.get("/ui", response_class=HTMLResponse)
def get_dashboard_ui():
    """Serve the owner dashboard UI"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Owner Dashboard</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f7fa;
                color: #333;
                line-height: 1.6;
            }
            
            header {
                background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                color: white;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .header-content {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            h1 {
                font-size: 32px;
                margin-bottom: 5px;
            }
            
            .subtitle {
                font-size: 14px;
                opacity: 0.9;
            }
            
            main {
                max-width: 1200px;
                margin: 0 auto;
                padding: 30px 20px;
            }
            
            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }
            
            .card {
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                padding: 25px;
                transition: transform 0.3s, box-shadow 0.3s;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
            }
            
            .card-header {
                display: flex;
                align-items: center;
                margin-bottom: 20px;
                gap: 12px;
            }
            
            .card-icon {
                font-size: 32px;
                width: 50px;
                height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #f0f4f8;
                border-radius: 10px;
            }
            
            .card h2 {
                font-size: 18px;
                color: #555;
                font-weight: 600;
            }
            
            .card-value {
                font-size: 36px;
                font-weight: bold;
                color: #1e3a8a;
                margin-bottom: 10px;
            }
            
            .card-stat {
                font-size: 13px;
                color: #999;
            }
            
            .table-section {
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                padding: 25px;
                margin-bottom: 30px;
            }
            
            .section-title {
                font-size: 20px;
                font-weight: 600;
                color: #333;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
            }
            
            thead {
                background: #f8f9fa;
                border-bottom: 2px solid #e9ecef;
            }
            
            th {
                padding: 15px;
                text-align: left;
                font-weight: 600;
                color: #555;
                font-size: 13px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            td {
                padding: 15px;
                border-bottom: 1px solid #e9ecef;
                font-size: 14px;
            }
            
            tbody tr:hover {
                background: #f8f9fa;
            }
            
            .badge {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
            }
            
            .badge-primary {
                background: #dbeafe;
                color: #1e40af;
            }
            
            .badge-success {
                background: #dcfce7;
                color: #166534;
            }
            
            .loading {
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 40px;
                color: #1e3a8a;
                font-weight: 600;
            }
            
            .spinner {
                display: inline-block;
                width: 30px;
                height: 30px;
                border: 4px solid #f3f3f3;
                border-top: 4px solid #1e3a8a;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 15px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .empty-state {
                text-align: center;
                padding: 40px 20px;
                color: #999;
            }
            
            .empty-state-icon {
                font-size: 48px;
                margin-bottom: 15px;
            }
            
            .refresh-btn {
                background: #3b82f6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                font-size: 13px;
                transition: background 0.3s;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .refresh-btn:hover {
                background: #2563eb;
            }
            
            .refresh-btn:disabled {
                background: #cbd5e0;
                cursor: not-allowed;
            }
            
            .controls {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                flex-wrap: wrap;
                gap: 10px;
            }
            
            @media (max-width: 768px) {
                header {
                    padding: 20px;
                }
                
                h1 {
                    font-size: 24px;
                }
                
                .dashboard-grid {
                    grid-template-columns: 1fr;
                }
                
                table {
                    font-size: 12px;
                }
                
                th, td {
                    padding: 10px;
                }
            }
        </style>
    </head>
    <body>
        <header>
            <div class="header-content">
                <h1>📊 Owner Dashboard</h1>
                <p class="subtitle">Real-time supermarket analytics and insights</p>
            </div>
        </header>
        
        <main>
            <div class="controls">
                <h2 style="font-size: 18px; margin: 0;">Analytics Overview</h2>
                <button class="refresh-btn" id="refreshBtn" onclick="loadAllData()">🔄 Refresh Data</button>
            </div>
            
            <!-- Key Metrics -->
            <div class="dashboard-grid">
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">👥</div>
                        <div>
                            <h2>Unique Buyers</h2>
                        </div>
                    </div>
                    <div class="card-value" id="uniqueBuyersValue">-</div>
                    <div class="card-stat">Total customers who made purchases</div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">⭐</div>
                        <div>
                            <h2>Loyal Customers</h2>
                        </div>
                    </div>
                    <div class="card-value" id="loyalCustomersValue">-</div>
                    <div class="card-stat">Customers with 3+ purchases</div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">🏆</div>
                        <div>
                            <h2>Top Product</h2>
                        </div>
                    </div>
                    <div class="card-value" id="topProductValue">-</div>
                    <div class="card-stat">Most purchased item</div>
                </div>
            </div>
            
            <!-- Loyal Buyers Table -->
            <div class="table-section">
                <div class="controls">
                    <h3 class="section-title">⭐ Loyal Customers</h3>
                </div>
                <div id="loyalBuyersContainer" class="loading">
                    <span class="spinner"></span> Loading loyal customers...
                </div>
            </div>
            
            <!-- Top Products Table -->
            <div class="table-section">
                <div class="controls">
                    <h3 class="section-title">🛍️ Top Products</h3>
                </div>
                <div id="topProductsContainer" class="loading">
                    <span class="spinner"></span> Loading top products...
                </div>
            </div>
        </main>
        
        <script>
            const API_BASE = window.location.origin;
            const REFRESH_INTERVAL = 30000; // 30 seconds
            let refreshInterval;
            
            // Load data when page loads
            window.addEventListener('load', () => {
                loadAllData();
                // Auto-refresh every 30 seconds
                refreshInterval = setInterval(loadAllData, REFRESH_INTERVAL);
            });
            
            async function loadAllData() {
                document.getElementById('refreshBtn').disabled = true;
                
                try {
                    await Promise.all([
                        loadUniqueBuyers(),
                        loadLoyalBuyers(),
                        loadTopProducts()
                    ]);
                } finally {
                    document.getElementById('refreshBtn').disabled = false;
                }
            }
            
            async function loadUniqueBuyers() {
                try {
                    const response = await fetch(`${API_BASE}/dashboard/unique-buyers`);
                    const data = await response.json();
                    document.getElementById('uniqueBuyersValue').textContent = data.unique_buyers || 0;
                } catch (error) {
                    console.error('Error loading unique buyers:', error);
                    document.getElementById('uniqueBuyersValue').textContent = 'Error';
                }
            }
            
            async function loadLoyalBuyers() {
                const container = document.getElementById('loyalBuyersContainer');
                try {
                    const response = await fetch(`${API_BASE}/dashboard/loyal-buyers`);
                    const data = await response.json();
                    
                    const loyalBuyers = data.loyal_buyers || [];
                    
                    if (loyalBuyers.length === 0) {
                        container.innerHTML = `
                            <div class="empty-state">
                                <div class="empty-state-icon">📭</div>
                                <p>No loyal customers yet</p>
                            </div>
                        `;
                        document.getElementById('loyalCustomersValue').textContent = '0';
                        return;
                    }
                    
                    document.getElementById('loyalCustomersValue').textContent = loyalBuyers.length;
                    
                    const tableHTML = `
                        <table>
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Customer ID</th>
                                    <th>Number of Purchases</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${loyalBuyers.map((buyer, index) => `
                                    <tr>
                                        <td>${index + 1}</td>
                                        <td><strong>${buyer.user_id}</strong></td>
                                        <td>${buyer.purchases}</td>
                                        <td>
                                            ${buyer.purchases >= 10 ? 
                                                '<span class="badge badge-success">VIP</span>' : 
                                                '<span class="badge badge-primary">Loyal</span>'}
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    `;
                    
                    container.innerHTML = tableHTML;
                } catch (error) {
                    console.error('Error loading loyal buyers:', error);
                    container.innerHTML = `
                        <div class="empty-state">
                            <p>⚠️ Error loading loyal customers</p>
                        </div>
                    `;
                }
            }
            
            async function loadTopProducts() {
                const container = document.getElementById('topProductsContainer');
                try {
                    const response = await fetch(`${API_BASE}/dashboard/top-products`);
                    const data = await response.json();
                    
                    const products = data.top_products || [];
                    
                    if (products.length === 0) {
                        container.innerHTML = `
                            <div class="empty-state">
                                <div class="empty-state-icon">📭</div>
                                <p>No purchase data available yet</p>
                            </div>
                        `;
                        document.getElementById('topProductValue').textContent = '-';
                        return;
                    }
                    
                    document.getElementById('topProductValue').textContent = products[0].product;
                    
                    const maxCount = Math.max(...products.map(p => p.count));
                    
                    const tableHTML = `
                        <table>
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Product Name</th>
                                    <th>Times Purchased</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${products.map((product, index) => {
                                    return `
                                        <tr>
                                            <td>${index + 1}</td>
                                            <td><strong>${product.product}</strong></td>
                                            <td>${product.count}</td>
                                        </tr>
                                    `;
                                }).join('')}
                            </tbody>
                        </table>
                    `;
                    
                    container.innerHTML = tableHTML;
                } catch (error) {
                    console.error('Error loading top products:', error);
                    container.innerHTML = `
                        <div class="empty-state">
                            <p>⚠️ Error loading top products</p>
                        </div>
                    `;
                }
            }
            
            // Cleanup on page unload
            window.addEventListener('unload', () => {
                if (refreshInterval) {
                    clearInterval(refreshInterval);
                }
            });
        </script>
    </body>
    </html>
    """


