# nbssh: Netbox SSH Helper
nbssh is a tool, written in a mix of Bash + Python 3, that will allow you to quickly establish SSH connections to devices in Netbox.

# Examples
```
$ nbssh device
>> ssh default_user@192.0.2.0
Password:

$ nbssh company2_device --instance=othercompany
>> ssh other_default_user@192.0.2.1
Password:

$ nbssh naynay@device
>> ssh naynay@192.0.2.0
Password:
```

# Why?
Sometimes it takes a little while (more than 5 seconds) to find the IP of a device in Netbox. Why spend that long?

# How?
## Configuration File
nbssh uses a configuration file located in `~/.nbssh/config.json` to define your Netbox instances, and some settings to go along with them. Below is an example.

```
{
    "instances": {
        "company1": {
            "default_user": "r00t",
            "url": "https://netbox.example.org",
            "token": "abcdefgiwantyou2peerwithcompany2"
        },
        "company2": {
            "default_user": "root", 
            "url": "https://netbox.example.com",
            "token": "abcdefgiwantyou2peerwithme"
        }
    },
    "default_instance": "company1",
    "force_ipv4": true
}
```

Hopefully the options are self-explanatory, but in case they aren't:

* `force_ipv4` tells the world that you are not an innovator
* `default_instance` specifies which instance to use by default, without having to specify `--instance company1` every time
* `instances` is the list of Netbox instances... you likely have one per company you work with or something like that
    * `default_user` says which user to use if you use `nbssh device` instead of `nbssh user@device`
    * `url` is the URL, including the scheme, excluding trailing slashes, for your Netbox instance
    * `token` is the API token (only requires read permissions) for your Netbox instance

## Installation
```
# git clone git@github.com:networkhorse/nbssh.git
# cd nbssh
# pip3 install --user -r requirements.txt
```

You then need to make an alias so you can use it everywhere (I was a little bit too lazy to figure out the whole complexity around symlinks and finding the actual path of the Python file)...

```
# For Bash users
chmod a+x nbssh
echo "alias nbssh=\"$(pwd)/nbssh\"" >> ~/.bashrc

# For zsh users (macOS, mostly)
chmod a+x nbssh
echo "alias nbssh=\"$(pwd)/nbssh\"" >> ~/.zshrc
```

## Usage
Short and simple:
```# nbssh [user@]device [--instance INSTANCE]```

Get help at any time with `-h`!
```
# nbssh -h
usage: nbssh [-h] [--instance INSTANCE] user_at_device

positional arguments:
  user_at_device       user@device

optional arguments:
  -h, --help           show this help message and exit
  --instance INSTANCE  Optional instance name.
```

# Broken?
Open an issue and, if you know how, submit a fix. :-)
