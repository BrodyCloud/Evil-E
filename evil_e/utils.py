import sys
import subprocess

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


# TODO Maybe move to displays
def player_death(attacker, player):
	clear()
	print("Death Message ;(")
	print(f"{attacker.name} Killed Player {player.name}")
	exit()