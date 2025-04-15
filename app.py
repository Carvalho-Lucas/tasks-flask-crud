from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

# Lista onde serão armazenadas as tarefas criadas
tasks = []

# Controlador de ID único para cada tarefa criada
proximo_id = 1

# ROTA POST - CRIAR uma nova tarefa
@app.route("/tasks", methods=['POST'])
def create_task():
    global proximo_id
    data = request.get_json()  # Recebe os dados enviados pelo cliente

    title = data.get("title")
    description = data.get("description")

    # Validação: title obrigatório, description opcional mas não vazio
    if not title:
        return jsonify({"ERROR": "Título é obrigatório"}), 400
    elif not description:
        return jsonify({"ERROR": "Descrição é obrigatória"}), 400

    new_task = Task(
        id=proximo_id,
        title=title,
        description=description
    )

    proximo_id += 1
    tasks.append(new_task)

    return jsonify({
        "message": "Nova tarefa criada com sucesso",
        "id": new_task.id
    }), 201

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
            break #Dica de performace para não gastar processamento à toa.

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
            break #Dica de performace para não gastar processamento à toa.

    if task is None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso"})

# Inicializa o servidor local
if __name__ == "__main__":
    app.run(debug=True)
