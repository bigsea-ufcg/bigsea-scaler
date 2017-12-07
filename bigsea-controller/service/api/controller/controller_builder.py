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

import ConfigParser

from service.api.controller.plugins.basic.basic_controller import Basic_Controller
from service.api.controller.metric_source_builder import Metric_Source_Builder
from service.api.actuator.actuator_builder import Actuator_Builder
from service.api.controller.plugins.single_application_controller import Single_Application_Controller
from service.api.controller.plugins.generic.generic_controller import Generic_Controller
from service.api.controller.plugins.tendency.tendency_aware_proportional_controller import (
    Tendency_Aware_Proportional_Controller
)
from service.api.controller.plugins.proportional.proportional_controller import Proportional_Controller
from service.api.controller.plugins.proportional_derivative.proportional_derivative_controller import (
    ProportionalDerivativeController
)


class Controller_Builder:

    def __init__(self):
        pass

    def get_controller(self, name, application_id, parameters):
        if name == "basic":
            config = ConfigParser.RawConfigParser()
            config.read("controller.cfg")

            # Read scaling policy
            metric_source_type = config.get("policy", "metric_source")
            actuator_type = config.get("policy", "actuator")

            # Read configuration
            check_interval = config.getfloat("scaling", "check_interval")
            trigger_down = config.getfloat("scaling", "trigger_down")
            trigger_up = config.getfloat("scaling", "trigger_up")
            min_cap = config.getfloat("scaling", "min_cap")
            max_cap = config.getfloat("scaling", "max_cap")
            actuation_size = config.getfloat("scaling", "actuation_size")
            metric_rounding = config.getint("scaling", "metric_rounding")

            parameters = {"check_interval": check_interval, "trigger_down": trigger_down,
                          "trigger_up": trigger_up, "min_cap": min_cap, "max_cap": max_cap,
                          "actuation_size": actuation_size, "metric_rounding": metric_rounding}

            metric_source = Metric_Source_Builder().get_metric_source(metric_source_type)
            actuator = Actuator_Builder().get_actuator(actuator_type)

            return Basic_Controller(metric_source, actuator, parameters)
        elif name == "single":
            return Single_Application_Controller(application_id, parameters)
        elif name == "progress-error":
            return Generic_Controller(application_id, parameters)
        elif name == "proportional":
            return Proportional_Controller(application_id, parameters)
        elif name == "proportional_derivative":
            return ProportionalDerivativeController(application_id, parameters)
        elif name == "progress-tendency":
            return Tendency_Aware_Proportional_Controller(application_id, parameters)
        else:
            # FIXME: exception type
            raise Exception("Unknown controller type")
