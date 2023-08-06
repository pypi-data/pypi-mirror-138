#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from os import getcwd, path
from pathlib import Path
from shutil import which
from subprocess import run
from sys import argv, exit, stderr

from colorama import init
from termcolor import colored, cprint


def app_help():
    """Show the application help message.

    Just print what the application does with an example, and exit.
    """
    print(f'Just download the Android application, and its that.\n\n',
          'You should try something like "', colored(f'{argv[0]} app', attrs=['bold']), '".', sep='')


def check_adb() -> str:
    """Check if the host OS has the necessary tooling.

    :return: The absolute PATH of ADB.
    """
    adb_path = which('adb')
    if adb_path is None:
        print_error('Unable to find ADB in your PATH!')
        exit(1)

    return adb_path


def print_error(message: str):
    """Just print a nice error message

    :param message: The content of the message
    """
    cprint(f'e {message}', color='red', attrs=['bold'], file=stderr)


def print_question(message: str):
    """Just print a nice question message

    :param message: The content of the message
    """
    print(colored('?', color='yellow', attrs=['bold']), message)


def print_info(message: str):
    """Just print a nice informational message

    :param message: The content of the message
    """
    print(colored('i', color='blue', attrs=['bold']), message)


def adb_command_handler(command: str) -> str:
    """Run a command in ADB

    :param command: Command will be executed in ADB
    :return: The stdout of the command
    """
    cmd = run(f'{ADB_PATH} -s {ADB_DEVICE} {command}', capture_output=True, shell=True, universal_newlines=True) \
        if ADB_DEVICE else run(f'{ADB_PATH} {command}', capture_output=True, shell=True, universal_newlines=True)

    if cmd.returncode != 0:
        print_error(f'ADB got a error running command "{command}", returned {cmd.returncode}!')
        if cmd.stderr:
            print_info(f'stderr: {cmd.stderr}')

    return cmd.stdout


def check_device() -> str:
    """Check if there is an available remote

    :return: The name of the device
    """
    cmd = adb_command_handler('devices').strip().split('\n')
    devices = []
    device = ''
    del cmd[0]
    for line in cmd:
        if 'device' not in line:
            continue
        device = line.split()
        devices.append(device[0])

    if len(devices) == 0:
        print_error('There is no available devices!')
        exit(1)

    if len(devices) > 1:
        print_question(f'There is more than one device, which one you wanna use? '
                       f'({colored("select by the index", attrs=["bold"])}): ')
        for i, device_name in enumerate(devices):
            new_index = i + 1
            print('-', f'[{new_index}]', colored(device_name, attrs=['bold']))

        user_choice = -1
        while user_choice == -1:
            try:
                user_choice = int(input(colored('> ', color='yellow', attrs=['bold']))) - 1
                if user_choice < 0 or user_choice > len(devices) - 1:
                    print_error('Your choice is out of range!')
                    user_choice = -1
                else:
                    device = devices[user_choice]
            except ValueError:
                print_error('Your input must be a valid integer!')
    else:
        device = devices[0]
    return device


def parse_package(pkg: str) -> (str, str):
    """Parse the output from ADB

    :param pkg: The output of ADB
    :return: The name and the path of the package
    """
    tmp = pkg.split(':')[1]
    k = tmp.rfind('/')
    pkg_path = ''
    for i in range(k):
        if not i > k:
            pkg_path += tmp[i]
    return pkg.split('/')[-1].split('=')[1], pkg_path


def get_package(app_name: str) -> (str, str):
    """Enumerate the package based in the user input

    :param app_name: The name of the application
    :return: Application ID that contains or match with `app_name`
    """
    command_packages = adb_command_handler(f'shell pm list packages -f -3 {app_name}')

    if not command_packages:
        print_error('Unable to find any Android application by given name!')
        exit(1)

    packages = command_packages.split('\n')
    del packages[-1]
    if len(packages) == 1:
        return parse_package(packages[0])

    print_question('There is more than one application that match your input, '
                   f'which one you wanna use? {colored("(select by the index)", attrs=["bold"])}')
    for i, pkg in enumerate(packages):
        new_index = i + 1
        pkg_name, pkg_path = parse_package(pkg)
        print('-', f'[{new_index}]', colored(pkg_name, attrs=['bold']), f'({pkg_path})')

    user_choice = -1
    while user_choice == -1:
        try:
            user_choice = int(input(colored('> ', color='yellow', attrs=['bold']))) - 1
            if user_choice < 0 or user_choice > len(packages) - 1:
                print_error('Your choice is out of range!')
                user_choice = -1
            else:
                tmp = packages[0].split(':')[1]
                k = tmp.rfind('/')
                pkg_path = ''
                for i in range(k):
                    if not i > k:
                        pkg_path += tmp[i]
                return packages[0].split('/')[-1].split('=')[1], pkg_path
        except ValueError:
            print_error('Your input must be a valid integer!')


def dump_package(app_name: str, app_path: str):
    output_path = path.join(getcwd(), app_name)
    if path.isdir(output_path):
        print_error(f'Output directory ({output_path}) already exist!')
        exit(1)

    pkgs = list((file for file in adb_command_handler(f'shell ls {app_path}').split('\n') if file.endswith('.apk')))
    if len(pkgs) == 0:
        print_error('Unable to find any .apk inside package installation directory!')
        exit(1)

    Path(output_path).mkdir()
    for pkg in pkgs:
        print_info(f'Pulling {pkg}...')
        pkg_output_path = path.join(output_path, pkg)
        adb_command_handler(f'pull {app_path}/{pkg} {pkg_output_path}')


ADB_PATH = ''
ADB_DEVICE = ''


def main():
    init()

    if len(argv) != 2:
        print_error('You must provide ONLY the Android application name!\n')
        app_help()
        exit(1)

    if argv[1] in ['-h', '--help']:
        app_help()
        exit()

    if not argv[1].isprintable() or any(c in '"!@#$%^&*;()-+?_=,<>/''' for c in argv[1]):
        print_error('You inputted bad chars, only alpha is allowed!')
        exit(1)

    global ADB_PATH
    ADB_PATH = check_adb()

    global ADB_DEVICE
    ADB_DEVICE = check_device()

    print_info(f'Using device {colored(ADB_DEVICE, attrs=["bold"])}')
    app_name, app_path = get_package(argv[1])
    print_info(f'Find application {colored(app_name, attrs=["bold"])} ({app_path})')
    dump_package(app_name, app_path)
    print_info(f'Done, your application is now locally on {colored(f"./{app_name}", attrs=["bold"])}.')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_info('Exiting gracefully...')
        try:
            exit(130)
        except SystemExit:
            exit(1)
