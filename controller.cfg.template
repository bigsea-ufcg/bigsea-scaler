# Logging configuration
[logging]
# Enable logging?
# Accepted values - True / False
enable = True
# Logging level
# Accepted values - "CRITICAL", "DEBUG", "ERROR", "FATAL", "INFO", "NOTSET", "WARN", "WARNING"
level = INFO

# Flask configuration
[flask]
# The host where the scaler service will be deployed
host = <host_ip>
# The port where the scaler service will be deployed
port = <port_number>

[authorization]
# BigSea's authentication endpoint
authorization_url =

[actuator]
# The ips or names of the compute nodes, separated by comma.
compute_nodes = 
# The keypair used to access the compute nodes.
keypair_compute_nodes =
# A list of ports. Required when using SSH through tunnels.
# The i-th port will be used to access the i-th compute node.
tunnel_ports = 
# The actuator service's port
actuator_port = 5047
# Frontend vm credentials
access_ip =
access_username =
access_password =
# Open Nebula Credentials
one_url =
one_username =
one_password =
# The max possible disk throughput (iops) that can be allocated to a virtual machine.
iops_reference = 
# The max possible disk throughput, in bytes/sec, that can be allocated to a virtual machine.
bs_reference =  
# The I/O cap to use in the CPU only actuators.
default_io_cap = 

[monasca]
# The endpoint for the Monasca's service.
monasca_endpoint = http://<ip:port>
# The username with permissions to publish and get metrics from monasca.
username = <monasca_user>
# The above-mentioned user's password.
password = <password>
# The above-mentioned user's keystone project.
project_name = <monasca_project_name>
# The keystone authentication endpoint.
auth_url = http://<ip>:<port>/v3/
# Monasca API version.
api_version = 2_0
