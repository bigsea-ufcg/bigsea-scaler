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

import time

from flask import Flask
from flask import request

from service.api.actuator.actuator_builder import Actuator_Builder
from service.api.controller.main_controller import Main_Controller
from utils.logger import Log
from utils.logger import configure_logging


SETUP_ROUTE = "/controller/setup_env"
START_SCALING_ROUTE = '/controller/start_scaling/<app_id>'
STOP_SCALING_ROUTE = '/controller/stop_scaling/<app_id>'
STATUS = '/controller/status'

app = Flask(__name__)

# Set up logging
logger = Log("controller.api.logger", "controller.api.log")
configure_logging()

main_controller = Main_Controller()

# API methods
# TODO: use Telles' code here


@app.route(SETUP_ROUTE, methods=['POST'])
def prepare_environment():
    data = request.json

    plugin_name = data["actuator"]
    actuator = Actuator_Builder().get_actuator(plugin_name, data)

    logger.log("%s-Preparing environment for instances %s" %
               (time.strftime("%H:%M:%S"), str(data)))

    try:
        actuator.adjust_resources(data['instances_cap'])
    except Exception as e:
        logger.log(str(e))

    return "prepared_environment"

# TODO: use Telles' code here


@app.route(START_SCALING_ROUTE, methods=['POST'])
def start_application_scaling(app_id):
    data = request.json
    logger.log("%s-Started scaling for application %s using parameters:%s" %
               (time.strftime("%H:%M:%S"), app_id, str(data)))

    main_controller.start_application_scaling(app_id, data)

    return "started-scaling"

# TODO: use Telles' code here


@app.route(STOP_SCALING_ROUTE, methods=['POST'])
def stop_application_scaling(app_id):
    logger.log("%s-Stopped scaling for application %s" %
               (time.strftime("%H:%M:%S"), app_id))

    main_controller.stop_application_scaling(app_id)

    return "stopped-scaling"


@app.route(STATUS, methods=['GET'])
def status():
    return main_controller.status()
