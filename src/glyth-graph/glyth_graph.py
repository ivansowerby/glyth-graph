import math

class graph_basic:

    def __init__(self, resolution: str, blank_glyth: str = None) -> None:
        """
        The constructor of the class to create an attached object, setup the canvas array with the arguements given, both the size and blank (background) glyth

        - resolution: the width by the height of the canvas measured in character glyths | 'x'.join([width, height])
        - blank_glyth: the background glyth used for spacing the graph
        """
        if blank_glyth == None:
            blank_glyth = '  '

        #Define class variables:
        self.blank_glyth = str(blank_glyth)
        self.min, self.max = 0, 0
        self.width, self.height = int(resolution[:resolution.find('x')]), int(resolution[resolution.find('x') + 1:])
        #Print Width and Height parameters:
        print(''.join(['\nWidth: ', str(self.width), ' | Height: ', str(self.height)]))

        #Define the 2D list canvas and fill with the blank glyth:
        self.canvas = [list(self.blank_glyth * self.width) for _ in range(0, self.height)]

    def format_equation(self, equation: str) -> str:
        """
        Format the graph equation such that all unecessary characters are removed to be processed, this includes removal of 'y' and '=' if given an equation to form an expression and all ' ' (spaces) present

        - equation: the mathematical equation of the graph going to be drawn
        """
        #Format the equation:
        equation = equation.replace(' ', '')
        if equation.find('=') != -1:
            equation = equation[equation.find('=') + 1:]
        
        return equation

    def y_bounds(self, equation: str, x_range: tuple) -> tuple:
        """
        Calculate the upper and lower bounds in the y-axis of a graph equation between the given x-axis range, to be used later for mapping positions

        - equation: the mathematical equation of the graph going to be drawn
        - x_range: a tuple of the x-axis range between which the graph will be used, all outside this is unnecessary
        """
        #Split the tuple element:
        range_from, range_to = x_range
        #Format the equation if required:
        if equation.find('=') != -1 or equation.find(' ') != -1:
            equation = self.format_equation(equation)

        #Calculate the Minimum and Maximum of the range:
        x, min, max = range_from, int(), int()
        while x <= range_to:
            y = eval(equation)
            if y < min:
                min = y
            elif y > max:
                max = y
            x += (range_to - range_from) / self.width

        #print(''.join(['y-axis Range | Min: ', str(min), ' | Max: ', str(max)]))
        return (min, max)

    def draw_graph(self, char_x: int, equation: str, glyth: str, x_range: tuple, y_bounds: tuple = None) -> list:
        """
        Draw a glyth onto the canvas array dependent on given arguments in relation to the graph equation, including the x-axis range and y-axis bounds of the 2-dimensional section of the graph and character position along the canvas

        - char_x: the x_axis glyth position of the canvas, such that it starts to the leftmost position (0) to the rightmost (canvas width - 1) | 0 <= char_x < canvas width
        - equation: the mathematical equation of the graph going to be drawn
        - glyth: the character/s to be drawn onto the canvas at the calculated coordinate relative to the graph equation
        - x_range: a tuple of the x-axis range between which the graph will be used, all outside this is unnecessary | (range_from, range_to)
        - y_bounds: a tuple of the y-axis bounds for the x-axis region of the graph, including both the minimum and maximum values | (min, max)
        """
        #Check for char_x within canvas width bounds:
        if char_x > self.width or char_x < 0:
            print(''.join(["Error: char_x argument is out of the graph's allocated bounds: Min: 0 | Max: ", str(self.width)]))
            exit()

        #Format the equation if required:
        if equation.find('=') != -1 or equation.find(' ') != -1:
            equation = self.format_equation(equation)
        #Calculate y-axis bounds for the equation within the given range if required:
        if y_bounds == None:
            y_bounds = self.y_bounds(equation, x_range)

        #Split the tuple elements:
        min, max = y_bounds
        range_from, range_to = x_range
        
        #Calculate the mapped y-axis char_x:
        x = (range_to - range_from) * char_x / (self.width - 1) + range_from
        char_y = (self.height - 1) - round((self.height - 1) * (eval(equation) + abs(min)) / (max - min))
        #print(''.join(['Coordinate (x, y): (', str(x), ', ', str(eval(equation)), ') | (', str(char_x), ', ', str(y_mapped), ')']))

        #Manpulate the canvas at a coordinate to be the glyth:
        self.canvas[char_y][char_x] = glyth

        return self.canvas

    def clear_canvas(self) -> None:
        """
        Clear the canvas by replacing all indicies in the array with the blank glyth assigned in the constructor, removing any graphs drawn
        """
        for y_index in range(0, self.height):
            for x_index in range(0, self.width):
                self.canvas[y_index][x_index] = self.blank_glyth

    def print_canvas(self, clear: bool = None) -> None:
        """
        Pretty print the canvas array into equal rows of the set width with newline character moving to the next row, as each index is printed incrementally

        - clear: a boolean value (either True or False) whether to clear the each canvas array index after printing the index | True or False
        """
        for y_index in range(0, self.height):
            for x_index in range(0, self.width):
                print(str(self.canvas[y_index][x_index]), end = '')
                if clear == True and self.canvas[y_index][x_index] != self.blank_glyth:
                    self.canvas[y_index][x_index] = self.blank_glyth
            print()