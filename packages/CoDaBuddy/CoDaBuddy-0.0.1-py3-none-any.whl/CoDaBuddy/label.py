from distutils import util
from typing import List, Dict, Type, Any, Union
import json
import yaml
import copy
import logging

from Configs import getConfig

from config import DEFAULT


config: DEFAULT = getConfig(config_classes=[DEFAULT])
log = logging.getLogger("databasebackupper")


class Label:
    def __init__(
        self,
        label: Union[str, Dict[str, str]],
        type_: Type = str,
        possible_values: List = None,
        default: Any = None,
        info: str = None,
        base_label_key: str = None,
    ):
        if isinstance(label, dict):
            key = list(label.keys())[0]
            val = list(label.values())[0]
        else:
            key, *val = label.split("=")
        self.key: str = f"{base_label_key + '/' if base_label_key and not key.startswith(base_label_key) else ''}{key}"
        try:
            if type_ == bool and isinstance(val, str):
                val = util.strtobool(val)
            self.val: Union[str, int, bool] = type_(val) if val else default
        except:
            raise ValueError(
                f"Label '{key}={val}' expected to be of type '{type_}'. Can not convert '{val}' to {type_}"
            )
        if possible_values and self.val and self.val not in possible_values:
            raise ValueError(
                f"Label value of '{self.key}' expected to be one of {possible_values} but is '{self.val}' (value type: '{type(self.val)}')"
            )
        self.type: Type = type_
        self.possible_values: List = possible_values
        self.default: Union[str, int, bool] = default
        self.info: str = info

    @classmethod
    def dict_to_label(cls, labels: dict) -> List["Label"]:
        l = []
        for key, val in labels.items():
            l.append(Label({key: val}))
        return l

    def to_dict(self, hide_val: bool = False) -> Dict:
        lbl_dict = {
            "key": self.key,
            "type": self.type.__name__,
            "possible_values": self.possible_values,
            "default": self.default,
            "info": self.info,
        }
        if not hide_val:
            lbl_dict["value"] = self.val
        return lbl_dict

    def __eq__(self, other: Union["Label", str]):
        return (
            type(other) is type(self)
            and self.key == other.key
            or type(other) == str
            and self.key == other
        )

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        if self.type == bool and self.val is not None:
            val = str(self.val).lower()
        else:
            val = self.val
        if val is not None and val != "":
            return f"{self.key}={val}"
        else:
            return self.key

    def __repr__(self):
        if self.val:
            return f"<Label '{self.key}={self.val}'>"
        else:
            return f"<Label '{self.key}'>"


