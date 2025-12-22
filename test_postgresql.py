#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Teste PostgreSQL - Sistema VendaCerta
Verifica se o PostgreSQL está instalado e acessível
"""

import sys
import subprocess

def print_header(texto):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f"  {texto}")
    print("=" * 70)

def verificar_psycopg2():
    """Verifica se psycopg2 está instalado"""
    try:
        import psycopg2
        print(f"[OK] psycopg2-binary instalado - Versão: {psycopg2.__version__}")
        return True
    except ImportError:
        print("[ERRO] psycopg2-binary não instalado")
        print("   Execute: pip install psycopg2-binary")
        return False

def verificar_postgresql_instalado():
    """Verifica se PostgreSQL está instalado no sistema"""
    try:
        # Tenta executar psql --version
        result = subprocess.run(
            ['psql', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            versao = result.stdout.strip()
            print(f"[OK] PostgreSQL instalado - {versao}")
            return True
        else:
            print("[ERRO] PostgreSQL não encontrado no PATH")
            return False
    
    except FileNotFoundError:
        print("[ERRO] PostgreSQL não instalado ou não está no PATH")
        print("\n📥 Para instalar PostgreSQL:")
        print("   Windows: https://www.postgresql.org/download/windows/")
        print("   Linux: sudo apt install postgresql")
        print("   macOS: brew install postgresql@16")
        return False
    
    except Exception as e:
        print(f"[AVISO]  Erro ao verificar PostgreSQL: {e}")
        return False

def verificar_servico_rodando():
    """Verifica se o serviço PostgreSQL está rodando"""
    try:
        # Tenta listar serviços do PostgreSQL no Windows
        result = subprocess.run(
            ['powershell', '-Command', 'Get-Service postgresql*'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if 'Running' in result.stdout:
            print("[OK] Serviço PostgreSQL está rodando")
            return True
        else:
            print("[AVISO]  Serviço PostgreSQL não está rodando")
            print("   Execute: Start-Service postgresql-x64-16")
            return False
    
    except Exception:
        # Em Linux/macOS ou se PowerShell falhar
        try:
            # Tenta conectar na porta 5432
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', 5432))
            sock.close()
            
            if result == 0:
                print("[OK] PostgreSQL está escutando na porta 5432")
                return True
            else:
                print("[AVISO]  PostgreSQL não está escutando na porta 5432")
                print("   O serviço pode não estar rodando")
                return False
        
        except Exception as e:
            print(f"[AVISO]  Não foi possível verificar o serviço: {e}")
            return False

def testar_conexao():
    """Testa conexão com PostgreSQL"""
    try:
        import psycopg2
        
        print("\n[PROC] Tentando conectar ao PostgreSQL...")
        print("   (Você precisará fornecer a senha do usuário 'postgres')")
        
        import getpass
        senha = getpass.getpass("Digite a senha do usuário 'postgres': ")
        
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password=senha,
            database='postgres'
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        versao = cursor.fetchone()[0]
        
        print(f"\n[OK] Conexão bem-sucedida!")
        print(f"[INFO] Versão completa: {versao}")
        
        cursor.close()
        conn.close()
        
        return True
    
    except Exception as e:
        print(f"\n[ERRO] Erro ao conectar: {e}")
        return False

def main():
    """Função principal"""
    print_header("VERIFICAÇÃO POSTGRESQL - SISTEMA VENDACERTA")
    
    print("\n🔍 Verificando componentes...")
    
    # Verificações
    checks = []
    
    print("\n[1/4] Verificando psycopg2...")
    checks.append(verificar_psycopg2())
    
    print("\n[2/4] Verificando PostgreSQL instalado...")
    checks.append(verificar_postgresql_instalado())
    
    print("\n[3/4] Verificando serviço PostgreSQL...")
    checks.append(verificar_servico_rodando())
    
    # Resumo
    print_header("RESUMO DA VERIFICAÇÃO")
    
    if all(checks[:3]):
        print("\n[OK] Todos os componentes estão OK!")
        print("\n🔧 Próximo passo:")
        print("   Execute: python setup_postgresql.py")
        
        resposta = input("\n🤔 Deseja testar a conexão agora? [s/N]: ")
        if resposta.lower() == 's':
            print("\n[4/4] Testando conexão...")
            if testar_conexao():
                print("\n[OK] Tudo pronto para configurar o banco!")
                print("   Execute: python setup_postgresql.py")
    else:
        print("\n[AVISO]  Alguns componentes precisam ser configurados:")
        
        if not checks[0]:
            print("\n   • Instale psycopg2-binary:")
            print("     pip install psycopg2-binary")
        
        if not checks[1]:
            print("\n   • Instale PostgreSQL:")
            print("     https://www.postgresql.org/download/")
        
        if not checks[2]:
            print("\n   • Inicie o serviço PostgreSQL")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
