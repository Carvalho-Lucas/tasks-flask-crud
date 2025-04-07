from flask import Flask, request, jsonify
from models.task import Task


app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route("/tasks", methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()

    title = data.get("title")
    description = data.get("description", "")

    if not title:
        return jsonify({"error": "Título é obrigatório"}), 400

    new_task = Task(id=task_id_control, title=title, description=description)
    task_id_control += 1
    tasks.append(new_task)

    return jsonify(new_task.to_dict()), 201


"""
@app.route("/tasks", methods = ['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id= task_id_control, title=data['title'], description= data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Nova tarefa criada com sucesso"})

"""
           
#código implementado somente na máquina - Desenvolvimento local
if __name__ == "__main__":
    app.run(debug=True)
