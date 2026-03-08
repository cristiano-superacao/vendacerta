"""
Script para limpar todos os dados do banco de dados
Mantém apenas a estrutura das tabelas e o usuário Super Admin
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import (
    User, Empresa, Cliente, Vendedor, Supervisor, 
    Funcionario, Equipe, Meta, Venda, Comissao,
    ConfiguracaoMeta, RelatorioVenda, Estoque, 
    ProdutoEstoque, MovimentacaoEstoque, BackupConfig
)
from werkzeug.security import generate_password_hash

def limpar_dados():
    """Remove todos os dados mas mantém o Super Admin"""
    with app.app_context():
        try:
            print("🗑️  Iniciando limpeza do banco de dados...")
            
            # Lista de tabelas para limpar (ordem importa por causa de foreign keys)
            tabelas = [
                ('Comissões', Comissao),
                ('Vendas', Venda),
                ('Relatórios de Venda', RelatorioVenda),
                ('Movimentações de Estoque', MovimentacaoEstoque),
                ('Produtos em Estoque', ProdutoEstoque),
                ('Estoques', Estoque),
                ('Configurações de Meta', ConfiguracaoMeta),
                ('Metas', Meta),
                ('Equipes', Equipe),
                ('Funcionários', Funcionario),
                ('Clientes', Cliente),
                ('Vendedores', Vendedor),
                ('Supervisores', Supervisor),
                ('Configurações de Backup', BackupConfig),
            ]
            
            # Remove dados de cada tabela
            total_removidos = 0
            for nome, model in tabelas:
                count = model.query.delete()
                total_removidos += count
                print(f"  ✅ {nome}: {count} registro(s) removido(s)")
            
            # Remove usuários exceto o Super Admin
            usuarios_removidos = User.query.filter(User.email != 'admin@suameta.com.br').delete()
            total_removidos += usuarios_removidos
            print(f"  ✅ Usuários (exceto Super Admin): {usuarios_removidos} removido(s)")
            
            # Remove empresas
            empresas_removidas = Empresa.query.delete()
            total_removidos += empresas_removidas
            print(f"  ✅ Empresas: {empresas_removidas} removida(s)")
            
            # Garante que o Super Admin existe e reseta a senha
            super_admin = User.query.filter_by(email='admin@suameta.com.br').first()
            if super_admin:
                super_admin.password = generate_password_hash('Admin@2025!')
                super_admin.ativo = True
                super_admin.empresa_id = None
                print(f"  ✅ Super Admin resetado (senha: Admin@2025!)")
            else:
                # Cria Super Admin se não existir
                super_admin = User(
                    nome='Super Administrador',
                    email='admin@suameta.com.br',
                    password=generate_password_hash('Admin@2025!'),
                    cargo='super_admin',
                    ativo=True,
                    empresa_id=None
                )
                db.session.add(super_admin)
                print(f"  ✅ Super Admin criado (senha: Admin@2025!)")
            
            # Commit das alterações
            db.session.commit()
            
            print(f"\n✅ Limpeza concluída!")
            print(f"📊 Total de registros removidos: {total_removidos}")
            print(f"\n🔐 CREDENCIAIS DE ACESSO:")
            print(f"   Email: admin@suameta.com.br")
            print(f"   Senha: Admin@2025!")
            print(f"\n⚠️  Altere a senha após o primeiro acesso!")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erro ao limpar dados: {e}")
            raise

if __name__ == '__main__':
    limpar_dados()
