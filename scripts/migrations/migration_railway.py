"""
Script para executar migração no Railway
Execute este comando no Railway CLI ou via interface web
"""

import os
from sqlalchemy import create_engine, text, inspect
from datetime import datetime

# URL do banco de dados (Railway fornece via variável de ambiente)
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL não encontrada!")
    print("💡 Este script deve ser executado no Railway")
    exit(1)

# Substituir postgres:// por postgresql:// se necessário (Railway usa postgres://)
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

print("=" * 70)
print("🚀 MIGRAÇÃO RAILWAY - SISTEMA DE MENSAGENS E PERMISSÕES")
print("=" * 70)
print(f"\n📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print(f"🔗 Banco: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'Railway PostgreSQL'}")

try:
    # Criar engine
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)

    print("\n✅ Conexão estabelecida com sucesso!")

    # Verificar tabelas existentes
    tabelas = inspector.get_table_names()
    print(f"\n📊 Tabelas encontradas: {len(tabelas)}")

    with engine.connect() as conn:
        # 1. Criar tabela mensagens se não existir
        if 'mensagens' not in tabelas:
            print("\n📧 Criando tabela 'mensagens'...")
            conn.execute(text("""
                CREATE TABLE mensagens (
                    id SERIAL PRIMARY KEY,
                    remetente_id INTEGER NOT NULL REFERENCES usuarios(id),
                    destinatario_id INTEGER NOT NULL REFERENCES usuarios(id),
                    assunto VARCHAR(200) NOT NULL,
                    mensagem TEXT NOT NULL,
                    lida BOOLEAN DEFAULT FALSE,
                    data_leitura TIMESTAMP,
                    arquivada_remetente BOOLEAN DEFAULT FALSE,
                    arquivada_destinatario BOOLEAN DEFAULT FALSE,
                    prioridade VARCHAR(20) DEFAULT 'normal',
                    tipo VARCHAR(50) DEFAULT 'normal',
                    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.execute(text("CREATE INDEX idx_mensagens_remetente ON mensagens(remetente_id)"))
            conn.execute(text("CREATE INDEX idx_mensagens_destinatario ON mensagens(destinatario_id)"))
            conn.execute(text("CREATE INDEX idx_mensagens_data ON mensagens(data_envio)"))
            conn.commit()
            print("✅ Tabela 'mensagens' criada!")
        else:
            print("\n✅ Tabela 'mensagens' já existe")

        # 2. Verificar e adicionar colunas na tabela usuarios
        print("\n🔐 Verificando colunas de permissões...")
        colunas = [col['name'] for col in inspector.get_columns('usuarios')]

        novas_colunas = {
            'vendedor_id': 'INTEGER REFERENCES vendedores(id)',
            'pode_ver_dashboard': 'BOOLEAN DEFAULT TRUE',
            'pode_gerenciar_vendedores': 'BOOLEAN DEFAULT FALSE',
            'pode_gerenciar_metas': 'BOOLEAN DEFAULT FALSE',
            'pode_gerenciar_equipes': 'BOOLEAN DEFAULT FALSE',
            'pode_gerenciar_comissoes': 'BOOLEAN DEFAULT FALSE',
            'pode_enviar_mensagens': 'BOOLEAN DEFAULT TRUE',
            'pode_exportar_dados': 'BOOLEAN DEFAULT FALSE',
            'pode_ver_todas_metas': 'BOOLEAN DEFAULT FALSE',
            'pode_aprovar_comissoes': 'BOOLEAN DEFAULT FALSE'
        }

        for coluna, tipo in novas_colunas.items():
            if coluna not in colunas:
                print(f"  ➕ Adicionando coluna '{coluna}'...")
                conn.execute(text(f"ALTER TABLE usuarios ADD COLUMN {coluna} {tipo}"))
                conn.commit()
                print(f"  ✅ Coluna '{coluna}' adicionada")
            else:
                print(f"  ℹ️  Coluna '{coluna}' já existe")

        # 3. Configurar permissões para usuários existentes
        print("\n⚙️  Configurando permissões para usuários existentes...")

        # Super Admins
        result = conn.execute(text("""
            UPDATE usuarios 
            SET pode_ver_dashboard = TRUE,
                pode_gerenciar_vendedores = TRUE,
                pode_gerenciar_metas = TRUE,
                pode_gerenciar_equipes = TRUE,
                pode_gerenciar_comissoes = TRUE,
                pode_enviar_mensagens = TRUE,
                pode_exportar_dados = TRUE,
                pode_ver_todas_metas = TRUE,
                pode_aprovar_comissoes = TRUE
            WHERE is_super_admin = TRUE
        """))
        conn.commit()
        print(f"  ✅ Super Admins configurados: {result.rowcount}")

        # Admins
        result = conn.execute(text("""
            UPDATE usuarios 
            SET pode_ver_dashboard = TRUE,
                pode_gerenciar_vendedores = TRUE,
                pode_gerenciar_metas = TRUE,
                pode_gerenciar_equipes = TRUE,
                pode_gerenciar_comissoes = TRUE,
                pode_enviar_mensagens = TRUE,
                pode_exportar_dados = TRUE,
                pode_ver_todas_metas = TRUE,
                pode_aprovar_comissoes = TRUE
            WHERE cargo = 'admin'
        """))
        conn.commit()
        print(f"  ✅ Admins configurados: {result.rowcount}")

        # Gerentes
        result = conn.execute(text("""
            UPDATE usuarios 
            SET pode_ver_dashboard = TRUE,
                pode_gerenciar_vendedores = TRUE,
                pode_gerenciar_metas = TRUE,
                pode_gerenciar_equipes = TRUE,
                pode_gerenciar_comissoes = FALSE,
                pode_enviar_mensagens = TRUE,
                pode_exportar_dados = TRUE,
                pode_ver_todas_metas = TRUE,
                pode_aprovar_comissoes = FALSE
            WHERE cargo = 'gerente'
        """))
        conn.commit()
        print(f"  ✅ Gerentes configurados: {result.rowcount}")

        # Supervisores
        result = conn.execute(text("""
            UPDATE usuarios 
            SET pode_ver_dashboard = TRUE,
                pode_gerenciar_vendedores = FALSE,
                pode_gerenciar_metas = TRUE,
                pode_gerenciar_equipes = FALSE,
                pode_gerenciar_comissoes = FALSE,
                pode_enviar_mensagens = TRUE,
                pode_exportar_dados = FALSE,
                pode_ver_todas_metas = FALSE,
                pode_aprovar_comissoes = FALSE
            WHERE cargo = 'supervisor'
        """))
        conn.commit()
        print(f"  ✅ Supervisores configurados: {result.rowcount}")

        # Vendedores
        result = conn.execute(text("""
            UPDATE usuarios 
            SET pode_ver_dashboard = TRUE,
                pode_gerenciar_vendedores = FALSE,
                pode_gerenciar_metas = FALSE,
                pode_gerenciar_equipes = FALSE,
                pode_gerenciar_comissoes = FALSE,
                pode_enviar_mensagens = TRUE,
                pode_exportar_dados = FALSE,
                pode_ver_todas_metas = FALSE,
                pode_aprovar_comissoes = FALSE
            WHERE cargo = 'vendedor'
        """))
        conn.commit()
        print(f"  ✅ Vendedores configurados: {result.rowcount}")

        # 4. Criar usuário Sistema se não existir
        print("\n👤 Verificando usuário 'Sistema'...")
        result = conn.execute(text("SELECT id FROM usuarios WHERE email = 'sistema@suameta.com'"))
        sistema = result.fetchone()

        if not sistema:
            print("  ➕ Criando usuário 'Sistema'...")
            # Usar hash fixo para senha do sistema
            from werkzeug.security import generate_password_hash
            senha_hash = generate_password_hash('sistema123!@#')

            conn.execute(text("""
                INSERT INTO usuarios (
                    nome, email, senha_hash, cargo, ativo, 
                    is_super_admin, pode_enviar_mensagens
                ) VALUES (
                    'Sistema', 'sistema@suameta.com', :senha, 'admin', FALSE,
                    FALSE, TRUE
                )
            """), {'senha': senha_hash})
            conn.commit()

            result = conn.execute(text("SELECT id FROM usuarios WHERE email = 'sistema@suameta.com'"))
            sistema = result.fetchone()
            print("  ✅ Usuário 'Sistema' criado")
        else:
            print("  ℹ️  Usuário 'Sistema' já existe")

        sistema_id = sistema[0]

        # 5. Enviar mensagens de boas-vindas
        print("\n📨 Verificando mensagens de boas-vindas...")
        result = conn.execute(text("SELECT COUNT(*) FROM mensagens WHERE remetente_id = :id"), 
                             {'id': sistema_id})
        count = result.scalar()

        if count == 0:
            print("  📧 Enviando mensagens de boas-vindas...")

            # Buscar todos os usuários ativos
            result = conn.execute(text("""
                SELECT id, nome FROM usuarios 
                WHERE ativo = TRUE AND id != :sistema_id
            """), {'sistema_id': sistema_id})

            usuarios = result.fetchall()

            for usuario_id, nome in usuarios:
                conn.execute(text("""
                    INSERT INTO mensagens (
                        remetente_id, destinatario_id, assunto, mensagem,
                        prioridade, tipo, data_envio
                    ) VALUES (
                        :remetente, :destinatario, :assunto, :mensagem,
                        'alta', 'sistema', CURRENT_TIMESTAMP
                    )
                """), {
                    'remetente': sistema_id,
                    'destinatario': usuario_id,
                    'assunto': '🎉 Bem-vindo ao Sistema de Mensagens!',
                    'mensagem': f"""Olá {nome}!

O sistema de mensagens está agora disponível! 

Você pode:
• Enviar mensagens para outros usuários
• Enviar mensagens para toda sua equipe
• Receber notificações importantes
• Organizar suas mensagens por prioridade

Suas permissões foram configuradas automaticamente baseadas no seu cargo.

Qualquer dúvida, consulte a Central de Ajuda.

Atenciosamente,
Sistema SuaMeta"""
                })

            conn.commit()
            print(f"  ✅ {len(usuarios)} mensagens enviadas")
        else:
            print(f"  ℹ️  Mensagens já enviadas ({count} existentes)")

        # 6. Estatísticas finais
        print("\n" + "=" * 70)
        print("📊 ESTATÍSTICAS FINAIS")
        print("=" * 70)

        stats = {}

        result = conn.execute(text("SELECT COUNT(*) FROM usuarios"))
        stats['usuarios'] = result.scalar()

        result = conn.execute(text("SELECT COUNT(*) FROM mensagens"))
        stats['mensagens'] = result.scalar()

        result = conn.execute(text("SELECT COUNT(*) FROM vendedores"))
        stats['vendedores'] = result.scalar()

        result = conn.execute(text("SELECT COUNT(*) FROM equipes"))
        stats['equipes'] = result.scalar()

        result = conn.execute(text("SELECT COUNT(*) FROM metas"))
        stats['metas'] = result.scalar()

        print(f"\n  👥 Usuários: {stats['usuarios']}")
        print(f"  📧 Mensagens: {stats['mensagens']}")
        print(f"  🎯 Vendedores: {stats['vendedores']}")
        print(f"  👨‍👩‍👦 Equipes: {stats['equipes']}")
        print(f"  📊 Metas: {stats['metas']}")

    print("\n" + "=" * 70)
    print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    print("\n🚀 O sistema de mensagens está pronto para uso!")
    print("📝 Todas as permissões foram configuradas")
    print("💡 Usuários podem acessar /mensagens para começar\n")

except Exception as e:
    print(f"\n❌ ERRO na migração:")
    print(f"   {str(e)}")
    print("\n💡 Verifique:")
    print("   1. Se a DATABASE_URL está correta")
    print("   2. Se o banco PostgreSQL está acessível")
    print("   3. Se as tabelas base existem (usuarios, vendedores, etc)")
    exit(1)
