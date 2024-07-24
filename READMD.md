# Headscale Node Modifier

Simple script to modify the headscale node information.

# Usage

**Remember to restart headscale after modification!**

## Install requirements

```bash
pip install -r requirements.txt
```

## List all nodes

```bash
python node_modifier.py {db_path} list [-f {format}]
```

- **db_path:** path to headscale database, example: `/var/lib/headscale/headscale.db`
- **format:** output format, optional, default: `simple`, choices: `simple`, `json`, `yaml`


## Modify node

```bash
python node_modifier.py {db_path} edit \
    -i {node_id} \
    [-4 {new_ipv4_addr}] \
    [-6 {new_ipv6_addr}] \
    [-H {new_hostname}] \
    [-n {new_given_name}]
```

- **db_path:** path to headscale database, example: `/var/lib/headscale/headscale.db`
- **node_id:** node id, can be found by running `python node_modifier.py {db_path} list`
- **new_ipv4_addr:** new ipv4 address, optional
- **new_ipv6_addr:** new ipv6 address, optional
- **new_hostname:** new hostname, optional
- **new_given_name:** new given name, optional
