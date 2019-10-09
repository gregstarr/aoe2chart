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

max_counters = max([len(unit_dict[unit]['counters']) for unit in unit_dict])

width_per_cell = 2.5
height_per_cell = 2
font = 'Myanmar Text'
title_size = 84
label_size = 56
text_size = 16
line_size = 3
chart = plt.figure(figsize=((max_counters + 1) * width_per_cell,
                            height_per_cell * len(unit_dict)))

# Background stuff
background = chart.add_axes([0, 0, 1, 1])
background.axis('off')
background.imshow(Image.open(os.path.join(resource_directory, "background_middle.jpg")), aspect='auto', extent=[0, 1, 0, 1])
background.plot([0.05, 0.95], [.965, .965], color='black', lw=line_size)
background.plot([0.16, 0.16], [.005, .965], color='black', lw=line_size)


# for i in range(100):
#     if not i % 10:
#         background.text(.04, i / 100, f"{i / 100}", ha='center', size=label_size)
#     else:
#         background.text(.04, float(i) / 100, "-", ha='center', size=label_size)
background.text(.04, .835, "Infantry", ha='center', size=label_size, family=font, weight='semibold', rotation='vertical')
background.text(.04, .63, "Archers", ha='center', size=label_size, family=font, weight='semibold', rotation='vertical')
background.text(.04, .49, "Cavalry Archers", ha='center', size=label_size, family=font, weight='semibold', rotation='vertical')
background.text(.04, .345, "Cavalry", ha='center', size=label_size, family=font, weight='semibold', rotation='vertical')
background.text(.04, .2, "Siege", ha='center', size=label_size, family=font, weight='semibold', rotation='vertical')
background.text(.04, .09, "Navy", ha='center', size=label_size, family=font, weight='semibold', rotation='vertical')
background.text(.04, .015, "Misc", ha='center', size=label_size, family=font, weight='semibold', rotation='vertical')
background.set_xlim([0, 1])
background.set_ylim([0, 1])

grid = chart.add_gridspec(len(unit_dict) + 2, max_counters + 1, hspace=.6, wspace=.5,
                          left=.08, right=.95, bottom=.01, top=.99, width_ratios=[1.2] + max_counters * [1])

# Title
title_ax = chart.add_subplot(grid[0, :])
title_ax.axis('off')
title_ax.text(.5, .5, "Age of Empires 2 Counter Chart", ha='center', size=title_size, family=font, style='oblique', weight='bold')
title_ax.patch.set_alpha(0.0)

# Unit
ax = chart.add_subplot(grid[1, 0])
ax.axis('off')
ax.text(.5, .5, "Unit", ha='center', size=label_size, weight='semibold', family=font)

# Counter
ax = chart.add_subplot(grid[1, 1:])
ax.axis('off')
ax.text(.5, .5, "Counters", ha='center', size=label_size, weight='semibold', family=font)

for row, unit_name in enumerate(units_to_include):
    ax = chart.add_subplot(grid[row + 2, 0])
    ax.axis('off')
    text = ax.text(.5, .95, unit_dict[unit_name]['display_name'], ha='center', family=font, size=text_size)
    image = Image.open(unit_dict[unit_name]['thumbnail'])
    ax.imshow(image, aspect='auto', extent=[.1, .9, 0, .9])

    # counters
    for i, counter_name in enumerate(unit_dict[unit_name]['counters']):
        ax = chart.add_subplot(grid[row + 2, i + 1])
        ax.axis('off')
        text = ax.text(.5, .95, unit_dict[counter_name]['display_name'], ha='center', family=font, size=text_size)
        image = Image.open(unit_dict[counter_name]['thumbnail'])
        ax.imshow(image, aspect='auto', extent=[.1, .9, 0, .9])

chart.savefig(os.path.join(resource_directory, "chart.pdf"), bbox_inches='tight')
