"""
This program controls the admin commands in the game.
Also any menu navigations.


Note: SpecimenImplant has a player's ID called "Sample #: 34225234"
Can have user input their sample #


"""

from arkdriver import ApplicationDriver
from pywinauto import keyboard
from pathlib import Path
from time import sleep
import json


class ArkDriver:
    def __init__(self, application=None):
        if application is None:
            application = ApplicationDriver()
            application.start()
        self.app = application
        self.pane = application.pane

    def click_start(self):
        """ Clicks on Start """
        coords = self.app.locate_button_by_image('intro_menu', 'start_template')
        self.app.click(coords=coords)

    def click_join_ark(self):
        """ Clicks on the Join Ark button """
        coords = self.app.locate_button_by_image('main_menu', 'join_ark_template')
        self.app.click(coords=coords)

    def click_back(self):
        coords = self.app.locate_button_by_image('main_menu', 'back_template')
        self.app.click(coords=coords)

    def __click_search(self):
        """ Clicks on the Search text input """
        coords = self.app.locate_button_by_image('session_list', 'search_template')
        self.app.click(coords=coords)

    def __type_search(self, string):
        """ Types into the input text """
        keyboard.send_keys(string, pause=0.5)

    def click_first_search_result(self):
        """ Clicks onto the first item in the list """
        left, top, right, bottom = self.app.sides(self.pane)
        unit = ((bottom - top) // 30)
        start_top = top + (unit * 7)
        start_left = left + ((right - left) // 2)
        self.app.set_focus()
        self.app.click((start_left, start_top))

    def click_refresh(self):
        """ Clicks on Refresh button """
        coords = self.app.locate_button_by_image('session_list', 'refresh_template')
        self.app.click(coords=coords)

    def search(self, string):
        self.__click_search()
        self.__type_search(string)

    def click_join(self):
        """ Clicks on the Join button """
        coords = self.app.locate_button_by_image('session_list', 'join_template')
        self.app.click(coords=coords)

    def click_join_last_played_session(self):
        left, top, right, bottom = self.app.sides(self.pane)
        start_top = bottom - ((bottom - top) // 8)
        unit = ((right - left) // 5)
        start_left = left + (unit * 2)
        self.app.set_focus()
        self.app.click((start_left, start_top))

    def click_cancel(self):
        coords = self.app.locate_button_by_image('session_list', 'cancel_template')
        self.app.click(coords=coords)

    def open_players_list(self):
        """ In spectator mode, lists all current players """
        self.app.set_focus()
        sleep(1)
        self.app.send_key_ctrl_n()

    def close_players_list(self):
        """ Closes the players list window """
        coords = self.app.locate_button_by_image('player_list', 'close_template')
        self.app.click(coords=coords)

    def save_players_list(self):
        """ Stores the list of all players """
        # TODO: Machine learning and OCR to get the text list
        pass

    def close_admin_menu(self):
        """ Closes the admin menu window """
        coords = self.app.locate_button_by_image('admin_menu', 'close_template')
        self.app.click(coords=coords)

    def resume_pause_menu(self):
        """ Closes the pause menu window """
        coords = self.app.locate_button_by_image('pause_menu', 'close_template')
        self.app.click(coords=coords)

    def close_pause_menu(self):
        """ Closes the pause menu window """
        coords = self.app.locate_button_by_image('pause_menu', 'resume_template')
        self.app.click(coords=coords)

    def exit_to_main_menu(self):
        """ Exits to the main menu """
        coords = self.app.locate_button_by_image('pause_menu', 'exit_to_main_menu_template')
        self.app.click(coords=coords)

    def target_player_name(self, name):
        """ While in spectator mode, find player and lock onto them """
        # TODO: Machine learning and OCR
        # TODO: Dynamically recognize a list and click to them
        pass

    def scrape_player_data(self):
        """ Gather player blueprint_data (e.g. player_id and tribe_id) """
        # TODO: machine learning to scrape images text and OCR
        pass

    def teleport_default(self):
        """ Teleport to a hidden location """
        # TODO: find a hidden place with x, y, z coodinates
        pass

    def copy_coords(self):
        """ Copies your current coordinates and rotation to clipboard in the form x,y,z Yaw pitch """
        self.write_console('ccc')

    def save_current_coordinates(self, map, name):
        """ Stores the coordinates into file with a name
        :param name: str, name for the coordinates
        """
        data = {'center': {}, 'gen1': {}, 'gen2': {}, 'island': {},
                'scortched': {}, 'ragnarok': {}, 'extinction': {}, 'aberration': {}}
        if map not in data:
            raise NotImplemented("'{}' isn't part of the map list: {}".format(map, data.keys()))
        self.copy_coords()
        coords = [float(val) for val in self.app.get_from_clipboard().split()]
        file_path = Path.cwd() / Path('../logs/saved_coordinates.json')
        if file_path.exists():
            with open(file_path, 'r') as r:
                data = json.load(r)

        cc = {'x': coords[0], 'y': coords[1], 'z': coords[2], 'yaw': coords[3], 'pitch': coords[4]}
        data[map][name] = cc
        with open(file_path, 'w') as w:
            json.dump(data, w)

    def write_console(self, *commands):
        self.app.set_focus()
        sleep(1)
        self.app.save_to_clipboard_text('|'.join(['{}'.format(command) for command in commands]) + '|')
        self.app.send_key_tab()
        self.app.send_key_paste()
        self.app.send_key_enter()

    def write_console_args(self, args: list, *command_formats):
        """ player_ids is a list of player ids
            command_formats are commands in format form: "cheat GiveItemTO {} Pickaxe 1 1"
                where there is a '{}' in the string
         """
        commands = []
        for str_format in command_formats:
            commands.append(str_format.format(*args))
        self.write_console(*commands)

