import sublime, sublime_plugin
import shutil
import os

class RenameFileCommand(sublime_plugin.WindowCommand):

  def run(self):
    ask_for_name_relative_to_active_view(self.window, self.rename_and_retarget)

  def rename_and_retarget(self, src, dest):
    try:
      os.rename(src, dest)
      self.window.find_open_file(src).retarget(dest)
    except:
      sublime.status_message("Unable to rename")

class DuplicateFileCommand(sublime_plugin.WindowCommand):

  def run(self):
    ask_for_name_relative_to_active_view(self.window, self.copy_and_open_new_buffer)

  def copy_and_open_new_buffer(self, src, dest):
    try:
      shutil.copy(src, dest)
      self.window.open_file(dest)
    except:
      sublime.status_message("Unable to copy")


def ask_for_name_relative_to_active_view(window, on_done):
  old_path = window.active_view().file_name()
  branch, leaf = os.path.split(old_path)

  def on_input_given(new_leaf):
    new_path = os.path.join(branch, new_leaf)
    if old_path != new_path:
      on_done(old_path, new_path)

  # Show input panel with basename of current view
  v = window.show_input_panel("New Name:", leaf, on_input_given, None, None)

  # Highlight name and not extension
  name, ext = os.path.splitext(leaf)
  v.sel().clear()
  v.sel().add(sublime.Region(0, len(name)))
