#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick Start - Sistema VendaCerta PostgreSQL
Assistente interativo para configuração rápida
"""

import os
import sys
import subprocess

def print_header(texto, char="="):
    """Imprime cabeçalho formatado"""
    print("\n" + char * 70)
    print(f"  {texto}")
    print(char * 70)

def print_step(texto):
    """Imprime passo"""
    print(f"\n📋 {texto}")

def executar_comando(comando, descricao):
    """Executa comando e mostra resultado"""
    print(f"\n[PROC] {descricao}...")
    try:
        result = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print(f"[OK] {descricao} - Concluído!")
            return True
        else:
            print(f"[ERRO] {descricao} - Erro!")
            if result.stderr:
                print(f"   {result.stderr[:200]}")
            return False
    
    except subprocess.TimeoutExpired:
        print(f"[TIME] {descricao} - Timeout!")
        return False
    except Exception as e:
        print(f"[ERRO] {descricao} - Erro: {e}")
        return False

def verificar_sqlite():
    """Verifica se existe banco SQLite com dados"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    sqlite_path = os.path.join(basedir, 'instance', 'vendacerta.db')
    
    if os.path.exists(sqlite_path):
        tamanho = os.path.getsize(sqlite_path)
        if tamanho > 10000:  # Mais de 10KB = tem dados
            return True, tamanho
    
    return False, 0

def menu_principal():
    """Menu principal"""
    print_header("🚀 SISTEMA VENDACERTA - QUICK START", "=")
    
    print("\n📦 O que você deseja fazer?\n")
    print("[1]  Executar sistema com SQLite (rápido, sem configuração)")
    print("[2]  Verificar se PostgreSQL está instalado")
    print("[3]  Configurar PostgreSQL do zero")
    print("[4]  Migrar dados do SQLite para PostgreSQL")
    print("[5]  Executar sistema com PostgreSQL")
    print("[6]  Ajuda e documentação")
    print("[0]  Sair")
    
    return input("\n🤔 Escolha uma opção: ").strip()

def opcao_1_sqlite():
    """Executa com SQLite"""
    print_header("EXECUTANDO COM SQLITE", "-")
    
    print("\n✨ Vantagens do SQLite:")
    print("   • Zero configuração necessária")
    print("   • Perfeito para desenvolvimento")
    print("   • Backup simples (copiar arquivo)")
    print("   • Rápido para pequenos volumes")
    
    resposta = input("\n🤔 Deseja iniciar o sistema agora? [S/n]: ")
    if resposta.lower() != 'n':
        print("\n🚀 Iniciando sistema...")
        print("📌 Acesse: http://127.0.0.1:5001/login")
        print("📧 Email: admin@vendacerta.com")
        print("🔑 Senha: admin123")
        print("\n[KEY]  Pressione Ctrl+C para parar\n")
        
        try:
            subprocess.run(['python', 'app.py'])
        except KeyboardInterrupt:
            print("\n\n[OK] Sistema encerrado!")

def opcao_2_verificar():
    """Verifica PostgreSQL"""
    print_header("VERIFICANDO POSTGRESQL", "-")
    executar_comando('python test_postgresql.py', 'Verificação PostgreSQL')

def opcao_3_configurar():
    """Configura PostgreSQL"""
    print_header("CONFIGURANDO POSTGRESQL", "-")
    
    print("\n📋 Este processo irá:")
    print("   1. Conectar ao PostgreSQL como administrador")
    print("   2. Criar banco de dados 'vendacerta_db'")
    print("   3. Criar usuário 'vendacerta_user'")
    print("   4. Configurar permissões")
    print("   5. Atualizar arquivo .env")
    print("   6. Testar conexão")
    
    print("\n[AVISO]  Você precisará:")
    print("   • PostgreSQL instalado no sistema")
    print("   • Senha do usuário 'postgres'")
    
    resposta = input("\n🤔 Deseja continuar? [s/N]: ")
    if resposta.lower() == 's':
        executar_comando('python setup_postgresql.py', 'Configuração PostgreSQL')

def opcao_4_migrar():
    """Migra dados"""
    print_header("MIGRANDO DADOS SQLITE → POSTGRESQL", "-")
    
    tem_dados, tamanho = verificar_sqlite()
    
    if not tem_dados:
        print("\n[AVISO]  Nenhum banco SQLite com dados foi encontrado.")
        print("   Se você ainda não tem dados, pode pular este passo.")
        
        resposta = input("\n🤔 Deseja continuar mesmo assim? [s/N]: ")
        if resposta.lower() != 's':
            return
    else:
        print(f"\n[OK] Banco SQLite encontrado ({tamanho:,} bytes)")
    
    print("\n📋 Este processo irá:")
    print("   1. Fazer backup do SQLite")
    print("   2. Criar estrutura no PostgreSQL")
    print("   3. Migrar todos os dados")
    print("   4. Gerar relatório")
    
    print("\n[AVISO]  Pré-requisitos:")
    print("   • PostgreSQL configurado (opção 3)")
    print("   • Arquivo .env com DATABASE_URL")
    
    resposta = input("\n🤔 Deseja continuar? [s/N]: ")
    if resposta.lower() == 's':
        executar_comando('python migrate_to_postgresql.py', 'Migração de dados')

