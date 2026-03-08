"""
Teste rápido para verificar campo preco_servico
"""

import os
import unittest


if os.getenv("RUN_INTEGRATION_TESTS") != "1":
    raise unittest.SkipTest(
        "Teste de integração (depende de app/banco). "
        "Defina RUN_INTEGRATION_TESTS=1 para executar."
    )

from app import app, db
from models import Produto

def testar_preco_servico():
    with app.app_context():
        # Buscar primeiro produto
        produto = Produto.query.first()
        
        if produto:
            print('✅ Produto encontrado:')
            print(f'   Código: {produto.codigo}')
            print(f'   Nome: {produto.nome}')
            print(f'   Preço Venda: R$ {produto.preco_venda:.2f}')
            print(f'   Preço Serviço: R$ {produto.preco_servico if produto.preco_servico else 0:.2f}')
            print('\n✅ Campo preco_servico está acessível!')
        else:
            print('⚠️  Nenhum produto cadastrado ainda')
        
        # Verificar total de produtos
        total = Produto.query.count()
        print(f'\n📊 Total de produtos: {total}')

if __name__ == '__main__':
    testar_preco_servico()
