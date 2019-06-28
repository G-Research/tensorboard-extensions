from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import shutil
import pathlib

from tensorboard import default
from tensorboard.program import TensorBoard
# from .backend import program

if sys.version_info[0] < 3:
    from paramplot import paramplot_plugin
    from runsenabler import runsenabler_loader
    print(sys.version_info)
else:
    print(sys.version_info)
    from .paramplot import paramplot_plugin
    from .runsenabler import runsenabler_loader

def run_main(asset_path):
    plugins = default.get_plugins() + [paramplot_plugin.ParamPlotPlugin, runsenabler_loader.RunsEnablerLoader("some_dir")]
    gr_tensorboard = TensorBoard(plugins, lambda: open(asset_path, 'rb'))
    gr_tensorboard.configure(sys.argv)

    use_filesystem_controller = gr_tensorboard.flags.use_filesystem_controller
    if use_filesystem_controller:
        # Retrieve the actual log directory and replace it in the context with the new logdir 
        original_logdir = pathlib.Path(tensorboard.flags.logdir)
        parent_dir = original_logdir.parent
        print("logdir provided: " + original_logdir)
        new_logdir = parent_dir / "temp_dir"
        print("creating temporary workspace in " + new_logdir)

        # Create the temp dir
        new_logdir.mkdir(parents=True)

        # swap the original logdir for the new one
        loader.actual_logdir = original_logdir
        tensorboard.flags.logdir = str(new_logdir)
        
    try:
        sys.exit(gr_tensorboard.main())
    except:
        if use_filesystem_controller:
            

