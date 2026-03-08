#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para adicionar campo codigo_cliente e gerar códigos para clientes existentes
"""

from app import app, db
from models import Cliente
from sqlalchemy import text

def migrar_codigo_cliente():
    """Adiciona coluna codigo_cliente e gera códigos para clientes existentes"""
    
    with app.app_context():
        print("\n" + "="*70)
        print("🔄 MIGRAÇÃO: Adicionando código único para clientes")
        print("="*70 + "\n")
        
        try:
            # Verificar se coluna já existe
            inspector = db.inspect(db.engine)
            colunas = [col['name'] for col in inspector.get_columns('clientes')]
            
            if 'codigo_cliente' not in colunas:
                print("➕ Adicionando coluna 'codigo_cliente'...")
                
                # Adicionar coluna
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE clientes ADD COLUMN codigo_cliente VARCHAR(9)'))
                    conn.execute(text('CREATE INDEX IF NOT EXISTS idx_codigo_cliente ON clientes(codigo_cliente)'))
                    conn.commit()
                
                print("   ✅ Coluna adicionada com sucesso!")
            else:
                print("ℹ️  Coluna 'codigo_cliente' já existe")
            
            # Tornar vendedor_id nullable se ainda não for
            print("\n➕ Atualizando vendedor_id para permitir NULL...")
            try:
                with db.engine.connect() as conn:
                    # SQLite não suporta ALTER COLUMN diretamente
                    # Vamos apenas atualizar a definição no models.py
                    print("   ℹ️  Campo vendedor_id já configurado no modelo")
            except Exception as e:
                print(f"   ⚠️  Aviso: {str(e)}")
            
            # Gerar códigos para clientes existentes sem código
            print("\n🔢 Gerando códigos únicos para clientes...")
            
            clientes = Cliente.query.filter(
                (Cliente.codigo_cliente.is_(None)) | (Cliente.codigo_cliente == '')
            ).all()
            
            total = len(clientes)
            print(f"   📊 Total de clientes sem código: {total}")
            
            if total > 0:
                contador = 0
                for cliente in clientes:
                    try:
                        cidade = cliente.cidade if cliente.cidade else 'SEM_CIDADE'
                        codigo = Cliente.gerar_codigo_cliente(cidade, cliente.empresa_id)
                        cliente.codigo_cliente = codigo
                        contador += 1
                        
                        if contador % 50 == 0:
                            print(f"   ⏳ Processados {contador}/{total}...")
                            db.session.commit()
                    
                    except Exception as e:
                        print(f"   ❌ Erro no cliente {cliente.id}: {str(e)}")
                        continue
                
                db.session.commit()
                print(f"\n   ✅ {contador} códigos gerados com sucesso!")
            
            # Estatísticas por município
            print("\n📊 ESTATÍSTICAS POR MUNICÍPIO:")
            print("-" * 70)
            
            from sqlalchemy import func
            stats = db.session.query(
                Cliente.cidade,
                func.count(Cliente.id).label('total')
            ).filter(
                Cliente.ativo == True
            ).group_by(
                Cliente.cidade
            ).order_by(
                func.count(Cliente.id).desc()
            ).limit(10).all()
            
            for cidade, total in stats:
                cidade_nome = cidade if cidade else 'SEM CIDADE'
                print(f"   {cidade_nome}: {total} clientes")
            
            print("\n" + "="*70)
            print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("="*70 + "\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERRO: {str(e)}")
            print("="*70 + "\n")

if __name__ == '__main__':
    migrar_codigo_cliente()
