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

from api.v10 import app
import ConfigParser
import utils.logger as logging


def main():
    config = ConfigParser.RawConfigParser()
    config.read("controller.cfg")

    host = config.get("flask", "host")
    port = config.getint("flask", "port")

    enable_logging = config.get("logging", "enable")
    logging_level = config.get("logging", "level")

    if enable_logging == "True":
        logging.enable()
        logging.configure_logging(logging_level)
    else:
        logging.disable()

    app.run(host, port, debug=True)


if __name__ == "__main__":
    main()
