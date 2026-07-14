# VoxNav

A Windows voice-control assistant for mouse movement, keyboard shortcuts, application launching, media control, and real-time dictation.

VoxNav explores hands-free desktop navigation with an intentionally explicit command vocabulary. Global hotkeys trigger listening and dictation modes, while a separate parser maps recognized phrases to local desktop actions.

> **Status:** functional Windows prototype. The command architecture is clear, but automated tests, offline recognition, permission guidance, and safeguards for destructive desktop actions are still needed.

## Capabilities

- one-shot and continuous mouse movement with speed modifiers
- left, right, and double clicking
- scrolling and common browser/editing shortcuts
- media and volume keys
- configured application launching
- dictation with spoken punctuation and editing commands
- emergency stop through Escape
- PyAutoGUI corner fail-safe

## Architecture

```text
microphone
  -> speech recognition
  -> normalized transcript
  -> command parser
       -> action executor
       -> mouse / keyboard / media / app launch
```

`state.py` tracks listening, dictation, and continuous-movement state. `config.py` contains hotkeys, movement values, and application mappings.

## Requirements

- Windows
- Python 3.11–3.13
- microphone access
- internet access for the current Google speech-recognition backend

Python 3.14 is not currently supported because of PyAudio compatibility.

## Setup

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -c "import pyautogui, keyboard, speech_recognition, pyaudio; print('OK')"
```

If PyAudio cannot be installed, use a compatible Python version and an official wheel rather than running untrusted installation scripts.

## Run

```powershell
python main.py
```

### Hotkeys

| Key | Action |
|---|---|
| F8 | Listen for one command |
| F9 | Toggle dictation mode |
| Escape | Stop continuous movement or leave dictation mode |
| Ctrl+C in terminal | Exit VoxNav |

## Example commands

- Movement: `move up`, `move right faster`, `hold left`, `stop`
- Mouse: `click`, `double click`, `right click`, `scroll down`
- Browser/editing: `new tab`, `previous tab`, `copy`, `undo`
- Windows/media: `alt tab`, `minimize window`, `volume up`, `next track`
- Apps: `open chrome`, `open notepad`, `open calculator`
- Dictation: `dictate`, then ordinary speech or commands such as `new line` and `question mark`

Application names and executable paths are configured in `config.py`.

## Safety and privacy

VoxNav can type, click, launch programs, and send global shortcuts to the active desktop. Review `config.py` before running it, keep the Escape stop hotkey available, and test in non-sensitive applications first.

The current speech-recognition backend sends audio to an external Google service. Do not dictate sensitive information until an offline backend and explicit privacy controls are implemented.

## Validation status

No automated tests or CI workflow currently exist. The command parser is the best first testing target because it can be validated with a fake action executor without moving the real mouse.

## Known limitations

- commands currently require close phrase matches
- speech recognition requires internet access
- application mappings are Windows-specific
- foreground context is not checked before keyboard actions
- launch commands use shell execution and need tighter allowlisting
- there is no visible tray status or confirmation for risky commands

## Roadmap

- add unit tests for parsing and state transitions
- replace shell-based launch behavior with strict executable mappings
- add offline speech recognition with Vosk or Whisper
- add audible/visual confirmation and cancellation
- add custom commands and a system-tray interface
- package a signed Windows build after safety testing

## License and authorship

Created by [SimpleCaci](https://github.com/SimpleCaci) and released under the [MIT License](LICENSE).
