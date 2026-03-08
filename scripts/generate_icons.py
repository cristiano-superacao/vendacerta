"""
Script para criar ícones PWA do Sistema SuaMeta
Gera ícones SVG que podem ser usados como placeholder até ter ícones customizados
"""

import os

# Define o caminho para o diretório de imagens
img_dir = os.path.join(os.path.dirname(__file__), 'static', 'img')

# Template SVG base
svg_template = '''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="{size}" height="{size}" fill="url(#grad)" rx="20"/>
  <g transform="translate({size}/2, {size}/2)">
    <path d="M-{arrow_size},0 L0,-{arrow_size} L{arrow_size},0 L{arrow_size},-{arrow_size2} L0,-{arrow_size3} L-{arrow_size},-{arrow_size2} Z" 
          fill="#ffffff" stroke="#ffd700" stroke-width="2"/>
    <circle cx="0" cy="{circle_y}" r="{circle_r}" fill="#ffd700"/>
  </g>
  <text x="50%" y="75%" text-anchor="middle" font-family="Arial, sans-serif" 
        font-size="{font_size}" font-weight="bold" fill="#ffffff">SM</text>
</svg>'''

# Tamanhos dos ícones necessários para PWA
icon_sizes = [72, 96, 128, 144, 152, 192, 384, 512]

def create_icon_svg(size):
    """Cria um ícone SVG do tamanho especificado"""
    arrow_size = size * 0.15
    arrow_size2 = size * 0.25
    arrow_size3 = size * 0.35
    circle_y = size * 0.18
    circle_r = size * 0.06
    font_size = size * 0.15

    svg_content = svg_template.format(
        size=size,
        arrow_size=arrow_size,
        arrow_size2=arrow_size2,
        arrow_size3=arrow_size3,
        circle_y=circle_y,
        circle_r=circle_r,
        font_size=font_size
    )

    # Salva o arquivo SVG
    filename = os.path.join(img_dir, f'icon-{size}x{size}.svg')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f'✓ Criado: {filename}')

def convert_svg_to_png():
    """
    Instruções para converter SVG para PNG:

    Opção 1 - Online (Mais Fácil):
    1. Acesse: https://svgtopng.com/
    2. Faça upload dos arquivos SVG criados em static/img/
    3. Baixe os PNGs gerados
    4. Substitua os arquivos .svg por .png na pasta static/img/

    Opção 2 - Com Pillow (Python):
    pip install pillow cairosvg

    Depois execute o código abaixo:

    from PIL import Image
    import cairosvg
    import os

    for size in [72, 96, 128, 144, 152, 192, 384, 512]:
        svg_path = f'static/img/icon-{size}x{size}.svg'
        png_path = f'static/img/icon-{size}x{size}.png'
        cairosvg.svg2png(url=svg_path, write_to=png_path)
        print(f'Convertido: {png_path}')
    """
    print("\n" + "="*60)
    print("INSTRUÇÕES PARA CONVERTER SVG → PNG")
    print("="*60)
    print("\nOpção 1 - Online (Recomendado):")
    print("1. Acesse: https://svgtopng.com/")
    print("2. Faça upload de todos os arquivos icon-*.svg")
    print("3. Baixe os PNGs gerados")
    print("4. Salve em: static/img/")
    print("5. Renomeie mantendo o mesmo padrão: icon-72x72.png, etc.")

    print("\nOpção 2 - Usando Python (Avançado):")
    print("pip install pillow cairosvg")
    print("Depois execute o código disponível no arquivo generate_icons.py")
    print("="*60)

if __name__ == '__main__':
    print("Gerando ícones PWA para SuaMeta...\n")

    # Cria o diretório se não existir
    os.makedirs(img_dir, exist_ok=True)

    # Gera os ícones SVG
    for size in icon_sizes:
        create_icon_svg(size)

    print(f'\n✓ {len(icon_sizes)} ícones SVG criados com sucesso!')
    print(f'✓ Localização: {img_dir}')

    # Mostra instruções de conversão
    convert_svg_to_png()
