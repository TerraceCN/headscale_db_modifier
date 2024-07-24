#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import json
import os
import sqlite3
import sqlite3.dbapi2
from typing import Literal, Optional, List, Dict, Any, Tuple

import yaml
from prettytable import PrettyTable


class NodeModifier:
    def __init__(self, db_path: os.PathLike):
        self.db = db_path
        self.db = sqlite3.connect(db_path)

    def list_nodes(self, format: Literal["simple", "json", "yaml"] = "simple"):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM nodes")
        nodes = cursor.fetchall()

        rows: List[Dict[str, Any]] = []
        columns = [d[0] for d in cursor.description]
        for node in nodes:
            node = dict(zip(columns, node))
            node["endpoints"] = json.loads(node["endpoints"])
            node["host_info"] = json.loads(node["host_info"])
            rows.append(node)

        if format == "simple":
            columns = ["id", "ipv4", "ipv6", "hostname", "given_name"]
            tb = PrettyTable(columns)
            tb.add_rows([[row[col] for col in columns] for row in rows])
            print(tb)
        elif format == "json":
            print(json.dumps(rows, indent=2))
        elif format == "yaml":
            print(yaml.dump(rows, indent=2, sort_keys=False))
        else:
            raise ValueError("Invalid format")

    def edit_node(
        self,
        node_id: int,
        ipv4: Optional[str],
        ipv6: Optional[str],
        hostname: Optional[str],
        given_name: Optional[str],
    ):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM nodes WHERE id = ?", (node_id,))
        original_node = cursor.fetchone()
        if not original_node:
            raise ValueError(f"Node (id={node_id}) not found")
        columns = [d[0] for d in cursor.description]
        original_node = dict(zip(columns, original_node))

        prompt_head = f"========== Modification to node (id={node_id}) =========="
        print(prompt_head)

        sqls: List[Tuple[str, sqlite3.dbapi2._Parameters]] = []

        if ipv4 is not None:
            cursor.execute("SELECT COUNT(*) FROM nodes WHERE ipv4 = ?", (ipv4,))
            if cursor.fetchone()[0] > 0:
                raise ValueError(f"IPv4 address (ipv4={ipv4}) already exists")
            sqls.append(("UPDATE nodes SET ipv4 = ? WHERE id = ?", (ipv4, node_id)))
            print(f"ipv4:\t{original_node['ipv4']} => {ipv4}")

        if ipv6 is not None:
            cursor.execute("SELECT COUNT(*) FROM nodes WHERE ipv6 = ?", (ipv6,))
            if cursor.fetchone()[0] > 0:
                raise ValueError(f"IPv6 address (ipv6={ipv6}) already exists")
            sqls.append(("UPDATE nodes SET ipv6 = ? WHERE id = ?", (ipv6, node_id)))
            print(f"ipv6:\t{original_node['ipv6']} => {ipv6}")

        if hostname is not None:
            sqls.append(
                ("UPDATE nodes SET hostname = ? WHERE id = ?", (hostname, node_id))
            )
            print(f"hostname:\t{original_node['hostname']} => {hostname}")

        if given_name is not None:
            cursor.execute(
                "SELECT COUNT(*) FROM nodes WHERE given_name = ?", (given_name,)
            )
            if cursor.fetchone()[0] > 0:
                raise ValueError(f"Given name (given_name={given_name}) already exists")
            sqls.append(
                ("UPDATE nodes SET given_name = ? WHERE id = ?", (given_name, node_id))
            )
            print(f"given_name:\t{original_node['given_name']} => {given_name}")

        print("=" * len(prompt_head))
        if len(sqls) == 0:
            print(f"Node (id={node_id}) not modified")
            return

        if input("Confirm changes? [y/N] ").lower() != "y":
            print("Abort")
            return

        for sql, params in sqls:
            cursor.execute(sql, params)
        self.db.commit()
        print(f"Node (id={node_id}) updated")

    def delete_node(self, node_id: int):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM nodes WHERE id = ?", (node_id,))
        if cursor.fetchone()[0] == 0:
            raise ValueError(f"Node (id={node_id}) not found")

        cursor.execute("DELETE FROM nodes WHERE id = ?", (node_id,))
        self.db.commit()
        print(f"Node (id={node_id}) deleted")


def main():
    parser = ArgumentParser()
    parser.add_argument("db_path", type=str)

    sps = parser.add_subparsers(dest="node")

    list_sp = sps.add_parser("list")
    list_sp.add_argument(
        "-f", "--format", type=str, default="simple", choices=["simple", "json", "yaml"]
    )

    edit_sp = sps.add_parser("edit")
    edit_sp.add_argument("-i", "--id", type=int, required=True)
    edit_sp.add_argument("-4", "--ipv4", type=str)
    edit_sp.add_argument("-6", "--ipv6", type=str)
    edit_sp.add_argument("-H", "--hostname", type=str)
    edit_sp.add_argument("-n", "--given-name", type=str)

    delete_sp = sps.add_parser("delete")
    delete_sp.add_argument("-i", "--id", type=int, required=True)

    args = parser.parse_args()

    modifier = NodeModifier(args.db_path)
    if args.node == "list":
        modifier.list_nodes(args.format)
    elif args.node == "edit":
        modifier.edit_node(
            args.id, args.ipv4, args.ipv6, args.hostname, args.given_name
        )
    elif args.node == "delete":
        modifier.delete_node(args.id)
    else:
        raise ValueError("Invalid command")


if __name__ == "__main__":
    main()
