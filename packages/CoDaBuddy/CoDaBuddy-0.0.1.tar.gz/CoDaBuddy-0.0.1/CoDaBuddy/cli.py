#!/usr/bin/env python3

# from email.policy import default
# from pydoc import describe
from statistics import mode
import click
import os
import sys
from typing import Dict, List, Type
from pathlib import Path, PurePath
import json
from collections import OrderedDict

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "..")
    sys.path.append(os.path.normpath(SCRIPT_DIR))


from backup_manager import RetentionType
from backupper import (
    BaseBackupper,
    MySQLBackupper,
    PostgresBackupper,
    Neo4jOfflineBackupper,
    Neo4jOnlineBackupper,
)
from cli_helper import (
    list_backups,
    format_n_output_backup_list,
    click_check_required_params_not_None,
)
from log import log

from label import ValidLabels, Label
from container_helper import ContainerHelper, Container

# Todo: Skip container related question in native mode. maybe via groups? https://click.palletsprojects.com/en/8.0.x/commands/#nested-handling-and-contexts

database_type_backupper_mapping: Dict[str, Type[BaseBackupper]] = {
    "mysql": MySQLBackupper,
    "postgres": PostgresBackupper,
    "neo4j-on": Neo4jOnlineBackupper,
    "neo4j-off": Neo4jOfflineBackupper,
}


@click.group()
@click.option(
    "--debug/--no-debug",
    help="Enable debug logging",
    default=False,
)
def cli_root(debug):
    if debug:
        click.echo(f"Debug mode is on")
        log.setLevel("DEBUG")


@cli_root.group(name="backup")
@click.option(
    "--debug/--no-debug",
    help="Enable debug logging",
    default=False,
)
def backup_cli(debug):
    if debug:
        click.echo(f"Debug mode is on")
        log.setLevel("DEBUG")


@backup_cli.command(name="now")
@click.option(
    "--mode",
    "-m",
    default="Docker",
    prompt="How is your DB running?",
    help="Environment the database is running in: 'docker', 'kubernetes'",
    type=click.Choice(["docker", "kubernetes"], case_sensitive=False),
)
@click.option(
    "--container-identifier",
    "-c",
    prompt="Containername or k8s-namespace/Workload-Name? e.g.: 'mariadb01' in docker or 'default/mariadb01' in k8s ",
    help="The Docker container name/id (as in `docker ps`) or kubernetes pod name. Split by ',' if multiple",
)
@click.option(
    "--database-type",
    "-t",
    default="mysql",
    prompt="Database type?",
    help="Do we backup a mysql/maria/neo4j db or a postgres db?",
    type=click.Choice(["mysql", "postgres", "neo4j"], case_sensitive=False),
)
@click.option(
    "--database-host",
    "-h",
    default="127.0.0.1",
    prompt="Database host?",
    help="Hostname or IP where the database is running. In non `native`-mode this will be likely the 'localhost'/' 127.0.0.1' (default value)",
)
@click.option(
    "--database-user",
    "-u",
    default="root",
    prompt="Database user?",
    help="User to access the database?",
)
@click.option(
    "--database-password",
    "-p",
    hide_input=True,
    prompt="Database password?",
    help="Password to access the database?",
)
@click.option(
    "--database-names",
    "-n",
    default="",
    prompt="Database(s) to backup ('mydb' or 'mydb01,mydb02')? Leave empty for all DBs.",
    help="The Databases to backup. We can select a specific database by name . e.g. 'my_database01' or a list of databases e.b. ['mydb01', 'mydb02']. If left empty all databses accessable for the user will be backuped.",
)
def backup_now(
    mode,
    container_identifier,
    database_type,
    database_host,
    database_user,
    database_password,
    database_names,
):
    """Wizard to backup a specific database running in a container, now!"""

    container_names = container_identifier.split(",")

    for container_name in container_names:
        backup_name = container_name
        namespace = None
        if mode == "kubernetes":
            # in kubernetes mode, we expect the static workload name. now we need to query the running pod in this workload, which is the actuall container running the database
            if not "/" in container_name:
                raise ValueError(
                    f"Expected '--container-identifier' in format 'namespace/workload-name' got '{container_name}'"
                )
            namespace, workload_name = container_name.split("/")
            # You are here. you need to find the workload by name and then find the pod in the workload. maybe we need some more container helper funcs

            workload = next(
                (
                    wl
                    for wl in ContainerHelper.kubernetes_get_workloads(
                        namespace=namespace, describe=True
                    )
                    if wl["metadata"]["name"] == workload_name
                ),
                None,
            )
            if workload is None:
                raise ValueError(
                    f"Can not find workload with name '{workload_name}' in namespace '{namespace}'. Cancel backup."
                )
            container = ContainerHelper.kubernetes_get_pods_by_workload(workload)
            if len(container) != 1:
                raise ValueError(
                    f"Workload '{workload['metadata']['namespace']}/{workload['metadata']['name']}' contains multiple pods. Dont know what to do..."
                )
            backup_name = workload_name
            container_name = container[0].name

        container = Container(
            mode=mode,
            id="",
            name=container_name,
            backup_name=container_name,
            coda_labels=ValidLabels.valid_labels_from_dict(
                {
                    ValidLabels.backup_name.key: backup_name,
                    ValidLabels.database_type.key: database_type,
                    ValidLabels.database_host.key: database_host,
                    ValidLabels.database_password.key: database_password,
                    ValidLabels.database_username.key: database_user,
                    ValidLabels.database_names.key: database_names,
                },
                add_missing_default_labels=True,
            ),
            other_labels={},
            kubernetes_namespace=namespace,
        )
        BackupperClass = database_type_backupper_mapping[database_type]
        bu = BackupperClass(container)
        bu.backup(
            databases=database_names,
            retention_type=RetentionType.MANUAL,
        )


