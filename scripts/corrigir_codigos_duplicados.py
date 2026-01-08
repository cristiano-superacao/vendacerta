#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para corrigir códigos de clientes duplicados no banco de dados
"""

from app import app, db
from models import Cliente
from sqlalchemy import func
import sys

def encontrar_duplicados():
    """Encontra códigos de clientes duplicados"""
    with app.app_context():
        print("\n" + "="*70)
        print("🔍 PROCURANDO CÓDIGOS DUPLICADOS")
        print("="*70 + "\n")
        
        # Buscar códigos duplicados
        duplicados = db.session.query(
            Cliente.codigo_cliente,
            Cliente.empresa_id,
            func.count(Cliente.id).label('total')
        ).filter(
            Cliente.codigo_cliente.isnot(None),
            Cliente.codigo_cliente != ''
        ).group_by(
            Cliente.codigo_cliente,
            Cliente.empresa_id
        ).having(
            func.count(Cliente.id) > 1
        ).all()
        
        if not duplicados:
            print("✅ Nenhum código duplicado encontrado!")
            print("="*70 + "\n")
            return []
        
        print(f"⚠️  Encontrados {len(duplicados)} códigos duplicados:\n")
        
        for codigo, empresa_id, total in duplicados:
            print(f"  Código: {codigo} (Empresa {empresa_id}) - {total} clientes")
            clientes = Cliente.query.filter_by(
                codigo_cliente=codigo,
                empresa_id=empresa_id
            ).all()
            for c in clientes:
                print(f"    - ID {c.id}: {c.nome} ({c.cidade or 'SEM CIDADE'})")
        
        print("\n" + "="*70 + "\n")
        return duplicados


def corrigir_duplicados():
    """Corrige códigos duplicados gerando novos códigos"""
    with app.app_context():
        duplicados = encontrar_duplicados()
        
        if not duplicados:
            return True
        
        print("🔧 INICIANDO CORREÇÃO")
        print("="*70 + "\n")
        
        total_corrigidos = 0
        
        try:
            for codigo, empresa_id, total in duplicados:
                print(f"\n📝 Processando código duplicado: {codigo} (Empresa {empresa_id})")
                
                # Buscar todos os clientes com este código
                clientes = Cliente.query.filter_by(
                    codigo_cliente=codigo,
                    empresa_id=empresa_id
                ).order_by(Cliente.id).all()
                
                # Manter o primeiro, regerar código para os demais
                primeiro = True
                for cliente in clientes:
                    if primeiro:
                        print(f"  ✓ Mantendo ID {cliente.id}: {cliente.nome}")
                        primeiro = False
                        continue
                    
                    # Gerar novo código
                    cidade = cliente.cidade or cliente.municipio or 'SEM_CIDADE'
                    tentativas = 0
                    max_tentativas = 10
                    novo_codigo = None
                    
                    while tentativas < max_tentativas:
                        try:
                            novo_codigo = Cliente.gerar_codigo_cliente(cidade, empresa_id)
                            
                            # Verificar se o novo código já existe
                            existente = Cliente.query.filter_by(
                                codigo_cliente=novo_codigo,
                                empresa_id=empresa_id
                            ).first()
                            
                            if not existente:
                                break  # Código único encontrado!
                            
                            tentativas += 1
                            import time
                            time.sleep(0.05)
                        except Exception as e:
                            print(f"    ⚠️  Erro na tentativa {tentativas + 1}: {str(e)}")
                            tentativas += 1
                    
                    if novo_codigo and not existente:
                        cliente.codigo_cliente = novo_codigo
                        print(f"  ✓ ID {cliente.id}: {cliente.nome} -> novo código: {novo_codigo}")
                        total_corrigidos += 1
                    else:
                        print(f"  ❌ Falha ao gerar código único para ID {cliente.id}: {cliente.nome}")
            
            # Commit das alterações
            db.session.commit()
            
            print("\n" + "="*70)
            print(f"✅ CORREÇÃO CONCLUÍDA: {total_corrigidos} clientes corrigidos!")
            print("="*70 + "\n")
            
            # Verificar se ainda há duplicados
            print("🔍 Verificando se ainda há duplicados...")
            restantes = encontrar_duplicados()
            
            if not restantes:
                print("✅ Todos os códigos duplicados foram corrigidos!")
                return True
            else:
                print(f"⚠️  Ainda restam {len(restantes)} códigos duplicados.")
                print("Execute o script novamente para tentar corrigi-los.")
                return False
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERRO: {str(e)}")
            print("="*70 + "\n")
            return False


def verificar_integridade():
    """Verifica a integridade dos códigos de clientes"""
    with app.app_context():
        print("\n" + "="*70)
        print("🔍 VERIFICANDO INTEGRIDADE DOS CÓDIGOS")
        print("="*70 + "\n")
        
        # Contar clientes sem código
        sem_codigo = Cliente.query.filter(
            (Cliente.codigo_cliente.is_(None)) | (Cliente.codigo_cliente == '')
        ).count()
        
        if sem_codigo > 0:
            print(f"⚠️  {sem_codigo} clientes sem código de cliente")
        else:
            print("✅ Todos os clientes possuem código")
        
        # Contar códigos inválidos (não seguem padrão XXXX-XXXX)
        import re
        clientes = Cliente.query.filter(
            Cliente.codigo_cliente.isnot(None),
            Cliente.codigo_cliente != ''
        ).all()
        
        invalidos = 0
        for c in clientes:
            if not re.match(r'^\d{4}-\d{4}$', c.codigo_cliente):
                print(f"  ⚠️  Código inválido: {c.codigo_cliente} (ID {c.id}: {c.nome})")
                invalidos += 1
        
        if invalidos > 0:
            print(f"\n⚠️  {invalidos} códigos com formato inválido")
        else:
            print("✅ Todos os códigos seguem o padrão correto")
        
        print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🔧 CORRETOR DE CÓDIGOS DUPLICADOS")
    print("="*70 + "\n")
    
    print("Escolha uma opção:")
    print("  1. Verificar duplicados")
    print("  2. Corrigir duplicados")
    print("  3. Verificar integridade")
    print("  4. Executar tudo")
    print()
    
    if len(sys.argv) > 1:
        opcao = sys.argv[1]
    else:
        opcao = input("Digite a opção (1-4): ").strip()
    
    if opcao == "1":
        encontrar_duplicados()
    elif opcao == "2":
        corrigir_duplicados()
    elif opcao == "3":
        verificar_integridade()
    elif opcao == "4":
        encontrar_duplicados()
        if corrigir_duplicados():
            verificar_integridade()
    else:
        print("❌ Opção inválida!")
        sys.exit(1)
    
    print("✅ Script concluído!")
