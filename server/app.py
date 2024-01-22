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
def messages(body="empty", username="bob"):

    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.all()]
        # sorted_messages = sorted(messages, key=lambda message:message.created_at)
        # response = make_response(
        #     messages,
        #     200
        # )
        # return response
        return make_response(messages, 200)
    
    elif request.method == 'POST':
# POST not working still
        new_message = Message(
            body = body,
            username = username
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()

        response = make_response(
            new_message_dict,
            201
        )

        return response

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    return ''

if __name__ == '__main__':
    app.run(port=5555)
