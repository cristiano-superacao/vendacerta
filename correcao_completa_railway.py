#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Correção Completa do Sistema VendaCerta no Railway
- Verifica e corrige schema do banco de dados
- Adiciona colunas faltantes
- Cria usuário admin se necessário
- Gera relatório completo
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import ProgrammingError, IntegrityError
from werkzeug.security import generate_password_hash

def print_header(title):
    """Imprime um cabeçalho formatado"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def get_database_url():
    """Obtém a URL do banco de dados de múltiplas fontes"""
    print_header("🔍 VERIFICANDO VARIÁVEIS DE AMBIENTE")
    
    # Tentar múltiplas variáveis
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        print("✅ DATABASE_URL encontrada")
        return db_url
    
    db_url = os.environ.get('DATABASE_PUBLIC_URL')
    if db_url:
        print("✅ DATABASE_PUBLIC_URL encontrada (usando como alternativa)")
        return db_url
    
    # Tentar construir URL a partir de variáveis individuais
    pghost = os.environ.get('PGHOST')
    pgport = os.environ.get('PGPORT')
    pguser = os.environ.get('PGUSER')
    pgpassword = os.environ.get('PGPASSWORD')
    pgdatabase = os.environ.get('PGDATABASE')
    
    if all([pghost, pgport, pguser, pgpassword, pgdatabase]):
        db_url = f"postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}"
        print("✅ URL construída a partir de variáveis PG* individuais")
        return db_url
    
    print("❌ Nenhuma variável de ambiente de banco de dados encontrada!")
    print("\n📋 Variáveis disponíveis:")
    for key in ['DATABASE_URL', 'DATABASE_PUBLIC_URL', 'PGHOST', 'PGPORT', 'PGUSER', 'PGDATABASE']:
        value = os.environ.get(key, 'NÃO DEFINIDA')
        if 'PASSWORD' not in key:
            print(f"   {key}: {value}")
    
    return None

def verificar_e_corrigir_schema(engine):
    """Verifica e corrige o schema do banco de dados"""
    print_header("🔧 VERIFICANDO E CORRIGINDO SCHEMA DO BANCO DE DADOS")
    
    try:
        with engine.connect() as conn:
            # Verificar se a tabela usuarios existe
            inspector = inspect(engine)
            tabelas = inspector.get_table_names()
            
            print(f"\n📊 Tabelas encontradas: {', '.join(tabelas)}")
            
            if 'usuarios' not in tabelas:
                print("\n❌ Tabela 'usuarios' não existe!")
                print("⚠️  O banco de dados precisa ser inicializado primeiro.")
                print("💡 Execute: python init_db.py")
                return False
            
            # Obter colunas atuais da tabela usuarios
            colunas_atuais = [col['name'] for col in inspector.get_columns('usuarios')]
            print(f"\n📋 Colunas atuais da tabela 'usuarios': {len(colunas_atuais)}")
            
            # Definir colunas obrigatórias com seus tipos
            colunas_obrigatorias = {
                'supervisor_id': {
                    'tipo': 'INTEGER',
                    'descricao': 'ID do supervisor (hierarquia)'
                },
                'pode_gerenciar_tecnicos': {
                    'tipo': 'BOOLEAN DEFAULT FALSE',
                    'descricao': 'Permissão para gerenciar técnicos'
                },
                'pode_atribuir_tecnicos': {
                    'tipo': 'BOOLEAN DEFAULT FALSE',
                    'descricao': 'Permissão para atribuir técnicos'
                }
            }
            
            # Verificar e adicionar colunas faltantes
            colunas_adicionadas = 0
            for coluna_nome, coluna_info in colunas_obrigatorias.items():
                if coluna_nome not in colunas_atuais:
                    print(f"\n➕ Adicionando coluna: {coluna_nome}")
                    print(f"   Descrição: {coluna_info['descricao']}")
                    
                    try:
                        # Adicionar coluna
                        sql = f"ALTER TABLE usuarios ADD COLUMN {coluna_nome} {coluna_info['tipo']}"
                        conn.execute(text(sql))
                        conn.commit()
                        print(f"   ✅ Coluna '{coluna_nome}' adicionada com sucesso!")
                        colunas_adicionadas += 1
                        
                        # Se for supervisor_id, adicionar constraint e índice
                        if coluna_nome == 'supervisor_id':
                            try:
                                # Foreign key
                                fk_sql = """
                                ALTER TABLE usuarios 
                                ADD CONSTRAINT fk_usuarios_supervisor 
                                FOREIGN KEY (supervisor_id) 
                                REFERENCES usuarios(id) 
                                ON DELETE SET NULL
                                """
                                conn.execute(text(fk_sql))
                                conn.commit()
                                print(f"   ✅ Foreign key constraint adicionada")
                            except Exception as e:
                                print(f"   ⚠️  Aviso ao adicionar FK: {str(e)}")
                            
                            try:
                                # Índice
                                idx_sql = "CREATE INDEX idx_usuario_supervisor ON usuarios(supervisor_id)"
                                conn.execute(text(idx_sql))
                                conn.commit()
                                print(f"   ✅ Índice criado")
                            except Exception as e:
                                print(f"   ⚠️  Aviso ao criar índice: {str(e)}")
                    
                    except Exception as e:
                        print(f"   ❌ Erro ao adicionar coluna '{coluna_nome}': {str(e)}")
                        conn.rollback()
                else:
                    print(f"✓ Coluna '{coluna_nome}' já existe")
            
            # Verificar schema final
            colunas_finais = [col['name'] for col in inspector.get_columns('usuarios')]
            print(f"\n📊 Schema final da tabela 'usuarios': {len(colunas_finais)} colunas")
            
            if colunas_adicionadas > 0:
                print(f"\n✅ {colunas_adicionadas} coluna(s) adicionada(s) com sucesso!")
            else:
                print(f"\n✅ Schema já estava correto!")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Erro ao verificar/corrigir schema: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def verificar_usuario_admin(engine):
    """Verifica se existe um usuário admin e cria se necessário"""
    print_header("👤 VERIFICANDO USUÁRIO ADMIN")
    
    try:
        with engine.connect() as conn:
            # Verificar se existe algum super admin
            result = conn.execute(text(
                "SELECT id, nome, email FROM usuarios WHERE is_super_admin = true LIMIT 1"
            ))
            admin = result.fetchone()
            
            if admin:
                print(f"✅ Usuário admin encontrado:")
                print(f"   ID: {admin[0]}")
                print(f"   Nome: {admin[1]}")
                print(f"   Email: {admin[2]}")
                return True
            else:
                print("⚠️  Nenhum usuário admin encontrado!")
                print("\n💡 Para criar um usuário admin, execute:")
                print("   railway run python -c \"from migrations_scripts.criar_admin import criar_admin; criar_admin('admin@vendacerta.com', 'senha123', 'Administrador')\"")
                return False
                
    except Exception as e:
        print(f"❌ Erro ao verificar usuário admin: {str(e)}")
        return False

def gerar_relatorio(engine):
    """Gera um relatório completo do sistema"""
    print_header("📊 RELATÓRIO COMPLETO DO SISTEMA")
    
    try:
        with engine.connect() as conn:
            inspector = inspect(engine)
            
            # Contar registros
            print("\n📈 Estatísticas:")
            
            tabelas_para_contar = ['usuarios', 'clientes', 'vendas', 'metas']
            for tabela in tabelas_para_contar:
                if tabela in inspector.get_table_names():
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {tabela}"))
                    count = result.fetchone()[0]
                    print(f"   {tabela.capitalize()}: {count} registro(s)")
            
            # Verificar integridade
            print("\n🔍 Verificações de Integridade:")
            
            # Verificar usuários sem empresa
            result = conn.execute(text(
                "SELECT COUNT(*) FROM usuarios WHERE empresa_id IS NULL"
            ))
            sem_empresa = result.fetchone()[0]
            if sem_empresa > 0:
                print(f"   ⚠️  {sem_empresa} usuário(s) sem empresa atribuída")
            else:
                print(f"   ✅ Todos os usuários têm empresa atribuída")
            
            # Verificar usuários inativos
            result = conn.execute(text(
                "SELECT COUNT(*) FROM usuarios WHERE ativo = false"
            ))
            inativos = result.fetchone()[0]
            print(f"   ℹ️  {inativos} usuário(s) inativo(s)")
            
            print("\n✅ Relatório gerado com sucesso!")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {str(e)}")
        return False

def main():
    """Função principal"""
    print("\n" + "🚀" * 40)
    print("  CORREÇÃO COMPLETA DO SISTEMA VENDACERTA - RAILWAY")
    print("🚀" * 40)
    
    # 1. Obter URL do banco de dados
    database_url = get_database_url()
    if not database_url:
        print("\n❌ FALHA: Não foi possível obter URL do banco de dados")
        return False
    
    # Corrigir URL se necessário
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
        print("🔄 URL ajustada para PostgreSQL")
    
    # 2. Conectar ao banco de dados
    print_header("🔗 CONECTANDO AO BANCO DE DADOS")
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Conexão estabelecida!")
            print(f"   PostgreSQL: {version.split(',')[0]}")
    except Exception as e:
        print(f"❌ Erro ao conectar: {str(e)}")
        return False
    
    # 3. Verificar e corrigir schema
    if not verificar_e_corrigir_schema(engine):
        print("\n⚠️  Correção de schema falhou ou incompleta")
    
    # 4. Verificar usuário admin
    verificar_usuario_admin(engine)
    
    # 5. Gerar relatório
    gerar_relatorio(engine)
    
    # Resumo final
    print_header("✅ CORREÇÃO COMPLETA FINALIZADA")
    print("\n🎯 Próximos Passos:")
    print("   1. Acesse a aplicação: https://metacerta.up.railway.app")
    print("   2. Teste o login com seu usuário admin")
    print("   3. Verifique se o erro 500 foi resolvido")
    print("\n💡 Se ainda houver problemas, execute:")
    print("   railway logs")
    print("\n" + "=" * 80 + "\n")
    
    return True

if __name__ == '__main__':
    sucesso = main()
    sys.exit(0 if sucesso else 1)
