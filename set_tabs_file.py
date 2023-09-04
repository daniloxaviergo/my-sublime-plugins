import sublime
import sublime_plugin
import sublime_api
import re
import os
import json
import unicodedata
from . import tab

class SetTabsFileCommand(sublime_plugin.WindowCommand):
  def run(self, **args):
    show_captions = False
    include_path = True
    settings = sublime.load_settings("set_window_title.sublime-settings")

    wmctrl_out = os.popen('wmctrl -dliGux | grep sublime').read()
    wmctrl_out = wmctrl_out.split('\n')
    wmctrl_out.pop()

    for window in sublime.windows():
      project = self.get_project(window)
      official_title = self.get_official_title(window.active_view(), project, settings)
      # print(official_title)
      for wmctrl in wmctrl_out:
        if wmctrl.find(official_title) >= 0:
          wmctrl_window_id = wmctrl.split(' ')[0]

      if not str(wmctrl_window_id) == args['window_id']:
        continue;

      path_tabs = []
      tabs = []

      for idx, view in enumerate(window.views(), start=0):
        if not str(idx) == args['idx']:
          continue;

        # print('focus--focus---')
        sublime_api.window_focus_view(window.id(), view.id())
        if 'find_text' in args:
          # print('focusllllasldkfaçlskdjf')
          # print(args['find_text'])
          # view.find("import json", 0, sublime.IGNORECASE)
          # view.run_command('insert', { 'characters': 'testing123' })
          window.run_command("show_panel", {"panel": "find", "pattern": args['find_text'] })
        break;
  
  def get_official_title(self, view, project, settings):
    """Returns the official name for a given view.
    Note: The full file path isn't computed,
    because ST uses `~` to shorten the path.
    """
    view_name = view.name() or view.file_name() or "untitled"
    official_title = os.path.basename(view_name)
    if view.is_dirty():
      official_title += " •"
    if project:
      official_title += " (%s)" % project
    official_title += " - Sublime Text"
    if settings.get("unregistered", False):
      official_title += " (UNREGISTERED)"

    return official_title

  def get_project(self, window):
    """Returns the project name for the given window.
    If there is no project, uses the name of opened folders.
    """
    if not window:
      return

    project = window.project_file_name()
    if not project:
      folders = window.folders()
      project = ", ".join(self.get_folder_name(x) for x in folders) if folders else None
    else:
      project = self.get_folder_name(project)

    return project

  def get_folder_name(self, path):
    return os.path.splitext(os.path.basename(path))[0]

