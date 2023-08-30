import sublime
import sublime_api
import sublime_plugin
import re
import os
import sys
import json

import string
import random

sys.path.append("/home/danilo/scripts/")
from sublime_tab import SublimeTab

class CreateSnippetsCommand(sublime_plugin.TextCommand):
  def id_generator(self, size=3, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

  def run(self, edit):
    self.id = self.id_generator()
    self.title = ''
    self.description = ''
    self.view.window().show_input_panel('title', '', self.on_done_title, None, self.on_cancel_title)

  def on_cancel_title(self, value):
    self.title = ''

  def on_done_title(self, value):
    self.title = value
    if len(self.title) > 0:
      self.view.window().show_input_panel('description', '', self.on_done_description, None, self.on_cancel_description)

  def on_cancel_description(self, value):
    self.title = ''
    self.description = ''

  def on_done_description(self, value):
    self.description = value or ''

    self.title = "##" + self.id + "-" + self.title
    self.description = "###" + self.description

    characters = self.title + "\n" + self.description

    self.view.window().run_command('insert', { 'characters': characters })
    self.view.window().run_command('save', {})
    self.view.window().run_command("reload_snippets", {})
