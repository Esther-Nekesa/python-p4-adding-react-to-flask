#!/usr/bin/env python3
from flask import Flask, request, make_response
from flask_restful import Api, Resource
from flask_cors import CORS  # MUST have this
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize CORS - This allows your React app (port 4000) to talk to Flask (port 5555)
CORS(app)

db.init_app(app)
api = Api(app)

class Messages(Resource):
    def get(self):
        messages = [m.to_dict() for m in Message.query.all()]
        return make_response(messages, 200)

    def post(self):
        data = request.get_json()
        new_msg = Message(
            username=data.get('username'),
            body=data.get('body')
        )
        db.session.add(new_msg)
        db.session.commit()
        return make_response(new_msg.to_dict(), 201)

class MessageByID(Resource):
    def delete(self, id):
        msg = Message.query.filter_by(id=id).first()
        if msg:
            db.session.delete(msg)
            db.session.commit()
            return make_response("", 204)
        return make_response({"error": "Message not found"}, 404)

api.add_resource(Messages, '/messages')
api.add_resource(MessageByID, '/messages/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)