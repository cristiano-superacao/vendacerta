"""
Verificacao Simples da Integracao Sistema-Banco
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

from sqlalchemy import inspect, text
from config import Config
from models import db, Vendedor, Cliente, Meta, Produto

# Conectar ao banco
from sqlalchemy import create_engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

print("\n" + "="*80)
print("VERIFICACAO DE INTEGRACAO SISTEMA-BANCO DE DADOS")
print("="*80)

# Verificar tabelas
inspector = inspect(engine)
tabelas_esperadas = ['vendedor', 'clientes', 'metas', 'produtos', 'compra_cliente']
tabelas_existentes = inspector.get_table_names()

print("\nTabelas no banco de dados:")
for tabela in tabelas_existentes:
    print(f"  - {tabela}")

print(f"\nTotal de tabelas: {len(tabelas_existentes)}")

# Verificar colunas de tabelas principais
print("\n" + "="*80)
print("ESTRUTURA DAS TABELAS PRINCIPAIS")
print("="*80)

for tabela in ['vendedor', 'clientes', 'metas', 'produtos']:
    if tabela in tabelas_existentes:
        print(f"\nTabela: {tabela}")
        colunas = inspector.get_columns(tabela)
        print(f"  Colunas ({len(colunas)}):")
        for col in colunas[:10]:  # Mostrar apenas primeiras 10
            print(f"    - {col['name']} ({col['type']})")
        if len(colunas) > 10:
            print(f"    ... e mais {len(colunas)-10} colunas")
    else:
        print(f"\nTabela: {tabela} - NAO EXISTE!")

# Testar queries
print("\n" + "="*80)
print("TESTE DE COMUNICACAO")
print("="*80)

try:
    with engine.connect() as conn:
        # Contar registros
        if 'vendedor' in tabelas_existentes:
            result = conn.execute(text("SELECT COUNT(*) FROM vendedor"))
            print(f"Vendedores: {result.scalar()}")
        
        if 'clientes' in tabelas_existentes:
            result = conn.execute(text("SELECT COUNT(*) FROM clientes"))
            print(f"Clientes: {result.scalar()}")
        
        if 'metas' in tabelas_existentes:
            result = conn.execute(text("SELECT COUNT(*) FROM metas"))
            print(f"Metas: {result.scalar()}")
        
        if 'produtos' in tabelas_existentes:
            result = conn.execute(text("SELECT COUNT(*) FROM produtos"))
            print(f"Produtos: {result.scalar()}")
        
        print("\nComunicacao com banco: OK")
except Exception as e:
    print(f"ERRO na comunicacao: {e}")

print("\n" + "="*80)
print("VERIFICACAO CONCLUIDA")
print("="*80 + "\n")
