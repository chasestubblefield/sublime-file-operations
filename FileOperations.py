import sublime, sublime_plugin
import os
import functools
import send2trash

class RenameFileCommand(sublime_plugin.WindowCommand):

  def run(self):
    branch, leaf = os.path.split(self.window.active_view().file_name())
    v = self.window.show_input_panel("New Name:", leaf, functools.partial(self.__on_name_given, branch, leaf), None, None)

    # Highlight name and not extension
    name, ext = os.path.splitext(leaf)
    v.sel().clear()
    v.sel().add(sublime.Region(0, len(name)))

  def __on_name_given(self, branch, old_leaf, new_leaf):
    old = os.path.join(branch, old_leaf)
    new = os.path.join(branch, new_leaf)
    try:
        os.rename(old, new)
        v = self.window.find_open_file(old)
        if v:
            v.retarget(new)
    except:
        sublime.status_message("Unable to rename")

class DuplicateFileCommand(sublime_plugin.WindowCommand):

  def run(self):
    pass

class DeleteFileCommand(sublime_plugin.WindowCommand):

  def run(self):
    send2trash.send2trash(self.window.active_view().file_name())
