"""Script para verificar permissões do admin"""
from app import app, db, Usuario

with app.app_context():
    # Buscar admin
    admin = Usuario.query.filter_by(cargo='admin').first()

    if admin:
        print(f"✅ Admin encontrado: {admin.nome}")
        print(f"   Email: {admin.email}")
        print(f"   Cargo: {admin.cargo}")
        print(f"   Empresa ID: {admin.empresa_id}")
        print(f"   Super Admin: {admin.is_super_admin}")
        print(f"   Ativo: {admin.ativo}")

        # Verificar permissões
        print("\n🔐 Permissões:")
        permissoes = [attr for attr in dir(admin) if attr.startswith('pode_')]

        if permissoes:
            for perm in permissoes:
                valor = getattr(admin, perm, None)
                emoji = "✅" if valor else "❌"
                print(f"   {emoji} {perm}: {valor}")
        else:
            print("   ⚠️  Nenhuma permissão encontrada (colunas não existem)")
            print("   💡 Execute migration_mensagens_permissoes.py")
    else:
        print("❌ Nenhum admin encontrado no banco de dados")
        print("\n👥 Usuários cadastrados:")
        usuarios = Usuario.query.all()
        for u in usuarios:
            print(f"   - {u.nome} ({u.cargo}) - Empresa {u.empresa_id}")
