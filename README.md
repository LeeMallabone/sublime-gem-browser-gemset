SublimeGemBrowserGemset
=======================

Browse the gems in your Gemfile and open their source in a new Sublime window, all without leaving the editor.
*Note:* this plugin is for users of rvm gemsets. For other project structures, check out [SublimeGemBrowser](https://github.com/NaN1488/sublime-gem-browser), on which this plugin is based.


Installation
------------

Copy to your sublime packages directory. (In OS X: `~/Library/Application Support/Sublime Text 2/Packages`)

Then add a keyboard binding:

```
{ "keys": ["super+ctrl+e"], "command": "sublime_gem_browser_gemset" }
```

Then hit `⌘-CTRL-e` to fuzzy search your gems.

License
-------

Written by Lee Mallabone. MIT License. Based liberally on Sublime Gem Browser.