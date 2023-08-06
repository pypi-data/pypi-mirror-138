from ast import Str
from typing import List, Dict, Union, Tuple
import logging
from Configs import getConfig
import json
from dataclasses import dataclass

from config import DEFAULT
from label import ValidLabels, Label
from executer import Executer

config: DEFAULT = getConfig(config_classes=[DEFAULT])
from log import log

# TodO: You are here. Make the docker* func work with new Container class


@dataclass
class Container:
    mode: str
    id: str
    name: str
    backup_name: str
    coda_labels: Dict[str, Label]
    other_labels: Dict[str, Label]
    desc: Dict = None
    parent: Dict = None
    kubernetes_namespace: str = None

    @classmethod
    def from_docker_inspect_dict(cls, container_inspect_result: Dict):

        # todo validate correct dict type
        container = cls(
            mode="docker",
            id=container_inspect_result[0]["Id"],
            name=container_inspect_result[0]["Name"],
            backup_name=container_inspect_result[0]["Name"],
            coda_labels=ValidLabels.valid_labels_from_dict(
                container_inspect_result[0]["Config"]["Labels"],
                add_missing_default_labels=True,
            ),
            other_labels=ValidLabels.non_valid_labels_from_dict(
                container_inspect_result[0]["Config"]["Labels"]
            ),
            desc=container_inspect_result[0],
        )
        if (
            ValidLabels.backup_name in container.coda_labels
            and container.coda_labels[ValidLabels.backup_name].val
        ):
            container.name = container.coda_labels[ValidLabels.backup_name].val
        return container

    @classmethod
    def from_kubernetes_get_dict(cls, kubectl_get_item_result: Dict):
        # todo validate correct item by "kind" field
        lbls = kubectl_get_item_result["metadata"]["labels"]
        if "annotations" in kubectl_get_item_result["metadata"]:
            lbls = {**lbls, **kubectl_get_item_result["metadata"]["annotations"]}
        container = cls(
            mode="kubernetes",
            id=kubectl_get_item_result["metadata"]["uid"],
            name=kubectl_get_item_result["metadata"]["name"],
            backup_name=kubectl_get_item_result["metadata"]["name"],
            coda_labels=ValidLabels.valid_labels_from_dict(
                lbls,
                add_missing_default_labels=True,
            ),
            other_labels=ValidLabels.non_valid_labels_from_dict(
                kubectl_get_item_result["metadata"]["labels"]
            ),
            desc=kubectl_get_item_result,
            kubernetes_namespace=kubectl_get_item_result["metadata"]["namespace"],
        )
        if (
            ValidLabels.backup_name in container.coda_labels
            and container.coda_labels[ValidLabels.backup_name].val
        ):
            container.backup_name = container.coda_labels[ValidLabels.backup_name].val
        return container


