from flask import Blueprint, jsonify, request
from reserva_model import Reserva
from sql import db
import requests
import threading

routes = Blueprint("routes", __name__)

turmas_cache = {}

def atualizar_cache_turmas():
    global turmas_cache
    try:
        url = "https://gest-o-escolar-api-docker.onrender.com/api/turmas"
        resp = requests.get(url)
        if resp.status_code == 200:
            # A correção está aqui: 'dados' JÁ É a lista de turmas
            turmas = resp.json() # Ou dados = resp.json(), e então turmas = dados
            
            # Atualiza o cache: armazenamos as turmas pelo id para fácil busca
            turmas_cache = {turma['id']: turma for turma in turmas}
            print(f"Cache de turmas atualizado: {len(turmas_cache)} turmas carregadas")
        else:
            print(f"Falha ao atualizar cache de turmas: Status {resp.status_code}")
    except Exception as e:
        print(f"Erro ao atualizar cache de turmas: {e}")

    threading.Timer(600, atualizar_cache_turmas).start()

# Inicializa o cache assim que o módulo é importado
atualizar_cache_turmas()

def validar_turma(turma_id):
    return turma_id in turmas_cache

@routes.route('/reservas', methods=['POST'])
def criar_reserva():
    data = request.json
    turma_id = data.get('turma_id')

    if turma_id is None:
        return jsonify({'erro': 'O campo turma_id é obrigatório'}), 400

    if not validar_turma(turma_id):
        return jsonify({'erro': 'Turma não encontrada'}), 400

    reserva = Reserva(
        sala=data.get('sala'),
        data=data.get('data'),
        hora_inicio=data.get('hora_inicio'),
        hora_fim=data.get('hora_fim'),
        turma_id=turma_id
    )
    db.session.add(reserva)
    db.session.commit()

    # Pega a turma do cache
    turma = turmas_cache.get(turma_id)

    return jsonify({
        'mensagem': 'Reserva criada com sucesso',
        'reserva': {
            'id': reserva.id,
            'sala': reserva.sala,
            'data': reserva.data,
            'hora_inicio': reserva.hora_inicio,
            'hora_fim': reserva.hora_fim,
            'turma': turma  # inclui dados da turma no retorno
        }
    }), 201


@routes.route('/reservas', methods=['GET'])
def listar_reservas():
    reservas = Reserva.query.all()
    resultado = []
    for r in reservas:
        turma = turmas_cache.get(r.turma_id)
        resultado.append({
            'id': r.id,
            'sala': r.sala,
            'data': r.data,
            'hora_inicio': r.hora_inicio,
            'hora_fim': r.hora_fim,
            'turma': turma  # dados da turma no retorno
        })
    return jsonify(resultado)


@routes.route('/reservas/<int:id>', methods=['GET'])
def buscar_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    turma = turmas_cache.get(reserva.turma_id)
    return jsonify({
        'id': reserva.id,
        'sala': reserva.sala,
        'data': reserva.data,
        'hora_inicio': reserva.hora_inicio,
        'hora_fim': reserva.hora_fim,
        'turma': turma  # dados da turma
    })