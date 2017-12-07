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

# TODO: Documentation


class Remote_KVM_Tunnel:

    def __init__(self, ssh_utils, compute_nodes_key, iops_reference=1000, bs_reference=1000000):
        self.ssh_utils = ssh_utils
        self.compute_nodes_key = compute_nodes_key
        self.iops_reference = iops_reference
        self.bs_reference = bs_reference

    def change_vcpu_quota(self, host_ip, vm_id, cap):
        # TODO: check ip value
        # TODO: check id value
        if cap < 0 or cap > 100:
            # FIXME review this exception type
            raise Exception("Invalid cap value")

        command = "virsh schedinfo %s" \
            " --set vcpu_quota=$(( %s * `virsh schedinfo %s | awk 'FNR == 3 {print $3}'`/100 ))" \
            " > /dev/null" % (vm_id, cap, vm_id)

        # TODO: check errors
        self.ssh_utils.run_command_tunnel(
            command, "root", host_ip, self.compute_nodes_key)

    def change_io_quota(self, host_ip, vm_id, cap):
        if cap < 0 or cap > 100:
            # FIXME review this exception type
            raise Exception("Invalid cap value")

        command_iops_quota = (cap * self.iops_reference) / 100
        command_bs_quota = (cap * self.bs_reference) / 100

        command_set_io_quota = "virsh blkdeviotune %s" \
            " \"`virsh domblklist %s | awk 'FNR == 3 {print $1}'`\"" \
            " --current --total_iops_sec %s --total_bytes_sec %s" % (vm_id, vm_id,
                                                                     command_iops_quota, command_bs_quota)

        self.ssh_utils.run_command_tunnel(command_set_io_quota, "root", host_ip,
                                          self.compute_nodes_key)

    # TODO: Change this method name to get_vcpu_quota
    def get_allocated_resources(self, host_ip, vm_id):
        # TODO: check ip value
        # TODO: check id value
        command = "virsh schedinfo %s" \
            " | awk '{if(NR==3){period=$3} if(NR==4){print 100*$3/period}}'" % (vm_id)

        # TODO: check errors
        ssh_result = self.ssh_utils.run_and_get_result_tunnel(command, "root", host_ip,
                                                              self.compute_nodes_key)

        try:
            cap = int(ssh_result)

            if cap == 0:
                raise Exception("Could not get allocated resources")

            if cap < 0:
                return 100
            return cap
        except:
            # FIXME: review this exception type
            raise Exception("Could not get allocated resources")

    def get_io_quota(self, host_ip, vm_id):
        command = "virsh blkdeviotune %s" \
            " \"`virsh domblklist %s | awk 'FNR == 3 {print $1}'`\"" \
            " | grep total_iops_sec: | awk '{print $2}'" % (vm_id, vm_id)

        ssh_result = self.ssh_utils.run_and_get_result_tunnel(command, "root", host_ip,
                                                              self.compute_nodes_key)

        try:
            quota = int(ssh_result)
            return 100 * quota / float(self.iops_reference)
        except:
            # FIXME: review this exception type
            raise Exception("Could not get allocated resources")
