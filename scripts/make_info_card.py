#!/usr/bin/env python3
"""
Generate neofetch-style info card SVG with line-by-line fade-in animations.
"""
import os

def make_info_card(output_path):
    # Terminal palette
    bg_color = "#0d1117"
    text_color = "#c9d1d9"
    accent_color = "#58a6ff"
    green = "#3fb950"
    yellow = "#d29922"
    pink = "#ff7b72"
    
    content = [
        ("silveirinhajuan@github ~ $ ./whoami --verbose", "#58a6ff"),
        ("", text_color),
        ("     ╔══════════════════════════════════════════════╗", green),
        ("     ║   JUAN GUERRA :: SILVEIRINHAJUAN // ITA ’27    ║", pink),
        ("     ╚══════════════════════════════════════════════╝", green),
        ("", text_color),
        ("OS:     Linux (Ubuntu 22.04) x86_64", green),
        ("Host:   DonJuan Holding / ITA 2027 Candidate", green),
        ("Kernel: Quantum Computing Research Pipeline", green),
        ("Shell:  zsh + tmux + neovim", green),
        ("Editor: Neovim (Lua config)", green),
        ("Uptime: ~1 yr  Software Developer @ Pegueleve", green),
        ("Pkgs:   Python · FastAPI · Django · PyTorch · TF", green),
        ("Term:   Alacritty / Kitty", green),
        ("CPU:    Intel i7  Quantum Simulators", green),
        ("GPU:    NVIDIA RTX  CUDA Enabled", green),
        ("Mem:    ML Models + Data Pipelines Loaded", green),
        ("", text_color),
        ("— MISSION —", pink),
        ("› Eng. Computação ITA + PFC-F (Min. Eng. Física)", yellow),
        ("› PMG → PhD Computação Quântica (7 anos)", yellow),
        ("› Retorno CE remoto + Aline → São José dos Campos", yellow),
        ("", text_color),
        ("— STATUS —", pink),
        ("🎓 ITA 2027: 1ª Fase 27/09/2026 · IME 2027: 1ª Fase 20/09/2026", yellow),
        ("📍 Caucaia-CE · Prova: Fortaleza (Av. Santos Dumont 485)", yellow),
        ("💼 Backend Dev @ Pegueleve · APIs · IA/ML · Data Pipelines", yellow),
        ("🎨 Projeto Paralelo: Silveira Arte (Arte Família)", yellow),
        ("🤖 Íris: Assistente Pessoal Autônoma (Hermes Agent)", yellow),
    ]
    
    width = 540
    char_height = 18
    line_height = 20
    padding = 20
    height = padding * 2 + len(content) * line_height
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" rx="10" fill="{bg_color}" stroke="#30363d" />
  <style>
    .line {{
      font-family: 'JetBrains Mono', 'Courier New', Courier, monospace;
      font-size: {char_height}px;
      opacity: 0;
      animation: typeIn 0.3s ease forwards;
    }}
    .cursor {{
      animation: blink 1s infinite;
    }}
    @keyframes typeIn {{
      from {{ opacity: 0; transform: translateX(-8px); }}
      to {{ opacity: 1; transform: translateX(0); }}
    }}
    @keyframes blink {{
      0%, 50% {{ opacity: 1; }}
      51%, 100% {{ opacity: 0; }}
    }}
  </style>
'''
    
    for i, (text, color) in enumerate(content):
        delay = i * 0.08
        y = padding + (i + 1) * line_height
        if ": " in text and not text.startswith(" "):
            parts = text.split(": ", 1)
            key = parts[0] + ": "
            val = parts[1]
            svg += f'  <text x="{padding}" y="{y}" class="line" style="animation-delay: {delay:.2f}s">'
            svg += f'<tspan fill="{green}">{key}</tspan><tspan fill="{text_color}">{val}</tspan></text>\n'
        else:
            svg += f'  <text x="{padding}" y="{y}" fill="{color}" class="line" style="animation-delay: {delay:.2f}s">{text}</text>\n'
    
    # Cursor at end
    svg += f'''  <text x="{width - 30}" y="{height - padding}" fill="{accent_color}" class="line cursor" style="animation-delay: {len(content)*0.08 + 0.5:.2f}s">█</text>
</svg>'''
    
    with open(output_path, 'w') as f:
        f.write(svg)
    print(f"Generated {output_path} ({len(content)} lines, {width}x{height})")

if __name__ == "__main__":
    make_info_card("info-card.svg")