@backup_cli.command(name="kubernetes")
@click.option(
    "--namespace",
    "-n",
    type=str,
    default="default",
    help="Define the namespace we should search for database pods to be backed up.",
)
@click.option(
    "--all-namespaces",
    "-all-namespaces",
    is_flag=True,
    default=False,
    help="If we should search for pods, to be backed up, in all namespaces. When used `--namespace` will be ignored.",
)
@click.option(
    "--target-dir",
    "-d",
    type=str,
    default=None,
    help=f"Define a non standard target dir. Default to '{ValidLabels.backup_dir.val}' or can be specified per container via docker-label '{ValidLabels.backup_dir.key}'",
)
def backup_kubernetes(namespace, all_namespaces, target_dir):
    """Backup databases in a kubernetes environment"""
    from container_helper import ContainerHelper

    count_db_instances = 0
    count_dbs = 0
    for pod in ContainerHelper.kubernetes_get_pods_to_be_backed_up(
        namespace=namespace, all_namespaces=all_namespaces
    ):
        if pod.coda_labels[ValidLabels.enabled].val:
            BackupperClass = database_type_backupper_mapping[
                pod.coda_labels[ValidLabels.database_type].val
            ]
            bu: BaseBackupper = BackupperClass(pod, target_dir)

            if not pod.coda_labels[ValidLabels.database_names].val:
                databases = None
            else:
                databases = pod.coda_labels[ValidLabels.database_names].val.split(",")
            backup_files = bu.backup(
                databases=databases,
                retention_type=RetentionType.DAILY,
            )
            count_dbs += len(backup_files)

            count_db_instances += 1
            bu.manager.rotate_existing_backups()
    click.echo(
        f"\nBackuped {count_dbs} database(s) in {count_db_instances} instance(s)"
    )


@backup_cli.command(name="docker")
@click.option(
    "--target-dir",
    "-d",
    default=None,
    help=f"Define a non standard target dir. Default to '{ValidLabels.backup_dir.val}' or can be specified per container via docker-label '{ValidLabels.backup_dir.key}'",
)
def backup_docker(target_dir):
    """Backup databases in a docker environment"""

    for container in ContainerHelper.docker_get_container_to_be_backed_up(
        describe=True
    ):
        if container.coda_labels[ValidLabels.enabled].val:
            BackupperClass = database_type_backupper_mapping[
                container.coda_labels[ValidLabels.database_type].val
            ]

            bu: BaseBackupper = BackupperClass(container, target_base_dir=target_dir)
            bu.backup(
                databases=container.coda_labels[ValidLabels.database_names].val,
                retention_type=RetentionType.DAILY,
            )

            bu.manager.rotate_existing_backups()


@cli_root.group(name="restore")
@click.option(
    "--debug/--no-debug",
    help="Enable debug logging",
    default=False,
)
def restore_cli(debug):
    if debug:
        click.echo(f"Debug mode is on")
        log.setLevel("DEBUG")


