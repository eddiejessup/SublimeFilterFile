# FilterFile: A package for Sublime Text 3

Pass your file through an external program that writes some function of the file's contents to standard output.

## Installation

### Recommended option: Use the Package Control plugin

- Follow [these instructions](http://wbond.net/sublime_packages/package_control) to install the Package Control plugin
- In Sublime Text, pick `Package Control: Install Package` from the command palette, then search for and select the package `FilterFile`.

### Alternative option: Clone the repository

Clone the repository containing the plugin into `Sublime Text 3/Packages`, whose location depends on your operating system:

MacOS:

`git clone git://github.com/eddiejessup/FilterFile.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/FilterFile`

Windows:

`git clone git://github.com/eddiejessup/FilterFile.git "%APPDATA%\Sublime Text 3\Packages\FilterFile"`

Linux:

`git clone git://github.com/eddiejessup/FilterFile.git ~/.config/sublime-text-3/Packages/FilterFile`

## Usage

### Low-level functionality

The package provides a command, `filter_file`, that takes one required string argument, `cmd_key`. This key is used to look up a filter command from a list specified in the plugin settings (explained in the 'Configuration' section). The key should map to a list of strings, representing a command, potentially with arguments.

This command is run with the path of the file in the current view appended to the list of arguments. If the command's return code is zero, then the current view's contents are replaced by the standard output produced by running the command.

### Command-palette interface

The plugin adds an entry to the command palette called `FilterFile: Select filter`. This lets you interactively pick the filter to apply to the current view.

### Menu interface

The plugin adds a menu entry under `Tools/Filter file`, which opens the interactive filter dialog.

### Key-binding interface

The plugin binds a shortcut, `"ctrl+k", "ctrl+f"`, or `"cmd+k", "cmd+f"` on MacOS, which opens the interactive filter dialog.

You can also define a keyboard shortcut which runs the plugin for a particular filter, by binding a key pattern to the `filter_file` command with the argument `cmd_key` specifying your intended file filter, as listed in the plugin settings.

For example, to add a shortcut to run a command defined under the key 'Stylish Haskell', you might add a key binding like:

```
{
    "keys": ["ctrl+k", "ctrl+s"],
    "command": "filter_file",
    args: { "cmd_key": "Stylish Haskell" }
}
```

## Configuration

You can edit the key mappings, and plugin settings through the menu, at `Sublime Text/Preferences/Package Settings/Filter File`.

The value under the key `filters` in the plugin settings should define an object mapping a `cmd_key` string to an array of strings representing some terminal command.

When running the filter command, any `~` characters at the start of any of the command arguments will be expanded to the user's home directory.

### Example

There is a code formatter called 'Stylish Haskell'. It expects the name of a file containing Haskell source code, and returns the contents of the file with some stylistic changes applied. Let's consider setting up the plugin to process Haskell files with this program. The `stylish-haskell` program also accepts a path to a configuration file, through the `--config` argument.

We will assume the program lives at `~/.local/bin/stylish-haskell`.

To add this filter, our user plugin settings might look like:

```
{
    "filters": {
        "Stylish Haskell": [
            "~/.local/bin/stylish-haskell",
            "--config",
            "~/.stylish-haskell.yaml",
        ],
    }
}
```

See the "Key-binding interface" section for an example of how we might add a key binding to run this particular filter, or alternatively we could run it by picking it from the interactive dialog.

## Author & Contributors

- [Elliot Marsden](https://github.com/eddiejessup)

## License

MIT License
