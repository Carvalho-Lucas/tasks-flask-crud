from flask import Flask, request, jsonify
app = Flask(__name__)

# Lista onde armazenamos as tarefas (simulando um banco de dados)
tarefas = []
proximo_id = 1

# ROTA POST - Cria uma nova tarefa
@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    global proximo_id
    dados = request.get_json()
    titulo = dados.get("title")

    if not titulo:
        return jsonify({"erro": "Título é obrigatório"}), 400

    nova = {"id": proximo_id, "title": titulo}
    tarefas.append(nova)
    proximo_id += 1
    return jsonify(nova), 201

# ROTA GET - Lista todas as tarefas
@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    return jsonify(tarefas), 200

# ROTA PUT - Atualiza o título de uma tarefa pelo ID
@app.route("/tarefas/<int:id>", methods=["PUT"])
def atualizar_tarefa(id):
    dados = request.get_json()
    titulo = dados.get("title")

    for tarefa in tarefas:
        if tarefa["id"] == id:
            tarefa["title"] = titulo
            return jsonify(tarefa), 200

    return jsonify({"erro": "Tarefa não encontrada"}), 404

# ROTA DELETE - Remove uma tarefa pelo ID
@app.route("/tarefas/<int:id>", methods=["DELETE"])
def deletar_tarefa(id):
    for tarefa in tarefas:
        if tarefa["id"] == id:
            tarefas.remove(tarefa)
            return jsonify({"mensagem": "Tarefa deletada com sucesso"}), 200

    return jsonify({"erro": "Tarefa não encontrada"}), 404

# Inicia o servidor
if __name__ == "__main__":
    app.run(debug=True)
