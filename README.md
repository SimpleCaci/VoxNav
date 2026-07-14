# VoxNav

A Windows voice-control assistant for mouse movement, keyboard shortcuts, application launching, media control, and real-time dictation.

VoxNav explores hands-free desktop navigation with an intentionally explicit command vocabulary. Global hotkeys trigger listening and dictation modes, while a separate parser maps recognized phrases to local desktop actions.

> **Status:** functional Windows prototype. The parser has deterministic tests, a side-effect-free demo mode, and visible decision tracing. Offline recognition, broader device testing, and safeguards for high-impact desktop actions are still needed.

## Capabilities

- one-shot and continuous mouse movement with speed modifiers
- left, right, and double clicking
- scrolling and common browser/editing shortcuts
- media and volume keys
- configured application launching
- dictation with spoken punctuation and editing commands
- emergency stop through Escape
- PyAutoGUI corner fail-safe
- heard → matched → executed command timeline in the terminal
- safe text preview mode that never controls the real desktop

## Architecture

```text
microphone
  -> speech recognition
  -> normalized transcript
  -> command parser
       -> command trace console
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

### Safe command preview

Exercise the real parser without granting microphone access or controlling the keyboard and mouse:

```powershell
python main.py --text "move right faster" --text "open notepad"
```

The terminal shows each command moving through `HEARD`, `MATCHED`, and `EXECUTED` stages. Unknown or disallowed commands appear as `IGNORED`.

### Live voice control

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

The standard-library test suite covers transcript normalization, exact commands, movement modifiers, application allowlist feedback, event tracing, and the side-effect-free preview path:

```powershell
python -m unittest discover -s tests -v
```

Microphone recognition, global hotkeys, and real desktop actions still require an intentional Windows manual test.

## Known limitations

- commands currently require close phrase matches
- speech recognition requires internet access
- application mappings are Windows-specific
- foreground context is not checked before keyboard actions
- there is no tray status or confirmation step for risky commands

## Roadmap

- expand tests across dictation and state transitions
- add confirmation policies for high-impact shortcuts
- add offline speech recognition with Vosk or Whisper
- add audible confirmation and cancellation
- add custom commands and a system-tray interface
- package a signed Windows build after safety testing

## License and authorship

Created by [SimpleCaci](https://github.com/SimpleCaci) and released under the [MIT License](LICENSE).
