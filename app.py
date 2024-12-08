import os
import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'database/app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_ids = db.Column(db.PickleType)
    date = db.Column(db.String)
    total = db.Column(db.Float)

    def __repr__(self):
        return f'<Ticket {self.id}>'

with app.app_context():
    db.create_all()

@app.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json()
    print(f"Received data: {data}")
    new_ticket = Ticket(
        user_id=data['user_id'],
        product_ids=data['product_ids'],
        date=data['date'],
        total=data['total']
    )
    db.session.add(new_ticket)
    db.session.commit()
    print(f"Created ticket: {new_ticket}")
    return jsonify({'message': 'Ticket créé avec succès'}), 201

@app.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    print(f"Fetching ticket with ID: {ticket_id}")
    ticket = Ticket.query.get(ticket_id)
    if ticket is None:
        print(f"Ticket with ID {ticket_id} not found")
        return jsonify({'error': 'Ticket non trouvé'}), 404
    ticket_dict = {
        'id': ticket.id,
        'user_id': ticket.user_id,
        'product_ids': ticket.product_ids,
        'date': ticket.date,
        'total': ticket.total
    }

    print(f"Found ticket: {ticket_dict}")
    return jsonify(ticket_dict)

@app.route('/users/<int:user_id>/tickets', methods=['GET'])
def get_user_tickets(user_id):
    print(f"Fetching tickets for user ID: {user_id}")
    tickets = Ticket.query.filter_by(user_id=user_id).all()
    print(f"Found tickets: {tickets}")
    user_tickets = []
    for ticket in tickets:
        ticket_dict = {
            'id': ticket.id,
            'user_id': ticket.user_id,
            'product_ids': ticket.product_ids,
            'date': ticket.date,
            'total': ticket.total
        }
        user_tickets.append(ticket_dict)
    return jsonify(user_tickets)

@app.route('/products/<int:product_id>/tickets', methods=['GET'])
def get_product_tickets(product_id):
    print(f"Fetching tickets for product ID: {product_id}")
    tickets = Ticket.query.all()
    print(f"Found tickets: {tickets}")
    product_tickets = []
    for ticket in tickets:
        if product_id in ticket.product_ids:
            ticket_dict = {
                'id': ticket.id,
                'user_id': ticket.user_id,
                'product_ids': ticket.product_ids,
                'date': ticket.date,
                'total': ticket.total
            }
            product_tickets.append(ticket_dict)
    return jsonify(product_tickets)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')