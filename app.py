from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage
shows = []
registrations = []
vendors = []

@app.route('/')
def index():
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
        vendor_name = request.form['vendor_name']
        items = request.form.getlist('items[]')
        prices = request.form.getlist('prices[]')
        
        # Debugging print statements to check the content of items and prices
        print('items:', items)
        print('prices:', prices)

        # Ensure items and prices are iterables and have the same length
        if items and prices and len(items) == len(prices):
            vendor_items = list(zip(items, prices))
            vendor = {'vendor_name': vendor_name, 'items': vendor_items, 'show_id': show_id}
            vendors.append(vendor)
        return redirect(url_for('vendors_view', show_id=show_id))
    return render_template('vendors.html', show_id=show_id, vendors=show_vendors)

@app.route('/articles')
def articles():
    return render_template('articles.html')

if __name__ == '__main__':
    app.run(debug=True)
