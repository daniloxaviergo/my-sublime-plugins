import sublime
import sublime_plugin
import sublime_api
import re
import os
import sys
import json

sys.path.append("/home/danilo/scripts/")
from wmctrl_window import WmctrlWindow

class GotoLastEditCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    str_json = open("/home/danilo/scripts/goto_last_edit.json", "r").read()
    self.goto_last_edit = json.loads(str_json)

    self.files = []
    for last_edit in self.goto_last_edit:
      parts_file_name = last_edit["file_name"].split("/")
      file_name = "/".join(parts_file_name[4:]) + ":" + str(last_edit["line"]) + ":" + str(last_edit["column"]) + ":" + str(last_edit["view_id"])
      file = [file_name]
      self.files.append(file)

    self.show_quick_panel(self.files, self.view.window())

  def show_quick_panel(self, files, window):
    window.show_quick_panel(files, self.on_done)

  def on_done(self, index):
    if index == -1:
      return

    file_name_with_args = self.files[index][0]
    file_name, line, column, view_id = file_name_with_args.split(":")
    settings = sublime.load_settings("set_window_title.sublime-settings")

    for window in sublime.windows():
      for idx, view in enumerate(window.views(), start=0):
        if not str(view.id()) == view_id:
          continue

        project = self.get_project(window)
        official_title = self.get_official_title(window.active_view(), project, settings)

        wmctrl_out = os.popen("wmctrl -dliGux | grep '{sublime_title}'".format(sublime_title=official_title)).read()
        wmctrl_out = wmctrl_out.split('\n')[0]

        current_window = WmctrlWindow(wmctrl_out)
        current_window.set_focus()
        sublime_api.window_focus_view(window.id(), view.id())
        view.sel().clear()
        view.sel().add(sublime.Region(view.text_point(int(line), int(column))))
        view.show(view.text_point(int(line), int(column)))
        break

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




class CaptureFileEditing(sublime_plugin.EventListener):
  # def on_modified(self, view):
  #   only on save
  #   self.save_line_column(view)

  def on_post_save_async(self, view):
    self.save_line_column(view)

  def save_line_column(self, view):
    sel = view.sel()[0]
    curr_line, curr_column = view.rowcol(sel.begin())
    file_name = view.file_name()

    str_goto_last_edit = open("/home/danilo/scripts/goto_last_edit.json", "r").read()
    goto_last_edit = json.loads(str_goto_last_edit)
    file_edit = {}

    file_edit["file_name"] = file_name
    file_edit["view_id"] = view.id()
    file_edit["line"] = curr_line
    file_edit["column"] = curr_column

    for i in range(len(goto_last_edit)):
      if goto_last_edit[i]["file_name"] == file_name:
        del goto_last_edit[i]
        break

    goto_last_edit.insert(0, file_edit)
    goto_last_edit = goto_last_edit[:50]

    json_goto_last = open("/home/danilo/scripts/goto_last_edit.json", "w")
    json_goto_last.write(json.dumps(goto_last_edit))
    json_goto_last.close()
