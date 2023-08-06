# venvify
Python package to turn Python installations into venv-like environments that you can activate.

Say you have the following python installation:

```
python_env
|- bin
|   |- python3.9
|- include
|- lib
```

Then you can venvify it by running the following script:
```
venvify ~/python_env
```

The result:
```
python_env
|- bin
|   |- python3.9
|   |- python (symlink)
|   |- python3 (symlink)
|   |- activate
|   |- activate.sh
|   |- etc.
|- include
|- lib
```
Now you can source the `activate` file to use the environment as you would use a venv:
```console
user@laptop: source python_env/bin/activate
(python_env) user@laptop: python -m pip install <some_package>
``` 

To undo the venvifying, simply remove the `activate` scripts and the symlinks from the `bin` directory.

## Installation
All the logic of the package can be found in a single script `venvify.py`.
The only dependency is the [venv](https://docs.python.org/3/library/venv.html) Python standard library package.
`venv` should be shipped with Python 3, but can be installed with `sudo apt install python3-venv`.

So if you don't want to pip install, you can clone this repo and simply run `venvify.py` with any Python interpreter.

However if you don't mind you can:
```
pip install venvify
```
And then run the `venvify` command.

## Use case: Blender Python environment
I made this package to make developing python scripts for Blender a bit more convenient. 

Blender ships with its own Python installation.
But specifying the entire path to the Blender Python executable is tedious.
My initial solution was to add an alias `bpython` to my `.bashrc`. 
This relieved the burden of typing long paths, but another problem remained.

Some Python packages come with command line entry points. For example, a package I use `BlenderProc` has a command `blenderproc`.
After installing BlenderProc into the Blender Python installation, there was no way access this command.

However, when you install such a package into a virtual environment, its commands are exposed after sourcing the created `activate` file.
Hence this package, which allowed me to activate the Blender Python environment and use the commands of the installed Python packages.


## TODO
Maybe in the future this package could also ensure pip gets installed into the environment.
