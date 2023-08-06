""" Adds activate scripts to a python installation so we can use it as if it were a virtual env create with venv.
"""
import venv
import types
import os
import sys


def find_python_executable(dir):
    for name in os.listdir(dir):
        if "." not in name:
            continue

        name_start = name.split(".")[0]
        if name_start == "python3" or name_start == "python2":
            return name
    raise FileNotFoundError(f"Could not find an existing Python executable in {dir}")


def setup_python_symlinks(bin_path, executable_name):
    python_symlink_names = ["python", executable_name.split(".")[0]]
    for symlink_name in python_symlink_names:
        symlink_path = os.path.join(bin_path, symlink_name)
        if not os.path.exists(symlink_path):
            os.symlink(executable_name, symlink_path)  # relative symlink


def setup_activate_scripts(python_dir, bin_path, bin_name, executable_name, env_name):
    # This context variable is used to interface with the EnvBuilder of the venv package.
    context = types.SimpleNamespace()
    context.env_dir = python_dir
    context.env_name = env_name
    context.prompt = f"({context.env_name}) "
    context.bin_name = bin_name
    context.bin_path = bin_path
    context.env_exe = os.path.join(bin_path, executable_name)
    context.executable = context.env_exe

    env_builder = venv.EnvBuilder(symlinks=True)
    env_builder.setup_scripts(context)


def venvify(python_dir, env_name):
    python_dir = os.path.abspath(python_dir)
    bin_name = "Scripts" if sys.platform == "win32" else "bin"
    bin_path = os.path.join(python_dir, bin_name)

    executable_name = find_python_executable(bin_path)

    if not env_name:
        env_name = executable_name

    setup_python_symlinks(bin_path, executable_name)
    setup_activate_scripts(python_dir, bin_path, bin_name, executable_name, env_name)

    print(f"Added symlinks and activate scripts to {bin_path}")
    print(f"You can activate this environment with:")
    print(f"source {os.path.join(bin_path, 'activate')}")


def cli():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "python_dir",
        help="Path to the Python directory with bin, include and lib as subdirectories.",
    )
    parser.add_argument(
        "--env_name", help="Name to display in the terminal when the env is activated."
    )
    args = parser.parse_args()
    venvify(args.python_dir, args.env_name)


if __name__ == "__main__":
    cli()
