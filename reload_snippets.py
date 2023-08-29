import sublime
import sublime_api
import sublime_plugin
import re
import os
import sys
import json

class ReloadSnippetsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    pattern  = '(##.{3}-.*)(\n)?(###.*)?'
    snippets = []

    srtlist      = open("/home/danilo/scripts/sublime_tabs.json", "r").read()
    sublime_tabs = json.loads(srtlist)

    paths = []
    for file in os.listdir('/home/danilo/scripts/snippets'):
      if not file == 'list.json':
        paths.append("/home/danilo/scripts/snippets/" + file)

    for path in paths:
      relative_path = path.replace('/home/danilo/', '')
      content_file  = open(path, 'r').read()

      matches = re.finditer(pattern, content_file)
      for match in matches:
        # find sublime window id
        window_id = False
        view_id   = 0
        for sublime_window in sublime_tabs.keys():
          for idx, path_file in enumerate(sublime_tabs[sublime_window], start=0):
            if not window_id and relative_path == path_file:
              window_id = sublime_window
              view_id   = str(idx)

        if window_id:
          snippets.append({
            'title': match.group(1),
            'description': match.group(3) or '',
            'window_id': window_id,
            'view_id': view_id,
            'file_path': relative_path
          })

    file_config = open("/home/danilo/scripts/snippets/list.json", "w")
    file_config.write(json.dumps(snippets, indent=2))
    file_config.close()
