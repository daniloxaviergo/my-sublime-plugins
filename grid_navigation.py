import sublime
import sublime_plugin
import re
import os
import json

def focusNextVertical(win):
	active_group = win.active_group()
	num_groups = win.num_groups()

	if num_groups == 2:
		if active_group == 0:
			win.focus_group(1)

		if active_group == 1:
			win.focus_group(0)

	if num_groups == 4:
		if active_group == 2:
			win.focus_group(0)

		if active_group == 0:
			win.focus_group(2)

		if active_group == 1:
			win.focus_group(3)

		if active_group == 3:
			win.focus_group(1)

def focusNextHorizontal(win):
	active_group = win.active_group()
	num_groups = win.num_groups()

	if num_groups == 2:
		if active_group == 0:
			win.focus_group(1)

		if active_group == 1:
			win.focus_group(0)

	if num_groups == 4:
		if active_group == 2:
			win.focus_group(3)

		if active_group == 3:
			win.focus_group(2)

		if active_group == 0:
			win.focus_group(1)

		if active_group == 1:
			win.focus_group(0)

class GridNavigationCommand(sublime_plugin.TextCommand):
	def run(self, edit, direction):
		win = self.view.window()

		if direction == 'up' or direction == 'down':
			focusNextVertical(win)
		else:
			focusNextHorizontal(win)
