#!/usr/bin/env python3

# Copyright © 2022 erzo <erzo@posteo.de>
# This work is free. You can use, copy, modify, and/or distribute it
# under the terms of the BSD Zero Clause License, see LICENSE.

"""
usage: gits [<options>] [<commit>]

This is a wrapper around `git show` using the details view from gitl.
It takes the following command line arguments:

    --config FILE   a config file to load instead of the default config file
                    if you want to load this additionally to the default config file
                    start the file with `config.load --default`
    --command-pipe FILE
                    a named pipe which another program can write
                    commands to which gits will execute.
                    Create the pipe with `mkfifo FILE`.
                    The pipe is deleted by gits when gits quits
                    so that the controller can check if gits is still running.
    --open-always   open an urwid screen even if the view is empty
                    or if the start up checks do not pass, e.g. if
                    the current working directory is not a git repository.
                    This is useful if you want to run this in a separate terminal
                    window which closes immediately when this program quits.
    --version       show the version of this progam as well as
                    the used python, urwid and git versions
    -h, --help      show this help

All other command line arguments are passed through to git show.
You can use that for example in your vimrc:

    map <c-c> :!gits <C-r><C-w><cr><cr>

With that line pressing control + c opens the commit whose hash id is under the cursor.
This is useful while writing a commit message if you want to verify that you have copied
the correct hash or when doing an interactive rebase.

For more information see `git show --help`.
"""

from . import main
from . import check

main.DetailsView.max_lines_per_file = 2000


def run():
	import sys

	args = sys.argv[1:]

	FLAG_OPEN_ALWAYS = "--open-always"

	config_file = main.get_arg_with_one_argument(args, "--config")
	cmdpipe = main.get_arg_with_one_argument(args, "--command-pipe")

	if FLAG_OPEN_ALWAYS in args:
		args.remove(FLAG_OPEN_ALWAYS)
		open_always = True
	else:
		open_always = False

	if not args:
		diff_args = []
		hash_id = "HEAD"
	else:
		diff_args = args[:-1]
		hash_id = args[-1]

	if '--help' in args or '-h' in args:
		print(__doc__.strip('\n'))
		exit()
	if "--version" in args:
		main.print_version()
		exit()

	a = main.App(show=hash_id, diff_args=diff_args, config_file=config_file, command_pipe=cmdpipe, open_always=open_always)

	while a.continue_running:
		a.run()
		a.run_external_if_requested()


if __name__ == '__main__':
	run()
