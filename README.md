# GR Tensorboard - a collection of plugins for tensorboard

<!-- This document was last reviewed on Nov 1, 2018. It should be
reviewed occasionally to make sure it stays up-to-date. -->

How to build and run
====================
I have provided a script build_and_run_pip_package.sh which should be run in the directory above this with a virtual environment activated. It assumes that the directory with all the gr tensorboard code is called gr_tensorboard (clearly because i like to make things more difficult). This script will run bazel to build all the assets and then build the pip wheel, exporting the assets and then installing the wheel to your virtual environment. It will finally call grtensorboard with some default command line arguments. 

Bazel versions
==============
I had found difficulty in determining a suitable version of bazel with which to build grtensorboard with and have settled with bazel 0.21.0 (obtained through binary search between broken versions). Bazel build command used is located in build_pip_package.sh and is ```bazel build --incompatible_remove_native_http_archive=false --incompatible_package_name_is_a_function=false :gr_tensorboard```. You may find a more up to date version of bazel to build tensorboard. If so then do feel free to use the up to date version.

What plugins already exist 
==========================
Currently, I have developed (and am continuing to develop) two plugins:
1. Runsenabler - a tool to select which runs are exposed to tensorboard during runtime
2. Paramplot - a tool to plot metrics against parameter configurations for each run

RunsEnabler
===========
![RunsEnabler Dashboard](/images/runsenabler.png)