@restore_cli.command(name="now")
@click.option(
    "--mode",
    default="docker",
    prompt="How is your DB running?",
    help="Environment the database is running in: 'docker', 'kubernetes', 'native'",
    type=click.Choice(["docker", "kubernetes", "native"], case_sensitive=False),
)
@click.option(
    "--container-identifier",
    prompt="Container/pod name(s) (seperated by comma)? (Ignore question in `native` mode)",
    help="The Docker container name/id (as in `docker ps`) or kubernetes pod name.",
)
@click.option(
    "--database-type",
    default="mysql",
    prompt="Database type?",
    help="Do we backup a mysql/maria db or a postgres db?",
    type=click.Choice(["mysql", "postgres"], case_sensitive=False),
)
@click.option(
    "--database-host",
    default="127.0.0.1",
    prompt="Database host?",
    help="Hostname or IP where the database is running. In non `native`-mode this will be likely the 'localhost'/' 127.0.0.1' (default value)",
)
@click.option(
    "--database-user",
    default="root",
    prompt="Database user?",
    help="User to access the database?",
)
@click.option(
    "--database-password",
    hide_input=True,
    prompt="Database password?",
    help="Password to access the database?",
)
@click.option(
    "--database-name",
    default="",
    prompt="Database(s) to backup ('mydb' or ['mydb01', 'mydb02'])? Leave empty for all DBs.",
    help="The Databases to backup. We can select a specific database by name . e.g. 'my_database01' or a list of databases e.b. ['mydb01', 'mydb02']. If left empty all databses accessable for the user will be backuped.",
)
@click.option(
    "--backup-path",
    prompt="Which back to restore?",
    help="Name of the backup as listed in `coda-restore <mode> list <database instance name>`?",
)
def restore_now(
    mode,
    container_identifier,
    database_type,
    database_host,
    database_user,
    database_password,
    database_name,
    backup_path,
):
    raise NotImplementedError


@restore_cli.group(invoke_without_command=True, name="kubernetes")
@click.pass_context
@click.option(
    "--namespace",
    "-n",
    type=str,
    default="default",
    help="Define the namespace we should search for database pods to be backed up.",
)
@click.option(
    "--workload-name",
    type=str,
    help="Name of the pod/container the to be restored database runs in?",
)
@click.option(
    "--backup-name",
    type=str,
    help="Name of the backup (find via coda-restore kubernetes list)?",
)
@click.option(
    "--database-name",
    type=str,
    help="name of the database instance to be restored",
)
def restore_kubernetes(
    ctx: click.Context, namespace, workload_name, backup_name, database_name
):
    if ctx.invoked_subcommand is None:
        click_check_required_params_not_None(
            ctx, ["workload_name", "backup_name", "database_name"]
        )
        workload = next(
            (
                wl
                for wl in ContainerHelper.kubernetes_get_workloads(
                    namespace=namespace, describe=True
                )
                if wl["metadata"]["name"] == workload_name
            ),
            None,
        )
        if not workload:
            raise ValueError(
                f"Could not find workload with name '{workload}' in namespace '{namespace}'"
            )
        pods = ContainerHelper.kubernetes_get_pods_by_workload(workload)
        if len(pods) > 1:
            raise NotImplementedError("Only single pod workloads are supported atm")
        pod = pods[0]
        BackupperClass = database_type_backupper_mapping[
            pod.coda_labels[ValidLabels.database_type].val
        ]
        bu = BackupperClass(db_container=pod)
        bu.restore(database=database_name, backup_name=backup_name, dry_run=False)


@restore_kubernetes.command(name="list")
@click.option(
    "--workload-name",
    "-w",
    default=None,
    help="User to access the database?",
)
@click.option(
    "--databases",
    "-d",
    default=None,
    help="List only these databases (seperated by comma)",
)
@click.option(
    "--namespace",
    "-n",
    type=str,
    default="default",
    help="Define the namespace we should search for database pods with backups.",
)
@click.option(
    "--all-namespaces",
    "-all-namespaces",
    is_flag=True,
    default=False,
    help="If we should search for pods, with backups, in all namespaces. When used `--namespace` will be ignored.",
)
@click.option(
    "--source-dir",
    "-s",
    type=str,
    default=None,
    help=f"Where to look for the backups. Will default to '{ValidLabels.backup_dir.val}'",
)
@click.option(
    "--output-format",
    "-o",
    default="human",
    help="Define the output format: 'human' an easy to read table, 'json' or 'yaml' for inter-process readability, dict if used in a python script",
    type=click.Choice(["human", "json", "yaml", "dict"], case_sensitive=False),
)
def restore_kubernetes_list(
    workload_name, databases, namespace, all_namespaces, source_dir, output_format
):
    """Display available backup files for existing workloads"""

    data = list_backups(
        database_type_backupper_mapping=database_type_backupper_mapping,
        mode="kubernetes",
        container_name=workload_name,
        databases=databases,
        namespace=namespace,
        all_namespaces=all_namespaces,
        source_dir=source_dir,
    )
    return format_n_output_backup_list(data, output_format)


