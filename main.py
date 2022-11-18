import tkinter
import customtkinter

customtkinter.set_appearance_mode(
    "Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue")  # Themes: "blue" (standard), "green", "dark-blue"


class RubiksApp(customtkinter.CTk):
    WIDTH = 1120
    HEIGHT = 720

    color_details = [
        {'color_name': 'red', 'color_reference': 'r', 'main_color': 'red',
         'hover_color': '#b00502'},
        {'color_name': 'blue', 'color_reference': 'b', 'main_color': 'blue',
         'hover_color': '#19158a'},
        {'color_name': 'yellow', 'color_reference': 'y', 'main_color': 'yellow',
         'hover_color': '#91991f'},
        {'color_name': 'orange', 'color_reference': 'o', 'main_color': 'orange',
         'hover_color': '#a16312'},
        {'color_name': 'green', 'color_reference': 'g', 'main_color': 'green',
         'hover_color': '#0e5207'},
        {'color_name': 'white', 'color_reference': 'w', 'main_color': 'white',
         'hover_color': '#afb8ae'},
        {'color_name': 'default', 'color_reference': 'd',
         'main_color': '#1f6aa5', 'hover_color': '#1f6aa5'}
    ]
    face_frames = {'white_face': None,
                        'orange_face': None,
                        'green_face': None,
                        'red_face': None,
                        'blue_face': None,
                        'yellow_face': None}

    color_palette_buttons = {
                            'red_button': None,
                            'blue_button': None,
                            'yellow_button': None,
                            'orange_button': None,
                            'green_button': None,
                            'white_button': None
                            }
    check_box_details = [
                        {'name': 'cross', 'check_box': None, 'text': 'Cross', 'variable': None, 'required_states': [[0, 0, 0], [1, 0, 0]]},
                        {'name': 'f2l', 'check_box': None, 'text': 'F2L  ', 'variable': None, 'required_states': [[1, 0, 0], [1, 1, 0]]},
                        {'name': 'oll', 'check_box': None, 'text': 'OLL  ', 'variable': None, 'required_states': [[1, 1, 0], [1, 1, 1]]}
                        ]
    edge_indices = {'top': None, 'middle': None, 'buttom': None}

    corner_indices = {'top': None, 'buttom': None}

    cube_buttons = None

    coloring_reference = None

    selected_color = None

    start_color = None

    def __init__(self):
        super().__init__()

        self.title("Rubik's App")
        self.geometry(f"{RubiksApp.WIDTH}x{RubiksApp.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # =========== create frames ===================

        # configure grid layout (2x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.coloring_toggles_frame = customtkinter.CTkFrame(master=self,
                                                             width=180,
                                                             corner_radius=0)
        self.coloring_toggles_frame.grid(row=0, column=0, sticky='nswe',
                                         rowspan=2)

        self.color_palette_frame = customtkinter.CTkFrame(master=self)
        self.color_palette_frame.grid(row=0, column=1, sticky='nswe', padx=20,
                                      pady=20)

        self.cube_frame = customtkinter.CTkFrame(master=self)
        self.cube_frame.grid(row=1, column=1, sticky='nswe', padx=20, pady=20)

        # ================ coloring toggles frame ===================

        # configure grid layout (1x6)
        self.coloring_toggles_frame.grid_columnconfigure(0, weight=1)
        self.coloring_toggles_frame.grid_rowconfigure(5, weight=1)

        self.start_color_menu_var = customtkinter.StringVar(
            value="Start From")  # set initial value
        self.start_color_menu = customtkinter.CTkOptionMenu(
            master=self.coloring_toggles_frame,
            values=["White",
                    "Yellow",
                    "Green",
                    "Blue",
                    "Orange",
                    "Red"],
            command=self.start_color_menu_callback,
            variable=self.start_color_menu_var)
        self.start_color_menu.grid(row=0, column=0, padx=20, pady=10)

        self.create_check_boxes()

        # =============== color palette frame ==============

        # configure grid layout (6x1)
        self.color_palette_frame.grid_columnconfigure(5, weight=1)
        self.color_palette_frame.grid_rowconfigure(0, weight=1)

        # add buttons for color palette argument = list of dictionaries
        self.create_color_palette()

        # ============== cube frame ========================

        # configure grid layout (4x3)
        self.color_palette_frame.grid_columnconfigure(3, weight=1)
        self.color_palette_frame.grid_rowconfigure(2, weight=1)

        # add cube face frames
        self.create_cube_face_frames()

        # add tiles/buttons to each face
        self.cube_buttons = self.create_cube_representation(
            None)  # creates an empty cube with default value None
        self.add_tiles_to_face_frames()

        self.coloring_reference = self.create_cube_representation(
            'd')  # creates an empty cube with default value d

        self.add_empty_lists_to_indices_dictionary(self.edge_indices,
                                                   self.corner_indices)

        self.create_edge_indices()
        self.create_corner_indices()

    def create_cube_representation(self, default_value):
        '''Creates a list with a default value in a way that represents the cube.'''
        faces, rows, columns = (6, 3, 3)
        return [[[default_value for column in range(columns)] for row in range(rows)] for face in range(faces)]

    def create_cube_copy(self, cube):
        '''Returns a copy of the cube representation passed in.'''
        return [[row[:] for row in face[:]] for face in cube]

    def add_empty_lists_to_indices_dictionary(self, *indices_dictionaies):
        '''Adds 4 empty lists to each section of the indices dictionary.'''
        for dictionary in indices_dictionaies:
            for key in dictionary.keys():
                dictionary[key] = [[] for x in range(4)]

    def create_edge_indices(self):
        '''Creates the indices for each edge on the cube using modulus to create
        a specific index sequence.'''

        # top edge indices sequencies
        # -----sequence 1------sequence 2-----
        #       1 0 1           0 1 0
        #       2 0 1           0 2 1
        #       3 0 1           0 1 2
        #       4 0 1           0 0 1

        # middle edge indices sequencies
        # -----sequence 3------sequence 4-----
        #       1 1 0           4 1 2
        #       1 1 2           2 1 0
        #       2 1 2           3 1 0
        #       3 1 2           4 1 0

        # buttom edge indices sequencies
        # -----sequence 6------sequence 6-----
        #       1 2 1           5 1 0
        #       2 2 1           5 0 1
        #       3 2 1           5 1 2
        #       4 2 1           5 2 1

        for index in range(4):
            self.edge_indices['top'][index].append(
                [index + 1, 0, 1])  # creates sequence 1
            self.edge_indices['top'][index].append(
                [0, 5 % (index + 2), 5 % (index + 1)])  # creates sequence 2

            self.edge_indices['middle'][index].append(
                [(index - 1) % (index + 1) + 1, 1,
                 2 % (index + 2)])  # creates sequence 3
            self.edge_indices['middle'][index].append([4 - ((3 - index) % 3), 1,
                                                       abs(2 % (
                                                                   index + 2) - 2)])  # creates sequence 4

            self.edge_indices['buttom'][index].append(
                [index + 1, 2, 1])  # creates sequence 5
            self.edge_indices['buttom'][index].append(
                [5, abs(index - 1), 5 % (index + 1)])  # creates sequence 6

    def create_corner_indices(self):
        '''Creates the indices for each corner on the cube using modulus to create
        a specific index sequence.'''

        # top corner indices sequencies
        # -----sequence 1------sequence 2------sequence 3-----
        #       0 0 0           1 0 0           4 0 2
        #       0 0 2           4 0 0           3 0 2
        #       0 2 2           3 0 0           2 0 2
        #       0 2 0           2 0 0           1 0 2

        # buttom corner indices sequencies
        # -----sequence 4------sequence 5------sequence 6-----
        #       5 0 0           1 2 2           2 2 0
        #       5 0 2           2 2 2           3 2 0
        #       5 2 2           3 2 2           4 2 0
        #       5 2 0           4 2 2           1 2 0

        for index in range(4):
            self.corner_indices['top'][index].append([0, 2 % (index + 1), 2 * (
                        index ** 2) % 3])  # creates sequence 1
            self.corner_indices['top'][index].append(
                [(5 - index) % (4 + index), 0, 0])  # creates sequence 2
            self.corner_indices['top'][index].append(
                [4 - index, 0, 2])  # creates sequence 3

            self.corner_indices['buttom'][index].append([5, 2 % (index + 1),
                                                         2 * (
                                                                     index ** 2) % 3])  # creates sequence 4
            self.corner_indices['buttom'][index].append(
                [index + 1, 2, 2])  # creates sequence 5
            self.corner_indices['buttom'][index].append(
                [(index + 2) % (7 - index), 2, 0])  # creates sequence 6

    def create_color_palette(self):
        '''Creates and adds buttons to the color_palette_frame according to the
        amount of items in the parameter colors (In this case 6). This must be a list of
        dictionaries containg the main color and the hover color.'''
        row = 0
        column = 0
        button_keys = list(
            self.color_palette_buttons.keys())  # creates a list of the keys in color_palette_buttons
        colors = self.order_colors(
            list("rbyogw"))  # returns a ordered copy of the color details

        for color in colors:
            button = customtkinter.CTkButton(master=self.color_palette_frame,
                                             text='',
                                             fg_color=(color['main_color'],
                                                       color['hover_color']),
                                             hover_color=color['hover_color'],
                                             state="disabled",
                                             command=lambda
                                                 color=color: self.color_palette_button_event(
                                                 color))
            button.grid(row=row, column=column, pady=5, padx=5)
            # adds the button instance to the dictionary using the button_keys list and the column as the index
            self.color_palette_buttons[button_keys[column]] = button

            column += 1

    def color_palette_button_event(self, color):
        '''Sets the value of the attribute selected color to color.'''
        self.selected_color = color

    def create_cube_face_frames(self):
        '''Creates the layout of the cube faces using frames.'''
        cube_layout = [
            ['space', 'frame', 'space', 'space'],
            ['frame'] * 4,
            ['space', 'frame', 'space', 'space']
        ]
        face_keys = list(
            self.face_frames.keys())  # creates a list of the keys in cube_face_frames
        face_index = 0

        for row in range(3):
            for column in range(4):
                if cube_layout[row][column] == 'frame':
                    face = customtkinter.CTkFrame(master=self.cube_frame)
                    face.grid(row=row, column=column)
                    # adds the frame instance to the dictionary using the cube_face_keys list and the face_index
                    self.face_frames[face_keys[face_index]] = face
                    face_index += 1

    def add_tiles_to_face_frames(self):
        '''Adds the tiles/buttons to each face frame.'''
        size = 60
        face_index = 0

        for face in self.face_frames.values():  # loops through the instances of the face frames
            for row in range(3):
                for column in range(3):
                    tile = customtkinter.CTkButton(master=face,
                                                   text='',
                                                   width=size,
                                                   height=size,
                                                   command=lambda
                                                       face_index=face_index,
                                                       row=row,
                                                       column=column: self.tile_button_event(
                                                       face_index, row, column))
                    tile.grid(row=row, column=column, padx=3, pady=3)

                    self.cube_buttons[face_index][row][
                        column] = tile  # Adds the button instance to the list representing the cube

            face_index += 1

    def tile_button_event(self, face_index, row_index, colum_index):
        '''Colors an individual tiles according to the arguments passed in.'''
        if self.selected_color != None:  # ensures a color has been selected.
            main_color = self.selected_color["main_color"]
            hover_color = self.selected_color["hover_color"]

            self.coloring_reference[face_index][row_index][colum_index] = \
            self.selected_color[
                "color_reference"]  # adds the reference color to the cubes coloring reference
            self.cube_buttons[face_index][row_index][colum_index].configure(
                fg_color=main_color,
                hover_color=hover_color)  # changes the tile/button color

    def color_centre_tiles(self, start_color):
        '''Colors the centre tile of each face relative to the rotation details.'''
        default_color_order = list('wogrby')  # sets a defual order of colors
        # contains rotation details for each color if they were to be the start color
        rotation_details = {'yellow': ('X', 0),
                            'white': ('X', 2),
                            'green': ('X', 1, -1),
                            'blue': ('X', 1),
                            'orange': ('Z', 1, -1),
                            'red': ('Z', 1)
                            }
        coloring_reference_copy = self.create_cube_copy(self.coloring_reference)

        for key in rotation_details.keys():
            if key == start_color:
                # passes in the default color order and returns a list after the rotations have been performed
                color_order = self.cube_rotation(default_color_order,
                                                 *rotation_details[key])
                break

        colors = self.order_colors(
            color_order)  # returns a copy of the color details in order

        for face_index in range(6):
            main_color = colors[face_index]["main_color"]
            hover_color = colors[face_index]["hover_color"]
            # adds the color reference to the centre of each face
            coloring_reference_copy[face_index][1][1] = colors[face_index][
                'color_reference']
            # passes in the coloring reference copy then colors the tiles
        self.color_tiles(coloring_reference_copy)

    def order_colors(self, order):
        '''Returns a ordered copy of the color details.'''
        color_list = self.color_details[:6]  # creates the copy

        for index in range(len(order)):
            # Loops through color list until all the values in the list order, equal the coresponding color details
            for color in color_list:
                if order[index] == color['color_reference']:
                    order[
                        index] = color  # turns the color reference to the color details
                    color_list.remove(color)  # removes that color
        return order

    def color_tiles(self, copy_of_coloring_reference):
        '''Uses a modified copy of the cube coloring reference list, colors the
        tiles and then updates the coloring reference to the values in the copy
        which is the current state.'''
        for face in range(6):
            for row in range(3):
                for column in range(3):
                    # colors a tile only if the value has been modified
                    if copy_of_coloring_reference[face][row][column] != \
                            self.coloring_reference[face][row][column]:
                        color_reference = copy_of_coloring_reference[face][row][
                            column]  # gets the color reference at specific position
                        color = self.get_dictionary_details(self.color_details,
                                                            color_reference)  # uses the refernce to get color details

                        main_color = color['main_color']
                        hover_color = color['hover_color']

                        self.cube_buttons[face][row][column].configure(
                            fg_color=main_color,
                            hover_color=hover_color)  # updates the color

        self.coloring_reference = copy_of_coloring_reference  # updates the coloring reference

    def get_centre_tile_colors(self):
        '''Returns a list of all the centre tile color reference.'''
        return [face[1][1] for face in self.coloring_reference]

    def cube_rotation(self, cube_state, X_Y_Z, amount=1, prime=1):
        '''Simulates a rotation of the cube.'''

        # rotation cordinates
        X = [[0, 2], [2, 5], [5, 4]]
        Y = [[1, 2], [2, 3], [3, 4]]
        Z = [[0, 1], [1, 5], [5, 3]]

        if X_Y_Z == 'X':
            rotation = X
        elif X_Y_Z == 'Y':
            rotation = Y
        elif X_Y_Z == 'Z':
            rotation = Z

        for number_of_rotations in range(amount):
            # if prime equals -1 the values in the list are reversedc
            for r in rotation[::prime]:
                r = r[::prime]
                cube_state[r[0]], cube_state[r[1]] = cube_state[r[1]], \
                                                     cube_state[r[
                                                         0]]  # swaps the values in the cube

        return cube_state

    def display_cube(self, cube_state):
        '''Displays the cube's values line by line in a neat manner.'''

        for stage in range(1, 4):  # 3 stages of displaying
            if stage in (1, 3):
                # set face index according to the stage
                if stage == 1:
                    face = 0
                else:
                    face = 5

                for row in range(3):
                    v1, v2, v3 = cube_state[face][row]
                    print(f"{v1:>8} {v2} {v3}")
            else:
                print()
                for row in range(3):
                    row_display = ''
                    for face in cube_state[1: 5]:
                        v1, v2, v3 = face[row]
                        row_display += f"{v1} {v2} {v3}  "
                    print(row_display)
                print()

    def create_check_boxes(self):
        '''Creates check boxes using a list of dictionaries that contains the
        check box details.'''
        row = 1  # we set the row to 1 becuase the frame that contains the check boxes already has one item
        for index in range(
                len(self.check_box_details)):  # the number of loops depend on the length of the list
            check_box = self.check_box_details[index]

            check_box['variable'] = tkinter.IntVar()  # add an integer variable
            # add an check box instance
            check_box['check_box'] = customtkinter.CTkCheckBox(
                master=self.coloring_toggles_frame,
                text=check_box['text'],
                state=tkinter.DISABLED,
                command=lambda name=check_box['name'],
                               variable=check_box['variable'],
                               required_states=check_box[
                                   'required_states']: self.checkbox_event(name,
                                                                           variable,
                                                                           required_states),
                variable=check_box['variable'],
                onvalue=1,
                offvalue=0)
            check_box['check_box'].grid(row=row, column=0, padx=20, pady=10)
            row += 1

    def change_check_box_states(self, required_states):
        '''Changes the state of the check boxes according to a list of required
        states and returns the required states list which is the current states
        after the for loop has ended.'''

        # returns a list of the check boxes variables.
        check_box_variables = self.get_dictionary_details(
            self.check_box_details, return_value='variable')
        # creates a list of binary values representing the current states
        current_states = [variable.get() for variable in check_box_variables]

        # returns the check box instances
        check_boxes = self.get_dictionary_details(self.check_box_details,
                                                  return_value='check_box')

        for index in range(len(current_states)):
            current, required = current_states[index], required_states[index]
            if current != required:
                # if the check box state is 0/off it is set to 1/on
                if current == 0:
                    check_boxes[index].select()
                # if the check box state is 1/on it is set to 0/off
                elif current == 1:
                    check_boxes[index].deselect()

        return required_states

    def color_tiles_according_to_check_box_states(self, check_box_states):
        '''With a list of the check box states this function calls a function
        to color or remove color from a section of the cube.'''

        # retuns the check box's names that are used to identify what sections need to be colored.
        check_box_names = self.get_dictionary_details(self.check_box_details,
                                                      return_value='name')

        for index in range(len(check_box_states)):
            # if the check box state is 0/off color is removed from the tiles.
            if check_box_states[index] == 0:
                self.check_box_tile_coloring(check_box_names[index], 'remove')

            # if the check box state is 1/on the tiles are colored.
            elif check_box_states[index] == 1:
                self.check_box_tile_coloring(check_box_names[index], 'add')

    def get_dictionary_details(self, detail_dictionaries, reference_value=None, return_value=None):
        '''This function can be used to return specific details of a dictionary using a
        reference value (actual value we have) and a return value (key of the value we want).'''

        # if a reference value is not passed in, a list of all the values in the
        # list of dictionaries with the key return value is returned.
        if reference_value == None:
            return [details[return_value] for details in detail_dictionaries]
        else:
            for item in detail_dictionaries:
                if reference_value in item.values():
                    # if a return value is not passed in, the dictionary containing
                    # the reference value is returned.
                    if return_value == None:
                        return item
                    # if both the reference value and the return value are passed
                    # in the specific value in the dictionary is returned.
                    else:
                        return item[return_value]

    def checkbox_event(self, checkbox_name, variable, required_states):
        '''Calls a coloring function and a function that changes the check box
        states, when any of the check boxes is clicked.'''

        state = variable.get()  # returns 0 or 1 (represents the state: 0 = off, 1 = on)

        # changes the check box states to their required state
        specific_required_states = self.change_check_box_states(
            required_states[state])
        # colors sections on the cube using a list of states
        self.color_tiles_according_to_check_box_states(specific_required_states)

    def start_color_menu_callback(self, start_color):
        self.start_color = start_color.lower()
        self.color_centre_tiles(self.start_color)

    def cross_checkbox_event(self):
        print(self.cross_check_var.get())
        # if self.cross_check_var.get() == 1:
        #     self.cube_coloring_reference[]

    def f2l_checkbox_event(self):
        print(self.f2l_check_var.get())

    def oll_checkbox_event(self):
        print(self.oll_check_var.get())

    def color_cross_tiles(self):
        # fix this
        self.cube_coloring_reference[1][2][1] = 'o'
        self.cube_coloring_reference[2][2][1] = 'y'
        self.cube_coloring_reference[3][2][1] = 'r'
        self.cube_coloring_reference[4][2][1] = 'w'
        self.cube_coloring_reference[5][0][1] = 'b'
        self.cube_coloring_reference[5][1][2] = 'b'
        self.cube_coloring_reference[5][2][1] = 'b'
        self.cube_coloring_reference[5][1][0] = 'b'

    def cube_rotation(self, cube_state, X_Y_Z, amount, prime=1):
        '''Rotates the cube. prime = 1 or -1 if -2 the prime rotation is performed.'''

        # rotation cordinates
        X = [[0, 2], [2, 5], [5, 4]]
        Y = [[1, 2], [2, 3], [3, 4]]
        Z = [[0, 1], [1, 5], [5, 3]]

        if X_Y_Z == 'X':
            rotation = X
        elif X_Y_Z == 'Y':
            rotation = Y
        elif X_Y_Z == 'Z':
            rotation = Z

        # creates a slice, inverts list
        for n in range(amount):
            for r in rotation[::prime]:
                r = r[::prime]
                cube_state[r[0]], cube_state[r[1]] = cube_state[r[1]], cube_state[r[0]]

        return cube_state

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = RubiksApp()
    app.mainloop()
