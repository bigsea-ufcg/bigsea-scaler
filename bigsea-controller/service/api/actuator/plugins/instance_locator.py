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

from service.exceptions.kvm_exceptions import InstanceNotFoundException

# TODO: documentation


class Instance_Locator(object):

    def __init__(self, ssh_utils, compute_nodes, compute_nodes_key):
        self.compute_nodes = compute_nodes
        self.compute_nodes_key = compute_nodes_key
        self.ssh_utils = ssh_utils

    def locate(self, vm_id):
        # TODO: check vm_id
        for compute_node in self.compute_nodes:
            check_command = "virsh schedinfo %s > /dev/null 2> /dev/null ; echo $?" % (vm_id)
            in_node = self.ssh_utils.run_and_get_result(check_command, "root", compute_node, self.compute_nodes_key)
            if in_node == "0\n":
                return compute_node

        raise InstanceNotFoundException(vm_id,
                                        "It was not possible to find the instance: command %s, ssh return value %s" %
                                        (check_command, in_node))