@restore_cli.group(invoke_without_command=True, name="docker")
@click.pass_context
@click.option(
    "--container-name",
    hide_input=False,
    help="Name of the pod/container the to be restored database runs in?",
)
@click.option(
    "--backup-name",
    hide_input=False,
    help="Name of the backup (find via coda-restore kubernetes list)?",
)
def restore_docker(ctx, container_name, backup_name):
    if ctx.invoked_subcommand is None:
        click.echo("DO docker restore")


@restore_docker.command(name="list")
@click.option(
    "--container-name",
    "-c",
    default=None,
    help="User to access the database?",
)
@click.option(
    "--databases",
    "-d",
    default=None,
    help="List only these databases (seperated by comma)",
)
@click.option(
    "--source-dir",
    "-s",
    type=str,
    default=None,
    help=f"Where to look for the backups. Will default to '{ValidLabels.backup_dir.val}'",
)
@click.option(
    "--output-format",
    "-o",
    default="human",
    help="Define the output format: 'human' an easy to read table, 'json' or 'yaml' for inter-process readability, dict if used in a python script",
    type=click.Choice(["human", "json", "yaml", "dict"], case_sensitive=False),
)
def restore_docker_list(container_name, databases, source_dir, output_format):
    """Display available backup files for existing containers"""
    data = list_backups(
        database_type_backupper_mapping=database_type_backupper_mapping,
        mode="docker",
        container_name=container_name,
        databases=databases,
        source_dir=source_dir,
    )
    return format_n_output_backup_list(data, output_format)


@cli_root.group(name="auto-create")
@click.option(
    "--debug/--no-debug",
    help="Enable debug logging",
    default=False,
)
def auto_create(debug):
    if debug:
        click.echo(f"Debug mode is on")
        log.setLevel("DEBUG")


@auto_create.command(name="kubernetes")
@click.option(
    "--namespace",
    "-n",
    type=str,
    default="default",
    help="Define the namespace we should search for database pods to be backed up.",
)
@click.option(
    "--all-namespaces",
    "-all-namespaces",
    is_flag=True,
    default=False,
    help="If we should search for pods, to be backed up, in all namespaces. When used `--namespace` will be ignored.",
)
def auto_create_kubernetes(namespace, all_namespaces):
    # you are here. maybe we dont new "now" command and instead a kubernetes and a docker version

    from container_helper import ContainerHelper

    count_db_instances = 0
    count_dbs = 0

    for pod in ContainerHelper.kubernetes_get_pods_to_be_backed_up(
        namespace=namespace, all_namespaces=all_namespaces
    ):
        count_db_instances += 1
        if pod.coda_labels[ValidLabels.enabled].val:
            BackupperClass = database_type_backupper_mapping[
                pod.coda_labels[ValidLabels.database_type].val
            ]
            bu: BaseBackupper = BackupperClass(pod)

            created_dbs = bu.auto_create()
            if created_dbs:
                count_dbs += len(created_dbs)
    click.echo(f"Created {count_dbs} database(s) in {count_db_instances} instance(s)")


@auto_create.command(name="docker")
def auto_create_docker():
    # you are here. maybe we dont new "now" command and instead a kubernetes and a docker version

    from container_helper import ContainerHelper

    count_db_instances = 0
    count_dbs = 0

    for container in ContainerHelper.docker_get_container_to_be_backed_up():
        count_db_instances += 1
        if container.coda_labels[ValidLabels.enabled].val:
            BackupperClass = database_type_backupper_mapping[
                container.coda_labels[ValidLabels.database_type].val
            ]
            bu: BaseBackupper = BackupperClass(container)

            created_dbs = bu.auto_create()
            if created_dbs:
                count_dbs += len(created_dbs)
    click.echo(f"Created {count_dbs} database(s) in {count_db_instances} instance(s)")


@cli_root.command(name="list-labels")
@click.option(
    "--output-format",
    "-o",
    default="human",
    help="Define the output format: 'human' an easy to read table, 'json' or 'yaml' for inter-process readability, dict if used in a python script",
    type=click.Choice(["human", "json", "yaml", "dict"], case_sensitive=False),
)
def list_labels(output_format):
    output = ValidLabels.list_labels(output_format)
    click.echo(output)
    return output


if __name__ == "__main__":
    cli_root()
