# Easy Stuff
## Simple tasks made easier.
This module uses `requests` to download files, without the hastle of writing it to a file. It also uses `shutil` to copy files from one location to another.

### Instalation
To install `easystuff`, open Command Prompt or Terminal and run: `python3 -m pip install easystuff`.

### Example
Here is a simple example of how this module can be used:
```python
# Import the module
import easystuff

# Download a file
easystuff.download('https://www.example.com/file.png', 'save_here.png')
# Copy a file
easystuff.copy('copy_me.txt', 'this_is_a_copy.txt')
```