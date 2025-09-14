from flask import Blueprint, request, jsonify
from src.models.produto import Produto, db
import pandas as pd
import io
import os

produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/produtos/buscar', methods=['GET'])
def buscar_produtos():
    """Busca produtos por código ou descrição"""
    termo = request.args.get('termo', '')
    
    if not termo:
        return jsonify({'error': 'Termo de busca é obrigatório'}), 400
    
    # Busca por código (se for numérico) ou por nome
    if termo.isdigit():
        produtos = Produto.query.filter(Produto.cod == int(termo)).all()
    else:
        produtos = Produto.query.filter(
            Produto.nome_do_produto.ilike(f'%{termo}%')
        ).all()
    
    return jsonify([produto.to_dict() for produto in produtos])

@produto_bp.route('/produtos', methods=['POST'])
def cadastrar_produto():
    """Cadastra um novo produto"""
    data = request.get_json()
    
    if not data or 'cod' not in data:
        return jsonify({'error': 'Código do produto é obrigatório'}), 400
    
    # Verifica se o produto já existe
    produto_existente = Produto.query.filter_by(cod=data['cod']).first()
    if produto_existente:
        return jsonify({'error': 'Produto com este código já existe'}), 400
    
    produto = Produto(
        cod=data['cod'],
        nome_do_produto=data.get('nome_do_produto', ''),
        marca=data.get('marca', ''),
        ceara=data.get('ceara', 0),
        santa_catarina=data.get('santa_catarina', 0),
        sao_paulo=data.get('sao_paulo', 0),
        total=data.get('total', 0),
        reserva=data.get('reserva', 0)
    )
    
    db.session.add(produto)
    db.session.commit()
    
    return jsonify(produto.to_dict()), 201

@produto_bp.route('/produtos/<int:cod>', methods=['PUT'])
def atualizar_produto(cod):
    """Atualiza um produto existente"""
    produto = Produto.query.filter_by(cod=cod).first()
    
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    data = request.get_json()
    
    produto.nome_do_produto = data.get('nome_do_produto', produto.nome_do_produto)
    produto.marca = data.get('marca', produto.marca)
    produto.ceara = data.get('ceara', produto.ceara)
    produto.santa_catarina = data.get('santa_catarina', produto.santa_catarina)
    produto.sao_paulo = data.get('sao_paulo', produto.sao_paulo)
    produto.total = data.get('total', produto.total)
    produto.reserva = data.get('reserva', produto.reserva)
    
    db.session.commit()
    
    return jsonify(produto.to_dict())

@produto_bp.route('/produtos/upload', methods=['POST'])
def upload_planilha():
    """Upload de planilha CSV"""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Apenas arquivos CSV são aceitos'}), 400
    
    try:
        # Lê o CSV
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        df = pd.read_csv(stream)
        
        # Limpa os dados
        df = df.dropna(subset=['COD'])  # Remove linhas sem código
        df = df[df['COD'] != '']  # Remove linhas com código vazio
        
        produtos_inseridos = 0
        produtos_atualizados = 0
        
        for _, row in df.iterrows():
            try:
                cod = int(row['COD'])
                
                # Tenta converter valores numéricos, usa 0 se falhar
                def safe_int(value):
                    try:
                        if pd.isna(value) or str(value).strip() in ['', '#REF!', '#VALUE!']:
                            return 0
                        return int(float(str(value)))
                    except:
                        return 0
                
                produto_existente = Produto.query.filter_by(cod=cod).first()
                
                if produto_existente:
                    # Atualiza produto existente
                    produto_existente.nome_do_produto = str(row.get('NOME DO PRODUTO', ''))
                    produto_existente.marca = str(row.get('MARCA', ''))
                    produto_existente.ceara = safe_int(row.get('CEARÁ', 0))
                    produto_existente.santa_catarina = safe_int(row.get('SANTA CATARINA', 0))
                    produto_existente.sao_paulo = safe_int(row.get('SÃO PAULO', 0))
                    produto_existente.total = safe_int(row.get('TOTAL', 0))
                    produto_existente.reserva = safe_int(row.get('RESERVA', 0))
                    produtos_atualizados += 1
                else:
                    # Cria novo produto
                    produto = Produto(
                        cod=cod,
                        nome_do_produto=str(row.get('NOME DO PRODUTO', '')),
                        marca=str(row.get('MARCA', '')),
                        ceara=safe_int(row.get('CEARÁ', 0)),
                        santa_catarina=safe_int(row.get('SANTA CATARINA', 0)),
                        sao_paulo=safe_int(row.get('SÃO PAULO', 0)),
                        total=safe_int(row.get('TOTAL', 0)),
                        reserva=safe_int(row.get('RESERVA', 0))
                    )
                    db.session.add(produto)
                    produtos_inseridos += 1
                    
            except Exception as e:
                print(f"Erro ao processar linha: {e}")
                continue
        
        db.session.commit()
        
        return jsonify({
            'message': 'Planilha processada com sucesso',
            'produtos_inseridos': produtos_inseridos,
            'produtos_atualizados': produtos_atualizados
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao processar planilha: {str(e)}'}), 500

@produto_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    """Lista todos os produtos com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    produtos = Produto.query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        'produtos': [produto.to_dict() for produto in produtos.items],
        'total': produtos.total,
        'pages': produtos.pages,
        'current_page': produtos.page
    })

