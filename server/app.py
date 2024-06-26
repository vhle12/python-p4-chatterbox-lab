from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    
    getter = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
    
    if request.method == 'GET':
        return getter, 200
    
    elif request.method == 'POST':
        data = request.get_json()
        
        new_message = Message(
            body = data.get('body'),
            username = data.get('username'),
            created_at = data.get('created_at'),
            updated_at = data.get('updated_at')
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return new_message.to_dict(), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    
    if not message:
        return {'error': 'message not found'}, 404
    
    if request.method == 'PATCH':
        data = request.get_json()
        
        message.body = data.get('body')
        
        db.session.add(message)
        db.session.commit()
        
        return message.to_dict(), 200
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return {}, 204

if __name__ == '__main__':
    app.run(port=5555)
