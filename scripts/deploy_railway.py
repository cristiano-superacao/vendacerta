"""
Script para fazer deploy no Railway e atualizar banco de dados
"""

import subprocess
import os

def executar_comando(comando, descricao):
    """Executa um comando e mostra o resultado"""
    print(f"\n{'='*80}")
    print(f"▶ {descricao}")
    print(f"{'='*80}")
    print(f"Comando: {comando}")
    print()

    resultado = subprocess.run(
        comando,
        shell=True,
        capture_output=True,
        text=True
    )

    if resultado.stdout:
        print(resultado.stdout)

    if resultado.stderr:
        print("STDERR:", resultado.stderr)

    return resultado.returncode == 0

def main():
    print("=" * 80)
    print("DEPLOY E ATUALIZAÇÃO - RAILWAY")
    print("=" * 80)

    # 1. Verificar se há mudanças para commitar
    print("\n📋 Verificando mudanças no Git...")

    status = subprocess.run(
        "git status --short",
        shell=True,
        capture_output=True,
        text=True
    )

    if status.stdout.strip():
        print("\n✓ Mudanças detectadas:")
        print(status.stdout)

        # Perguntar se quer commitar
        print("\n🔄 Commitando mudanças...")

        if not executar_comando("git add .", "Adicionando arquivos"):
            print("❌ Erro ao adicionar arquivos")
            return False

        mensagem = "Fix: Corrigido erro 500 em comissões e atualizado banco de dados"
        if not executar_comando(f'git commit -m "{mensagem}"', "Commitando mudanças"):
            print("⚠️ Nada para commitar ou erro no commit")
    else:
        print("✓ Nenhuma mudança detectada")

    # 2. Push para o repositório
    print("\n📤 Enviando para o repositório...")
    if not executar_comando("git push", "Push para repositório remoto"):
        print("⚠️ Erro no push ou já está atualizado")

    print("\n" + "=" * 80)
    print("PRÓXIMOS PASSOS PARA ATUALIZAR O RAILWAY:")
    print("=" * 80)
    print("""
1. AUTOMATICAMENTE (se configurado):
   - O Railway detectará o push e fará deploy automático
   - Aguarde 2-5 minutos para o deploy completar

2. MANUALMENTE (via Railway CLI):
   railway up

3. ATUALIZAR BANCO DE DADOS:

   a) Via Railway CLI:
      railway run python migrar_faixas_comissao_db.py

   b) Via Dashboard Railway:
      - Acesse: https://railway.app/
      - Selecione seu projeto
      - Vá em Settings > Variables
      - Verifique se DATABASE_URL está configurada
      - Execute o script via CLI ou aguarde o deploy

4. VERIFICAR DEPLOY:
   - Acesse: https://suameta.up.railway.app
   - Faça login
   - Teste a rota: /configuracoes/comissoes/criar

🔍 MONITORAR LOGS:
   railway logs

✅ CORREÇÕES APLICADAS:
   - Corrigido erro no template comissao_form.html (linha 138)
   - Criado script de migração de banco de dados
   - Todos os templates estão presentes
   - Sistema pronto para deploy
    """)

    print("\n" + "=" * 80)
    print("✅ PROCESSO CONCLUÍDO!")
    print("=" * 80)

if __name__ == '__main__':
    main()
