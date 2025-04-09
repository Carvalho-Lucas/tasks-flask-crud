from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

# Lista onde serão armazenadas as tarefas criadas
tasks = []

# Controlador de ID único para cada tarefa criada
task_id_control = 1

# ROTA POST - CRIAR uma nova tarefa
@app.route("/tasks", methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()# pega o JSON enviado pelo cliente

    title = data.get("title")# extrai o título
    description = data.get("description", "")

    if not title:
        return jsonify({"error": "Título é obrigatório"}), 400

    new_task = Task(id=task_id_control, title=title, description=description)# cria tarefa
    task_id_control += 1
    tasks.append(new_task)

    return jsonify(new_task.to_dict()), 201  # Retorna a nova tarefa criada + status 201

# ROTA GET - LISTAR TODAS as tarefas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = []

    for task in tasks:
        task_list.append(task.to_dict())

    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }

    return jsonify(output)

# ROTA GET - BUSCAR tarefa específica pelo ID
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
    return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

# ROTA PUT - ATUALIZAR uma tarefa específica
@app.route('/tasks/<int:id>', methods=["PUT"])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t  # Localiza a tarefa pelo ID

    if task is None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

    data = request.get_json()

    # Atualiza os dados da tarefa existente com os valores enviados
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']

    return jsonify({"message": "Tarefa atualizada com sucesso"})

# ROTA DELETE - DELETA uma tarefa específica
@app.route('/tasks/<int:id>', methods=["DELETE"])
def delete_task(id):
    task = None

    for t in tasks:
        if t.id == id:
            task = t  # Localiza a tarefa pelo ID
            break
        
    if task is None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso"})

# Inicializa o servidor local
if __name__ == "__main__":
    app.run(debug=True)
