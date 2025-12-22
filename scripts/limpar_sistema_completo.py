#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Limpeza Completa do Sistema
Remove duplicações e espaços vazios mantendo layout responsivo
"""

import re
import os
from pathlib import Path
from collections import defaultdict

class LimpadorSistema:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.estatisticas = {
            'arquivos_processados': 0,
            'linhas_removidas': 0,
            'duplicacoes_removidas': 0
        }
    
    def limpar_linhas_vazias_excessivas(self, conteudo):
        """Remove linhas vazias excessivas, mantendo apenas uma entre blocos"""
        # Substituir 3 ou mais linhas vazias por apenas 2
        conteudo = re.sub(r'\n\n\n+', '\n\n', conteudo)
        
        # Remover espaços no final das linhas
        linhas = conteudo.split('\n')
        linhas = [linha.rstrip() for linha in linhas]
        
        return '\n'.join(linhas)
    
    def limpar_arquivo_python(self, caminho):
        """Limpa arquivo Python removendo espaços vazios excessivos"""
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo_original = f.read()
            
            # Contar linhas originais
            linhas_originais = len(conteudo_original.split('\n'))
            
            # Limpar espaços
            conteudo_limpo = self.limpar_linhas_vazias_excessivas(conteudo_original)
            
            # Remover imports duplicados (preservando ordem)
            linhas = conteudo_limpo.split('\n')
            imports_vistos = set()
            linhas_sem_imports_duplicados = []
            
            for linha in linhas:
                # Detectar imports
                if linha.strip().startswith(('import ', 'from ')):
                    if linha.strip() not in imports_vistos:
                        imports_vistos.add(linha.strip())
                        linhas_sem_imports_duplicados.append(linha)
                else:
                    linhas_sem_imports_duplicados.append(linha)
            
            conteudo_final = '\n'.join(linhas_sem_imports_duplicados)
            
            # Contar linhas finais
            linhas_finais = len(conteudo_final.split('\n'))
            linhas_removidas = linhas_originais - linhas_finais
            
            # Salvar apenas se houve mudanças
            if conteudo_final != conteudo_original:
                with open(caminho, 'w', encoding='utf-8') as f:
                    f.write(conteudo_final)
                return True, linhas_removidas
            
            return False, 0
            
        except Exception as e:
            print(f"❌ Erro ao processar {caminho.name}: {e}")
            return False, 0
    
    def limpar_arquivo_css(self, caminho):
        """Limpa arquivo CSS removendo duplicações e espaços"""
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo_original = f.read()
            
            linhas_originais = len(conteudo_original.split('\n'))
            
            # Limpar espaços vazios excessivos
            conteudo_limpo = self.limpar_linhas_vazias_excessivas(conteudo_original)
            
            # Remover comentários vazios
            conteudo_limpo = re.sub(r'/\*\s*\*/', '', conteudo_limpo)
            
            linhas_finais = len(conteudo_limpo.split('\n'))
            linhas_removidas = linhas_originais - linhas_finais
            
            if conteudo_limpo != conteudo_original:
                with open(caminho, 'w', encoding='utf-8') as f:
                    f.write(conteudo_limpo)
                return True, linhas_removidas
            
            return False, 0
            
        except Exception as e:
            print(f"❌ Erro ao processar {caminho.name}: {e}")
            return False, 0
    
    def limpar_arquivo_html(self, caminho):
        """Limpa arquivo HTML removendo espaços e divs vazias"""
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo_original = f.read()
            
            linhas_originais = len(conteudo_original.split('\n'))
            
            # Limpar espaços vazios excessivos
            conteudo_limpo = self.limpar_linhas_vazias_excessivas(conteudo_original)
            
            # Remover divs vazias (mas preservar estrutura do layout)
            # Só remove se não tiver classes importantes
            conteudo_limpo = re.sub(
                r'<div\s*>\s*</div>', 
                '', 
                conteudo_limpo
            )
            
            # Remover comentários HTML vazios
            conteudo_limpo = re.sub(r'<!--\s*-->', '', conteudo_limpo)
            
            linhas_finais = len(conteudo_limpo.split('\n'))
            linhas_removidas = linhas_originais - linhas_finais
            
            if conteudo_limpo != conteudo_original:
                with open(caminho, 'w', encoding='utf-8') as f:
                    f.write(conteudo_limpo)
                return True, linhas_removidas
            
            return False, 0
            
        except Exception as e:
            print(f"❌ Erro ao processar {caminho.name}: {e}")
            return False, 0
    
    def processar_diretorio(self, extensao, metodo_limpeza):
        """Processa todos os arquivos de uma extensão"""
        arquivos_modificados = 0
        total_linhas_removidas = 0
        
        if extensao == '.py':
            # Arquivos Python específicos
            arquivos = [
                self.base_path / 'app.py',
                self.base_path / 'models.py',
                self.base_path / 'forms.py',
                self.base_path / 'config.py',
                self.base_path / 'calculo_comissao.py',
                self.base_path / 'calculo_projecao.py',
                self.base_path / 'pdf_generator.py',
                self.base_path / 'wsgi.py',
            ]
        elif extensao == '.css':
            arquivos = list((self.base_path / 'static' / 'css').glob('*.css'))
        elif extensao == '.html':
            arquivos = list((self.base_path / 'templates').rglob('*.html'))
        else:
            return 0, 0
        
        for arquivo in arquivos:
            if arquivo.exists():
                modificado, linhas_removidas = metodo_limpeza(arquivo)
                if modificado:
                    arquivos_modificados += 1
                    total_linhas_removidas += linhas_removidas
                    print(f"  ✅ {arquivo.name}: {linhas_removidas} linhas removidas")
        
        return arquivos_modificados, total_linhas_removidas
    
    def executar(self):
        """Executa a limpeza completa"""
        print("\n" + "=" * 80)
        print("🧹 LIMPEZA COMPLETA DO SISTEMA".center(80))
        print("=" * 80 + "\n")
        
        # 1. Limpar arquivos Python
        print("📄 Limpando arquivos Python...")
        py_modificados, py_linhas = self.processar_diretorio('.py', self.limpar_arquivo_python)
        self.estatisticas['arquivos_processados'] += py_modificados
        self.estatisticas['linhas_removidas'] += py_linhas
        print(f"   ✅ {py_modificados} arquivos Python otimizados\n")
        
        # 2. Limpar arquivos CSS
        print("🎨 Limpando arquivos CSS...")
        css_modificados, css_linhas = self.processar_diretorio('.css', self.limpar_arquivo_css)
        self.estatisticas['arquivos_processados'] += css_modificados
        self.estatisticas['linhas_removidas'] += css_linhas
        print(f"   ✅ {css_modificados} arquivos CSS otimizados\n")
        
        # 3. Limpar arquivos HTML
        print("📝 Limpando templates HTML...")
        html_modificados, html_linhas = self.processar_diretorio('.html', self.limpar_arquivo_html)
        self.estatisticas['arquivos_processados'] += html_modificados
        self.estatisticas['linhas_removidas'] += html_linhas
        print(f"   ✅ {html_modificados} templates HTML otimizados\n")
        
        # Exibir estatísticas finais
        print("=" * 80)
        print("📊 ESTATÍSTICAS FINAIS".center(80))
        print("=" * 80)
        print(f"\n✅ Arquivos processados: {self.estatisticas['arquivos_processados']}")
        print(f"✅ Linhas removidas: {self.estatisticas['linhas_removidas']}")
        print(f"\n{'🎯 LIMPEZA CONCLUÍDA COM SUCESSO!'.center(80)}\n")
        print("=" * 80 + "\n")

if __name__ == '__main__':
    limpador = LimpadorSistema()
    limpador.executar()
