from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="CoDaBuddy",
    description="Container Database Backup - A tool to backup your database containers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.connect.dzd-ev.de/dzdtools/CoDaBuddy",
    author="TB",
    author_email="tim.bleimehl@helmholtz-muenchen.de",
    license="MIT",
    packages=["CoDaBuddy"],
    install_requires=["DZDConfigs", "Click", "tabulate", "humanize", "pyyaml"],
    python_requires=">=3.7",
    zip_safe=False,
    include_package_data=True,
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        # "local_scheme": "node-and-timestamp"
        "local_scheme": "no-local-version",
        "write_to": "version.py",
    },
    setup_requires=["setuptools_scm"],
    entry_points={
        "console_scripts": [
            "coda-backup=CoDaBuddy.cli:backup_cli",
            "coda-restore=CoDaBuddy.cli:restore_cli",
            "coda-auto-create=CoDaBuddy.cli:auto_create",
        ],
    },
)
