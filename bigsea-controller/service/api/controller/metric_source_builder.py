# Copyright (c) 2017 LSD - UFCG.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from service.api.controller.plugins.monasca.monasca_metric_source import Monasca_Metric_Source
from service.api.controller.plugins.nop.nop_metric_source import Nop_Metric_Source
from service.api.controller.plugins.spark.spark_metric_source import Spark_Metric_Source
from service.api.controller.plugins.os_generic.os_generic_metric_source import OS_Generic_Metric_Source


class Metric_Source_Builder:

    def get_metric_source(self, name, parameters):
        if name == "monasca":
            return Monasca_Metric_Source(parameters)
        elif name == "nop":
            return Nop_Metric_Source()
        elif name == "spark":
            return Spark_Metric_Source(parameters)
        elif name == "os-generic":
            return OS_Generic_Metric_Source(parameters)
        else:
            # FIXME: exception type
            raise Exception("Unknown metric source type")
