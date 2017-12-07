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
import paramiko

from service.api.actuator.plugins.instance_locator_tunnel import Instance_Locator_Tunnel
from service.api.actuator.plugins.remote_KVM_tunnel import Remote_KVM_Tunnel
from utils.ssh_utils import SSH_Utils
from service.api.actuator.plugins.kvm_actuator import KVM_Actuator
from service.api.actuator.plugins.instance_locator import Instance_Locator
from service.api.actuator.plugins.remote_kvm import Remote_KVM
from service.api.actuator.plugins.nop_actuator import Nop_Actuator
from service.api.actuator.plugins.service_actuator import Service_Actuator
from service.api.actuator.plugins.service_instance_locator import Service_Instance_Locator
from service.api.actuator.plugins.kvm_io_actuator import KVM_IO_Actuator
from service.api.actuator.plugins.kvm_upv import KVM_Actuator_UPV


# TODO: documentation
class Actuator_Builder:

    def get_actuator(self, name, parameters):
        config = ConfigParser.RawConfigParser()
        config.read("controller.cfg")

        authorization_url = config.get("authorization", "authorization_url")
        bigsea_username = parameters["bigsea_username"]
        bigsea_password = parameters["bigsea_password"]

        authorization_data = dict(authorization_url=authorization_url,
                                  bigsea_username=bigsea_username,
                                  bigsea_password=bigsea_password)

        if name == "kvm":
            compute_nodes_str = config.get("actuator", "compute_nodes")
            compute_nodes_keypair = config.get("actuator", "keypair_compute_nodes")
            iops_reference = config.getint("actuator", "iops_reference")
            bs_reference = config.getint("actuator", "bs_reference")
            default_io_cap = config.getint("actuator", "default_io_cap")

            compute_nodes = [x.strip() for x in compute_nodes_str.split(",")]

            instance_locator = Instance_Locator(SSH_Utils({}), compute_nodes, compute_nodes_keypair)
            remote_kvm = Remote_KVM(SSH_Utils({}), compute_nodes_keypair,
                                    iops_reference, bs_reference)
            return KVM_Actuator(instance_locator, remote_kvm, authorization_data, default_io_cap)

        elif name == "kvm-tunnel":
            compute_nodes_str = config.get("actuator", "compute_nodes")
            compute_nodes_keypair = config.get("actuator", "keypair_compute_nodes")
            iops_reference = config.getint("actuator", "iops_reference")
            bs_reference = config.getint("actuator", "bs_reference")
            default_io_cap = config.getint("actuator", "default_io_cap")

            compute_nodes = [x.strip() for x in compute_nodes_str.split(",")]

            ports_str = config.get("actuator", "tunnel_ports")
            ports = [x.strip() for x in ports_str.split(",")]

            hosts_ports = {compute_nodes[i]: ports[i] for i in xrange(len(ports))}

            instance_locator = Instance_Locator_Tunnel(SSH_Utils(hosts_ports), compute_nodes,
                                                       compute_nodes_keypair)
            remote_kvm = Remote_KVM_Tunnel(SSH_Utils(hosts_ports), compute_nodes_keypair,
                                           iops_reference, bs_reference)
            return KVM_Actuator(instance_locator, remote_kvm, authorization_data, default_io_cap)

        elif name == "kvm-io":
            compute_nodes_str = config.get("actuator", "compute_nodes")
            compute_nodes_keypair = config.get("actuator", "keypair_compute_nodes")
            iops_reference = config.getint("actuator", "iops_reference")
            bs_reference = config.getint("actuator", "bs_reference")
            compute_nodes = [x.strip() for x in compute_nodes_str.split(",")]

            instance_locator = Instance_Locator(SSH_Utils({}), compute_nodes, compute_nodes_keypair)
            remote_kvm = Remote_KVM(SSH_Utils({}), compute_nodes_keypair, iops_reference,
                                    bs_reference)
            return KVM_IO_Actuator(instance_locator, remote_kvm, authorization_data)

        elif name == "kvm-io-tunnel":
            compute_nodes_str = config.get("actuator", "compute_nodes")
            compute_nodes_keypair = config.get("actuator", "keypair_compute_nodes")
            iops_reference = config.getint("actuator", "iops_reference")
            bs_reference = config.getint("actuator", "bs_reference")

            compute_nodes = [x.strip() for x in compute_nodes_str.split(",")]

            ports_str = config.get("actuator", "tunnel_ports")
            ports = [x.strip() for x in ports_str.split(",")]

            hosts_ports = {compute_nodes[i]: ports[i] for i in xrange(len(ports))}

            instance_locator = Instance_Locator_Tunnel(SSH_Utils(hosts_ports), compute_nodes,
                                                       compute_nodes_keypair)
            remote_kvm = Remote_KVM_Tunnel(SSH_Utils(hosts_ports), compute_nodes_keypair,
                                           iops_reference, bs_reference)
            return KVM_IO_Actuator(instance_locator, remote_kvm, authorization_data)

        elif name == "kvm-upv":
            iops_reference = config.getint("actuator", "iops_reference")
            bs_reference = config.getint("actuator", "bs_reference")

            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname=config.get("actuator", "access_ip"),
                         username=config.get("actuator", "access_username"),
                         password=config.get("actuator", "access_password"))

            return KVM_Actuator_UPV(conn, iops_reference, bs_reference)

        elif name == "nop":
            return Nop_Actuator()
        elif name == "service":
            actuator_port = config.get("actuator", "actuator_port")

            compute_nodes_str = config.get("actuator", "compute_nodes")
            compute_nodes = [x.strip() for x in compute_nodes_str.split(",")]

            instance_locator = Service_Instance_Locator(compute_nodes, actuator_port)
            return Service_Actuator(actuator_port, instance_locator)
        else:
            # FIXME: review this exception type
            raise Exception("Unknown actuator type")
