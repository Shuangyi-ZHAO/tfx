# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TFX Pusher component definition."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Any, Dict, Optional, Text, Type

from tfx import types
from tfx.components.base import base_component
from tfx.components.base import base_executor
from tfx.components.pusher import executor
from tfx.proto import pusher_pb2
from tfx.types import standard_artifacts
from tfx.types.standard_component_specs import PusherSpec


# TODO(b/133845381): Investigate other ways to keep push destination converged.
class Pusher(base_component.BaseComponent):
  """Official TFX Pusher component.

  The `Pusher` component can be used to push an validated SavedModel from output
  of `Trainer` to tensorflow Serving (tf.serving). If the model is not blessed
  by `ModelValidator`, no push will happen.
  """

  SPEC_CLASS = PusherSpec
  EXECUTOR_CLASS = executor.Executor

  def __init__(
      self,
      model_export: types.Channel = None,
      model_blessing: types.Channel = None,
      push_destination: Optional[pusher_pb2.PushDestination] = None,
      custom_config: Optional[Dict[Text, Any]] = None,
      executor_class: Optional[Type[base_executor.BaseExecutor]] = None,
      model_push: Optional[types.Channel] = None,
      model: Optional[types.Channel] = None,
      name: Optional[Text] = None):
    """Construct a Pusher component.

    Args:
      model_export: A Channel of 'ModelExportPath' type, usually produced by
        Trainer component (required).
      model_blessing: A Channel of 'ModelBlessingPath' type, usually produced by
        ModelValidator component (required).
      push_destination: A pusher_pb2.PushDestination instance, providing
        info for tensorflow serving to load models. Optional if executor_class
        doesn't require push_destination.
      custom_config: A dict which contains the deployment job parameters to be
        passed to Google Cloud ML Engine.  For the full set of parameters
        supported by Google Cloud ML Engine, refer to
        https://cloud.google.com/ml-engine/reference/rest/v1/projects.models
      executor_class: Optional custom python executor class.
      model_push: Optional output 'ModelPushPath' channel with result of push.
      model: Forwards compatibility alias for the 'model_exports' argument.
      name: Optional unique name. Necessary if multiple Pusher components are
        declared in the same pipeline.
    """
    model_export = model_export or model
    model_push = model_push or types.Channel(
        type=standard_artifacts.PushedModel,
        artifacts=[standard_artifacts.PushedModel()])
    if push_destination is None and not executor_class:
      raise ValueError('push_destination is required unless a custom '
                       'executor_class is supplied that does not require '
                       'it.')
    spec = PusherSpec(
        model_export=model_export,
        model_blessing=model_blessing,
        push_destination=push_destination,
        custom_config=custom_config,
        model_push=model_push)
    super(Pusher, self).__init__(spec=spec,
                                 custom_executor_class=executor_class,
                                 name=name)
