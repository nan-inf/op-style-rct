import json
import os
import shutil

from color_schemes import base_colors, color_schemes


def main():
    """Generate Openplanet overlay styles for every color scheme defined in
    `color_schemes.py`.
    """
    with open('template.toml', 'r') as f:
        template = f.read()

    info = {
        'styles': []
    }

    if os.path.isdir('styles'):
        shutil.rmtree('styles')
    os.makedirs('styles', exist_ok=True)

    for color_name, scheme in color_schemes.items():
        print(color_name)

        scheme_name = f'RCT2 {color_name.title()}'
        scheme_description = f'A clone of the {color_name} menu windows from RollerCoaster Tycoon 2.'
        scheme_screenshot = f'screenshots/{color_name.replace(" ", "-")}.png'
        scheme_style = f'styles/{color_name.replace(" ", "-")}.toml'

        scheme = base_colors | scheme
        scheme['average_border_color'] = average(scheme['dark_border_color'], scheme['light_border_color'])
        scheme['average_background_border_color'] = average(scheme['background_color'], scheme['light_border_color'])

        style = template.format(**scheme)

        with open(scheme_style, 'w') as f:
            f.write(style)

        info['styles'].append({
            'name': scheme_name,
            'author': 'NaNInf',
            'description': scheme_description,
            'screenshot': scheme_screenshot,
            'style': scheme_style
        })

    with open('info.json', 'w') as f:
        json.dump(info, f, indent=4)


def average(c1: str, c2: str) -> str:
    """Calculate the average of two hex colors (by simply taking the average
    of the R, G, and B components) and return it. Expects input strings in the
    format '#RRGGBB'.

    Args:
        c1 (str): Color 1.
        c2 (str): Color 2.

    Returns:
        str: Averaged color.
    """
    c1, c2 = [[int(c[i:i+2], base=16) for i in range(1, 7, 2)] for c in [c1, c2]]
    average = [(c1[i] + c2[i]) // 2 for i in range(3)]
    average_hex = '#' + ''.join(f'{c:02X}' for c in average)
    return average_hex


if __name__ == '__main__':
    main()
