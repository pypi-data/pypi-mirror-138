from os import path

import todoist
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk



CONFIG = path.expanduser("~/.config/todoist")


class Prompt(Gtk.Dialog):
    def __init__(self, message):
        super().__init__()
        self.set_decorated(False)
        box = self.get_content_area()
        self.entry = Gtk.Entry()
        self.entry.set_text(message)

        self.entry.connect("destroy", Gtk.main_quit)

        self.entry.grab_focus()
        box.add(self.entry)


class APITokenPrompt(Prompt):
    def __init__(self, reason=""):
        super().__init__("API Token")
        self.entry.connect("activate", self.save_api)

        label = Gtk.Label()
        if reason != "":
            reason += ". "

        label.set_markup(
            "{}<a href='https://todoist.com/prefs/integrations'>Get your API token here</a>".format(
                reason
            )
        )
        box = self.get_content_area()
        box.add(label)

    def save_api(self, *args):
        with open(CONFIG, "w") as stream:
            stream.write(self.entry.get_text())
        self.destroy()


class NewTaskWindow(Prompt):
    def __init__(self, project_id):
        super().__init__("New Task")
        self.project_id = project_id
        self.entry.connect("activate", self.create_task)

    def create_task(self, *args):
        task = self.entry.get_text()
        self.create_new_task(task)
        self.destroy()

    def create_new_task(self, task):
        with open(CONFIG) as stream:
            api = todoist.TodoistAPI(stream.read())
            if self.project_id:
                res = api.add_item(task, project_id=self.project_id)
            else:
                res = api.add_item(task)

            if res.get("error_tag") == "AUTH_INVALID_TOKEN":
                show_prompt(APITokenPrompt("Invalid token"))

def show_prompt(prompt):
    prompt.show_all()
    Gtk.main()


def add_todoist_task(project_id):
    if not path.exists(CONFIG):
        show_prompt(APITokenPrompt("Missing token"))
    show_prompt(NewTaskWindow(project_id))
