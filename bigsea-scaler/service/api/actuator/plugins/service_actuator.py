from service.api.actuator.actuator import Actuator
import requests
import json

class Service_Actuator(Actuator):

    def __init__(self, actuator_port, instance_locator):
        self.instance_locator = instance_locator
        self.actuator_port = actuator_port
    
    def prepare_environment(self, vm_data):
        self.adjust_resources(vm_data)
        
    def adjust_resources(self, vm_data):
        for vm_id in vm_data.keys():
            actuator_ip = self.instance_locator.locate(vm_id)
            url = "http://" + actuator_ip + ":" + self.actuator_port + "/actuator/set_vcpu_cap/"
            cap = vm_data[vm_id]
            options = {"actuator_plugin":"kvm",
                       "vm_id":vm_id,
                       "cap":cap}
            
            requests.post(url, headers = {"Content-Type":"application/json"}, data = json.dumps(options))

    def get_allocated_resources(self, vm_id):
        try:
            actuator_ip = self.instance_locator.locate(vm_id)
            url = "http://" + actuator_ip + ":" + self.actuator_port + "/actuator/allocated_resources/"
            options = {"actuator_plugin":"kvm", "vm_id":vm_id}
            response = requests.post(url, headers = {"Content-Type":"application/json"}, data = json.dumps(options))
            return float(response.text)
        except:
            raise Exception("Could not get allocated resources")
        