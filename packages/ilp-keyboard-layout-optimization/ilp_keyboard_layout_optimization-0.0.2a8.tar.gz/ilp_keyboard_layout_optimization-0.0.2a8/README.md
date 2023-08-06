# Keyboard layout optimization via ILP

This repository contains my implementation of the task to optimize a keyboard layout 
in terms of assigning the available characters to the keys in a clever way. This is 
part of my participation in the _Seminar: Integer Programming modeling of puzzles, 
games, and real-world problems_ during the winter term 21/22 at Technische 
Universität zu Berlin.

## Usage

This code requires the [SCIP Optimization Suite
](https://www.scipopt.org/index.php#download) to be installed on the machine to be 
used, which we prepared in a Docker image at [docker_pyscipopt
](https://github.com/BjoernLudwigPTB/docker_pyscipopt). The proper use of this image 
is well documented in its [README.md
](https://github.com/BjoernLudwigPTB/docker_pyscipopt#how-to-build-image). The 
actual code can then be found in the [_src/ilp_keyboard_layout_optimization_ subfolder
](https://git.tu-berlin.de/blutub3d/ilp_keyboard_layout_optimization/-/tree/main/src/ilp_keyboard_layout_optimization).

## Remote development

We included [a bash script _pull_and_optimize.sh_
](https://git.tu-berlin.de/blutub3d/ilp_keyboard_layout_optimization/-/blob/main/pull_and_optimize.sh)
in our codebase to streamline a remote development workflow. We work on the code on a 
computer, that is well-equipped for that task. The committed and pushed code then 
gets processed on another machine, which uses this script, to update its code base 
and run the parameters handed over. It is designed to be called without parameters
to execute the _optimize_ module of the [latest version released on Test.PyPI.org
](https://test.pypi.org/project/ilp-keyboard-layout-optimization/).

```shell
$ ./pull_and_optimize.sh
```

The execution requires the Docker image of our repository [docker_pyscipopt
](https://github.com/BjoernLudwigPTB/docker_pyscipopt) to be built in advance, but it 
could be easily adapted for a local installation of the SCIP Optimization Suite.