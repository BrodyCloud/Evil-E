import sys
import subprocess

COLOR_BLANK = "\033[0;0m"
COLOR_YELLOW = "\033[1;38;2;255;255;51m"
COLOR_RED = "\033[1;38;2;255;0;0m"
COLOR_BLUE = "\033[1;38;2;51;255;255m"
COLOR_GREEN = "\033[1;38;2;20;255;3m"

if sys.platform[:3] == 'win':
	import msvcrt

	def get_key():
		key = msvcrt.getch()
		return key

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
	if os.name in ('nt', 'dos'):
		subprocess.call("cls")
	elif os.name in ('linux', 'osx', 'posix'):
		subprocess.call("clear")
	else:
		print("\n" * 120)


# TODO FINISH OUT RIGHT DISPLAY
def output_handler(input_string, map_width, position='left'):
	if position == 'left':
		return input_string
	elif position == 'center':
		input_size = len(input_string)
		color_size = 0
		colors = [COLOR_BLANK, COLOR_YELLOW, COLOR_BLUE, COLOR_RED, COLOR_GREEN]
		for color in colors:
			if input_string.count(color) > 0:
				color_size += input_string.count(color) * len(color)
		centered_output = ((' ' * round(((map_width * 3) - (input_size - color_size)) / 2)) + input_string)
		return centered_output
	elif position == 'right':
		pass
	else:
		raise ValueError('Invalid position argument. Only left, center, right permitted.')
