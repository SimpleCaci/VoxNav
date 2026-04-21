VoxNav — Voice-Controlled Desktop Assistant

VoxNav is a Windows-based voice assistant that allows you to control your computer using speech.

It supports:

Mouse control
Keyboard shortcuts
Media control
Application launching
Real-time dictation
Prerequisites
1. Python Version (IMPORTANT)

This project requires Python 3.11–3.13.

Python 3.14 is NOT supported due to PyAudio compatibility issues.

Check your version:
python --version

If you are on Python 3.14, install Python 3.13:

winget install Python.Python.3.13

or download manually from:
https://www.python.org/downloads/

Make sure to check “Add Python to PATH” during installation.

2. Create Virtual Environment

In your project folder:

py -3.13 -m venv .venv
.venv\Scripts\activate

3. Install Dependencies

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

If PyAudio fails:

python -m pip install pipwin
python -m pipwin install pyaudio

4. Verify Installation

python -c "import pyautogui, keyboard, speech_recognition, pyaudio; print('OK')"

5. VS Code Setup (Important)

If using VS Code:

Press Ctrl + Shift + P
Select Python: Select Interpreter
Choose: .venv\Scripts\python.exe

Avoid using "Run Code". Use:

Run Python File in Terminal
or terminal commands
Running the App

python main.py

Controls
Hotkeys

F8 → Listen for one command
F9 → Toggle dictation mode
ESC → Stop movement / exit dictation

Command List
Mouse Movement

up
down
left
right
move up
move down
move left
move right

Speed modifiers:
move up slowly
move right faster
move down more

Continuous movement:
hold up
hold down
hold left
hold right

Stop:
stop
ESC

Clicking

click
double click
right click

Scrolling

scroll up
scroll down

Keyboard / Shortcuts

Tabs:
new tab
close tab
switch tab
next tab
previous tab
reopen tab

Editing:
copy
paste
cut
undo
redo
select all

Keys:
enter
press enter
escape
press escape

Window control:
alt tab
minimize window
close window

Media Control

pause music
play
next track
previous track
volume up
volume down
mute

Application Launching

open chrome
open spotify
open discord
open notepad
open calculator
open explorer
open file explorer
open paint

Dictation Mode
Start Dictation

dictate
start dictation
enter dictation mode

Stop Dictation

stop dictation
exit dictation mode
leave dictation mode
ESC

Text Input

Any speech will be typed into the active window.

Example:
hello how are you

Formatting Commands

comma → ,
period → .
question mark → ?
exclamation mark → !
colon → :
semicolon → ;
quote → "
apostrophe → '

Structure

new line
new paragraph

Editing

backspace
delete word
select all
tab

Limitations
Commands must match exact phrases
No natural language understanding yet
Requires internet (Google speech recognition)
PyAudio dependency required for microphone input
Future Improvements
Offline speech recognition (Whisper / Vosk)
Wake word activation
Custom command system
Natural language parsing
System tray interface
Windows executable packaging