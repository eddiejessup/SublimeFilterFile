"""
@name     FilterFile
@package  sublime_plugin
@author   Elliot Marsden

Pass file contents through an external program.
"""

import subprocess
import os

import sublime  # pylint: disable=import-error
import sublime_plugin  # pylint: disable=import-error

OUTPUT_PANEL_NAME = 'file_filter_error'
SETTINGS_FILE_NAME = 'FilterFile.sublime-settings'

def get_filters():
    settings = sublime.load_settings(SETTINGS_FILE_NAME)
    return settings.get('filters', {})

def set_contents(view, edit, text):
    view.replace(edit, sublime.Region(0, view.size()), text)

def show_panel_message(window, message):
    v = window.create_output_panel(OUTPUT_PANEL_NAME)
    v.run_command("set_contents", {"text": message})
    window.run_command("show_panel", {f"panel": "output.{OUTPUT_PANEL_NAME}"})

class SetContentsCommand(sublime_plugin.TextCommand):  # pylint: disable=too-few-public-methods

    def run(self, edit, text):
        set_contents(self.view, edit, text)
        self.view.end_edit(edit)

class FilterFileCommand(sublime_plugin.TextCommand):  # pylint: disable=too-few-public-methods

    def input_description(self):  # pylint: disable=no-self-use
        return "Filter with"

    def input(self, args):  # pylint: disable=no-self-use
        return None if "cmd_key" in args else CmdKeyInputHandler()

    def show_error(self, msg):
        show_panel_message(self.view.window(), f'Error: {msg}')

    def run(self, edit, cmd_key):
        filename = self.view.file_name()

        if filename:
            dirname = os.path.dirname(filename)
            filters = get_filters()

            try:
                cmd_raw = filters[cmd_key]
            except KeyError:
                self.show_error(f'Command key "{cmd_key}" not found')
            else:
                cmd = list(map(os.path.expanduser, cmd_raw))
                cmd_full = cmd + [filename]

                try:
                    completed_process = subprocess.run(
                        cmd_full,
                        capture_output=True,
                        timeout=10,
                        cwd=dirname,
                        check=True,
                        text=True,
                    )
                except subprocess.CalledProcessError as exc:
                    cmd_full_str = ' '.join(cmd_full)
                    self.show_error(
                        f'Running command "{cmd_full_str}", '
                        f'got return code "{exc.returncode}". '
                        f'stdout: "{exc.stdout.strip()}", '
                        f'stderr: "{exc.stderr.strip()}".'
                    )
                except FileNotFoundError as exc:
                    self.show_error(
                        f'Could not find command "{cmd[0]}" (exception: {exc})'
                    )
                else:
                    set_contents(self.view, edit, completed_process.stdout)
        else:
            self.show_error('Current view has no filename')


class CmdKeyInputHandler(sublime_plugin.ListInputHandler):  # pylint: disable=too-few-public-methods

    def name(self):  # pylint: disable=no-self-use
        return "cmd_key"

    def placeholder(self):  # pylint: disable=no-self-use
        return "file filter"

    def list_items(self):  # pylint: disable=no-self-use
        return list(get_filters().keys())
