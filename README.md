Wordle Solver Bot
=================

Cautions
--------
If you're running this locally it; beware that it is not well tested and might not work for you


How to run
----------
You need to have `pipenv` installed on your machine. Run `pipenv sync` to install all the packages
that are locked. This is currently tested on Arch Linux and might not work on other platform.
The scripts that are defined in `Pipfile` to check:
- `pipenv run python -m solve`
- `pipenv run pytest`

Inspiration
-----------
This is the code to the original wordle game: [Wordle](https://github.com/coolbutuseless/wordle).
I thought that I should write a script that solves wordle.
Initially I thought that I should write a browser automation system.
The tool that used for tests from browser Eg: `selenium` or `Cypress`.
I initially started off by using `Cypress` initially, but it could not access the elements in the browser.
Being unable to access the elements in the browser; rather than switching form `Cypress` to `Selenium`,
I thought of switching to a some computer vision tool.
Although this project is still in a pretty rough state, I will still call it a complete project.

Toolchain
---------
- Pillow for image processing
- PyAutoGUI as an actuator that can click and move the mouse and also type on the screen
- Open CV for matching patterns and acting as a sensor that will look at the changes in the screen
- Numpy for the arrays from Open CV
- Termcolor for outputting colored output to the terminal
- Pyperclip to paste text copied from the browser
- Pytest for testing the code that's written
- Black and MyPy for formatting and static checks

License: MIT License
--------------------

Copyright 2022 Tanay PrabhuDesai

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software and
associated documentation files (the "Software"),
to deal in the Software without restriction, including
without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom
the Software is furnished to do so, subject to the
following conditions:

The above copyright notice and this permission
notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO
EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
