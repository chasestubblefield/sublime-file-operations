import sublime, sublime_plugin
import os
import shutil
import functools

class FileOperationsCommand(sublime_plugin.TextCommand):

  # Displays quick panel of available commands
  def run(self, edit):
    self.commands = [
      ['New', "Create new file current file's directory"],
      ['Duplicate (Save As)', "Same as above, and copy contents of current file"],
      ['Rename', "Rename the current file"]
    ]
    self.window = self.view.window()
    self.window.show_quick_panel(self.commands,
      lambda x:
        {
          0: lambda: self.window.new_file(),
          1: lambda: self.ask_for_file_from_current_file(True),
          2: lambda: self.ask_for_file_from_current_file(False)
        }[x]()
    )

  def ask_for_file_from_current_file(self, is_copy):
    branch, leaf = os.path.split(self.view.file_name())
    v = self.window.show_input_panel("New Name:", leaf, functools.partial(self.file_move_copy_on_done, is_copy, branch, leaf), None, None)

    # Highlight name and not extension
    name, ext = os.path.splitext(leaf)
    v.sel().clear()
    v.sel().add(sublime.Region(0, len(name)))

  def file_move_copy_on_done(self, is_copy, branch, old_leaf, new_leaf):
    old = os.path.join(branch, old_leaf)
    new = os.path.join(branch, new_leaf)
    try:
        if is_copy:
          shutil.copyfile(old, new)
        else:
          os.rename(old, new)
        v = self.window.find_open_file(old)
        if v:
            v.retarget(new)
    except:
        sublime.status_message("Unable to rename")
