"""
Script para verificar e atualizar template de vendedores
"""
import pandas as pd
import os

# Caminho do template
template_path = os.path.join('static', 'templates_excel', 'template_vendedores.xlsx')

# Verificar se existe
if os.path.exists(template_path):
    print(f"✅ Template encontrado: {template_path}")

    # Ler template
    df = pd.read_excel(template_path)

    print(f"\n📋 Colunas atuais do template:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. '{col}'")

    # Verificar colunas obrigatórias
    colunas_obrigatorias = ['Nome', 'Email', 'Telefone', 'CPF']
    colunas_faltando = [col for col in colunas_obrigatorias if col not in df.columns]

    if colunas_faltando:
        print(f"\n❌ Colunas obrigatórias faltando: {colunas_faltando}")
    else:
        print(f"\n✅ Todas as colunas obrigatórias presentes!")

    # Verificar colunas opcionais
    colunas_opcionais = ['Supervisor Email', 'Equipe Nome']
    print(f"\n📝 Colunas opcionais:")
    for col in colunas_opcionais:
        status = "✅" if col in df.columns else "❌"
        print(f"  {status} {col}")

    print(f"\n📊 Total de linhas de exemplo: {len(df)}")

else:
    print(f"❌ Template não encontrado: {template_path}")
    print("\n🔧 Criando novo template...")

    # Criar DataFrame com estrutura correta
    df = pd.DataFrame({
        'Nome': ['João Silva', 'Maria Santos'],
        'Email': ['joao@exemplo.com', 'maria@exemplo.com'],
        'Telefone': ['71999999999', '71988888888'],
        'CPF': ['123.456.789-00', '987.654.321-00'],
        'Supervisor Email': ['supervisor@empresa.com', 'supervisor@empresa.com'],
        'Equipe Nome': ['Equipe A', 'Equipe B']
    })

    # Criar diretório se não existir
    os.makedirs(os.path.dirname(template_path), exist_ok=True)

    # Salvar template
    df.to_excel(template_path, index=False)
    print(f"✅ Template criado: {template_path}")
