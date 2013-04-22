import sublime
import sublime_plugin
import os.path
import subprocess

import re
import commands

class SublimeGemBrowserGemset(sublime_plugin.WindowCommand):
    PATTERN_GEM_VERSION = "\* (.*)"
    PATTERN_GEM_NAME = "(.*)\("
    GEMS_NOT_FOUND = 'Gems Not Found'

    def find_nearest_file(self, starting_filename, needle):
        potential_file = starting_filename

        while True:
            active_directory = os.path.split(os.path.dirname(potential_file))[0]
            potential_file = active_directory + "/" + needle

            if os.path.exists(potential_file):
                return potential_file
            if active_directory == '/':
                return None

    def gemset(self, current_file_path):
        config_file = self.find_nearest_file(current_file_path, ".ruby-gemset")
        if config_file:
            return open(config_file).read().rstrip()
        return None

    def bundler(self, command):
        view = sublime.active_window().active_view()
        cwd = os.path.dirname(view.file_name())

        ruby = "ruby-1.9.3"
        gemset = self.gemset(view.file_name())

        if gemset == None:
            sublime.error_message("No gemset file configured. Do you have a .ruby-gemset file in your project root?")
            return

        # output = subprocess.Popen(['/bin/bash', 'cd',
        #                           cwd.replace(" ", "\ "), '&&', '$HOME/.rvm/bin/rvm-shell',
        #                           ruby + "@" + gemset,
        #                           "-c",
        #                           "bundle",
        #                           command],
        #                           shell=True, stdout=subprocess.PIPE).communicate()[0]

        command = "cd " + cwd.replace(" ", "\ ") + " && $HOME/.rvm/bin/rvm-shell " + ruby + "@" + gemset + " -c 'bundle " + command + "'"
        exit_status, output = commands.getstatusoutput(command)
        return output

    def parse_bundle_list(self, output):
        if output != None:
          gems = []
          for line in output.split('\n'):
              gem_name_version = re.search(self.PATTERN_GEM_VERSION, line)
              if gem_name_version != None:
                  gems.append(gem_name_version.group(1))

          if gems == []:
              gems.append(self.GEMS_NOT_FOUND)

          self.gem_list = gems
          self.window.show_quick_panel(self.gem_list, self.on_done)
        else:
          sublime.error_message('Error getting the output, the shell could probably not be loaded or there is no Gemfile in this project.')

    def on_done(self, picked):
        if self.gem_list[picked] != self.GEMS_NOT_FOUND and picked != -1:
            gem_name = re.search(self.PATTERN_GEM_NAME,self.gem_list[picked]).group(1)
            
            gem_path = self.bundler("show " + gem_name)
            if gem_path != None:
                self.sublime_command_line(['-n', gem_path.rstrip()]) 

    def get_sublime_path(self):
        if sublime.platform() == 'osx':
            return '/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl'
        if sublime.platform() == 'linux':
            return open('/proc/self/cmdline').read().split(chr(0))[0]
        return sys.executable

    def sublime_command_line(self, args):
        args.insert(0, self.get_sublime_path())
        return subprocess.Popen(args)

    def run(self):
        gems = self.bundler("list")
        self.parse_bundle_list(gems)
