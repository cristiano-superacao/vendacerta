#!/usr/bin/env python3
"""
Script para verificar variáveis de ambiente necessárias no Railway
"""
import os
import sys

def check_environment_variables():
    """Verifica se todas as variáveis de ambiente necessárias estão configuradas"""
    print("\n" + "=" * 70)
    print("🔍 VERIFICAÇÃO DE VARIÁVEIS DE AMBIENTE - RAILWAY")
    print("=" * 70 + "\n")
    
    required_vars = {
        'DATABASE_URL': 'URL de conexão do PostgreSQL (fornecida automaticamente)',
        'FLASK_SECRET_KEY': 'Chave secreta do Flask (32+ caracteres)',
        'PORT': 'Porta do servidor (fornecida automaticamente)',
    }
    
    optional_vars = {
        'FLASK_ENV': 'Ambiente do Flask (production)',
        'FLASK_DEBUG': 'Debug do Flask (False)',
        'RAILWAY_ENVIRONMENT': 'Ambiente Railway (fornecido automaticamente)',
    }
    
    all_ok = True
    
    print("📋 VARIÁVEIS OBRIGATÓRIAS:\n")
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            # Ocultar valores sensíveis
            if var in ['DATABASE_URL', 'FLASK_SECRET_KEY']:
                display_value = value[:10] + "..." + value[-10:] if len(value) > 20 else "***"
            else:
                display_value = value
            print(f"  ✅ {var}")
            print(f"     {description}")
            print(f"     Valor: {display_value}\n")
        else:
            print(f"  ❌ {var} - NÃO CONFIGURADA")
            print(f"     {description}\n")
            all_ok = False
    
    print("\n📋 VARIÁVEIS OPCIONAIS:\n")
    for var, description in optional_vars.items():
        value = os.environ.get(var)
        if value:
            print(f"  ✅ {var} = {value}")
            print(f"     {description}\n")
        else:
            print(f"  ⚠️  {var} - não configurada")
            print(f"     {description}\n")
    
    print("=" * 70)
    
    if all_ok:
        print("✅ TODAS AS VARIÁVEIS OBRIGATÓRIAS ESTÃO CONFIGURADAS")
        print("=" * 70 + "\n")
        return 0
    else:
        print("❌ FALTAM VARIÁVEIS OBRIGATÓRIAS")
        print("\n📝 COMO CONFIGURAR NO RAILWAY:")
        print("   1. Acesse o painel do Railway (railway.app)")
        print("   2. Selecione seu projeto")
        print("   3. Vá em 'Variables'")
        print("   4. Adicione as variáveis faltantes")
        print("   5. Faça o redeploy do projeto")
        print("\n💡 DICA: Para gerar FLASK_SECRET_KEY:")
        print("   python -c \"import secrets; print(secrets.token_hex(32))\"")
        print("=" * 70 + "\n")
        return 1

if __name__ == '__main__':
    sys.exit(check_environment_variables())
