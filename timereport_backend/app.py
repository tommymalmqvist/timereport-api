import os
from chalice import Chalice
from chalicelib.lib import dynamo

"""
GET        /user/<user_id>
GET        /user/<user_id>?startDate=YYYYMMDD&endDate=YYYYMMDD
POST       /event
GET        /event/?startDate=YYYYMMDD&endDate=YYYYMMDD
GET        /event/<_id>
PUT        /event/<_id>
DELETE     /event/<_id>
GET        /table-name  : returns name of dynamodb table (good for testing connection)

{'user_id': 'U2FGC795G', 'user_name': 'kamger', 'reason': 'vab', 'event_date': datetime.datetime(2018, 12, 5, 0, 0), 'hours': '8'}
{"user_id": "U2FGC795G", "user_name": "kamger", "reason": "vab", "event_date": "2018-12-03", "hours":8}
"""

app = Chalice(app_name='timereport_backend')
app.debug = os.getenv('BACKEND_DEBUG', False)

@app.route('/table-name')
def test_name():
    """
    :return: table name
    """
    return dynamo.dynamoboto.table.name

@app.route('/user/{user_id}', methods=['GET'])
def get_user_by_id(user_id):
    if app.current_request.query_params:
        start_date = app.current_request.query_params.get('startDate')
        end_date = app.current_request.query_params.get('endDate')
        return dynamo.get_user_between_date(user_id, start_date, end_date)
    else:
        return dynamo.get_id(user_id)

@app.route('/event', methods=['POST'])
def create_event():
    dynamo.create_event(app.current_request.json_body)
    return app.current_request.json_body

@app.route('/event/{_id}', methods=['GET'])
def get_event_by_id(_id):
    return {'event_id': _id}

@app.route('/event/{_id}', methods=['PUT'])
def put_event_by_id(_id):
    return app.current_request.json_body

@app.route('/event/{_id}', methods=['DELETE'])
def delete_event_by_id(_id):
    return {'event_id': _id}
