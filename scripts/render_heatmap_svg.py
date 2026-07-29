import json
import os

def generate_svg(data_path, output_path):
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    days = data['days']
    if not days:
        return
        
    # Heatmap dimensions
    cell_size = 12
    gutter = 3
    rows = 7
    cols = (len(days) + rows - 1) // rows
    
    width = cols * (cell_size + gutter)
    height = rows * (cell_size + gutter)
    
    colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    
    svg_content = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .day {{
      opacity: 0;
      animation: fadeIn 0.5s ease forwards;
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: scale(0.5); }}
      to {{ opacity: 1; transform: scale(1); }}
    }}
  </style>
'''
    
    for i, day in enumerate(days):
        col = i // rows
        row = i % rows
        x = col * (cell_size + gutter)
        y = row * (cell_size + gutter)
        level = day['level']
        color = colors[level] if level < len(colors) else colors[-1]
        
        # Delay based on column to create a wave effect
        delay = col * 0.02 + row * 0.01
        
        svg_content += f'  <rect class="day" x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}" style="animation-delay: {delay:.2f}s" />\n'
        
    svg_content += '</svg>'
    
    with open(output_path, 'w') as f:
        f.write(svg_content)

if __name__ == "__main__":
    generate_svg("data/contributions.json", "contrib-heatmap.svg")
