import os
import sys

import click
from click import ClickException

import manta_lab as ml

from .cli_base import cli, CONTEXT, manta_api
from .utils import display_error


####################
# Artifacts
####################
@cli.group(help="Commands for artifacts")
def artifact():
    pass


@artifact.command(context_settings=CONTEXT, help="List all artifacts in a project")
@click.argument("path")
@click.option("--type", "-t", help="The type of artifacts to list")
@display_error
def ls(path, type):
    api = manta_api()
    if type is not None:
        types = [api.artifact_type(type, path)]
    else:
        types = api.artifact_types(path)

    for kind in types:
        for collection in kind.collections():
            versions = api.artifact_versions(
                kind.type,
                "/".join([kind.entity, kind.project, collection.name]),
                per_page=1,
            )
            latest = next(versions)
            print(
                "{:<15s}{:<15s}{:>15s} {:<20s}".format(
                    kind.type,
                    latest.updated_at,
                    ml.util.to_readable_size(latest.size),
                    latest.name,
                )
            )


@artifact.command(context_settings=CONTEXT, help="Upload an artifact to MantaLab")
@click.argument("path")
@click.option("--name", "-n", help="The name of the artifact to push: project/artifact_name")
@click.option("--description", "-d", help="A description of this artifact")
@click.option("--type", "-t", default="dataset", help="The type of the artifact")
@click.option(
    "--alias",
    "-a",
    default=["latest"],
    multiple=True,
    help="An alias to apply to this artifact",
)
@display_error
def upload(path, name, description, type, alias):
    if name is None:
        name = os.path.basename(path)
    api = manta_api()
    entity, project, artifact_name = api._parse_artifact_path(name)
    if project is None:
        project = click.prompt("Enter the name of the project you want to use")
    # TODO: settings nightmare...
    api = manta_api()
    api.set_setting("entity", entity)
    api.set_setting("project", project)
    artifact = ml.Artifact(name=artifact_name, type=type, description=description)
    artifact_path = "{entity}/{project}/{name}:{alias}".format(
        entity=entity, project=project, name=artifact_name, alias=alias[0]
    )
    if os.path.isdir(path):
        print(
            'Uploading directory {path} to: "{artifact_path}" ({type})'.format(
                path=path, type=type, artifact_path=artifact_path
            )
        )
        artifact.add_dir(path)
    elif os.path.isfile(path):
        print(
            'Uploading file {path} to: "{artifact_path}" ({type})'.format(
                path=path, type=type, artifact_path=artifact_path
            )
        )
        artifact.add_file(path)
    elif "://" in path:
        print(
            'Logging reference artifact from {path} to: "{artifact_path}" ({type})'.format(
                path=path, type=type, artifact_path=artifact_path
            )
        )
        artifact.add_reference(path)
    else:
        raise ClickException("Path argument must be a file or directory")

    run = ml.init(entity=entity, project=project, config={"path": path}, job_type="cli_put")
    # We create the artifact manually to get the current version
    res, _ = api.create_artifact(
        type,
        artifact_name,
        artifact.digest,
        client_id=artifact._client_id,
        sequence_client_id=artifact._sequence_client_id,
        entity_name=entity,
        project_name=project,
        run_name=run.run_id,
        description=description,
        aliases=[{"artifactCollectionName": artifact_name, "alias": a} for a in alias],
    )
    artifact_path = artifact_path.split(":")[0] + ":" + res.get("version", "latest")
    # Re-create the artifact and actually upload any files needed
    run.log_artifact(artifact, aliases=alias)
    print("Artifact uploaded, use this artifact in a run by adding:\n", prefix=False)

    print(
        '    artifact = run.use_artifact("{path}")\n'.format(
            path=artifact_path,
        ),
        prefix=False,
    )


@artifact.command(context_settings=CONTEXT, help="Download an artifact from MantaLab")
@click.argument("path")
@click.option("--root", help="The directory you want to download the artifact to")
@click.option("--type", help="The type of artifact you are downloading")
@display_error
def download(path, root, type):
    api = manta_api()
    entity, project, artifact_name = api._parse_artifact_path(path)
    if project is None:
        project = click.prompt("Enter the name of the project you want to use")

    try:
        artifact_parts = artifact_name.split(":")
        if len(artifact_parts) > 1:
            version = artifact_parts[1]
            artifact_name = artifact_parts[0]
        else:
            version = "latest"
        full_path = "{entity}/{project}/{artifact}:{version}".format(
            entity=entity, project=project, artifact=artifact_name, version=version
        )
        print("Downloading {type} artifact {full_path}".format(type=type or "dataset", full_path=full_path))
        artifact = api.artifact(full_path, type=type)
        path = artifact.download(root=root)
        print("Artifact downloaded to %s" % path)
    except ValueError:
        raise ClickException("Unable to download artifact")


@cli.command(context_settings=CONTEXT, help="Pull files from MantaLab")
@click.argument("run", envvar=ml.env.RUN_ID)
@click.option("--project", "-p", envvar=ml.env.PROJECT, help="The project you want to download.")
@click.option(
    "--entity",
    "-e",
    default="models",
    envvar=ml.env.ENTITY,
    help="The entity to scope the listing to.",
)
@display_error
def pull(run, project, entity):
    api = manta_api()
    project, run = api.parse_slug(run, project=project)
    urls = api.download_urls(project, run=run, entity=entity)
    if len(urls) == 0:
        raise ClickException("Run has no files")
    click.echo("Downloading: {project}/{run}".format(project=click.style(project, bold=True), run=run))

    for name in urls:
        if api.file_current(name, urls[name]["md5"]):
            click.echo("File %s is up to date" % name)
        else:
            length, response = api.download_file(urls[name]["url"])
            # TODO: I had to add this because some versions in CI broke click.progressbar
            sys.stdout.write("File %s\r" % name)
            dirname = os.path.dirname(name)
            if dirname != "":
                ml.util.mkdir(dirname)
            with click.progressbar(
                length=length,
                label="File %s" % name,
                fill_char=click.style("&", fg="green"),
            ) as bar:
                with open(name, "wb") as f:
                    for data in response.iter_content(chunk_size=4096):
                        f.write(data)
                        bar.update(len(data))


@cli.command(context_settings=CONTEXT, help="Pull files from MantaLab")
@click.argument("run", envvar=ml.env.RUN_ID)
@click.option("--project", "-p", envvar=ml.env.PROJECT, help="The project you want to download.")
@click.option(
    "--entity",
    "-e",
    default="models",
    envvar=ml.env.ENTITY,
    help="The entity to scope the listing to.",
)
@display_error
def pull(run, project, entity):
    api = manta_api()
    project, run = api.parse_slug(run, project=project)
    urls = api.download_urls(project, run=run, entity=entity)
    if len(urls) == 0:
        raise ClickException("Run has no files")
    click.echo("Downloading: {project}/{run}".format(project=click.style(project, bold=True), run=run))

    for name in urls:
        if api.file_current(name, urls[name]["md5"]):
            click.echo("File %s is up to date" % name)
        else:
            length, response = api.download_file(urls[name]["url"])
            # TODO: I had to add this because some versions in CI broke click.progressbar
            sys.stdout.write("File %s\r" % name)
            dirname = os.path.dirname(name)
            if dirname != "":
                ml.util.mkdir_exists_ok(dirname)
            with click.progressbar(
                length=length,
                label="File %s" % name,
                fill_char=click.style("&", fg="green"),
            ) as bar:
                with open(name, "wb") as f:
                    for data in response.iter_content(chunk_size=4096):
                        f.write(data)
                        bar.update(len(data))