class ContainerHelper:
    @classmethod
    def kubernetes_get_pods(
        cls,
        labels: List[Label] = None,
        pod_name: str = None,
        namespace: str = None,
        all_namespaces: bool = False,
        describe: bool = False,
    ) -> Union[List[str], List[Container]]:
        """[summary]

        Args:
            labels (List[Label], optional): Label to select pods. Defaults to None.
            namespace (str, optional): kubernetes namespace to search in. Defaults to None.
            all_namespaces (bool, optional): If true search all namespaces. This will ignore `namespace`. Defaults to False.
            describe (bool, optional): If True return list of `Container` instances otherwise just the uid of the pod. Defaults to False.

        Returns:
            Union[str, Dict]: Will return a list of pod uid if `describe` is set to False. Other wise all informations `kubectl` provides as dict
        """
        if all_namespaces:
            namespace_arg = "--all-namespaces"
        else:
            namespace_arg = (
                f"-n {namespace if namespace else config.KUBECTL_DEFAULT_NAMESPACE}"
            )
        selector_arg = ""
        if pod_name:
            selector_arg = pod_name
        elif labels:
            labels_str: str = ",".join([str(label) for label in labels])
            selector_arg: str = f"--selector '{labels_str}'" if labels_str else ""
        elif pod_name and labels:
            raise NotImplementedError(
                f"You tried to filter by pod name '{pod_name}' and lables '{labels}'. Only one filter is applieable"
            )
        pod_descs: Dict = json.loads(
            Executer.exec(
                f"{config.KUBECTL_COMMAND} get pods {namespace_arg} {selector_arg} -o json"
            )
        )
        if pod_descs["kind"] == "List":
            # we have multiple pods as result. lets extraxt the list of pods
            pod_descs = pod_descs["items"]
        elif pod_descs["kind"] == "Pod":
            # we have a single pod. lets put in a list to keep the format consistently
            pod_descs = [pod_descs]
        pods: List[Container] = []
        for pod_desc in pod_descs:
            pods.append(Container.from_kubernetes_get_dict(pod_desc))
        if describe:
            return pods
        else:
            return [pod.id for pod in pods]

    @classmethod
    def kubernetes_get_pods_to_be_backed_up(
        cls, namespace: str = None, all_namespaces: bool = False
    ) -> List[Container]:
        workloads = cls.kubernetes_get_workloads_to_be_backed_up(
            namespace, all_namespaces
        )
        pods: List[Container] = []
        for workload in workloads:
            for wl_pod in cls.kubernetes_get_pods_by_workload(workload):
                wl_pod = cls._attach_parent_workload_metadata_to_pod(wl_pod, workload)
                pods.append(wl_pod)
        return pods

    @classmethod
    def kubernetes_get_pods_by_workload(cls, workload: Dict):
        """[summary]

        Args:
            workload (dict): workload description as outputet by `kubectl get ... -o json` e.g. `kubectl get deployment --all-namespaces --selector backup.dzd-ev.de/enabled=true  -o json`

        Raises:
            NotImplementedError: [description]
        """
        pods: List[Container] = []
        if not (
            "spec" in workload
            and "selector" in workload["spec"]
            and "matchLabels" in workload["spec"]["selector"]
            and "namespace" in workload["metadata"]
        ):
            raise NotImplementedError(
                f"Can not query pods of workload. Unknown workload format. Expected to find keys 'spec.selector.matchLabels' in Workload. got \n\n{workload}\n\n"
            )
        pod_selector_labels: List[Label] = Label.dict_to_label(
            workload["spec"]["selector"]["matchLabels"]
        )
        for wl_pod in cls.kubernetes_get_pods(
            labels=pod_selector_labels,
            namespace=workload["metadata"]["namespace"],
            all_namespaces=False,
            describe=True,
        ):
            wl_pod = cls._attach_parent_workload_metadata_to_pod(wl_pod, workload)
            pods.append(wl_pod)
        return pods

    @classmethod
    def _attach_parent_workload_metadata_to_pod(
        cls, pod: Container, parent_workload: Dict
    ) -> Container:
        lbls = parent_workload["metadata"]["labels"]
        if "annotations" in parent_workload["metadata"]:
            lbls = {**lbls, **parent_workload["metadata"]["annotations"]}
        workload_backup_config_labels = ValidLabels.valid_labels_from_dict(
            lbls,
            add_missing_default_labels=True,
        )
        pod.coda_labels = {**workload_backup_config_labels, **pod.coda_labels}

        if (
            ValidLabels.backup_name in pod.coda_labels
            and not pod.coda_labels[ValidLabels.backup_name].val
        ):
            # if the backup subdir is not defined by a label we override the default (pod name) with the parent workload name to get a more consistent name
            pod.backup_name = parent_workload["metadata"]["name"]
        # Attach the parent workload data just for good measure... not in any use yet. maybe we can delete this step

        pod.parent = parent_workload
        return pod

    @classmethod
    def kubernetes_get_workloads(
        cls,
        namespace: str = None,
        all_namespaces: bool = False,
        labels: List[Label] = None,
        describe: bool = False,
    ) -> List[str]:
        # kubectl get all
        # kubectl get pods -o jsonpath='{range .items[?(.kind=StatefulSet)]}{.metadata.name}{end}'
        selector_arg = ""
        if labels:
            labels_str: str = ",".join([str(label) for label in labels])
            selector_arg: str = f"--selector '{labels_str}'" if labels_str else ""

        if all_namespaces:
            namespace_arg = "--all-namespaces"
        else:
            namespace_arg = (
                f"-n {namespace if namespace else config.KUBECTL_DEFAULT_NAMESPACE}"
            )
        workloads = []
        for workload_type in config.KUBECTL_VALID_WORKLOAD_TYPES:
            results_items: Dict = json.loads(
                Executer.exec(
                    f"{config.KUBECTL_COMMAND} get all {namespace_arg} {selector_arg} -o json"
                )
            )["items"]
            for res_item in results_items:
                if "kind" in res_item and res_item["kind"] == workload_type:
                    if describe:
                        workloads.append(res_item)
                    else:
                        workloads.append(res_item["metadata"]["name"])
        return workloads

    @classmethod
    def kubernetes_get_workloads_to_be_backed_up(
        cls, namespace: str = None, all_namespaces: bool = False
    ) -> List[Dict]:
        # kubectl get all
        # kubectl get pods -o jsonpath='{range .items[?(.kind=StatefulSet)]}{.metadata.name}{end}'

        backup_enabled_label = ValidLabels.label_from_valid_label_as_template(
            ValidLabels.enabled, val=True
        )
        return cls.kubernetes_get_workloads(
            namespace=namespace,
            all_namespaces=all_namespaces,
            labels=[backup_enabled_label],
            describe=True,
        )

    @classmethod
    def docker_get_container_to_be_backed_up(
        cls, describe: bool = False
    ) -> Union[List[str], List[Container]]:
        return cls.docker_get_containers(
            labels=[
                ValidLabels.label_from_valid_label_as_template(
                    ValidLabels.enabled, val=True
                )
            ],
            describe=describe,
        )

    @classmethod
    def docker_get_containers(
        cls, labels: List[Label] = None, describe: bool = False
    ) -> Union[List[str], List[Container]]:
        filter_args = ""
        if labels:
            filter_args = " ".join(
                ['--filter="label=' + str(label) + '"' for label in labels]
            )
        container_ids = (
            Executer.exec(
                f'{config.DOCKER_COMMAND} ps --format "{{{{ .ID }}}}" {filter_args}'
            )
            .decode("utf-8")
            .splitlines()
        )

        if not describe:
            return container_ids
        containers: List[Container] = []
        for container_id in container_ids:
            container = Container.from_docker_inspect_dict(
                json.loads(
                    Executer.exec(
                        f"{config.DOCKER_COMMAND} inspect {container_id}"
                    ).decode("utf-8")
                )
            )
            containers.append(container)
        log.debug(f"Containers found: {containers}")
        return containers

    @classmethod
    def kubernetes_get_config_by_labels(cls, pod_name: str) -> Dict[str, Label]:
        # config.DATABASE_CONTAINER_LABEL_BASE_KEY
        container_labels: Dict = json.loads(
            Executer.exec(
                f"{config.KUBECTL_COMMAND} get pods {config.KUBECTL_NAMESPACE_PARAM} {pod_name} -o json"
            )
        )

        config_labels_dict = {}
        for label in ValidLabels.iter():
            if label.key in container_labels["metadata"]["labels"].keys():
                label.val = container_labels["metadata"]["labels"][label.key]
            config_labels_dict[label.key] = label

        return config_labels_dict

    @classmethod
    def docker_get_labels(cls, container_name: str, valid=True) -> Dict[str, Label]:
        # config.DATABASE_CONTAINER_LABEL_BASE_KEY

        container_labels: Dict = json.loads(
            Executer.exec(
                f"{config.DOCKER_COMMAND} inspect --format '{{{{ json .Config.Labels }}}}' {container_name}"
            )
        )
        ValidLabels.valid_labels_from_dict()

        config_labels_dict = {}
        for label in ValidLabels.iter():
            if label.key in container_labels.keys():
                label.val = container_labels[label.key]
            config_labels_dict[label.key] = label
        return config_labels_dict
