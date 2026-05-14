import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    # check that health endpoint works
    res = client.get('/api/health')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['status'] == 'ok'

def test_get_tasks(client):
    # should return a list of study tasks
    res = client.get('/api/tasks')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert isinstance(data, list)

def test_create_task(client):
    # add a new study task and check it was created
    res = client.post('/api/tasks',
                      data=json.dumps({'subject': 'Math', 'task': 'Study for midterm'}),
                      content_type='application/json')
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['task'] == 'Study for midterm'
    assert data['done'] == False

def test_create_task_missing_field(client):
    # sending empty body should return 400
    res = client.post('/api/tasks',
                      data=json.dumps({}),
                      content_type='application/json')
    assert res.status_code == 400

def test_update_task(client):
    # create a task then mark it as done
    res = client.post('/api/tasks',
                      data=json.dumps({'subject': 'English', 'task': 'Read chapter 2'}),
                      content_type='application/json')
    task_id = json.loads(res.data)['id']

    res = client.put(f'/api/tasks/{task_id}',
                     data=json.dumps({'done': True}),
                     content_type='application/json')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['done'] == True

def test_update_task_not_found(client):
    # updating a task that doesnt exist
    res = client.put('/api/tasks/9999',
                     data=json.dumps({'done': True}),
                     content_type='application/json')
    assert res.status_code == 404

def test_info_endpoint(client):
    # check app info returns correct app name
    res = client.get('/api/info')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['app'] == 'Study Planner'

def test_homepage(client):
    # homepage should load and show the planner title
    res = client.get('/')
    assert res.status_code == 200
    assert b'My Study Planner' in res.data