import requests
import argparse
import json
import sys
import os

CONFIG = None
try:
    with open(os.path.expanduser("~/.nbssh/config.json"), "r") as config:
        CONFIG = json.loads(config.read())
except:
    print("Failed to read config from ~/.nbssh/config.json. Likely missing or invalid.")
    sys.exit(2)

if not CONFIG:
    sys.exit(2)

# Validate Configuration
if "force_ipv4" not in CONFIG:
    print("CONFIG.force_ipv4 not defined.")
    sys.exit(2)

if "default_instance" not in CONFIG:
    print("CONFIG.default_instance not defined.")
    sys.exit(2)

if "instances" not in CONFIG:
    print("CONFIG.instances not defined.")
    sys.exit(2)

if CONFIG["default_instance"] not in CONFIG["instances"]:
    print("CONFIG.default_instance invalid.")
    sys.exit(2)

for instance_name in CONFIG["instances"].keys():
    instance = CONFIG["instances"][instance_name]
    if "default_user" not in instance:
        print(f"CONFIG.instances.{instance_name}.default_user not defined.")
        sys.exit(2)

    if "url" not in instance:
        print(f"CONFIG.instances.{instance_name}.url not defined.")
        sys.exit(2)

    if "token" not in instance:
        print(f"CONFIG.instances.{instance_name}.token not defined.")
        sys.exit(2)

parser = argparse.ArgumentParser("nbssh")
parser.add_argument("user_at_device", help="user@device")
parser.add_argument("--instance", help="Optional instance name.")
args = parser.parse_args()

if not args.instance:
    args.instance = CONFIG["default_instance"]

INSTANCE = CONFIG["instances"][args.instance]
URL = INSTANCE["url"]
BEARER_TOKEN = INSTANCE["token"]

def get_device_by_name(name):
    url = f"{URL}/api/dcim/devices/?name={name}"
    response = requests.get(url, headers={"Authorization": f"Token {BEARER_TOKEN}"})
    return response.json()

user_at_device = args.user_at_device.split("@")
user = INSTANCE["default_user"]
device_name = None

if len(user_at_device) == 2:
    user = user_at_device[0]
    device_name = user_at_device[1]
elif len(user_at_device) == 1:
    device_name = user_at_device[0]
else:
    parser.print_usage()
    sys.exit(1)

device = get_device_by_name(device_name)

if device["count"] == 0:
    print("Device not found.")
    sys.exit(1)

ip_address = device["results"][0]["primary_ip"]["address"].split("/")[0]
if CONFIG["force_ipv4"]:
    ip_address = device["results"][0]["primary_ip4"]["address"].split("/")[0]

print(f"ssh {user}@{ip_address}")
