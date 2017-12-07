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

from service.api.controller.controller_builder import Controller_Builder
import threading
from utils.logger import Log, configure_logging


class Main_Controller:

    def __init__(self):
        self.logger = Log("main.controller.log", "controller.log")
        configure_logging()

        self.controller_thread_pool = {}
        self.controller_builder = Controller_Builder()

    def start_application_scaling(self, application_id, parameters):
        self.logger.log("Adding application id: %s" % (application_id))
        plugin_name = parameters["scaler_plugin"]
        controller = self.controller_builder.get_controller(plugin_name, application_id, parameters)
        controller_thread = threading.Thread(target=controller.start_application_scaling)
        controller_thread.start()

        self.controller_thread_pool[application_id] = controller

    def stop_application_scaling(self, app_id):
        if app_id in self.controller_thread_pool.keys():
            self.logger.log("Removing application id: %s" % (app_id))
            app_controller = self.controller_thread_pool[app_id]
            app_controller.stop_application_scaling()
            self.controller_thread_pool.pop(app_id)
        else:
            self.logger.log("Application %s not found" % (app_id))

    def status(self):
        status_string = "Status: OK\n"
        status_string += "Monitoring applications:\n"
        for application_id in self.controller_thread_pool.keys():
            status_string += application_id + "\n"
            status_string += "Last action:" + self.controller_thread_pool[application_id].status()
            status_string += "\n"

        return status_string
