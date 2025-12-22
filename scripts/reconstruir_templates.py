# reconstruir_templates.py
# Script para reconstruir todos os templates seguindo o guia de uso

import os
import shutil

# Diretório de templates
TEMPLATES_DIR = r"c:\Users\Superação\Desktop\Sistema\Metas\templates"
BACKUP_DIR = r"c:\Users\Superação\Desktop\Sistema\Metas\backups\templates_old"

# Criar backup
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Fazer backup dos templates atuais
for root, dirs, files in os.walk(TEMPLATES_DIR):
    for file in files:
        if file.endswith('.html'):
            src = os.path.join(root, file)
            rel_path = os.path.relpath(src, TEMPLATES_DIR)
            dst = os.path.join(BACKUP_DIR, rel_path)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"Backup: {rel_path}")

print("\n✅ Backup concluído!")
print(f"📁 Localização: {BACKUP_DIR}")