def opcao_5_executar_pg():
    """Executa com PostgreSQL"""
    print_header("EXECUTANDO COM POSTGRESQL", "-")
    
    # Verifica se .env tem DATABASE_URL
    if not os.path.exists('.env'):
        print("\n[ERRO] Arquivo .env não encontrado!")
        print("   Execute primeiro a opção 3 (Configurar PostgreSQL)")
        input("\n⏎ Pressione Enter para continuar...")
        return
    
    with open('.env', 'r', encoding='utf-8') as f:
        env_content = f.read()
    
    if 'DATABASE_URL=postgresql' not in env_content:
        print("\n[AVISO]  DATABASE_URL não está configurado para PostgreSQL no .env")
        print("   Execute primeiro a opção 3 (Configurar PostgreSQL)")
        
        resposta = input("\n🤔 Deseja continuar mesmo assim? [s/N]: ")
        if resposta.lower() != 's':
            return
    
    print("\n✨ Vantagens do PostgreSQL:")
    print("   • Escalabilidade ilimitada")
    print("   • Concorrência real")
    print("   • Recursos avançados")
    print("   • Pronto para produção")
    
    resposta = input("\n🤔 Deseja iniciar o sistema agora? [S/n]: ")
    if resposta.lower() != 'n':
        print("\n🚀 Iniciando sistema...")
        print("📌 Acesse: http://127.0.0.1:5001/login")
        print("📧 Email: admin@vendacerta.com")
        print("🔑 Senha: admin123")
        print("\n[KEY]  Pressione Ctrl+C para parar\n")
        
        try:
            subprocess.run(['python', 'app.py'])
        except KeyboardInterrupt:
            print("\n\n[OK] Sistema encerrado!")

def opcao_6_ajuda():
    """Mostra ajuda"""
    print_header("DOCUMENTAÇÃO E AJUDA", "-")
    
    print("\n📚 Documentação disponível:\n")
    print("1. CONFIGURACAO_POSTGRESQL.md - Resumo executivo")
    print("2. GUIA_POSTGRESQL.md - Guia completo detalhado")
    print("3. README_POSTGRESQL.md - Referência rápida")
    
    print("\n🔧 Scripts disponíveis:\n")
    print("• test_postgresql.py - Testa instalação PostgreSQL")
    print("• setup_postgresql.py - Configura banco e usuário")
    print("• migrate_to_postgresql.py - Migra dados")
    print("• quick_start.py - Este assistente")
    
    print("\n💡 Dicas:\n")
    print("SQLite:")
    print("  → Bom para: desenvolvimento, testes, pequenos volumes")
    print("  → Não precisa: instalação, configuração")
    print("  → Execute: python app.py")
    
    print("\nPostgreSQL:")
    print("  → Bom para: produção, grandes volumes, múltiplos usuários")
    print("  → Precisa: PostgreSQL instalado, configuração inicial")
    print("  → Passos: Opção 2 → 3 → 4 → 5")
    
    print("\n🆘 Troubleshooting:\n")
    print("• Erro de conexão PostgreSQL:")
    print("  → Verifique se o serviço está rodando")
    print("  → Windows: Get-Service postgresql*")
    print("  → Linux: sudo systemctl status postgresql")
    
    print("\n• PostgreSQL não instalado:")
    print("  → Windows: https://www.postgresql.org/download/windows/")
    print("  → Linux: sudo apt install postgresql")
    print("  → macOS: brew install postgresql@16")
    
    input("\n⏎ Pressione Enter para continuar...")

def main():
    """Função principal"""
    while True:
        try:
            opcao = menu_principal()
            
            if opcao == '0':
                print("\n👋 Até logo!\n")
                sys.exit(0)
            
            elif opcao == '1':
                opcao_1_sqlite()
            
            elif opcao == '2':
                opcao_2_verificar()
            
            elif opcao == '3':
                opcao_3_configurar()
            
            elif opcao == '4':
                opcao_4_migrar()
            
            elif opcao == '5':
                opcao_5_executar_pg()
            
            elif opcao == '6':
                opcao_6_ajuda()
            
            else:
                print("\n[ERRO] Opção inválida!")
            
            input("\n⏎ Pressione Enter para continuar...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!\n")
            sys.exit(0)
        
        except Exception as e:
            print(f"\n[ERRO] Erro: {e}")
            input("\n⏎ Pressione Enter para continuar...")

if __name__ == '__main__':
    main()
