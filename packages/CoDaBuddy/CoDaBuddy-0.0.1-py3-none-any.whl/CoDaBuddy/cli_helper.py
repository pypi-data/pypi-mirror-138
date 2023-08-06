from typing import Dict, List, Union, Type, Callable
from datetime import datetime, timedelta
import click
import time
import humanize
from pathlib import Path, PurePath
import tabulate

tabulate.PRESERVE_WHITESPACE = True
from backup_manager import Backup, RetentionType
from container_helper import Container, ContainerHelper
from label import ValidLabels
import json
import yaml


def list_backups(
    database_type_backupper_mapping: Dict,
    mode: str,
    container_name: str,
    databases: List[str],
    namespace: str = None,
    all_namespaces: bool = None,
    source_dir: str = None,
):

    # todo: can we improve this func? it is a little bit messy :)

    if isinstance(databases, str):
        databases = databases.split(",")
    containers: List[Dict[str, Container]] = []
    output_data: List = []
    # Lets find all the container with CoDa enabled and already create the namespace entries for the output data
    if mode == "kubernetes":
        for container in ContainerHelper.kubernetes_get_pods_to_be_backed_up(
            namespace=namespace, all_namespaces=all_namespaces
        ):
            if databases:
                databases = databases.split(",")
            # as this is container framework agnostic funtion we actually search for the workload and not the container/pod by name.
            # but we will extract the pod name in the workload for later use
            if (
                container_name
                and container.parent["metadata"]["name"] != container_name
            ):
                continue
            containers.append({container.backup_name: container})
            # create an entry for the namespace if not exists
            if container.kubernetes_namespace not in [
                ns["namespace"] for ns in output_data
            ]:
                namespace = {
                    "namespace": container.kubernetes_namespace,
                    "mode": "kubernetes",
                    "database_containers": [],
                }
                output_data.append(namespace)
            else:
                namespace = next(
                    ns
                    for ns in output_data
                    if ns["namespace"] == container.kubernetes_namespace
                )

    elif mode == "docker":
        # in docker we dont have namespaces we use only one placeholder "default" namespace to keep the format constistent
        namespace = "default"
        namespace = {
            "namespace": "default",
            "mode": "docker",
            "database_containers": [],
        }
        output_data.append(namespace)
        # collect all containers to be backed up
        for container in ContainerHelper.docker_get_container_to_be_backed_up(
            describe=True
        ):
            if container_name and container.name != container_name:
                continue
            containers.append({container.backup_name: container})

    for c in containers:
        container_output_name = list(c.keys())[0]
        container = list(c.values())[0]
        BackupperClass = database_type_backupper_mapping[
            container.coda_labels[ValidLabels.database_type].val
        ]
        bu = BackupperClass(container, target_base_dir=source_dir)
        for database_name in bu.manager.list_backuped_databases():
            if databases and not database_name in databases:
                continue
            namespace = None
            if mode == "docker":
                # in docker we dont have namespaces we use the placeholder "default" namespace
                namespace = output_data[0]
            elif mode == "kubernetes":
                namespace = next(
                    ns
                    for ns in output_data
                    if ns["namespace"] == container.kubernetes_namespace
                )
            # lets look up if there is already a namespace entry for this container
            container_entry = next(
                (
                    c
                    for c in namespace["database_containers"]
                    if c["name"] == container_output_name
                ),
                None,
            )
            if not container_entry:
                # this database is in a new container
                # lets create new container entry in this namespace
                container_entry = {
                    "name": container_output_name,
                    "basedir": bu.manager.base_path,
                    "databases": [],
                }
                namespace["database_containers"].append(container_entry)

            container_entry["databases"].append(
                {
                    "name": database_name,
                    "basedir": Path(PurePath(bu.manager.base_path, database_name)),
                    "backups": bu.manager.list_backups(database_name),
                }
            )
    return output_data


