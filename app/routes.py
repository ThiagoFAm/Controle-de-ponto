from flask import Blueprint, request, jsonify
from .database import get_connection

main = Blueprint('main', __name__)

# ==========================
# Registro de ponto (POST)
# ==========================
@main.route('/registro', methods=['POST'])
def registro():
    dado = request.get_json()

    usuario_id = dado.get('usuario_id')
    data_hora = dado.get('data_hora')

    # Validação básica
    if not usuario_id or not data_hora:
        return jsonify({
            "status": "erro",
            "mensagem": "usuario_id e data_hora são obrigatórios"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    # Buscar o último registro do usuário
    cursor.execute("""
        SELECT tipo FROM registros 
        WHERE usuario_id = ? 
        ORDER BY data_hora DESC 
        LIMIT 1
    """, (usuario_id,))
    ultimo = cursor.fetchone()

    # Definir tipo baseado no último registro
    if not ultimo:
        tipo = "entrada"
    elif ultimo[0] == "entrada":
        tipo = "saida"
    else:
        tipo = "entrada"

    # Inserir registro
    cursor.execute("""
        INSERT INTO registros (usuario_id, data_hora, tipo)
        VALUES (?, ?, ?)
    """, (usuario_id, data_hora, tipo))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "status": "sucesso",
        "mensagem": f"Registro de {tipo} criado",
        "dados": {
            "id": novo_id,
            "usuario_id": usuario_id,
            "data_hora": data_hora,
            "tipo": tipo
        }
    }), 201

# ==========================
# Listar todos os registros (GET)
# ==========================
@main.route('/registros', methods=['GET'])
def registros():
    conn = get_connection()
    dados = conn.execute(
        "SELECT * FROM registros ORDER BY data_hora DESC"
    ).fetchall()

    resultados = []
    for i in dados:
        resultados.append({
            "id": i["id"],
            "usuario_id": i["usuario_id"],
            "data_hora": i["data_hora"],
            "tipo": i["tipo"]
        })
    
    conn.close()
    return jsonify({
        "status": "sucesso",
        "dados": resultados
    })

# ==========================
# Listar registros por usuário (GET)
# ==========================
@main.route('/registros/usuario/<int:usuario_id>', methods=['GET'])
def registros_por_usuario(usuario_id):
    conn = get_connection()
    dados_do_usuario = conn.execute(
        "SELECT * FROM registros WHERE usuario_id = ? ORDER BY data_hora DESC",
        (usuario_id,)
    ).fetchall()
     
    resultado = []
    for i in dados_do_usuario:
        resultado.append({
            "id": i["id"],
            "usuario_id": i["usuario_id"],
            "data_hora": i["data_hora"],
            "tipo": i["tipo"]
        })

    conn.close()
    return jsonify({
        "status": "sucesso",
        "dados": resultado
    })

# ==========================
# Deletar registro (DELETE)
# ==========================
@main.route('/registro/<int:id>', methods=['DELETE'])
def deletar_registro(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registros WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({
        "status": "sucesso",
        "mensagem": f"Registro {id} deletado"
    })

# ==========================
# Rota de teste
# ==========================
@main.route('/teste', methods=['GET'])
def teste():
    return "ok"
