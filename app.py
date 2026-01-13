from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

# Cargar preguntas
with open("preguntas.json", "r", encoding="utf-8") as f:
    banco_preguntas = json.load(f)

@app.route("/", methods=["GET"])
def examen():
    cantidad = min(30, len(banco_preguntas))
    preguntas_aleatorias = random.sample(banco_preguntas, cantidad)
    return render_template("examen.html", preguntas=preguntas_aleatorias)

@app.route("/corregir", methods=["POST"])
def corregir():
    respuestas_usuario = request.form
    resultados = []
    puntaje = 0
    total = 0

    # Solo evaluar las preguntas enviadas
    for pregunta in banco_preguntas:
        key = f"pregunta_{pregunta['id']}"
        if key in respuestas_usuario:
            total += 1
            respuesta = int(respuestas_usuario[key])
            correcta = pregunta['respuesta_correcta']
            acierto = respuesta == correcta
            if acierto:
                puntaje += 1
            resultados.append({
                "pregunta": pregunta['pregunta'],
                "respuesta_usuario": respuesta,
                "respuesta_correcta": correcta,
                "opciones": pregunta['opciones'],
                "acierto": acierto
            })

    porcentaje = round((puntaje / total) * 100, 2) if total > 0 else 0

    return render_template("resultado.html", puntaje=puntaje, total=total,
                           porcentaje=porcentaje, resultados=resultados)
    
if __name__ == "__main__":
    app.run(debug=True)
