# Screen Monkey

This package allows users to record and execute sequences of on-screen actions by interacting with Sequence objects.

Currently, only mouse actions are supported -- development of keyboard support is underway.

Currently, only saving/loading through excel files is supported -- csv and other filetypes is under developemnt.

Thanks to Pravin Nath for developing the pynput library, which this packed is based off. Details here: https://github.com/pravinnath/pynput

# Installation

# Examples

To record and save a Sequence of actions:

```python
from screenmonkey import Sequence

mySeq = Sequence()  # initializes your Sequence object
mySeq.record()  # prompts user to do actions that they wish to record
mySeq.save_excel('testSeq.xlsx')  # saves Sequence as Excel file for repeated use
```
To run a saved Sequence:

```python
from screenmonkey import Sequence

mySeq = Sequence()  # initializes your Sequence object
mySeq.load_excel('testSeq.xlsx')  # loads a saved Sequence of actions
mySeq.run()  # prompts user to prepare screen, then executes actions
```


# Contact

Screen Monkey is developed by Bryce Merrill, please contact at: brycelmerrill@gmail.com