def backup_list_to_human(backup_list: Dict):
    """[summary]

    Args:
        backup_list (Dict): [description]

    Returns:
        [type]: [description]

    backup_list input e.g.:
    ```json
    [
        {
            "namespace": "default",
            "database_containers": [
                {
                    "name": "mariadb01",
                    "databases": [
                        {
                            "name": "coda_test",
                            "basedir": "/backups/default/coda_test",
                            "backups": [
                                {
                                    "daily": [
                                        {
                                            "name": "sqlbackup_2022-01-26_10-18-49.sql",
                                            "date": "2022-01-26 09:18:49",
                                            "path": "daily/sqlbackup_2022-01-26_10-18-49.sql.gz",
                                            "full_path": "/backups/default/coda_test/daily/sqlbackup_2022-01-26_10-18-49.sql.gz",
                                        }
                                    ],
                                    "weekly": [],
                                    "monthly": [],
                                    "yearly": [],
                                    "manual": [],
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    ]
    ```
    """
    data = ""
    for namespace in backup_list:
        if len(backup_list) > 1:
            # we not only have the default namespace. otherwise we could hide it
            data = data + f"\n\n🌐 NAMESPACE: {namespace['namespace']}\n\n"
        for container in namespace["database_containers"]:
            data = data + f" 🖥️  Container: {container['name']}\n\n"
            for database in container["databases"]:
                data = data + f"  🛢  Database: {database['name']}\n"
                data = data + backup_file_list_to_human(database["backups"], 6)
    return data


# 🖥️
def backup_file_list_to_human(
    backups: Dict[RetentionType, List[Backup]], indent: int = 4
):
    headers = ["", "Name", "Date", "Age", "Path"]
    s = ""
    for retenetion_type, backup_list in backups.items():
        s = (
            s
            + f"\n    ⌚️ {retenetion_type}  {'@ ' + str(backup_list[0].path.parents[1].absolute()) if backup_list else ''}\n"
        )
        backups_table_struc = []
        for backup in backup_list:

            if not backup.retention_type == retenetion_type:
                continue

            backups_table_struc.append(
                [
                    "💾",
                    backup.name,
                    datetime.utcfromtimestamp(backup.creation_time).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    humanize.naturaldelta(
                        timedelta(seconds=time.time() - backup.creation_time)
                    ),
                    backup.path.parents[0].name + "/" + backup.path.name,
                ]
            )
        table = tabulate.tabulate(backups_table_struc, headers=headers)
        indented_table = ""
        for line in table.split("\n"):
            indented_table = indented_table + " " * indent + line + "\n"
        s = s + indented_table
    return s


def backup_list_to_machine_readable(backup_list: List, format: str = "json"):
    """Serialize all dict entries of a backup_list"""
    if format != "json" and format != "yaml":
        raise ValueError(
            f"Unknown format style. Expected 'json' or 'yaml' got '{format}'"
        )
    elif format == "json":
        dump_func = json.dumps
    elif format == "yaml":
        dump_func = lambda input: yaml.dump(input, sort_keys=False)
    for namespace in backup_list:
        for database_container in namespace["database_containers"]:
            for database in database_container["databases"]:
                backups_ = {}
                for retention, backups in database["backups"].items():
                    backups_[str(retention.value)] = [bu.to_dict() for bu in backups]
                database["backups"] = backups_
    backup_list = cast_type_in_nested_dict_or_list(
        backup_list, Path, lambda p: str(p.absolute())
    )
    return dump_func(backup_list)


def cast_type_in_nested_dict_or_list(
    data: Union[List, Dict], target_type: Type, cast_func: Callable
) -> Union[List, Dict]:

    if isinstance(data, list):
        return [
            cast_type_in_nested_dict_or_list(item, target_type, cast_func)
            for item in data
        ]
    elif isinstance(data, dict):
        new_data = {}
        for key, val in data.items():
            if isinstance(val, list):
                new_data[key] = cast_type_in_nested_dict_or_list(
                    val, target_type, cast_func
                )
            elif isinstance(val, dict):
                new_data[key] = cast_type_in_nested_dict_or_list(
                    val, target_type, cast_func
                )
            elif issubclass(type(val), target_type):
                new_data[key] = cast_func(val)
            else:
                new_data[key] = val
        return new_data
    elif isinstance(data, target_type):
        return cast_func(data)


def format_n_output_backup_list(data, output_format):
    if output_format in ["json", "yaml"]:
        output = backup_list_to_machine_readable(data, output_format)
        print(output)
        return output
    elif output_format == "human":
        output = backup_list_to_human(data)
        print(output)
        return output
    elif output_format == "dict":
        return data


def click_check_required_params_not_None(
    context: click.Context, required_names: List[str]
):
    missing_opts = []
    for param, val in context.params.items():
        missing_opt = next(
            (
                option
                for option in context.command.get_params(context)
                if option.name == param
                and option.name in required_names
                and val is None
            ),
            None,
        )

        if missing_opt is not None:
            missing_opts.append(missing_opt.opts[0])

    if missing_opts:
        click.echo(context.get_help() + "\n")
        raise click.ClickException(f"missing option(s): {', '.join(missing_opts)}")
