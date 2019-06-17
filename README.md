# GR Tensorboard - a collection of plugins for tensorboard

<!-- This document was last reviewed on Nov 1, 2018. It should be
reviewed occasionally to make sure it stays up-to-date. -->

How to build and run
====================
I have provided a script build_and_run_pip_package.sh which should be run in the directory above this with a virtual environment activated. It assumes that the directory with all the gr tensorboard code is called gr_tensorboard (clearly because i like to make things more difficult). This script will run bazel to build all the assets and then build the pip wheel, exporting the assets and then installing the wheel to your virtual environment. It will finally call grtensorboard with some default command line arguments. 

Bazel versions
==============
I had found difficulty in determining a suitable version of bazel with which to build grtensorboard and have settled with bazel 0.21.0 (obtained through binary search between broken versions). Bazel build command used is located in build_pip_package.sh and is ```bazel build --incompatible_remove_native_http_archive=false --incompatible_package_name_is_a_function=false :gr_tensorboard```. You may find a more up to date version of bazel to build tensorboard. If so then do feel free to use the up to date version.

What plugins already exist 
==========================
Currently, I have developed (and am continuing to develop) two plugins:
1. Runsenabler - a tool to select which runs are exposed to tensorboard during runtime
2. Paramplot - a tool to plot metrics against parameter configurations for each run

RunsEnabler
===========
![RunsEnabler Dashboard](/images/runsenabler.png)

## Overview
There are two columns, each with a regex for search / filtering: 

### Left column
1. The regex at the top is called the *group regex* and groups the runs by regex match
2. Left column displays regex matches of runs (which match the left regex called the *group regex*), each group being togglable by a checkbox
   Toggling the checkbox for a run group will enable or disable all the runs in that particular group (these are the runs which match *group regex* with the matching substring being the group key)
3. There are buttons to enable and disable *all* run groups (and hence all runs which match the *group regex*)
4. There is a checkbox below the regex text input which if enabled will enable newly created runs iff the new runs match the regex (useful so that tensorboard can automatically pick up and enable newly created runs)

### Right column
1. the regex at the top will filter the runs displayed whose corresponding run groups in the left column have been enabled
2. runs which *do not* match the regex will still maintain their current state (either ENABLED or DISABLED) 
3. Enable and disable all runs buttons exist to respectively enable or disable all the visible runs 
4. Checkboxes next to each run allow the user to enable or disable each run individually
