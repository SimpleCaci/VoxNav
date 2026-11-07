# Contributing to VoxNav

For a scoped first task, see [dictation-state test coverage](https://github.com/SimpleCaci/VoxNav/issues/3). The easiest place to start is the command parser. Its tests run without microphone access or desktop automation dependencies:

```powershell
python -m unittest discover -s tests -v
python main.py --text "move right faster" --text "open notepad"
```

`command_parser.py` handles transcripts; `config.py` holds the vocabulary and application allowlist; `preview_executor.py` records actions without touching the desktop. `tests/test_command_parser.py` includes a fake executor for parser changes.

Keep new commands explicit. Add tests for the accepted phrase, an ignored phrase, and any state transitions. Changes to mouse, keyboard, hotkeys, or microphone code also require intentional testing on Windows; describe those checks in the pull request. Do not make a CI job control a real desktop.

For bugs, include the exact phrase, current mode, expected action, and the preview trace if possible. Remove private dictation and executable paths before posting. Please discuss new speech services or higher-impact commands in an issue first.

Keep pull requests focused and preserve existing authorship. This is an experimental project with no guaranteed response time.
