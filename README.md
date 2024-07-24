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

# Example

## 1. List all nodes

```bash
python node_modifier.py /var/lib/headscale/headscale.db list
```

```
+----+--------------+--------------------+-----------------+-----------------+
| id |     ipv4     |        ipv6        |     hostname    |   given_name    |
+----+--------------+--------------------+-----------------+-----------------+
| 1  | 100.64.0.101 | fd7a:115c:a1e0::65 | Terrace-Desktop | terrace-desktop |
| 2  | 100.64.0.11  | fd7a:115c:a1e0::b  | TERRACE-GATEWAY | server-gateway  |
+----+--------------+--------------------+-----------------+-----------------+
```

## 2. Modify node

```bash
python node_modifier.py /var/lib/headscale/headscale.db edit \
    -i 1 \
    -4 100.64.0.102 \
    -6 fd7a:115c:a1e0::66 \
    -n "terrace-desktop-new"
```

```
========== Modification to node (id=1) ==========
ipv4:   100.64.0.101 => 100.64.0.102
ipv6:   fd7a:115c:a1e0::65 -> fd7a:115c:a1e0::66
given_name:  terrace-desktop => terrace-desktop-new
=================================================
Confirm changes? [y/N] y
Node (id=1) updated
```

## 3. Check changes

```bash
python node_modifier.py /var/lib/headscale/headscale.db list
```

```
+----+--------------+--------------------+-----------------+---------------------+
| id |     ipv4     |        ipv6        |     hostname    |     given_name      |
+----+--------------+--------------------+-----------------+---------------------+
| 1  | 100.64.0.102 | fd7a:115c:a1e0::66 | Terrace-Desktop | terrace-desktop-new |
| 2  | 100.64.0.11  | fd7a:115c:a1e0::b  | TERRACE-GATEWAY |   server-gateway    |
+----+--------------+--------------------+-----------------+---------------------+
```

## 4. Restart headscale and check changes with headscale-cli

```bash
systemctl restart headscale
headscale nodes list
```
