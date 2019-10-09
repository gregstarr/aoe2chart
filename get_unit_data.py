import requests
from bs4 import BeautifulSoup
import os
import yaml

resource_directory = "resources"
with open(os.path.join(resource_directory, "units.txt")) as f:
    unit_names = [l.strip() for l in f.readlines()]

unit_dict = {}

UNIT_PAGE_TEMPLATE_1 = "https://ageofempires.fandom.com/wiki/{}_(Age_of_Empires_II)"
UNIT_PAGE_TEMPLATE_2 = "https://ageofempires.fandom.com/wiki/{}"

for name in unit_names:
    unit_dict[name] = {'display_name': name}
    print(name)
    modified_name = name.replace(' ', '_')
    url = UNIT_PAGE_TEMPLATE_1.format(modified_name)
    r = requests.get(url)
    if r.status_code != 200:
        url = UNIT_PAGE_TEMPLATE_2.format(modified_name)
        r = requests.get(url)

    if r.status_code != 200:
        continue
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get thumbnail
    try:
        thumbnail_url = soup.find('img', attrs={'class': 'pi-image-thumbnail'})['src']
        img_file_name = os.path.join(resource_directory, "thumbnails", f"{name}.jpg")
        with open(img_file_name, 'wb') as img_file:
            img_file.write(requests.get(thumbnail_url).content)
        unit_dict[name]['thumbnail'] = img_file_name
    except Exception:
        print(f"Couldn't find thumbnail for {name}")

    # how to counter
    try:
        weak_vs = soup.find('table', attrs={'class': 'wikitable'}).contents[5].contents[2].text.strip().split(',')
        unit_dict[name]['counters'] = [w.strip()[:-1] if w.strip()[-1] == 's' else w.strip() for w in weak_vs]
    except Exception:
        print(f"Couldn't find counters for {name}")

with open(os.path.join(resource_directory, "unit_data.yml"), 'w') as f:
    yaml.safe_dump(unit_dict, f)
