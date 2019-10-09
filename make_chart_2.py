import matplotlib.pyplot as plt
from PIL import Image
import yaml
import os


resource_directory = "resources"

with open(os.path.join(resource_directory, "unit_data.yml")) as f:
    unit_dict = yaml.safe_load(f)

units_to_include = {'Infantry': [], 'Archers': [], 'Cavalry Archers': [],
                    'Cavalry': [], 'Siege': [], 'Navy': [], 'Misc': []}
all_units_to_include = []
section = None
with open(os.path.join(resource_directory, "units_to_include.txt")) as f:
    for l in f .readlines():
        line = l.strip()
        # skip blank lines
        if not line:
            continue
        if line in ['Infantry', 'Archers', 'Cavalry Archers', 'Cavalry', 'Siege', 'Navy', 'Misc']:
            section = line
        else:
            units_to_include[section].append(line)
            all_units_to_include.append(line)
for unit_type in units_to_include:
    print(f"{unit_type}: {len(units_to_include[unit_type])}")

unit_dict = {unit: unit_dict[unit] for unit in unit_dict if unit in all_units_to_include}
for unit in unit_dict:
    unit_dict[unit]['counters'] = [u for u in unit_dict[unit]['counters'] if u in all_units_to_include]

unit_widths = {
    'Infantry': max([len(unit_dict[unit]['counters']) for unit in units_to_include['Infantry']]) + 2,
    'Archers': max([len(unit_dict[unit]['counters']) for unit in units_to_include['Archers']]) + 2,
    'Cavalry Archers': max([len(unit_dict[unit]['counters']) for unit in units_to_include['Cavalry Archers']]) + 2,
    'Cavalry': max([len(unit_dict[unit]['counters']) for unit in units_to_include['Cavalry']]) + 2,
    'Siege': max([len(unit_dict[unit]['counters']) for unit in units_to_include['Siege']]) + 2,
    'Navy': max([len(unit_dict[unit]['counters']) for unit in units_to_include['Navy']]) + 2,
    'Misc': max([len(unit_dict[unit]['counters']) for unit in units_to_include['Misc']]) + 2
}

section_title_cells = 1
unit_heights = {
    'Infantry': len(units_to_include['Infantry']) + section_title_cells,
    'Archers': len(units_to_include['Archers']) + section_title_cells,
    'Cavalry Archers': len(units_to_include['Cavalry Archers']) + section_title_cells,
    'Cavalry': len(units_to_include['Cavalry']) + section_title_cells,
    'Siege': len(units_to_include['Siege']) + section_title_cells,
    'Navy': len(units_to_include['Navy']) + section_title_cells,
    'Misc': len(units_to_include['Misc']) + section_title_cells
}

sections = [['Infantry', 'Navy'], ['Archers', 'Cavalry'], ['Cavalry Archers', 'Siege', 'Misc']]
col_widths = [max([unit_widths[unit_type] for unit_type in column]) for column in sections]
total_width = sum(col_widths)
col_heights = [sum([unit_heights[unit_type] for unit_type in column]) for column in sections]
largest_height = max(col_heights)

main_title_cells = 1

width_per_cell = 1
height_per_cell = 1
font = 'Myanmar Text'
main_title_size = 80
section_title_size = 40
unit_text_size = 8
unit_wspace = .25
line_size = 3
chart = plt.figure(figsize=(total_width * width_per_cell, height_per_cell * (largest_height + main_title_cells)))

# Background
background = chart.add_axes([0, 0, 1, 1])
background.axis('off')
background.imshow(Image.open(os.path.join(resource_directory, "background.jpg")), aspect='auto', extent=[0, 1, 0, 1])
background.text(.95, .05, "by AssButt", ha='right', size=unit_text_size, family=font)

# title / main chart division
title_chart_division = chart.add_gridspec(2, 1, hspace=0, wspace=0, left=.03, right=.97, bottom=.03, top=.97,
                                          height_ratios=[main_title_cells, largest_height])
# title
title_ax = chart.add_subplot(title_chart_division[0])
title_ax.axis('off')
title_ax.text(.5, .5, "AoE 2 Counter Chart", ha='center', size=main_title_size, family=font,
              style='oblique', weight='bold')
title_ax.patch.set_alpha(0.0)

# main chart
main_columns = title_chart_division[1].subgridspec(1, 3, hspace=0, wspace=0.1, width_ratios=col_widths)
for i, column in enumerate(sections):
    column_sections = main_columns[i].subgridspec(len(column) + 1, 1, hspace=0, wspace=0,
                                                  height_ratios=[unit_heights[unit] for unit in column] +
                                                                [largest_height - col_heights[i]])
    for j, unit_type in enumerate(column):
        unit_section = column_sections[j].subgridspec(unit_heights[unit_type], unit_widths[unit_type] + 1,
                                                      hspace=.4, wspace=unit_wspace,
                                                      width_ratios=unit_widths[unit_type] * [1] +
                                                                   [col_widths[i] - unit_widths[unit_type]])
        unit_section_title_ax = chart.add_subplot(unit_section[:section_title_cells, :])
        unit_section_title_ax.text(.5, .1, unit_type, ha='center', family=font, size=section_title_size, weight='bold')
        unit_section_title_ax.axis('off')
        for k, unit_name in enumerate(units_to_include[unit_type]):
            ax = chart.add_subplot(unit_section[k + section_title_cells, 0])
            ax.axis('off')
            text = ax.text(.5, .95, unit_dict[unit_name]['display_name'], ha='center', family=font, size=unit_text_size)
            image = Image.open(unit_dict[unit_name]['thumbnail'])
            ax.imshow(image, aspect='auto', extent=[.1, .9, 0, .9])

            # counters
            for l, counter_name in enumerate(unit_dict[unit_name]['counters']):
                ax = chart.add_subplot(unit_section[k + section_title_cells, l + 2])
                ax.axis('off')
                text = ax.text(.5, .95, unit_dict[counter_name]['display_name'], ha='center', family=font,
                               size=unit_text_size)
                image = Image.open(unit_dict[counter_name]['thumbnail'])
                ax.imshow(image, aspect='auto', extent=[.1, .9, 0, .9])

chart.savefig(os.path.join(resource_directory, "chart.pdf"), bbox_inches='tight')
