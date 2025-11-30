"""
Cashier UI - Serves the HTML interface for cashier service
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

ui_app = FastAPI(title="Cashier UI")


@ui_app.get("/", response_class=HTMLResponse)
def get_cashier_ui():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cashier System</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 600px;
                width: 100%;
                padding: 40px;
            }
            
            h1 {
                color: #333;
                margin-bottom: 30px;
                text-align: center;
                font-size: 28px;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                color: #555;
                font-weight: 600;
                font-size: 14px;
            }
            
            input[type="text"],
            select,
            textarea {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                transition: border-color 0.3s;
                font-family: inherit;
            }
            
            input[type="text"]:focus,
            select:focus,
            textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            textarea {
                resize: vertical;
                min-height: 100px;
            }
            
            .help-text {
                font-size: 12px;
                color: #999;
                margin-top: 5px;
            }
            
            .items-list {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 20px;
            }
            
            .item-tag {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 6px 12px;
                border-radius: 20px;
                margin: 5px 5px 5px 0;
                font-size: 13px;
                cursor: pointer;
                transition: background 0.3s;
            }
            
            .item-tag:hover {
                background: #764ba2;
            }
            
            .item-tag .remove {
                margin-left: 8px;
                font-weight: bold;
            }
            
            .total-section {
                background: #f0f4ff;
                border-left: 4px solid #667eea;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            
            .total-section p {
                color: #666;
                margin-bottom: 10px;
            }
            
            .total-amount {
                font-size: 24px;
                font-weight: bold;
                color: #667eea;
            }
            
            .button-group {
                display: flex;
                gap: 10px;
                justify-content: center;
            }
            
            button {
                padding: 12px 30px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                flex: 1;
            }
            
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }
            
            .btn-primary:disabled {
                background: #ccc;
                cursor: not-allowed;
                transform: none;
            }
            
            .btn-secondary {
                background: #e0e0e0;
                color: #333;
                flex: 1;
            }
            
            .btn-secondary:hover {
                background: #d0d0d0;
            }
            
            .success-message {
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                display: none;
                border-left: 4px solid #28a745;
            }
            
            .error-message {
                background: #f8d7da;
                color: #721c24;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                display: none;
                border-left: 4px solid #f5c6cb;
            }
            
            .loading {
                display: none;
                text-align: center;
                color: #667eea;
                font-weight: 600;
            }
            
            .spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 10px;
                vertical-align: middle;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .info-box {
                background: #e7f3ff;
                border-left: 4px solid #2196F3;
                padding: 12px;
                border-radius: 4px;
                font-size: 13px;
                color: #0c5aa0;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛒 Cashier System</h1>
            
            <div class="info-box">
                ℹ️ Process purchases quickly and easily. Enter customer ID and scan items.
            </div>
            
            <div class="success-message" id="successMessage"></div>
            <div class="error-message" id="errorMessage"></div>
            
            <form id="purchaseForm" onsubmit="handleSubmit(event)">
                <div class="form-group">
                    <label for="supermarketId">Supermarket ID</label>
                    <input type="text" id="supermarketId" name="supermarketId" placeholder="e.g., supermarket-1" required>
                    <div class="help-text">Unique identifier for this supermarket</div>
                </div>
                
                <div class="form-group">
                    <label for="userId">Customer ID</label>
                    <input type="text" id="userId" name="userId" placeholder="e.g., customer-001" required>
                    <div class="help-text">Unique identifier for the customer</div>
                </div>
                
                <div class="form-group">
                    <label for="items">Items (comma-separated)</label>
                    <textarea id="items" name="items" placeholder="apple, banana, milk, bread" required></textarea>
                    <div class="help-text">Enter product names separated by commas</div>
                </div>
                
                <div class="items-list" id="itemsList"></div>
                
                <div class="total-section">
                    <p>Total Amount:</p>
                    <div class="total-amount">$<span id="totalAmount">0.00</span></div>
                </div>
                
                <div class="loading" id="loading">
                    <span class="spinner"></span> Processing purchase...
                </div>
                
                <div class="button-group">
                    <button type="button" class="btn-secondary" onclick="resetForm()">Clear</button>
                    <button type="submit" class="btn-primary" id="submitBtn">Complete Purchase</button>
                </div>
            </form>
        </div>
        
        <script>
            const API_URL = 'http://localhost:8000';
            
            // Update items and total when textarea changes
            document.getElementById('items').addEventListener('change', updateItemsDisplay);
            document.getElementById('items').addEventListener('input', updateItemsDisplay);
            
            function updateItemsDisplay() {
                const itemsText = document.getElementById('items').value;
                const items = itemsText.split(',').map(item => item.trim()).filter(item => item);
                
                const itemsList = document.getElementById('itemsList');
                itemsList.innerHTML = items.length > 0 
                    ? '<strong>Items to purchase:</strong><br>' + 
                      items.map(item => 
                        `<span class="item-tag">${item}</span>`
                      ).join('')
                    : '';
                
                // Calculate total
                if (items.length > 0) {
                    calculateTotal(items);
                } else {
                    document.getElementById('totalAmount').textContent = '0.00';
                }
            }
            
            async function calculateTotal(items) {
                try {
                    // For now, we'll show 0.00 until API supports calculation
                    // This would need a backend endpoint to calculate totals
                    document.getElementById('totalAmount').textContent = '0.00';
                } catch (error) {
                    console.error('Error calculating total:', error);
                }
            }
            
            async function handleSubmit(event) {
                event.preventDefault();
                
                const supermarketId = document.getElementById('supermarketId').value.trim();
                const userId = document.getElementById('userId').value.trim();
                const itemsText = document.getElementById('items').value.trim();
                
                if (!supermarketId || !userId || !itemsText) {
                    showError('Please fill in all fields');
                    return;
                }
                
                const items = itemsText.split(',').map(item => item.trim()).filter(item => item);
                
                if (items.length === 0) {
                    showError('Please enter at least one item');
                    return;
                }
                
                showLoading(true);
                hideMessages();
                
                try {
                    const response = await fetch(`${API_URL}/purchase/create`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            supermarket_id: supermarketId,
                            user_id: userId,
                            items_list: items
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (!response.ok) {
                        throw new Error(data.detail || 'Failed to create purchase');
                    }
                    
                    showSuccess(`✓ Purchase completed! 
Purchase ID: ${data.purchase_id}
Total: $${data.total_amount.toFixed(2)}
${data.new_user ? '(New customer registered)' : '(Returning customer)'}`);
                    
                    resetForm();
                    
                } catch (error) {
                    showError(`Error: ${error.message}`);
                } finally {
                    showLoading(false);
                }
            }
            
            function showSuccess(message) {
                const el = document.getElementById('successMessage');
                el.textContent = message;
                el.style.display = 'block';
                setTimeout(() => el.style.display = 'none', 5000);
            }
            
            function showError(message) {
                const el = document.getElementById('errorMessage');
                el.textContent = message;
                el.style.display = 'block';
            }
            
            function hideMessages() {
                document.getElementById('successMessage').style.display = 'none';
                document.getElementById('errorMessage').style.display = 'none';
            }
            
            function showLoading(show) {
                document.getElementById('loading').style.display = show ? 'block' : 'none';
                document.getElementById('submitBtn').disabled = show;
            }
            
            function resetForm() {
                document.getElementById('purchaseForm').reset();
                document.getElementById('itemsList').innerHTML = '';
                document.getElementById('totalAmount').textContent = '0.00';
                hideMessages();
            }
        </script>
    </body>
    </html>
    """

