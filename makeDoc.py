import PySimpleGUI as sg
import argparse
import json
import os.path


def get_data(data):

    sg.theme('dark grey 9')

    # Define the window's contents
    tab1_layout = [[sg.Text("What's your game name?")],  # Part 2 - The Layout
                   [sg.Input(data.get('name'), key='name')],
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

    layout = [[sg.TabGroup([[sg.Tab('Project', tab1_layout, key='-mykey-'),
                             sg.Tab('Story', tab2_characters),
                             sg.Tab('Story Progression',
                                    tab_story_progression),
                             sg.Tab('Gameplay 1', tab_gameplay1),
                             sg.Tab('Gameplay 2', tab_gameplay2),
                             sg.Tab('Art-Music', tab4_art_music),
                             sg.Tab('Technical Description', tab5_technical),
                             sg.Tab('Marketing & Funding', tab6_marketing)]],
                           key='-group2-', title_color='white',
                           selected_title_color='yellow', tab_location='left')],
              [sg.Button('Save')]]

    window = sg.Window('My window with tabs', layout,
                       default_element_size=(12, 1))

    is_dirty = True
    while True:
        event, values = window.read()
        sg.popup_non_blocking(event, values)
        if event == 'Save':
            is_dirty = False
            make_gd(values)

        if event == sg.WIN_CLOSED:           # always,  always give a way out!
            # TODO: Implement a real dirty flag that updates when values are changed above.
            break

    window.close()


def make_gd(data):
    print(data)


def load_gdd_values(file_path):
    """Loads the existing gdd values from a json file if they exist"""

    with open(file_path, 'r') as myfile:
        data = myfile.read()

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

    # read the command line args.
    parser = argparse.ArgumentParser(
        description='Generate a Game Development Doc (GDD).')
    parser.add_argument('-i', '--input', default='gameDoc.json',
                        help='the input file')
    parser.add_argument('-o', '--output', default='gameDoc.md',
                        help='the markdown content that was created')

    args = parser.parse_args()

    # == verify args ==
    # nothing to verify.

    # load existing values
    if os.path.isfile(args.input):
        print("Loading Values")
        data = load_gdd_values(args.input)
    else:
        print("No existing settings to load.")

    data = get_data(data)


if __name__ == "__main__":

    main()
