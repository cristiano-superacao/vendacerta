"""
Script para recriar a tabela de clientes forçando a sincronização com o modelo
"""
import sqlite3
from app import app, db
from models import Cliente
from datetime import datetime

def recriar_tabela_clientes():
    print("\n" + "="*70)
    print("🔧 RECRIANDO TABELA DE CLIENTES")
    print("="*70)
    
    with app.app_context():
        conn = sqlite3.connect('instance/metas.db')
        cursor = conn.cursor()
        
        # Backup dos dados existentes
        print("\n📦 Fazendo backup dos dados...")
        cursor.execute("SELECT * FROM clientes")
        dados_antigos = cursor.fetchall()
        print(f"   ✅ {len(dados_antigos)} clientes salvos em memória")
        
        # Pega os nomes das colunas antigas
        cursor.execute("PRAGMA table_info(clientes)")
        colunas_antigas = {col[1]: col[0] for col in cursor.fetchall()}
        
        # Remove a tabela antiga
        print("\n🗑️  Removendo tabela antiga...")
        cursor.execute("DROP TABLE IF EXISTS clientes")
        conn.commit()
        print("   ✅ Tabela removida")
        
        conn.close()
        
        # Cria a nova tabela usando SQLAlchemy
        print("\n🏗️  Criando nova tabela com SQLAlchemy...")
        db.create_all()
        print("   ✅ Tabela criada com estrutura atualizada")
        
        # Verifica a nova estrutura
        conn = sqlite3.connect('instance/metas.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(clientes)")
        colunas_novas = cursor.fetchall()
        
        print(f"\n📊 Nova estrutura: {len(colunas_novas)} colunas")
        for col in colunas_novas:
            print(f"   {col[0]:2}. {col[1]:<25} {col[2]:<15}")
        
        # Restaura os dados (se houver)
        if dados_antigos:
            print(f"\n♻️  Restaurando {len(dados_antigos)} clientes...")
            
            # Mapeia colunas antigas para novas
            mapa_colunas = {}
            for nome_col, idx in colunas_antigas.items():
                if nome_col in [c[1] for c in colunas_novas]:
                    mapa_colunas[idx] = nome_col
            
            clientes_restaurados = 0
            for linha in dados_antigos:
                try:
                    # Cria dicionário com dados mapeados
                    dados = {}
                    for idx_antiga, nome_col in mapa_colunas.items():
                        if idx_antiga < len(linha):
                            dados[nome_col] = linha[idx_antiga]
                    
                    # Cria novo cliente
                    cliente = Cliente()
                    for campo, valor in dados.items():
                        if hasattr(cliente, campo) and campo != 'id':
                            setattr(cliente, campo, valor)
                    
                    # Garante valores padrão para novos campos
                    if not hasattr(cliente, 'logradouro') or not cliente.logradouro:
                        cliente.logradouro = None
                    if not hasattr(cliente, 'municipio') or not cliente.municipio:
                        cliente.municipio = cliente.cidade if hasattr(cliente, 'cidade') else None
                    if not hasattr(cliente, 'codigo_cliente') or not cliente.codigo_cliente:
                        cliente.codigo_cliente = None
                    
                    db.session.add(cliente)
                    clientes_restaurados += 1
                    
                except Exception as e:
                    print(f"   ⚠️  Erro ao restaurar cliente: {e}")
                    continue
            
            db.session.commit()
            print(f"   ✅ {clientes_restaurados} clientes restaurados com sucesso")
        
        conn.close()
        
        print("\n" + "="*70)
        print("✅ TABELA RECRIADA COM SUCESSO!")
        print("="*70)
        
        return True

if __name__ == '__main__':
    try:
        recriar_tabela_clientes()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
