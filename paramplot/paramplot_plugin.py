from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
import tensorflow as tf
from werkzeug import wrappers

from tensorboard.backend import http_util
from tensorboard.backend.event_processing import event_multiplexer
from tensorboard.plugins import base_plugin
from tensorboard.backend.event_processing import io_wrapper

class ParamPlotPlugin(base_plugin.TBPlugin):
    """A plugin that serves greetings recorded during model runs."""

    # This static property will also be included within routes (URL paths)
    # offered by this plugin. This property must uniquely identify this plugin
    # from all other plugins.
    plugin_name = 'paramplot'

    def __init__(self, context: base_plugin.TBContext):
        """Instantiates a ParamPlotPlugin.

        Args:
          context: A base_plugin.TBContext instance. A magic container that
            TensorBoard uses to make objects available to the plugin.
        """
        # We retrieve the multiplexer from the context and store a reference
        # to it.
        self._multiplexer: event_multiplexer.EventMultiplexer = context.multiplexer
        self._context = context

        self._parameter_config = {}
        self.parameters = []
      
    def _initialise_config(self):
      # On the first request to getting the parameters, construct the config object
      if not self._parameter_config:
        # Read in all the config files in each run and create the combined config
        for run_name in self._multiplexer.Runs().keys():
          run_path = os.path.join(self._context.logdir, run_name, 'runparams.json')
          with open(run_path, 'r') as config_file_handle:
            self._parameter_config[run_name] = json.loads(config_file_handle.read())
    
        # backfill any parameters which are missing with default values
        parameter_keys = list(map(lambda x: x.keys(), self._parameter_config.values()))
        print(parameter_keys)
        self.parameters = set(parameter_keys[0])
        for parameter_list in parameter_keys[1:]:
          self.parameters.update(parameter_list)

        for run_name in self._parameter_config:
          run_parameters = self._parameter_config[run_name]
          for parameter in self.parameters:
            if parameter not in run_parameters:
              run_parameters[parameter] = 0 # We assume all parameter values are numerical so NaN is a suitable sentinel value

    def _get_valid_runs(self):
        return [run for run in self._multiplexer.Runs() if run in self._parameter_config]

    @wrappers.Request.application
    def tags_route(self, request):
        """A route (HTTP handler) that returns a response with tags.

        Returns:
          A response that contains a JSON object. The keys of the object
          are all the runs. Each run is mapped to a (potentially empty)
          list of all tags that are relevant to this plugin.
        """
        # This is a dictionary mapping from run to (tag to string content).
        # To be clear, the values of the dictionary are dictionaries.
        all_runs = self._multiplexer.PluginRunToTagToContent(
            ParamPlotPlugin.plugin_name)

        # tagToContent is itself a dictionary mapping tag name to string
        # content. We retrieve the keys of that dictionary to obtain a
        # list of tags associated with each run.
        response = {
            run: list(tagToContent.keys())
            for (run, tagToContent) in all_runs.items()
        }
        return http_util.Respond(request, response, 'application/json')

    def get_plugin_apps(self):
        """Gets all routes offered by the plugin.

        This method is called by TensorBoard when retrieving all the
        routes offered by the plugin.

        Returns:
          A dictionary mapping URL path to route that handles it.
        """
        # Note that the methods handling routes are decorated with
        # @wrappers.Request.application.
        return {
            '/tags': self.tags_route,
            '/paramdatabytag': self._paramdatabytag_route,
            '/parameters': self._parameters_route,
        }

    def is_active(self):
        """Determines whether this plugin is active.

        This plugin is only active if there are runs in the runparams file which intersect with the available runs being monitored in the logdir

        Returns:
          Whether this plugin is active.
        """
        if not self._multiplexer:
          return False

        # The plugin is active if there are any runs in the runparam dictionary which are in the logdir
        return bool(any(self._get_valid_runs()))
    
    def _get_tensor_events_payload(self, parameter, tag):
      processed_events = []
      # Loop through all the runs and compute the data which has parameter value as the independent variable and tensors as the dependent value
      for run in self._get_valid_runs():
        tensor_events = self._multiplexer.Tensors(run, tag)
        param_value = self._parameter_config[run][parameter]
        processed_events = processed_events + [{"run": run, "payload": (ev.wall_time, param_value, tf.make_ndarray(ev.tensor_proto).item())} for ev in tensor_events] 
      return processed_events

    @wrappers.Request.application
    def _paramdatabytag_route(self, request):
      """A route which returns the runparams for a particular run along with the tag specific data

      Returns:
        A JSON object of the form:
        [(wall_time, parameter_value, tag)] for each run
      """

      parameter = request.args.get('parameter')
      tag = request.args.get('tag')

      response = self._get_tensor_events_payload(parameter, tag)

      return http_util.Respond(request, response, 'application/json')

    @wrappers.Request.application
    def _parameters_route(self, request):
      """A route which returns the list of paramaters which each run is tagged with in the run parameters json file

      Returns: A JSON object which is an array of parameter names (it is an assumption of the runparams schema all 
      runs will be tagged with the same parameters)
      """

      self._initialise_config()

      response = {
          "payload": list(self.parameters)
      }

      print(response)
      return http_util.Respond(request, response, 'application/json')

    

