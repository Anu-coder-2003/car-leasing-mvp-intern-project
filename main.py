from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory data structures
vehicles = {f"V{id:03}": {"leased": False} for id in range(1, 21)}
lessees = {}
payments = {}  # {lessee_id: [ {amount, date} ]}

LEASE_AMOUNT = 500

@app.route('/')
def dashboard():
    total_collected = sum(p['amount'] for pays in payments.values() for p in pays)
    total_expected = sum(1 for v in vehicles.values() if v['leased']) * LEASE_AMOUNT
    overdue = [name for name in lessees if name not in payments or not payments[name]]

    return render_template('dashboard.html',
        total_collected=total_collected,
        total_expected=total_expected,
        leased=sum(1 for v in vehicles.values() if v['leased']),
        available=sum(1 for v in vehicles.values() if not v['leased']),
        overdue=overdue,
        lessees=lessees,
        payments=payments
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        vehicle_id = request.form['vehicle']
        email = request.form['email']
        phone = request.form['phone']

        if vehicle_id in vehicles and not vehicles[vehicle_id]['leased']:
            vehicles[vehicle_id]['leased'] = True
            lessees[name] = {
                'vehicle_id': vehicle_id,
                'email': email,
                'phone': phone
            }
            payments[name] = []
        return redirect(url_for('dashboard'))

    available_vehicles = [vid for vid, v in vehicles.items() if not v['leased']]
    return render_template('register.html', vehicles=available_vehicles)

@app.route('/pay/<lessee>', methods=['POST'])
def pay(lessee):
    if lessee in lessees:
        payments[lessee].append({
            'amount': LEASE_AMOUNT,
            'date': datetime.now().strftime('%Y-%m-%d')
        })
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
