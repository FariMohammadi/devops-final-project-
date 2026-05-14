from flask import Flask, jsonify, request, render_template_string
import datetime

app = Flask(__name__)

# my study tasks - i will add more later
study_list = [
    {"id": 1, "subject": "Math", "task": "Review chapter 3 exercises", "done": False},
    {"id": 2, "subject": "DevOps", "task": "Study Docker basics", "done": True},
    {"id": 3, "subject": "English", "task": "Write essay draft", "done": False},
]

# counter for new task ids
id_counter = 4


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Study Planner</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Arial, sans-serif; background: #f0f4f8; color: #2d3748; min-height: 100vh; padding: 30px 20px; }
        h1 { text-align: center; font-size: 1.8rem; margin-bottom: 6px; color: #2b6cb0; }
        .subtitle { text-align: center; color: #718096; margin-bottom: 28px; font-size: 0.88rem; }
        .container { max-width: 620px; margin: 0 auto; }
        .card { background: white; border-radius: 10px; padding: 22px; margin-bottom: 18px; border: 1px solid #e2e8f0; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
        .form-row { display: flex; gap: 8px; flex-wrap: wrap; }
        input[type=text] { flex: 1; padding: 9px 12px; border-radius: 7px; border: 1px solid #cbd5e0; font-size: 0.95rem; min-width: 120px; }
        input[type=text]:focus { outline: none; border-color: #4299e1; }
        select { padding: 9px 12px; border-radius: 7px; border: 1px solid #cbd5e0; font-size: 0.95rem; background: white; }
        button.add-btn { padding: 9px 18px; background: #3182ce; border: none; border-radius: 7px; color: white; font-weight: 600; cursor: pointer; font-size: 0.95rem; }
        button.add-btn:hover { background: #2b6cb0; }
        .task-list { list-style: none; margin-top: 8px; }
        .task-item { display: flex; align-items: center; gap: 10px; padding: 11px 0; border-bottom: 1px solid #f0f4f8; }
        .task-item:last-child { border-bottom: none; }
        .task-item input[type=checkbox] { width: 17px; height: 17px; accent-color: #3182ce; cursor: pointer; }
        .task-info { flex: 1; }
        .task-subject { font-size: 0.75rem; font-weight: 700; color: #3182ce; text-transform: uppercase; margin-bottom: 2px; }
        .task-title { font-size: 0.95rem; }
        .task-title.done { text-decoration: line-through; color: #a0aec0; }
        .badge { font-size: 0.72rem; padding: 2px 8px; border-radius: 999px; background: #bee3f8; color: #2b6cb0; white-space: nowrap; }
        .badge.done { background: #c6f6d5; color: #276749; }
        .api-section h3 { color: #a0aec0; font-size: 0.8rem; margin-bottom: 8px; letter-spacing: 0.05em; }
        .api-link { display: inline-block; margin: 3px 3px 3px 0; padding: 3px 9px; background: #ebf8ff; border: 1px solid #bee3f8; border-radius: 5px; color: #2b6cb0; text-decoration: none; font-size: 0.78rem; font-family: monospace; }
        .api-link:hover { border-color: #4299e1; }
    </style>
</head>
<body>
<div class="container">
    <h1>📚 My Study Planner</h1>
    <p class="subtitle">Keep track of your study tasks</p>

    <div class="card">
        <div class="form-row" style="margin-bottom: 16px;">
            <select id="subjectInput">
                <option value="Math">Math</option>
                <option value="DevOps">DevOps</option>
                <option value="English">English</option>
                <option value="Physics">Physics</option>
                <option value="Other">Other</option>
            </select>
            <input type="text" id="taskInput" placeholder="What do you need to study?" />
            <button class="add-btn" onclick="addTask()">Add</button>
        </div>
        <ul class="task-list" id="taskList"></ul>
    </div>

    <div class="card api-section">
        <h3>API ENDPOINTS</h3>
        <a class="api-link" href="/api/tasks">/api/tasks</a>
        <a class="api-link" href="/api/health">/api/health</a>
        <a class="api-link" href="/api/info">/api/info</a>
    </div>
</div>

<script>
async function loadTasks() {
    const res = await fetch('/api/tasks');
    const data = await res.json();
    const list = document.getElementById('taskList');
    list.innerHTML = data.map(t => `
        <li class="task-item">
            <input type="checkbox" ${t.done ? 'checked' : ''} onchange="toggleTask(${t.id}, this.checked)" />
            <div class="task-info">
                <div class="task-subject">${t.subject}</div>
                <div class="task-title ${t.done ? 'done' : ''}">${t.task}</div>
            </div>
            <span class="badge ${t.done ? 'done' : ''}">${t.done ? 'Done' : 'Pending'}</span>
        </li>
    `).join('');
}

async function addTask() {
    const subject = document.getElementById('subjectInput').value;
    const task = document.getElementById('taskInput').value.trim();
    if (!task) return;
    await fetch('/api/tasks', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ subject, task })
    });
    document.getElementById('taskInput').value = '';
    loadTasks();
}

async function toggleTask(id, done) {
    await fetch(`/api/tasks/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ done })
    });
    loadTasks();
}

document.getElementById('taskInput').addEventListener('keydown', e => {
    if (e.key === 'Enter') addTask();
});

loadTasks();
</script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_PAGE)


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(study_list)


@app.route('/api/tasks', methods=['POST'])
def add_task():
    global id_counter
    data = request.get_json()
    # make sure the task field is not empty
    if not data or not data.get('task'):
        return jsonify({"error": "task field is required"}), 400
    new_task = {
        "id": id_counter,
        "subject": data.get('subject', 'Other'),
        "task": data['task'],
        "done": False
    }
    study_list.append(new_task)
    id_counter += 1
    return jsonify(new_task), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # find the task by id
    found = None
    for t in study_list:
        if t['id'] == task_id:
            found = t
            break
    if not found:
        return jsonify({"error": "task not found"}), 404
    data = request.get_json()
    if 'done' in data:
        found['done'] = data['done']
    if 'task' in data:
        found['task'] = data['task']
    return jsonify(found)


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global study_list
    found = next((t for t in study_list if t['id'] == task_id), None)
    if not found:
        return jsonify({"error": "task not found"}), 404
    study_list = [t for t in study_list if t['id'] != task_id]
    return jsonify({"message": "task deleted"})


@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "ok",
        "time": datetime.datetime.utcnow().isoformat()
    })


@app.route('/api/info')
def app_info():
    return jsonify({
        "app": "Study Planner",
        "version": "1.0",
        "built_with": "Flask",
        "author": "Fariba Mohammadi"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)