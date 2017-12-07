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

from service.api.actuator.actuator import Actuator


class Nop_Actuator(Actuator):

    def prepare_environment(self, vm_data):
        pass

    def adjust_resources(self, vm_data):
        pass

    def get_allocated_resources(self, vm_id):
        return 100

    def get_allocated_resources_to_cluster(self, vms_ids):
        return 100
