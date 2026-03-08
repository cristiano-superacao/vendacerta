#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste de geração de código de cliente sob concorrência simulada.
Verifica se há duplicidades ao gerar múltiplos códigos simultaneamente.
"""

import os, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, db
from models import Cliente


def gerar_codigo_thread(thread_id, empresa_id):
    """Gera código em thread separada"""
    try:
        with app.app_context():
            codigo = Cliente.gerar_codigo_cliente('TesteCidade', empresa_id)
            return (thread_id, codigo, None)
    except Exception as e:
        return (thread_id, None, str(e))


def main():
    print("\n" + "="*70)
    print("🧪 TESTE: Geração concorrente de códigos de cliente")
    print("="*70 + "\n")
    
    empresa_id = 1
    num_threads = 20
    
    print(f"Iniciando {num_threads} threads para gerar códigos simultaneamente...")
    print(f"Empresa ID: {empresa_id}\n")
    
    codigos_gerados = []
    erros = []
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(gerar_codigo_thread, i, empresa_id)
            for i in range(num_threads)
        ]
        
        for future in as_completed(futures):
            thread_id, codigo, erro = future.result()
            if codigo:
                codigos_gerados.append(codigo)
                print(f"✓ Thread {thread_id:2d}: {codigo}")
            else:
                erros.append((thread_id, erro))
                print(f"✗ Thread {thread_id:2d}: ERRO - {erro}")
    
    print("\n" + "-"*70)
    print("📊 RESULTADOS:")
    print("-"*70)
    print(f"Total de códigos gerados: {len(codigos_gerados)}")
    print(f"Total de erros: {len(erros)}")
    
    # Verificar duplicidades
    duplicados = [c for c in codigos_gerados if codigos_gerados.count(c) > 1]
    if duplicados:
        print(f"\n❌ FALHA: {len(set(duplicados))} códigos duplicados encontrados:")
        for cod in set(duplicados):
            count = codigos_gerados.count(cod)
            print(f"   - {cod}: {count}x")
    else:
        print("\n✅ SUCESSO: Nenhum código duplicado!")
    
    # Mostrar amostra dos códigos
    if codigos_gerados:
        print(f"\nAmostra de códigos gerados (primeiros 10):")
        for cod in sorted(set(codigos_gerados))[:10]:
            print(f"   - {cod}")
    
    print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    main()
