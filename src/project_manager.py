import json
import os
import sys


if getattr(sys, 'frozen', False):
    script_dir = sys._MEIPASS
    settings_dir = os.path.join(script_dir, 'src/default/settings.json')
    timesheet_dir = os.path.join(script_dir, 'src/default/timesheet.csv')
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    settings_dir = os.path.join(script_dir, 'default/settings.json')
    timesheet_dir = os.path.join(script_dir, 'default/timesheet.csv')


class ProjectManager:
    """
    Class to manage projects and settings
    """

    def __init__(self, settings_file=settings_dir):
        self.settings_file = settings_file
        self.settings = self.load_settings()
        self.version = self.settings.get('version', '1.0.1')
        self.projects = self.settings.get('projects', [])
        self.csv_file_path = self.settings.get('csv_file_path', timesheet_dir)


    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                return json.load(file)
        return {
            "version": "1.0.1",
            "projects": [],
            "csv_file_path": timesheet_dir
        }


    def save_settings(self):
        self.settings['version'] = self.version
        self.settings['projects'] = self.projects
        self.settings['csv_file_path'] = self.csv_file_path
        with open(self.settings_file, 'w') as file:
            json.dump(self.settings, file)


    def add_project(self, name):
        if name not in self.projects:
            self.projects.append(name)
            self.save_settings()


    def edit_project(self, old_name, new_name):
        if old_name in self.projects:
            self.projects[self.projects.index(old_name)] = new_name
            self.save_settings()


    def delete_project(self, name):
        if name in self.projects:
            self.projects.remove(name)
            self.save_settings()


    def set_csv_file_path(self, path):
        self.csv_file_path = path
        self.save_settings()
