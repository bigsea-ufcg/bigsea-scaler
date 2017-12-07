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

import threading
import time

from service.api.actuator.actuator_builder import Actuator_Builder
from service.api.controller.controller import Controller
from service.api.controller.metric_source_builder import Metric_Source_Builder
from service.api.controller.plugins.basic.basic_alarm import Basic_Alarm
from utils.logger import Log, configure_logging


class Single_Application_Controller(Controller):

    def __init__(self, application_id, parameters):
        self.logger = Log("single.controller.log", "controller.log")
        configure_logging()

        scaling_parameters = parameters["scaling_parameters"]

        self.application_id = application_id
        self.instances = scaling_parameters["instances"]
        self.check_interval = scaling_parameters["check_interval"]
        self.trigger_down = scaling_parameters["trigger_down"]
        self.trigger_up = scaling_parameters["trigger_up"]
        self.min_cap = scaling_parameters["min_cap"]
        self.max_cap = scaling_parameters["max_cap"]
        self.actuation_size = scaling_parameters["actuation_size"]
        self.metric_rounding = scaling_parameters["metric_rounding"]
        self.actuator_type = scaling_parameters["actuator"]
        self.metric_source_type = scaling_parameters["metric_source"]

        self.running = True
        self.running_lock = threading.RLock()

        metric_source = Metric_Source_Builder().get_metric_source(self.metric_source_type, parameters)
        actuator = Actuator_Builder().get_actuator(self.actuator_type, parameters)
        self.alarm = Basic_Alarm(actuator, metric_source, self.trigger_down, self.trigger_up,
                                 self.min_cap, self.max_cap, self.actuation_size, self.metric_rounding)

    def start_application_scaling(self):
        run = True

        while run:
            self.logger.log("Monitoring application: %s" % (self.application_id))

            self.alarm.check_application_state(self.application_id, self.instances)

            time.sleep(float(self.check_interval))

            with self.running_lock:
                run = self.running

    def stop_application_scaling(self):
        with self.running_lock:
            self.running = False

    def status(self):
        return ""
