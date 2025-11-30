from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI(title="Cashier Service")

# Add CORS middleware for UI access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include controller routers
from cashier.controllers.purchase_controller import router as purchase_router
from cashier.controllers.product_controller import router as product_router
app.include_router(purchase_router)
app.include_router(product_router)


@app.get("/ui", response_class=HTMLResponse)
def get_cashier_ui():
    """Serve the cashier UI"""
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
                white-space: pre-wrap;
                font-family: monospace;
                font-size: 13px;
            }
            
            .error-message {
                background: #f8d7da;
                color: #721c24;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                display: none;
                border-left: 4px solid #f5c6cb;
                white-space: pre-wrap;
                font-family: monospace;
                font-size: 13px;
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
            
            .radio-group {
                display: flex;
                gap: 20px;
                margin-bottom: 15px;
            }
            
            .radio-group label {
                display: flex;
                align-items: center;
                margin-bottom: 0;
                cursor: pointer;
            }
            
            .radio-group input[type="radio"] {
                width: auto;
                margin-right: 8px;
                cursor: pointer;
            }
            
            .hidden-section {
                display: none;
            }
            
            .search-box {
                position: relative;
                margin-bottom: 10px;
            }
            
            .search-box input {
                width: 100%;
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
            }
            
            .customer-dropdown {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                max-height: 200px;
                overflow-y: auto;
                background: white;
                margin-top: 5px;
            }
            
            .customer-item {
                padding: 10px 12px;
                cursor: pointer;
                border-bottom: 1px solid #f0f0f0;
                transition: background 0.2s;
            }
            
            .customer-item:hover {
                background: #f5f5f5;
            }
            
            .customer-item.selected {
                background: #667eea;
                color: white;
            }
            
            .items-checklist {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                background: #f8f9fa;
                max-height: 300px;
                overflow-y: auto;
            }
            
            .checkbox-item {
                display: flex;
                align-items: center;
                padding: 10px;
                margin-bottom: 8px;
                background: white;
                border-radius: 6px;
                cursor: pointer;
                transition: background 0.2s;
                border: 1px solid #e0e0e0;
            }
            
            .checkbox-item:hover {
                background: #f5f5f5;
            }
            
            .checkbox-item input[type="checkbox"] {
                width: auto;
                margin-right: 12px;
                cursor: pointer;
            }
            
            .item-info {
                flex: 1;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .item-name {
                font-weight: 600;
                color: #333;
            }
            
            .item-price {
                color: #667eea;
                font-weight: 600;
                margin-left: 20px;
            }
            
            .selected-items-display {
                background: #f0f4ff;
                border-left: 4px solid #667eea;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 15px;
            }
            
            .selected-items-display.hidden {
                display: none;
            }
            
            .selected-item-tag {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: #667eea;
                color: white;
                padding: 6px 12px;
                border-radius: 20px;
                margin: 5px 5px 5px 0;
                font-size: 12px;
            }
            
            .remove-item-btn {
                background: rgba(255,255,255,0.3);
                border: none;
                color: white;
                cursor: pointer;
                padding: 0;
                font-size: 16px;
                line-height: 1;
                transition: background 0.2s;
            }
            
            .modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                animation: fadeIn 0.3s;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            .modal-content {
                background: white;
                margin: 10% auto;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 500px;
                width: 90%;
                text-align: center;
                animation: slideIn 0.3s;
            }

            @keyframes slideIn {
                from {
                    transform: translateY(-50px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }

            .modal-header {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
            }

            .modal-body {
                margin-bottom: 20px;
                text-align: left;
            }

            .modal-field {
                margin-bottom: 15px;
                padding: 12px;
                background: #f0f4ff;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }

            .modal-label {
                color: #666;
                font-size: 12px;
                font-weight: 600;
                text-transform: uppercase;
                margin-bottom: 5px;
            }

            .modal-value {
                color: #333;
                font-size: 18px;
                font-weight: bold;
                font-family: monospace;
            }

            .modal-button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            }

            .modal-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
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
                <!-- Supermarket Selection -->
                <div class="form-group">
                    <label for="supermarketId">Supermarket ID</label>
                    <select id="supermarketId" name="supermarketId" required onchange="handleSupermarketChange()">
                        <option value="">-- Select Supermarket --</option>
                        <option value="SMKT001">SMKT001 - Downtown Store</option>
                        <option value="SMKT002">SMKT002 - Mall Location</option>
                        <option value="SMKT003">SMKT003 - Airport Store</option>
                    </select>
                    <div class="help-text">Select the supermarket location</div>
                </div>
                
                <!-- Customer Type Selection -->
                <div class="form-group">
                    <label>Customer Type</label>
                    <div class="radio-group">
                        <label>
                            <input type="radio" name="customerType" value="new" checked onchange="handleCustomerTypeChange()">
                            New Customer
                        </label>
                        <label>
                            <input type="radio" name="customerType" value="existing" onchange="handleCustomerTypeChange()">
                            Existing Customer
                        </label>
                    </div>
                </div>
                
                <!-- New Customer ID Input -->
                <div class="form-group" id="newCustomerSection">
                    <div class="info-box" style="background: #e7f3ff; border-left: 4px solid #2196F3;">
                        ℹ️ Customer ID will be auto-generated during purchase
                    </div>
                </div>
                
                <!-- Existing Customer Selection -->
                <div class="form-group hidden-section" id="existingCustomerSection">
                    <label>Select Customer</label>
                    <div class="search-box">
                        <input type="text" id="customerSearch" placeholder="Search by customer ID..." onkeyup="filterCustomers()">
                    </div>
                    <div class="customer-dropdown" id="customerDropdown">
                        <span id="loadingCustomers" style="display: block; padding: 10px; text-align: center; color: #999;">Loading customers...</span>
                    </div>
                    <div class="help-text" style="margin-top: 10px;">Selected: <strong id="selectedCustomerDisplay">None</strong></div>
                </div>
                
                <!-- Items Selection as Checklist -->
                <div class="form-group">
                    <label>Items</label>
                    <div class="items-checklist" id="itemsChecklist">
                        <div style="text-align: center; color: #999; padding: 20px;">
                            Loading items from database...
                        </div>
                    </div>
                    <div class="help-text">Click to select items (each item max once)</div>
                </div>
                
                <!-- Selected Items Display -->
                <div class="selected-items-display hidden" id="selectedItemsDisplay">
                    <strong>Selected Items:</strong><br>
                    <div id="selectedItemsTags"></div>
                </div>
                
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

        <!-- Success Modal -->
        <div class="modal" id="successModal">
            <div class="modal-content">
                <div class="modal-header">✓ Purchase Completed!</div>
                <div class="modal-body">
                    <div class="modal-field">
                        <div class="modal-label">Purchase ID</div>
                        <div class="modal-value" id="modalPurchaseId">-</div>
                    </div>
                    <div class="modal-field">
                        <div class="modal-label">Customer ID</div>
                        <div class="modal-value" id="modalCustomerId">-</div>
                    </div>
                    <div class="modal-field">
                        <div class="modal-label">Total Amount</div>
                        <div class="modal-value">$<span id="modalTotalAmount">0.00</span></div>
                    </div>
                    <div class="modal-field" id="newCustomerBadge" style="display: none; background: #d4edda; border-left-color: #28a745;">
                        <div class="modal-label" style="color: #155724;">Status</div>
                        <div class="modal-value" style="color: #155724;">🎉 New Customer Registered</div>
                    </div>
                </div>
                <button class="modal-button" onclick="closeSuccessModal()">Done</button>
            </div>
        </div>
        
        <script>
            const API_BASE = window.location.origin;
            const selectedItems = new Map();
            
            let allCustomers = [];
            let allProducts = [];
            let selectedCustomer = null;
            
            // Initialize on page load
            document.addEventListener('DOMContentLoaded', function() {
                loadCustomersFromAPI();
                loadProductsFromAPI();
            });
            
            // Load products from API
            async function loadProductsFromAPI() {
                try {
                    const response = await fetch(`${API_BASE}/product/all`);
                    const data = await response.json();
                    allProducts = data.products || [];
                    populateItemsChecklist();
                } catch (error) {
                    console.error('Error loading products:', error);
                    showError('Failed to load products from database');
                }
            }
            
            // Populate items checklist from products
            function populateItemsChecklist() {
                const checklist = document.getElementById('itemsChecklist');
                
                if (allProducts.length === 0) {
                    checklist.innerHTML = '<div style="padding: 10px; text-align: center; color: #999;">No products found</div>';
                    return;
                }
                
                checklist.innerHTML = '';
                
                allProducts.forEach(product => {
                    const div = document.createElement('div');
                    div.className = 'checkbox-item';
                    div.onclick = (e) => toggleItem(e);
                    div.innerHTML = `
                        <input type="checkbox" name="items" value="${product.name}" data-price="${product.price}">
                        <div class="item-info">
                            <span class="item-name">${product.name}</span>
                            <span class="item-price">$${product.price.toFixed(2)}</span>
                        </div>
                    `;
                    checklist.appendChild(div);
                });
            }
            
            // Load customers from API
            async function loadCustomersFromAPI() {
                const dropdown = document.getElementById('customerDropdown');
                const loading = document.getElementById('loadingCustomers');

                if (loading) loading.style.display = 'block';
                
                try {
                    const response = await fetch(`${API_BASE}/purchase/customers`);
                    const data = await response.json();
                    allCustomers = data.customers || [];
                    populateCustomerDropdown();
                } catch (error) {
                    console.error('Error loading customers:', error);
                    showError('Failed to load customers from database');
                }
                finally {
                    if (loading) loading.style.display = 'none'; 
                }
            }
            
            // Populate customer dropdown
            function populateCustomerDropdown() {
                const dropdown = document.getElementById('customerDropdown');
                const loading = document.getElementById('loadingCustomers');
                
                 if (!dropdown) {
                    console.warn('Dropdown element not found');
                    return; // אם אין dropdown, אין מה לעשות
                }
                
                if (allCustomers.length === 0) {
                    dropdown.innerHTML = '<div style="padding: 10px; text-align: center; color: #999;">No customers found</div>';
                    return;
                }
                
                dropdown.innerHTML = '';
                if (loading) loading.style.display = 'none';
                
                allCustomers.forEach(customerId => {
                    const item = document.createElement('div');
                    item.className = 'customer-item';
                    item.textContent = customerId;
                    item.onclick = () => selectCustomer(customerId);
                    dropdown.appendChild(item);
                });
            }
            
            function handleSupermarketChange() {
                const value = document.getElementById('supermarketId').value;
                console.log('Selected supermarket:', value);
            }
            
            function handleCustomerTypeChange() {
                const customerType = document.querySelector('input[name="customerType"]:checked').value;
                const newCustomerSection = document.getElementById('newCustomerSection');
                const existingCustomerSection = document.getElementById('existingCustomerSection');
                
                if (customerType === 'new') {
                    newCustomerSection.classList.remove('hidden-section');
                    existingCustomerSection.classList.add('hidden-section');
                    selectedCustomer = null;
                    document.getElementById('selectedCustomerDisplay').textContent = 'None';
                } else {
                    newCustomerSection.classList.add('hidden-section');
                    existingCustomerSection.classList.remove('hidden-section');
                }
            }
            
            function filterCustomers() {
                const searchText = document.getElementById('customerSearch').value.toLowerCase();
                const items = document.querySelectorAll('.customer-item');
                
                items.forEach(item => {
                    const text = item.textContent.toLowerCase();
                    if (text.includes(searchText)) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            }
            
            function selectCustomer(customerId) {
                selectedCustomer = customerId;
                document.getElementById('selectedCustomerDisplay').textContent = customerId;
                
                const items = document.querySelectorAll('.customer-item');
                items.forEach(item => {
                    if (item.textContent === customerId) {
                        item.classList.add('selected');
                    } else {
                        item.classList.remove('selected');
                    }
                });
                
                document.getElementById('customerSearch').value = '';
                filterCustomers();
            }
            
            function toggleItem(event) {
                const checkbox = event.currentTarget.querySelector('input[type="checkbox"]');
                checkbox.checked = !checkbox.checked;
                updateSelectedItems();
            }
            
            function updateSelectedItems() {
                selectedItems.clear();
                let total = 0;
                
                const checkboxes = document.querySelectorAll('input[name="items"]:checked');
                checkboxes.forEach(checkbox => {
                    const itemName = checkbox.value;
                    const itemPrice = parseFloat(checkbox.dataset.price);
                    selectedItems.set(itemName, itemPrice);
                    total += itemPrice;
                });
                
                const displayDiv = document.getElementById('selectedItemsDisplay');
                const tagsDiv = document.getElementById('selectedItemsTags');
                
                if (selectedItems.size > 0) {
                    displayDiv.classList.remove('hidden');
                    let tagsHTML = '';
                    selectedItems.forEach((price, itemName) => {
                        tagsHTML += `
                            <span class="selected-item-tag">
                                ${itemName} ($${price.toFixed(2)})
                                <button type="button" class="remove-item-btn" onclick="removeItem('${itemName}')">×</button>
                            </span>
                        `;
                    });
                    tagsDiv.innerHTML = tagsHTML;
                } else {
                    displayDiv.classList.add('hidden');
                }
                
                document.getElementById('totalAmount').textContent = total.toFixed(2);
            }
            
            function removeItem(itemName) {
                const checkbox = document.querySelector(`input[name="items"][value="${itemName}"]`);
                checkbox.checked = false;
                updateSelectedItems();
            }
            
            async function handleSubmit(event) {
                event.preventDefault();
                
                const supermarketId = document.getElementById('supermarketId').value.trim();
                if (!supermarketId) {
                    showError('Please select a supermarket');
                    return;
                }
                
                let customerId = null;
                const customerType = document.querySelector('input[name="customerType"]:checked').value;
                
                if (customerType === 'existing') {
                    customerId = selectedCustomer;
                    if (!customerId) {
                        showError('Please select an existing customer');
                        return;
                    }
                }
                
                if (selectedItems.size === 0) {
                    showError('Please select at least one item');
                    return;
                }
                
                const items = Array.from(selectedItems.keys());
                
                showLoading(true);
                hideMessages();
                
                try {
                    const response = await fetch(`${API_BASE}/purchase/create`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            supermarket_id: supermarketId,
                            user_id: customerId,
                            items_list: items
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (!response.ok) {
                        throw new Error(data.detail || 'Failed to create purchase');
                    }
                    
                    const total = Array.from(selectedItems.values()).reduce((a, b) => a + b, 0);
                    showSuccessModal(data.purchase_id, data.user_id, total, data.is_new);
                    
                    if (data.is_new) {
                       setTimeout(() => loadCustomersFromAPI(), 0);
                    }
                    
                    resetForm();
                    
                } catch (error) {
                    showError(`Error: ${error.message}`);
                } finally {
                    showLoading(false);
                }
            }
            
            function showSuccessModal(purchaseId, customerId, total, isNew) {
                document.getElementById('modalPurchaseId').textContent = purchaseId;
                document.getElementById('modalCustomerId').textContent = customerId;
                document.getElementById('modalTotalAmount').textContent = total.toFixed(2);
                
                const badge = document.getElementById('newCustomerBadge');
                if (isNew) {
                    badge.style.display = 'block';
                } else {
                    badge.style.display = 'none';
                }
                
                document.getElementById('successModal').style.display = 'block';
            }
            
            function closeSuccessModal() {
                document.getElementById('successModal').style.display = 'none';
            }
            
            window.onclick = function(event) {
                const modal = document.getElementById('successModal');
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
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
                selectedItems.clear();
                selectedCustomer = null;
                document.getElementById('selectedCustomerDisplay').textContent = 'None';
                document.getElementById('selectedItemsDisplay').classList.add('hidden');
                document.getElementById('totalAmount').textContent = '0.00';
                document.getElementById('customerSearch').value = '';
                
                document.querySelector('input[name="customerType"][value="new"]').checked = true;
                handleCustomerTypeChange();
                
                document.querySelectorAll('input[name="items"]').forEach(cb => cb.checked = false);
                
                hideMessages();
            }
        </script>
    </body>
    </html>
    """
