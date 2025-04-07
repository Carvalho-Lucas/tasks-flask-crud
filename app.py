from flask import Flask
app = Flask(__name__)

#Rota -> recebe e devolve comunicação para quem solicita

@app.route("/")
def hello_world():
    return "Hello !!! 🚀"

@app.route("/about")
def about():
    return "Página sobre"
           
#código implementado somente na máquina - Desenvolvimento local
if __name__ == "__main__":
    app.run(debug=True)
