import sys
import os
import subprocess

COLOR_BLANK = "\033[0;0m"
COLOR_YELLOW = "\033[1;38;2;255;255;51m"
COLOR_RED = "\033[1;38;2;255;0;0m"
COLOR_BLUE = "\033[1;38;2;51;255;255m"
COLOR_GREEN = "\033[1;38;2;20;255;3m"

# If system is Windows
if sys.platform[:3] == 'win':
    import msvcrt


    def get_key():
        key = msvcrt.getch()
        return key

# If system is Linux
elif sys.platform[:3] == 'lin':
    import termios, sys, os

    TERMIOS = termios

    def get_key():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
        new[6][TERMIOS.VMIN] = 1
        new[6][TERMIOS.VTIME] = 0
        termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
        c = None
        try:
            c = os.read(fd, 1)
        finally:
            termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
        return c


def clear():
    """
    Will clear the terminal if it can determine the base OS method for clearing. If the terminal cannot be cleared,
    just print 120 blank lines.
    """
    if os.name in ('nt', 'dos'):
        subprocess.call("cls")
    elif os.name in ('linux', 'osx', 'posix'):
        subprocess.call("clear")
    else:
        print("\n" * 120)


def output_handler(input_string, map_width, position='left'):
    """
    Output handler that will return a string with appropriate spacing to either, left align, right align, or center.
    Due to the addition of colors, the length of output string needs to vary in its spacing to account for the individual
    color selectors that are added to the total len(str).
    @return: str()
    """
    if position == 'left':
        return input_string
    elif position == 'center':
        color_size = 0
        input_size = len(input_string)
        colors = [COLOR_BLANK, COLOR_YELLOW, COLOR_BLUE, COLOR_RED, COLOR_GREEN]
        for color in colors:
            if input_string.count(color) > 0:
                color_size += input_string.count(color) * len(color)
        centered_output = ((' ' * round(((map_width * 3) - (input_size - color_size)) / 2)) + input_string)
        return centered_output
    elif position == 'right':
        color_size = 0
        input_size = len(input_string)
        colors = [COLOR_BLANK, COLOR_YELLOW, COLOR_BLUE, COLOR_RED, COLOR_GREEN]
        for color in colors:
            if input_string.count(color) > 0:
                color_size += input_string.count(color) * len(color)
        right_output = ((' ' * round(((map_width * 3) - (input_size - color_size)))) + input_string)
        return right_output
    else:
        raise ValueError('Invalid position argument. Only left, center, right permitted.')
