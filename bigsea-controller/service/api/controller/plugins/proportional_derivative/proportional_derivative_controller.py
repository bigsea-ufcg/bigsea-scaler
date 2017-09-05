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

from service.api.controller.controller import Controller
from utils.logger import Log, configure_logging
import threading
from service.api.controller.metric_source_builder import Metric_Source_Builder
from service.api.actuator.actuator_builder import Actuator_Builder
from service.api.controller.plugins.proportional_derivative.proportional_derivative_alarm import ProportionalDerivativeAlarm
from service.exceptions.monasca_exceptions import No_Metrics_Exception
import time

class ProportionalDerivativeController(Controller):
    
    def __init__(self, application_id, parameters):
        self.logger = Log("proportional_derivative.controller.log", "controller.log")
        configure_logging()
        
        self.application_id = application_id
        # read scaling parameters
        self.instances = parameters["instances"]
        self.check_interval = parameters["check_interval"]
        self.trigger_down = parameters["trigger_down"]
        self.trigger_up = parameters["trigger_up"]
        self.min_cap = parameters["min_cap"]
        self.max_cap = parameters["max_cap"]
        self.metric_rounding = parameters["metric_rounding"]
        # The actuator plugin name
        self.actuator_type = parameters["actuator"]
        # The metric source plugin name
        self.metric_source_type = parameters["metric_source"]
        self.heuristic_options = parameters["heuristic_options"]
        
        # We use a lock here to prevent race conditions when stopping the controller
        self.running = True
        self.running_lock = threading.RLock()
        
        # Gets a new metric source plugin using the given name
        metric_source = Metric_Source_Builder().get_metric_source(self.metric_source_type, parameters)
        # Gets a new actuator plugin using the given name
        actuator = Actuator_Builder().get_actuator(self.actuator_type)
        # The alarm here is responsible for deciding whether to scale up or down, or even do nothing
        self.alarm = ProportionalDerivativeAlarm(actuator, metric_source, self.trigger_down, self.trigger_up, 
                                 self.min_cap, self.max_cap, self.metric_rounding, self.heuristic_options)
        
    def start_application_scaling(self):
        run = True
        
        while run:
            self.logger.log("Monitoring application: %s" % (self.application_id))

            # Call the alarm to check the application
            try:
                self.alarm.check_application_state(self.application_id, self.instances)
            except No_Metrics_Exception: 
                self.logger.log("No metrics available")
            except Exception as e:
                self.logger.log(str(e))

            # Wait some time
            time.sleep(float(self.check_interval))
            
            with self.running_lock:
                run = self.running
            
    def stop_application_scaling(self):
        with self.running_lock:
            self.running = False
            
    def status(self):
        return self.alarm.status()