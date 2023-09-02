import sublime
import sublime_api
import sublime_plugin
import re
import os
import sys
import json

sys.path.append("/home/danilo/scripts/")
from sublime_tab import SublimeTab

class ListSnippetsCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    str_snippets  = open("/home/danilo/scripts/snippets/list.json", "r").read()
    self.snippets = json.loads(str_snippets)

    self.list_snippets = []
    for snippet in self.snippets:
      title = re.sub('##.{3}-', '', snippet['title'])
      description = re.sub('###', '', snippet['description'])
      self.list_snippets.append([title, description])

    self.show_quick_panel(self.list_snippets, self.view.window())

  def show_quick_panel(self, files, window):
    self.window = window
    window.show_quick_panel(files, self.on_done)
    # window.show_input_panel('query', 'hello', self.on_done, self.on_change, self.on_cancel)

  def on_done(self, index):
    #  if user cancels with Esc key, do nothing
    #  if canceled, index is returned as  -1
    if index == -1:
      return

    snippet = self.snippets[index]
    # title = re.sub('##.{3}-', '', snippet['title'])
    os.popen('wmctrl -i -a {win_id}'.format(win_id=snippet['window_id'])).read()
    self.window.run_command("set_tabs_file", {"window_id": snippet['window_id'], "idx": snippet['view_id'], "find_text": snippet['title']})

    # self.window.run_command("goto_line", {"line": 10})
    # r = sublime_api.find('on_done(', 0, sublime.IGNORECASE)
    # view.show(r)
    # self.window.run_command("set_tabs_file", {"window_id": "0x08600033", "idx": "32", "find_text": "sublime_tabs"})
    
    # self.window.run_command("show_panel", {"panel": "find", "pattern": "on done" })

    # os.popen('subl --background --command "set_tabs_file {args}"'.format(args=args)).read()
    # sublime_tab = SublimeTab(snippet['window_id'], snippet['file_path'], snippet['view_id'])
    # sublime_tab.set_focus()
