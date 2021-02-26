import PySimpleGUI as sg
import markdown as md
import argparse
import json
import os.path
from shutil import copyfile


def edit_and_make_game_doc(data, template, save_file, destination_folder):

    sg.theme('dark grey 9')
    gdd_status = "Ready"

    # Define the window's contents
    tab1_layout = [[sg.Text("What's your game name?")],  # Part 2 - The Layout
                   [sg.Input(data.get('name'), key='name', enable_events=True)],
                   [sg.Text("Choose an image: "), sg.Input(
                       key="logoPath"), sg.FileBrowse(key='logo')],
                   [sg.Text("Project Description?")],
                   [sg.Multiline(data.get('description'), key='description', size=(60, 20))]]

    tab2_characters = [[sg.Text("Characters?")],
                       [sg.Multiline(data.get('characters'),
                                     key='characters', size=(60, 8))],
                       [sg.Text("Story?")],
                       [sg.Multiline(data.get('story'),
                                     key='story', size=(60, 10))],
                       [sg.Text("Theme?")],
                       [sg.Multiline(data.get('theme'),
                                     key='theme', size=(60, 10))]
                       ]

    tab_gameplay1 = [[sg.Text('Goals')],
                     [sg.Multiline(data.get('goals'),
                                   key='goals', size=(60, 10))],
                     [sg.Text('User Skills')],
                     [sg.Multiline(data.get('skills'),
                                   key='skills', size=(60, 10))],
                     [sg.Text('Game Mechanics:')],
                     [sg.Multiline(data.get('mechanics'),
                                   key='mechanics', size=(60, 10))]
                     ]

    tab_gameplay2 = [[sg.Text('Items and power-ups:')],
                     [sg.Multiline(data.get('items'),
                                   key='items', size=(60, 10))],
                     [sg.Text('Progression and challenge')],
                     [sg.Multiline(data.get('challenge'),
                                   key='challenge', size=(60, 12))],
                     [sg.Text('Losing:')],
                     [sg.Multiline(data.get('losing'), key='losing', size=(60, 5))]]

    tab_story_progression = [[sg.Text("Story Progression?")],
                             [sg.Multiline(data.get('progression'), key='progression', size=(60, 30))]]

    tab4_art_music = [[sg.Text('Art Style')],
                      [sg.Multiline(data.get('art'),
                                    key='art', size=(60, 15))],
                      [sg.Text('Music and Sounds')],
                      [sg.Multiline(data.get('music'), key='music', size=(60, 15))]]

    tab5_technical = [[sg.Text('Technical Description')],
                      [sg.Multiline(data.get('techical'), key='technical', size=(60, 25))]]

    tab6_marketing = [[sg.Text('General Plan')],
                      [sg.Multiline(data.get('marketing'),
                                    key='marketing', size=(60, 6))],
                      [sg.Text('Demographics')],
                      [sg.Multiline(data.get('demographics'),
                                    key='demographics', size=(60, 7))],
                      [sg.Text('Platforms & Monetization')],
                      [sg.Multiline(data.get('monetization'),
                                    key='monetization', size=(60, 7))],
                      [sg.Text('Localization')],
                      [sg.Multiline(data.get('localization'), key='localization', size=(60, 7))]]

    # main layout of window
    layout = [[sg.TabGroup([[sg.Tab('Project', tab1_layout, key='-mykey-'),
                             sg.Tab('Story', tab2_characters),
                             sg.Tab('Story Progression',
                                    tab_story_progression),
                             sg.Tab('Gameplay 1', tab_gameplay1),
                             sg.Tab('Gameplay 2', tab_gameplay2),
                             sg.Tab('Art-Music', tab4_art_music),
                             sg.Tab('Technical Description', tab5_technical),
                             sg.Tab('Marketing & Funding', tab6_marketing)]],
                           title_color='white',
                           selected_title_color='yellow',
                           tab_location='left')],
              [sg.Button('Save')]
              ]

    # create window
    window = sg.Window('Game Design Document Creator', layout,
                       default_element_size=(12, 1))

    is_dirty = True
    while True:
        event, values = window.read()
        if event == 'Save':
            is_dirty = False
            make_gd(values, template, destination_folder)
            save_json(values, save_file)
            sg.popup_non_blocking(f"Saved to {destination_folder}")
            gdd_status = f"Saved to file {save_file}"

        if event == sg.WIN_CLOSED:           # always,  always give a way out!
            # TODO: dirty flag is now implemented, but not able to not save.
            # if not is_dirty:
            break

        is_dirty = True

    window.close()


def save_json(values, save_file):
    with open(save_file, 'w') as json_save_file:
        json_save_file.write(json.dumps(values))
    json_save_file.close()


def make_gd(data, template, destination_folder):

    output = template

    for d in data.keys():
        if d == 'logoPath':
            if (os.path.isfile(d)):
                file_name = os.path.basename(data.get(d))
                copyfile(data.get(d), os.path.join(destination_folder, file_name))
            else:
                file_name = data.get(d)               
            output = output.replace(f'{{{{{d}}}}}', file_name)
        else:
            output = output.replace(f'{{{{{d}}}}}', data.get(d))

    with open(os.path.join(destination_folder, 'gameDoc.md'), 'w') as dest:
        dest.write(output)
    dest.close()

    # adding HTML version
    html_output = md.markdown(output)

    with open(os.path.join(destination_folder, 'gameDoc.html'), 'w') as dest_html:
        dest_html.write(html_output)

    return True


def load_gdd_values(file_path):
    """Loads the existing gdd values from a json file if they exist"""

    with open(file_path, 'r') as gdd_source_file:
        data = gdd_source_file.read()
    gdd_source_file.close()

    # parse file
    obj = json.loads(data)

    # TODO: add some verification of the json here.

    return obj


def main():
    """main starting point for this program that generates the GDD. This parses args, checks them, and then starts
    the main application. The app will attempt to read in existing content, if found, otherwise it will show starter content.
    Then if the user chooses to save the values, it will make a new file.

    TODO: Make sure that before it saves, it makes a backup of the previous file. """

    data = None
    save_file = 'gameDoc.json'

    # read the command line args.
    parser = argparse.ArgumentParser(
        description='Generate a Game Development Doc (GDD).')
    parser.add_argument('-i', '--input', default='gameDocDefault.json',
                        help='the input file')
    parser.add_argument('-t', '--template', default='design_doc_template.md',
                        help='the markdown content that was created')
    parser.add_argument('-o', '--output', default='output',
                        help='the folder to save the output too')

    args = parser.parse_args()

    # == verify args ==
    template = '# {{name}} Design Doc\n'

    if not os.path.isfile(args.template):
        print(
            'Template file is missing or unreadable. Default Template will be used instead.')
        print(f'Template file: {args.template}')
    else:
        with open(args.template, 'r') as template_file:
            template = template_file.read()
        template_file.close()

    # load existing values
    if os.path.isfile(save_file):
        print(f"Loading Saved Values from {save_file}")
        data = load_gdd_values(save_file)
        if os.path.isfile(args.input):
            print(f'WARNING! Save file will overwrite defaults specified on command line!')
    else:
        if os.path.isfile(args.input):
            print("Loading Values")
            data = load_gdd_values(args.input)
        else:
            print("No existing settings to load.")
            data = {}

    if not os.path.isdir(args.output):
        os.makedirs(args.output)

    edit_and_make_game_doc(data, template, save_file, args.output)


if __name__ == "__main__":

    main()
