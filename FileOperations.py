import sublime, sublime_plugin
import shutil
import os

class EditFileCommand(sublime_plugin.WindowCommand):

  def run(self):
    branch = os.getenv("HOME")
    v = self.window.active_view()
    if v:
      branch, current_file = os.path.split(v.file_name())

    def on_done(leaf):
      self.window.open_file(os.path.join(branch, leaf))

    self.window.show_input_panel("Edit File:", branch + "/", on_done, None, None)

class RenameFileCommand(sublime_plugin.WindowCommand):

  def run(self):
    ask_for_name_relative_to_active_view(self.window, self.rename_and_retarget)

  def rename_and_retarget(self, src, dest):
    try:
      os.rename(src, dest)
      v = self.window.find_open_file(src)
      if v:
        v.retarget(dest)
    except:
      sublime.status_message("Unable to rename")

  def is_enabled(self):
      return self.window.active_view() != None

class DuplicateFileCommand(sublime_plugin.WindowCommand):

  def run(self):
    ask_for_name_relative_to_active_view(self.window, self.copy_and_open)

  def copy_and_open(self, src, dest):
    try:
      shutil.copy(src, dest)
      self.window.open_file(dest)
    except:
      sublime.status_message("Unable to copy")

  def is_enabled(self):
      return self.window.active_view() != None

class DeleteCurrentFileCommand(sublime_plugin.WindowCommand):

  def run(self):

    v = self.window.active_view()
    if v:
      os.remove(v.file_name())

  def is_enabled(self):
      return self.window.active_view() != None

class CopyNameCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    basename = os.path.basename(self.view.file_name())
    sublime.set_clipboard(basename)
    sublime.status_message("Copied " + basename + " to clipboard")

  def is_enabled(self):
    return self.view.file_name() and len(self.view.file_name()) > 0

class CopyRelativePathCommand(sublime_plugin.WindowCommand):
  def run(self):
    relative_path = os.path.relpath(self.window.active_view().file_name(), self.window.folders()[0])
    sublime.set_clipboard(relative_path)
    sublime.status_message("Copied " + relative_path + " to clipboard")

  def is_enabled(self):
    return len(self.window.folders()) > 0 and self.window.active_view() and len(self.window.active_view().file_name()) > 0

def ask_for_name_relative_to_active_view(window, on_done):
  old_path = window.active_view().file_name()
  branch, leaf = os.path.split(old_path)

  def on_input_given(new_leaf):
    new_path = os.path.join(branch, new_leaf)
    if old_path != new_path:
      on_done(old_path, new_path)

  show_input_panel_for_file_name(window, leaf, on_input_given)

def show_input_panel_for_file_name(window, placeholder, callback):
  v = window.show_input_panel("New Name:", placeholder, callback, None, None)
  name, ext = os.path.splitext(placeholder)
  v.sel().clear()
  v.sel().add(sublime.Region(0, len(name)))
