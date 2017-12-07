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

import paramiko


class SSH_Utils(object):

    def __init__(self, hosts_ports={}):
        self.hosts_ports = hosts_ports

    def run_command(self, command, user, host, key):
        conn = self._get_ssh_connection(host, user, key)
        conn.exec_command(command)
        conn.close()

    def run_and_get_result(self, command, user, host, key):
        conn = self._get_ssh_connection(host, user, key)
        stdout = conn.exec_command(command)[1]
        result = stdout.read()
        conn.close()
        return result

    def run_command_tunnel(self, command, user, host, key):
        conn = self._get_ssh_connection_tunnel(host, "root", key)
        conn.exec_command(command)
        conn.close()

    def run_and_get_result_tunnel(self, command, user, host, key):
        conn = self._get_ssh_connection_tunnel(host, "root", key)
        stdout = conn.exec_command(command)[1]
        result = stdout.read()
        conn.close()
        return result

    def _get_ssh_connection(self, ip, username, keypair_path):
        keypair = paramiko.RSAKey.from_private_key_file(keypair_path)
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(hostname=ip, username=username, pkey=keypair)
        return conn

    def _get_ssh_connection_tunnel(self, ip, username, keypair_path):
        keypair = paramiko.RSAKey.from_private_key_file(keypair_path)
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(hostname="127.0.0.1", port=int(self.hosts_ports[ip]), username=username, pkey=keypair)
        return conn
