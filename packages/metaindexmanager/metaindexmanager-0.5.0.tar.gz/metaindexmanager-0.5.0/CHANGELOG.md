# Changelog

This file contains the changes made between released versions.

The format is based on [Keep a changelog](https://keepachangelog.com/) and the versioning tries to follow
[Semantic Versioning](https://semver.org).

## 0.5.0
### Changed
- Switched most references from github.com to vonshednob.cc
- Auto-index a file when the editor panel is launched and no metadata is available yet

### Added
- `--version` command line flag
- `--check-for-update` command line flag
- Support for addons in form of directories
- `is_hidden` and `is_executable` helper functions
- Autocompletion in `cd` command
- `cut` for cut and paste in file panel

### Fixed
- `set` command used to show the completion for the parameter’s values, too
- The completion used to cause quite some flickering
- Pasting a file (and outside changes) could change the selected item in the file panel


## 0.4.0
### Changed
- Depends on metaindex 0.7.0
- Refactoring of copy and paste, see `clipboard.py` for developer instructions

### Added
- `paste` command can paste files in the file browser

### Removed
- `copy-tag`, `copy-append-tag`, `paste-tag` have been removed. Use `copy`, `append`, and `paste` instead


## 0.3.1
### Fixed
- Selecting the last item in the filepanel did not show the selection marker ([#1](https://github.com/vonshednob/metaindexmanager/issues/1))
- Fixed crash when pasting in the metadata editor while the clipboard is empty
- Fixed crash when humanizing values that are of unusual types
- Fixed crash when attempting to edit metadata of a file in an external editor

### Added
- Document panel supports multi-selection in theory (ie. it can display the selection marks, but there is not command to select)


## 0.3.0
### Changed
- Depend on metaindex 0.6.0

### Added
- `all.history-size` configuration option
- Proper support for renaming files (updates the cache, rename of directories)

### Fixed
- `index` command used to only index the first file, even when indexing a whole folder
- Attempting to open an no longer existing file from the document panel, will no longer crash


## 0.2.0
### Added
- Autocompletion for 'add-tag' command (when editing metadata)

### Changed
- Depending on metaindex-0.5.0 now

### Fixed
- Various breaking incompatibilities there were following the switch from
  metaindex.ThreadedCache to metaindex.MemoryCache

## 0.1.0
- Initial release

