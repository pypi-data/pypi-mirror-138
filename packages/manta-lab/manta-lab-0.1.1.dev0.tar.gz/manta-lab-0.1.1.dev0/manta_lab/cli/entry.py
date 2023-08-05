import os
import sys

import click
from click import ClickException

import manta_lab as ml
from manta_lab.cli.utils import display_error

CONTEXT = dict(default_map={})


def manta_api(settings=None):
    s = settings or ml.setup().settings
    api = ml.api.MantaAPI(settings=s)
    api.cli_setup()
    return api


class BaseGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        return None


@click.command(cls=BaseGroup, invoke_without_command=True)
@click.version_option(version=ml.__version__)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(context_settings=CONTEXT, help="Login to MantaLab")
@click.argument("key", nargs=-1)
@click.option("--cloud", is_flag=True, help="Login to the cloud instead of local")
@click.option("--host", default=None, help="Login to a specific instance of MantaLab")
@click.option("--relogin", default=None, is_flag=True, help="Force relogin if already logged in.")
@display_error
def login(key, host, cloud, relogin):
    if host and not host.startswith("http"):
        raise click.ClickException("host must start with http(s)://")

    if key:
        key = key[0]
        relogin = True

    try:
        ml.setup(
            settings=ml.Settings(
                base_url=host,
            )
        )
    except TypeError as e:
        print(str(e))
        sys.exit(1)

    ml.login(api_key=key, relogin=relogin, base_url=host)


@cli.command(context_settings=CONTEXT, help="List accessible teams", hidden=True)
def teams():
    api = manta_api()

    teams = api.teams()
    message = "Accessible teams(entities) are"
    click.echo(click.style(message, bold=True))
    for team in teams:
        # add color if this team is personal
        click.echo(
            "".join(
                (
                    click.style(team["uid"], fg="blue", bold=True),
                    "\n  - ",
                    # str(team["description"] or "").split("\n")[0],
                    f"members: {[t['name'] for t in team['members']]}",
                    "\n  - ",
                    f"number of projects: {len(team['projects'])}",
                )
            )
        )
    return teams


@cli.command(context_settings=CONTEXT, help="List projects", hidden=True)
@click.option(
    "--entity",
    "-e",
    default=None,
    envvar=ml.env.ENTITY,
    help="The entity to scope the listing to.",
)
@display_error
def projects(entity, display=True):
    api = manta_api()
    # TODO: show items by entity name
    projects = api.projects()

    entity = entity or api.entity
    if len(projects) == 0:
        message = "No projects found for %s" % entity
    else:
        message = 'Latest projects for "%s"' % entity
    if display:
        click.echo(click.style(message, bold=True))
        for project in projects:
            click.echo(
                "".join(
                    (
                        "  ",
                        click.style(project["name"], fg="blue", bold=True),
                        ": ",
                        str(project["description"] or "").split("\n")[0],
                    )
                )
            )
    return projects


def sync():
    # TODO
    pass


def tuning():
    # TODO
    pass


####################
# Artifacts
####################
@cli.group(help="Commands for artifacts")
def artifact():
    pass


@artifact.command(context_settings=CONTEXT, help="List all artifacts in a project")
@click.argument("project")
@click.option("--entity", help="Team name")
@click.option("--run", "-e", help="Run id")
@click.option("--type", "-t", help="The type of artifacts to list")
@display_error
def ls(project, entity, run, type):
    api = manta_api()

    s = ml.Settings(entity=entity, project=project, run_name=run)
    api.update_settings(s)

    path = "{api.entity}/{api.project}"
    artifacts = api.artifacts()
    if len(artifacts) == 0:
        message = f"No artifacts found for {path}"
    else:
        message = f"Latest artifacts for {path}"
    click.echo(click.style(message, bold=True))
    for artifact in artifacts:
        description = str(artifact["description"] or "").split("\n")[0]
        click.echo(
            "".join(
                (
                    "  ",
                    click.style(artifact["name"], fg="blue", bold=True),
                    ":",
                    f"\n    - number of files: {len(artifact['manifests'])}",
                    f"\n    - description: {description}",
                )
            )
        )
    # TODO : filter by type


@artifact.command(context_settings=CONTEXT, help="Create Artifact to MantaLab")
@click.argument("name")
@click.option("--description", "-d", help="A description of this artifact")
@click.option("--group", "-g", default="dataset", help="The type of the artifact")
@click.option("--labels", "-l", default=["cli"], multiple=True, help="The label of the artifact")
def create(name, description, group, labels):
    api = manta_api()
    entity, project, run, artifact_name = api.parse_artifact_path(name)
    s = ml.Settings(entity=entity, project=project, run_name=run)

    artifact = ml.Artifact(artifact_name, description=description, group=group, labels=labels)
    artifact.save(settings=s)


if __name__ == "__main__":
    # name = "test-artifact/something5"
    # description = "i hope this trial succeed in one trial"
    # group = "test"
    # labels = ["test", "artifact", "create"]
    # create(name, description, group, labels)

    ls("test-artifact", None, None, None)
