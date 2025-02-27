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
"""TFX ExampleValidator component definition."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Optional, Text

from tfx import types
from tfx.components.base import base_component
from tfx.components.schema_gen import executor
from tfx.types import standard_artifacts
from tfx.types.standard_component_specs import SchemaGenSpec


class SchemaGen(base_component.BaseComponent):
  """Official TFX SchemaGen component.

  The SchemaGen component uses Tensorflow Data Validation (tfdv) to
  generate a schema from input statistics.
  """

  SPEC_CLASS = SchemaGenSpec
  EXECUTOR_CLASS = executor.Executor

  def __init__(self,
               stats: types.Channel = None,
               infer_feature_shape: bool = True,
               output: Optional[types.Channel] = None,
               statistics: Optional[types.Channel] = None,
               name: Optional[Text] = None):
    """Constructs a SchemaGen component.

    Args:
      stats: A Channel of 'ExampleStatisticsPath' type (required if spec is not
        passed). This should contain at least a 'train' split. Other splits are
        currently ignored (required).
      infer_feature_shape: bool value indicating whether or not to infer the
        shape of features. If feature shape is not inferred, downstream
        Tensorflow Transform component using the schema will parse input
        as tf.SparseTensor.
      output: Optional output 'SchemaPath' channel for schema result.
      statistics: Forwards compatibility alias for the 'stats' argument.
      name: Optional unique name. Necessary iff multiple SchemaGen components
        are declared in the same pipeline.
    """
    stats = stats or statistics
    output = output or types.Channel(
        type=standard_artifacts.Schema, artifacts=[standard_artifacts.Schema()])
    spec = SchemaGenSpec(
        stats=stats, infer_feature_shape=infer_feature_shape, output=output)
    super(SchemaGen, self).__init__(spec=spec, name=name)
