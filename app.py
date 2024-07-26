from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

# In-memory storage
shows = []
registrations = []
vendors = []

# List of eco-friendly brands
eco_friendly_brands = ["Patagonia", "BrandB", "BrandC"]

# List of fast fashion brands
fast_fashion_brands = ["Temu", "BrandY", "BrandZ"]

# Barcode Lookup API credentials
BARCODE_LOOKUP_API_KEY = 'k9i9fkc011ia4swrm44wn6hq20osuz'
BARCODE_LOOKUP_API_URL = 'https://api.barcodelookup.com/v2/products'

@app.route('/')
def index():
    print(f"Shows: {shows}")  # Debugging statement
    return render_template('index.html', shows=shows)

@app.route('/add_show', methods=['GET', 'POST'])
def add_show():
    if request.method == 'POST':
        neighborhood = request.form['neighborhood']
        date = request.form['date']
        info = request.form['info']
        address = request.form['address']
        show = {'neighborhood': neighborhood, 'date': date, 'info': info, 'address': address}
        shows.append(show)
        print(f"Added Show: {show}")  # Debugging statement
        return redirect(url_for('index'))
    return render_template('add_show.html')

@app.route('/register/<int:show_id>', methods=['GET', 'POST'])
def register(show_id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        registration = {'name': name, 'email': email, 'show_id': show_id}
        registrations.append(registration)
        return redirect(url_for('index'))
    return render_template('register.html', show_id=show_id)

@app.route('/registrations/<int:show_id>')
def view_registrations(show_id):
    show_registrations = [reg for reg in registrations if reg['show_id'] == show_id]
    return render_template('registrations.html', registrations=show_registrations)

@app.route('/vendors/<int:show_id>', methods=['GET', 'POST'])
def vendors_view(show_id):
    show_vendors = [vendor for vendor in vendors if vendor['show_id'] == show_id]
    
    if request.method == 'POST':
        vendor_name = request.form.get('vendor_name')
        items = request.form.getlist('items[]')
        prices = request.form.getlist('prices[]')

        # Debugging print statements
        print('Vendor Name:', vendor_name)
        print('Items:', items)
        print('Prices:', prices)

        # Ensure items and prices are lists and have the same length
        if isinstance(items, list) and isinstance(prices, list) and len(items) == len(prices):
            vendor_items = list(zip(items, prices))
            vendor = {'vendor_name': vendor_name, 'items': vendor_items, 'show_id': show_id}
            vendors.append(vendor)
        else:
            # Handle cases where items and prices don't match or are not lists
            print('Error: Items and prices do not match or are not lists')
            
        return redirect(url_for('vendors_view', show_id=show_id))
    
    return render_template('vendors.html', show_id=show_id, vendors=show_vendors)

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/scan-barcode')
def scan_barcode():
    return render_template('scan_barcode.html')

@app.route('/check-barcode', methods=['POST'])
def check_barcode():
    barcode = request.json.get('barcode')
    brand = barcode_to_brand(barcode)
    if brand in eco_friendly_brands:
        return jsonify({"message": "Good"})
    elif brand in fast_fashion_brands:
        return jsonify({"message": "Fast Fashion"})
    else:
        return jsonify({"message": "Unknown"})

def barcode_to_brand(barcode):
    # Make a request to the Barcode Lookup API
    response = requests.get(BARCODE_LOOKUP_API_URL, params={'barcode': barcode, 'key': BARCODE_LOOKUP_API_KEY})
    data = response.json()
    
    if 'products' in data and data['products']:
        brand = data['products'][0].get('brand', 'Unknown')
        return brand
    return 'Unknown'

if __name__ == '__main__':
    app.run(debug=True)
