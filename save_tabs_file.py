import sublime
import sublime_plugin
import re
import os
import json
import unicodedata
from . import tab

class SaveTabsFileCommand(sublime_plugin.WindowCommand):
  def run(self):
    sublime_tabs = {}
    self.window = sublime.active_window()
    self.views = []
    self.settings = sublime.load_settings("tabfilter.sublime-settings")
    settings = sublime.load_settings("set_window_title.sublime-settings")

    wmctrl_out = os.popen('wmctrl -dliGux | grep sublime').read()
    wmctrl_out = wmctrl_out.split('\n')
    wmctrl_out.pop()

    for window in sublime.windows():
      path_tabs = []
      tabs = []
      wmctrl_window_id = None

      project = self.get_project(window)
      official_title = self.get_official_title(window.active_view(), project, settings)
      # print(official_title)
      for wmctrl in wmctrl_out:
        if wmctrl.find(official_title) >= 0:
          wmctrl_window_id = wmctrl.split(' ')[0]

      # print(wmctrl_window_id)


      for view in window.views():
        self.views.append(view)
        tabs.append(self.make_tab(view))

      show_captions = False
      include_path = True

      for entity in tabs:
        tab_path = entity.get_details(0, include_path, show_captions)[0]
        tab_path = tab_path.replace('/home/danilo/', '')
        path_tabs.append(str(tab_path))

      sublime_tabs[str(wmctrl_window_id)] = list(path_tabs)

    file_tabs = open("/home/danilo/scripts/sublime_tabs.json", "w")
    jjson = json.dumps(sublime_tabs)
    file_tabs.write(jjson)
    file_tabs.close()

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

  def make_tab(self, view):
    """Makes a new Tab entity relating to the given view.
    Args:
    view (sublime.View): Sublime View to build the Tab from
    Returns (Tab): Tab entity containing metadata about the view.

    """
    name = view.file_name()
    is_file = True

    #If the name is not set, then we're dealing with a buffer
    #rather than a file, so deal with it accordingly.
    if name is None:
      is_file = False
      name = view.name()
      #set the view name to untitled if we get an empty name
      if len(name) == 0:
        name = "untitled"

    entity = tab.Tab(name, is_file)

    if self.window.get_view_index(self.window.active_view()) == self.window.get_view_index(view):
      entity.add_caption("Current File")

    if view.file_name() is None:
      entity.add_caption("Unsaved File")
    elif view.is_dirty():
      entity.add_caption("Unsaved Changes")

    if view.is_read_only():
      entity.add_caption("Read Only")

    return entity
