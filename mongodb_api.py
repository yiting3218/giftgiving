from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# 連接 MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['giftgiving']
friends_col = db['friends']
gifts_col = db['gifts']

# 取得所有好友
@app.route('/api/friends', methods=['GET'])
def get_friends():
    friends = list(friends_col.find({}, {'_id': 1, 'name': 1, 'birthday': 1}))
    for f in friends:
        f['id'] = str(f['_id'])
        del f['_id']
    return jsonify(friends)

# 新增好友
@app.route('/api/friends', methods=['POST'])
def add_friend():
    data = request.json
    name = data.get('name')
    birthday = data.get('birthday')
    if not name or not birthday:
        return jsonify({'error': 'Name and birthday required'}), 400
    result = friends_col.insert_one({'name': name, 'birthday': birthday})
    return jsonify({'id': str(result.inserted_id), 'name': name, 'birthday': birthday})

# 刪除好友
@app.route('/api/friends/<id>', methods=['DELETE'])
def delete_friend(id):
    from bson import ObjectId
    result = friends_col.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)

# 送禮紀錄 CRUD
@app.route('/api/gifts', methods=['POST'])
def add_gift():
    """新增送禮紀錄，body: {sender, receiver, gift, amount, date, category, note}"""
    data = request.json
    required = ['sender', 'receiver', 'gift', 'amount', 'date', 'category']
    if not all(data.get(k) for k in required):
        return jsonify({'error': '缺少必要欄位'}), 400
    result = gifts_col.insert_one(data)
    return jsonify({'id': str(result.inserted_id)})

@app.route('/api/gifts', methods=['GET'])
def get_gifts():
    query = {}
    sender = request.args.get('sender')
    receiver = request.args.get('receiver')
    gift = request.args.get('gift')
    if sender:
        query['sender'] = sender
    if receiver:
        query['receiver'] = receiver
    if gift:
        query['gift'] = gift
    gifts = list(gifts_col.find(query))
    for g in gifts:
        g['id'] = str(g['_id'])
        del g['_id']
    return jsonify(gifts)

@app.route('/api/gifts/<id>', methods=['DELETE'])
def delete_gift(id):
    from bson import ObjectId
    result = gifts_col.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Not found'}), 404
