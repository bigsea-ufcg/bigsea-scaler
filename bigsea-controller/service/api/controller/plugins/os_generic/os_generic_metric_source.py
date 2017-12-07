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

from service.api.controller.metric_source import Metric_Source
from utils.logger import Log, configure_logging
import paramiko
import time
import datetime


class OS_Generic_Metric_Source(Metric_Source):

    def __init__(self, parameters):
        self.keypair_path = parameters['keypair_path']
        self.host_ip = parameters['host_ip']
        self.log_path = parameters['log_path']
        self.start_time = parameters['start_time']
        self.expected_time = parameters['expected_time']
        self.host_username = 'ubuntu'
        self.last_checked = ''
        self.logger = Log("metrics.log", "metrics.log")
        configure_logging()

    def _get_metric_value_from_log_line(self, log):
        value = None
        for i in range(len(log) - 1, 0, -1):
            if log[i] == '#':
                value = float(log[i + 1:-1])
        return value

    def _get_elapsed_time(self):
        delay = time.time() - self.start_time
        return delay

    # This method returns a remote connection with the host where
    # the log will be captured. It is possible to execute a command
    # in the host using the function c.exec_command("write_command_here")
    # with the object returned here
    def _get_ssh_connection(self):
        keypair = paramiko.RSAKey.from_private_key_file(self.keypair_path)
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(hostname=self.host_ip,
                     username=self.host_username, pkey=keypair)
        return conn

    # This is an auxiliary function to prepare and publish the metric. The point is to keep
    # monitoring_application as simple as possible.
    def _extract_metric_from_log(self, last_log):
        # Check if this log line contains a new metric measurement.
        if '[Progress]' in last_log and self.last_checked != last_log:
            self.last_checked = last_log
            ref_value = self._get_elapsed_time() / self.expected_time
            measurement_value = self._get_metric_value_from_log_line(last_log)
            error = measurement_value - ref_value
            self.logger.log("ref-value:%f|measurement-value:%f|error:%f" % (ref_value,
                                                                            measurement_value, error))
            return error
        # Flag that checks if the log capture is ended
        elif '[END]' in last_log:
            self.running = False

    def _monitoring_application(self):
        try:
            # First of all, a connection with the host is created.
            conn = self._get_ssh_connection()
            # The second step consists in execute the command to capture the last log line from
            # the log file using the connection create below and saving the outputs.
            stdin, stdout, stderr = conn.exec_command(
                "sudo tail -1 %s" % self.log_path)
            timestamp = datetime.datetime.fromtimestamp(time.time())
            return timestamp, self._extract_metric_from_log(stdout.read())

        except Exception as ex:
            print "Monitoring is not possible. \nError: %s" % (ex.message)
            raise ex

    def get_most_recent_value(self, metric_name, options):
        return self._monitoring_application()
