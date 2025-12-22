
import sys
import os

# Adicionar diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Cliente
from sqlalchemy import func

def corrigir_codigos():
    with app.app_context():
        print("Iniciando correção de códigos de clientes...")
        
        # 1. Obter todas as empresas
        # Se empresa_id for None, vamos assumir empresa 1 ou tratar como global
        # Mas o sistema é multi-empresa. Vamos ver se existem clientes com empresa_id NULL
        clientes_sem_empresa = Cliente.query.filter(Cliente.empresa_id.is_(None)).count()
        if clientes_sem_empresa > 0:
            print(f"⚠️  Encontrados {clientes_sem_empresa} clientes sem empresa definida. Atribuindo à empresa padrão (1).")
            Cliente.query.filter(Cliente.empresa_id.is_(None)).update({Cliente.empresa_id: 1}, synchronize_session=False)
            db.session.commit()
            
        empresas_ids = db.session.query(Cliente.empresa_id).distinct().all()
        empresas_ids = [e[0] for e in empresas_ids if e[0] is not None]
        
        if not empresas_ids:
            print("Nenhuma empresa encontrada com clientes.")
            # Tentar pegar empresas da tabela Usuario se não houver clientes
            from models import Usuario
            empresas_ids = db.session.query(Usuario.empresa_id).distinct().all()
            empresas_ids = [e[0] for e in empresas_ids if e[0] is not None]
            print(f"Empresas encontradas via Usuários: {empresas_ids}")

        for empresa_id in empresas_ids:
            print(f"\nProcessando Empresa ID: {empresa_id}")
            
            # 2. Agrupar clientes por cidade (normalizada)
            # Pegar todos os clientes da empresa
            clientes = Cliente.query.filter_by(empresa_id=empresa_id).all()
            
            cidades_map = {}
            sem_cidade = []
            
            for c in clientes:
                cidade_nome = c.cidade.strip().upper() if c.cidade and c.cidade.strip() else "SEM_CIDADE"
                if cidade_nome not in cidades_map:
                    cidades_map[cidade_nome] = []
                cidades_map[cidade_nome].append(c)
            
            # 3. Ordenar cidades alfabeticamente
            cidades_ordenadas = sorted(cidades_map.keys())
            
            print(f"Encontradas {len(cidades_ordenadas)} cidades.")
            
            # 4. Atribuir códigos
            contador_cidade = 1
            total_atualizados = 0
            
            for cidade in cidades_ordenadas:
                codigo_cidade = str(contador_cidade).zfill(4)
                lista_clientes = cidades_map[cidade]
                
                # Ordenar clientes por ID (ordem de cadastro)
                lista_clientes.sort(key=lambda x: x.id)
                
                contador_cliente = 1
                for cliente in lista_clientes:
                    codigo_sequencia = str(contador_cliente).zfill(4)
                    novo_codigo = f"{codigo_cidade}-{codigo_sequencia}"
                    
                    if cliente.codigo_cliente != novo_codigo:
                        print(f"Atualizando {cliente.nome} ({cidade}): {cliente.codigo_cliente} -> {novo_codigo}")
                        cliente.codigo_cliente = novo_codigo
                        total_atualizados += 1
                    
                    contador_cliente += 1
                
                contador_cidade += 1
            
            try:
                db.session.commit()
                print(f"✅ Sucesso! {total_atualizados} clientes atualizados na empresa {empresa_id}.")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Erro ao salvar alterações: {e}")

if __name__ == "__main__":
    corrigir_codigos()
