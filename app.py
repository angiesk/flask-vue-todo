from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'todos'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/todos'

mongo = PyMongo(app)

CORS(app)
@app.route('/')
def hello():
  return('<h1>Hello world nothing to do here pls visit postman for testing apis</h1> ')
@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
  tasks = mongo.db.todo;
  result = []
  for field in tasks.find():
    result.append({'_id': str(field['_id']), 'title': field['title']})
  return jsonify(result)

@app.route('/api/task', methods=['POST'])
def add_task():
  tasks = mongo.db.todo;
  title = request.get_json()['title']
  task_id = tasks.insert({'title': title})
  new_task = tasks.find_one({'_id': task_id})
  result = {'title': new_task['title']}
  return jsonify({'result': result, 'status': 'task added successfully'})
  
@app.route('/api/task/<id>', methods=['PUT'])
def update_task():
  tasks = mongo.db.todo;
  title = request.get_json()['title']
  tasks.find_one_and_update({'_id': ObjectId(id)}, {"$set": {"title": title}}, upsert=False)
  new_task = tasks.find_one({'_id':ObjectId(id)})
  result = {'title': new_task['title']}
  return jsonify({'result': result, 'status': 'task updated successfully'})


  @app.route('/api/task/<id>', methods=['DELETE'])
  def delete_task():
    tasks = mongo.db.todo;

    response = tasks.delete_one({'_id': ObjectId(id)})
    
    if response.deleted_count == 1:
      result ={'status': 'task deleted successfully'}
    else:
      result = {'status': 'no task deleted'}
    return jsonify(result)



if __name__ == '__main__':
  app.run(debug=1)
