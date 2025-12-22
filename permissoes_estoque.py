"""
Sistema de Hierarquia de Permissões para Movimentação de Estoque

Define quais motivos de movimentação cada cargo/função pode acessar.
"""

# Hierarquia de permissões por cargo
PERMISSOES_MOTIVO_ESTOQUE = {
    'admin': {
        'entrada': ['compra', 'devolucao', 'ajuste', 'manutencao', 'consumo_interno', 'outro'],
        'saida': ['venda', 'devolucao', 'ajuste', 'manutencao', 'consumo_interno', 'perda', 'outro']
    },
    'gerente': {
        'entrada': ['compra', 'devolucao', 'ajuste', 'manutencao', 'consumo_interno', 'outro'],
        'saida': ['venda', 'devolucao', 'ajuste', 'manutencao', 'consumo_interno', 'perda', 'outro']
    },
    'supervisor': {
        'entrada': ['compra', 'devolucao', 'ajuste', 'outro'],
        'saida': ['venda', 'devolucao', 'ajuste', 'manutencao', 'consumo_interno', 'outro']
    },
    'vendedor': {
        'entrada': ['devolucao'],
        'saida': ['venda']
    },
    'tecnico': {
        'entrada': ['devolucao'],
        'saida': ['manutencao', 'consumo_interno']
    },
    'financeiro': {
        'entrada': ['compra', 'devolucao', 'ajuste'],
        'saida': ['venda', 'devolucao', 'ajuste', 'perda']
    },
    'rh': {
        'entrada': ['compra', 'outro'],
        'saida': ['consumo_interno', 'outro']
    },
    'usuario': {
        'entrada': ['devolucao'],
        'saida': ['consumo_interno']
    }
}

# Mapeamento de motivos (código -> nome)
MOTIVOS_DESCRICAO = {
    'compra': 'Compra',
    'venda': 'Venda',
    'devolucao': 'Devolução',
    'ajuste': 'Ajuste de Inventário',
    'manutencao': 'Manutenção/OS',
    'consumo_interno': 'Consumo Interno',
    'perda': 'Perda/Avaria',
    'outro': 'Outro'
}

def get_motivos_permitidos(cargo, tipo_movimento='entrada'):
    """
    Retorna lista de motivos permitidos para um cargo específico
    
    Args:
        cargo: Cargo do usuário (admin, gerente, vendedor, etc)
        tipo_movimento: 'entrada' ou 'saida'
    
    Returns:
        Lista de tuplas (código, descrição) dos motivos permitidos
    """
    cargo_lower = cargo.lower() if cargo else 'usuario'
    
    # Se o cargo não estiver mapeado, usar permissões de 'usuario'
    if cargo_lower not in PERMISSOES_MOTIVO_ESTOQUE:
        cargo_lower = 'usuario'
    
    motivos_permitidos = PERMISSOES_MOTIVO_ESTOQUE.get(cargo_lower, {}).get(tipo_movimento, [])
    
    # Retornar lista de tuplas (código, descrição)
    return [(m, MOTIVOS_DESCRICAO[m]) for m in motivos_permitidos]


def usuario_pode_usar_motivo(cargo, tipo_movimento, motivo):
    """
    Verifica se um usuário pode usar determinado motivo
    
    Args:
        cargo: Cargo do usuário
        tipo_movimento: 'entrada' ou 'saida'
        motivo: Código do motivo (ex: 'compra', 'venda')
    
    Returns:
        Boolean indicando se o usuário pode usar o motivo
    """
    cargo_lower = cargo.lower() if cargo else 'usuario'
    
    if cargo_lower not in PERMISSOES_MOTIVO_ESTOQUE:
        cargo_lower = 'usuario'
    
    motivos_permitidos = PERMISSOES_MOTIVO_ESTOQUE.get(cargo_lower, {}).get(tipo_movimento, [])
    
    return motivo in motivos_permitidos


# Resumo das permissões por cargo
"""
RESUMO DAS PERMISSÕES:

👨‍💼 ADMIN / GERENTE:
   ✅ Entrada: Compra, Devolução, Ajuste, Manutenção, Consumo Interno, Outro
   ✅ Saída: Venda, Devolução, Ajuste, Manutenção, Consumo Interno, Perda, Outro

👤 SUPERVISOR:
   ✅ Entrada: Compra, Devolução, Ajuste, Outro
   ✅ Saída: Venda, Devolução, Ajuste, Manutenção, Consumo Interno, Outro

💰 VENDEDOR:
   ✅ Entrada: Devolução
   ✅ Saída: Venda

🔧 TÉCNICO:
   ✅ Entrada: Devolução
   ✅ Saída: Manutenção/OS, Consumo Interno

💵 FINANCEIRO:
   ✅ Entrada: Compra, Devolução, Ajuste
   ✅ Saída: Venda, Devolução, Ajuste, Perda

👥 RH:
   ✅ Entrada: Compra, Outro
   ✅ Saída: Consumo Interno, Outro

📝 USUÁRIO PADRÃO:
   ✅ Entrada: Devolução
   ✅ Saída: Consumo Interno
"""