class ValidLabels:
    enabled: Label = Label(
        "enabled",
        bool,
        default=False,
        info="With this label you can enable or disable the backups for the container",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    backup_name: Label = Label(
        "backup_name",
        str,
        default=None,
        info="With this label you can define the sub-directory name for the the specific database. If not set, CoDaBuddy will determine the name by a containers docker name or kubernetes deployment name.",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    database_type: Label = Label(
        "type",
        str,
        possible_values=["mysql", "postgres", "neo4j"],
        info="Set the type of database running in the container",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    database_username: Label = Label(
        "username",
        str,
        info="Username to access the to be backed up database(s)",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    database_password: Label = Label(
        "password",
        str,
        info="Password to access the to be backed up database",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    database_host: Label = Label(
        "host",
        str,
        default="127.0.0.1",
        info="Hostname/IP-Address to access the database. In most container environments this will be the default value '127.0.0.1'",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    database_names: Label = Label(
        "databases",
        str,
        info="A single name or multiple names seperated by commata(','). Only databases with matching names will be backed up. If empty all databases will be backed up ",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    backup_dir: Label = Label(
        "backup_dir",
        str,
        default=config.BACKUP_DIR,
        info="Relative or absolute path to store the backups. Usally you can ignores this setting, you only need to specifiy this if you, for example, want to store your databases on different mounts/directories on your backup host",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    retention_daily: Label = Label(
        "retention_daily",
        int,
        default=config.RETENTION_KEEP_NUMBER_OF_DAILY_BACKUPS,
        info="How many daily backups should be kept?",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    retention_weekly: Label = Label(
        "retention_weekly",
        int,
        default=config.RETENTION_KEEP_NUMBER_OF_WEEKLY_BACKUPS,
        info="How many weekly backups should be kept?",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    retention_monthly: Label = Label(
        "retention_monthly",
        int,
        default=config.RETENTION_KEEP_NUMBER_OF_MONTHLY_BACKUPS,
        info="How many monthly backups should be kept?",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    retention_yearly: Label = Label(
        "retention_yearly",
        int,
        default=config.RETENTION_KEEP_NUMBER_OF_YEARLY_BACKUPS,
        info="How many yearly backups should be kept?",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    retention_manual: Label = Label(
        "retention_manual",
        int,
        default=config.RETENTION_KEEP_NUMBER_OF_MANUAL_BACKUPS,
        info="How many manual backups should be kept?",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )

    auto_create_enabled: Label = Label(
        "auto-create",
        bool,
        default=False,
        info="If the database does not exists, create it?",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    auto_create_user_name: Label = Label(
        "auto-create-user",
        str,
        default=None,
        info=f"The user to create a missing database (must have the priviledge to create a database). Defaults to backup user from label `{database_username.key}`?",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    auto_create_user_password: Label = Label(
        "auto-create-user-password",
        bool,
        default=None,
        info="The password for the user that is creating a missing database?",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    auto_create_encoding: Label = Label(
        "auto-create-encoding",
        str,
        default=None,
        info="Which database encoding should be used?",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    auto_create_collation: Label = Label(
        "auto-create-collation",
        str,
        default=None,
        info="Which database encoding should be used?",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )
    auto_create_databases: Label = Label(
        "auto-create-databases",
        str,
        default=None,
        info="Databases, Users and Password to create. Multiple entries seperated by comma are possible. \nformat:\n'<databasename>/<username>/<password>'\nExample:\n'mydb/myuser/supersave,otherdb/otheruser/savepw'",
        base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
    )

    @classmethod
    def iter(cls) -> List[Label]:
        """iterate all existing labels

        Returns:
            [List[Label]]: A list of all "Label"s
        """
        return [
            getattr(cls, a)
            for a in dir(cls)
            if not a.startswith("__") and not callable(getattr(cls, a))
        ]

    @classmethod
    def label_from_valid_label_as_template(cls, valid_label: Label, val):
        return Label(
            label={valid_label.key: val},
            type_=valid_label.type,
            possible_values=valid_label.possible_values,
            default=valid_label.default,
            info=valid_label.info,
            base_label_key=config.DATABASE_CONTAINER_LABEL_BASE_KEY,
        )

    @classmethod
    def valid_labels_from_dict(
        cls, labels: Union[List[dict], dict], add_missing_default_labels: bool = False
    ) -> Dict[str, Label]:
        if isinstance(labels, list):
            # convert list of labels to one dict representing all labels
            labels_as_dict = {}
            for label in labels:
                labels_as_dict[list(label.keys())[0]] = list(label.values())[0]
            labels = labels_as_dict
        lbls = {}
        for valid_label in cls.iter():
            for key, val in labels.items():
                if valid_label.key == key:
                    lbls[valid_label.key] = cls.label_from_valid_label_as_template(
                        valid_label=valid_label, val=val
                    )
                    break
            else:
                # ValidLabel was not in provided label dict. lets add it if desired by caller
                if add_missing_default_labels:
                    lbls[valid_label.key] = valid_label
        return lbls

    @classmethod
    def non_valid_labels_from_dict(
        cls, labels: Union[List[dict], dict]
    ) -> Dict[str, Label]:
        if isinstance(labels, list):
            # convert list of labels to one dict representing all labels
            labels_as_dict = {}
            for label in labels:
                labels_as_dict[list(label.keys())[0]] = list(label.values())[0]
            labels = labels_as_dict
        lbls = {}
        for key, val in labels.items():
            if key not in [valid_label for valid_label in ValidLabels.iter()]:
                label = Label(label={key: val})
                lbls[label.key] = label
        return lbls

    @classmethod
    def list_labels(cls, format: str = "human"):
        if format == "human":
            # ToDo: make this better readable for humans
            s = ""
            for label in cls.iter():
                s += f"\n# {label.key} \n"
                s += f"\ttype: {label.type.__name__}\n"
                if label.default is not None:
                    s += f"\tdefault: {label.default}\n"
                if label.possible_values:
                    s += f"\tpossible_values: {label.possible_values}\n"
                if label.info:
                    s += f"  {label.info}\n"
            return s
        elif format in ["yaml", "json", "dict"]:

            lbls = []
            for label in cls.iter():
                lbls.append(label.to_dict(hide_val=True))
            if format == "yaml":
                return yaml.dump(lbls)
            elif format == "json":
                return json.dumps(lbls)
            else:
                return lbls
        else:
            raise ValueError(
                "Expected format to be on of ['human','json','yaml','dict'] got '{format}'"
            )
