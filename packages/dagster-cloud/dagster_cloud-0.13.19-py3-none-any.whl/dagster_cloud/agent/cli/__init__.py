import logging
import os
from pathlib import Path
from typing import Optional

from dagster.core.errors import DagsterHomeNotSetError
from dagster.utils.interrupts import capture_interrupts
from dagster.utils.log import default_date_format_string, default_format_string
from dagster_cloud.agent.dagster_cloud_agent import DagsterCloudAgent
from dagster_cloud.instance import DagsterCloudAgentInstance
from typer import Argument, Typer

from ...cli import ui

app = Typer(help="Interact with the Dagster Cloud agent.")


def agent_home_exception():
    dagster_home_loc = (
        (
            f"No Dagster config provided in specified directory {os.getenv('DAGSTER_HOME')}. "
            "You must specify the location of a directory containing a dagster.yaml "
            "file as a parameter or by setting the DAGSTER_HOME environment variable."
        )
        if os.getenv("DAGSTER_HOME")
        else (
            "No directory provided or DAGSTER_CLOUD environment variable set. "
            "You must supply the location of a directory containing a dagster.yaml "
            "file as a parameter or by setting the DAGSTER_HOME environment variable."
        )
    )
    return ui.error(f"No Dagster config found.\n\n{dagster_home_loc}")


def run_local_agent():
    try:
        with DagsterCloudAgentInstance.get() as instance:
            user_code_launcher = instance.user_code_launcher
            user_code_launcher.start()

            with DagsterCloudAgent() as agent:
                agent.run_loop(instance, user_code_launcher, agent_uuid=instance.instance_uuid)
    except DagsterHomeNotSetError:
        raise agent_home_exception()


def run_local_agent_in_environment(dagster_home: Optional[Path]):
    with capture_interrupts():
        try:
            old_env = dict(os.environ)
            if dagster_home:
                os.environ["DAGSTER_HOME"] = str(dagster_home.resolve())
            run_local_agent()
        finally:
            os.environ.clear()
            os.environ.update(old_env)


@app.command(
    help=(
        "Runs the Dagster Cloud agent. Sources config from a dagster.yaml located in the "
        "optional provided directory, otherwise uses the directory specified by the DAGSTER_HOME "
        "environment variable."
    ),
    short_help="Run the Dagster Cloud agent.",
)
def run(dagster_home: Optional[Path] = Argument(None)):
    logging.basicConfig(
        level=logging.INFO,
        format=default_format_string(),
        datefmt=default_date_format_string(),
        handlers=[logging.StreamHandler()],
    )
    run_local_agent_in_environment(dagster_home)
