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
    data = request.get_json()  # Recebe os dados enviados pelo cliente

    new_task = Task(
        id=task_id_control,
        title=data['title'],
        description=data.get("description", "")
    )
    
    task_id_control += 1  # Atualiza o ID para a próxima tarefa
    tasks.append(new_task)  # Salva a nova tarefa

    print(tasks)  # DEBUG: mostra no console
    return jsonify({"message": "Nova tarefa criada com sucesso", "id": new_task.id})# Retorna a nova tarefa criada + status 200

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
