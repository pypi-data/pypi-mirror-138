import os
from typing import Any, Dict, List, Optional, Sequence, Union

import manta_lab.env as env
import manta_lab.util as util
from manta_lab.api.client import MantaClient
from manta_lab.base.settings import Settings

PROJECT_ENDPOINT = ""
EXPERIMENT_ENDPOINT = ""
USER_ENDPOINT = ""
TEAM_ENDPOINT = ""


class MantaAPI:
    def __init__(self, settings: Settings = None, environ: os.environ = None):
        self._settings = settings or Settings()
        self._environ = environ or os.environ

        self._client = MantaClient(self._settings)
        self._entity = None
        self._team_id = None
        self._project = None
        self._project_id = None
        self._experiment = None
        self._experiment_id = None

    @property
    def api_key(self):
        return self._client.api_key

    @property
    def client(self):
        return self._client

    @property
    def entity(self):
        entity = self._entity or self._settings.entity
        if not entity:
            entity = self.get_default_team()["uid"]
        return entity

    @property
    def team_id(self):
        return self._team_id

    @property
    def project(self):
        return self._project or self._settings.project

    @property
    def project_id(self):
        return self._project_id

    @property
    def experiment(self):
        return self._experiment or self._settings.experiment_name

    @property
    def experiment_id(self):
        #
        return self._experiment_id or self._settings.experiment_id

    def cli_setup(self):
        """
        set team by using settings.entity
        """
        s = self._settings

        self._team_id = None
        self._project_id = None
        self._experiment_id = None

        # set team
        team_name = s.entity
        if team_name:
            for team in self.teams():
                if team["uid"] == team_name:
                    self._team_id = team["Id"]
                    self._entity = team_name
                    break
        else:
            # TODO: server API not yet implemented
            default_team = self.get_default_team()
            self._team_id = default_team["Id"]
            self._entity = default_team["uid"]

    def setup(self):
        """
        1. set team by using settings.entity
        2. set project by using settings.project
        """
        s = self._settings

        self._team_id = None
        self._project_id = None
        self._experiment_id = None

        # set team
        team_name = s.entity
        if team_name:
            for team in self.teams():
                if team["uid"] == team_name:
                    self._team_id = team["Id"]
                    self._entity = team_name
                    break
        else:
            # TODO: server API not yet implemented
            default_team = self.get_default_team()
            self._team_id = default_team["Id"]
            self._entity = default_team["uid"]

        # set project
        project_name = s.project
        for proj in self.projects():
            if proj["name"] == project_name:
                self._project_id = proj["Id"]
                break

        if self._project_id is None:
            self.create_project(name=project_name)

    def _update_entity(self, entity):
        if entity == self.entity:
            return
        # update team id
        for t in self.teams():
            if t["uid"] == entity:
                self._team_id = t["Id"]
                self._entity = entity
                return
        raise AttributeError("Couldn't find team name in your temas list")

    def _update_project(self, project):
        if project == self._project:
            return
        # update project_id
        for p in self.projects():
            if p["name"] == project:
                self._project_id = p["Id"]
                self._project = project
                return
        raise AttributeError("Couldn't find project name in your project list")

    def _update_experiment(self, experiment):
        if experiment == self._experiment:
            return
        # update experiment_id
        for e in self.experiments():
            if e["name"] == experiment:
                self._experiment_id = e["Id"]
                self._experiment = experiment
                return
        raise AttributeError("Couldn't find experiment name in your experiment list")

    def update_settings(self, s: Settings):
        # TODO: do we need singleton update ?
        self._settings.update_settings(s)

        # while update, name should be changed to id
        if s.entity:
            self._update_entity(s.entity)
        if s.project:
            self._update_project(s.project)
        if s.experiment_name:
            self._update_experiment(s.experiment_name)

    def profile(self):
        return self.client.request_json("get", "user/profile")

    def teams(self):
        return self.client.request_json("get", "team/my")["teams"]

    def get_default_team(self):
        return self.client.request_json("get", "team/my/personal")

    def get_team(self, team_id: str = None) -> Dict:
        team_id = team_id or self.team_id
        return self.client.request_json("get", f"team/{team_id}")

    def create_team(self, name: str) -> str:
        kwargs = dict(uid=name)
        id = self.client.request_json("post", "team", kwargs)["Id"]
        self._team_id = id
        return id

    def delete_team(self, team_id: str) -> None:
        self.client.request_json("delete", f"team/{team_id}")

    def get_team_by_name(self, name: str):
        """
        Return team id
        """

        for team in self.teams():
            if name == team["uid"]:
                return team["Id"]
        return None

    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        thumbnail: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ):
        """
        Return upsert project
        """
        description = description or " "  # TODO: API will change it to optional later, delete here
        kwargs = locals()
        res = self.client.request_json("post", f"team/{self.team_id}/project", kwargs)
        self._project = name
        self._project_id = res["Id"]
        return self._project_id

    def projects(self, team_id: str = None) -> List[Dict[str, Any]]:
        """
        Return projects list
        """
        team_id = team_id or self.team_id
        return self.client.request_json("get", f"team/{team_id}/project")["projects"]

    def get_project(self, project_id: str = None):
        """
        Return project detail
        """
        project_id = project_id or self.project_id
        return self.client.request_json("get", f"project/{project_id}")

    def get_project_by_name(self, name: str):
        """
        Return project detail
        """

        for project in self.projects():
            if name == project["name"]:
                return project["Id"]
        return None

    def delete_project(self, project_id: str):
        """
        Return delete project
        """
        return self.client.request_json(
            "delete",
            f"project/{project_id}",
        )

    def experiments(self, project_id: str = None):
        """
        Return experiments list
        """
        project_id = project_id or self.project_id
        return self.client.request_json("get", f"project/{project_id}/experiment")["experiments"]

    def get_experiment(self, experiment_id: str = None):
        """
        Return experiment detail
        """
        experiment_id = experiment_id or self.experiment_id

        return self.client.request_json("get", f"experiment/{experiment_id}")

    def create_experiment(
        self,
        name: str = None,
        memo: str = None,
        config: Dict = None,
        metadata: Dict = None,
        hyperparameter: Dict = None,
        tags: Sequence = None,
    ):
        """
        Return experiment upsert
        """
        project_id = self.project_id
        name = name or util.generate_id()

        kwargs = locals()
        res = self.client.request_json("post", f"project/{project_id}/experiment", kwargs)
        self._experiment = name
        self._experiment_id = res["Id"]
        return self._experiment_id

    def delete_experiment(self, *args, **kwargs):
        """
        Return experiment delete
        """
        return {}

    def update_experiment_status(self, status):
        status = status.lower()
        assert status in ["pending", "running", "done", "error", "aborted"]
        return self.client.request("patch", f"experiment/{self.experiment_id}/status", {"status": status})

    def update_experiment_meta(self, metadata):
        return self.client.request("patch", f"experiment/{self.experiment_id}/metadata", metadata)

    def update_experiment_config(self, config):
        return self.client.request("patch", f"experiment/{self.experiment_id}/config", config)

    def update_experiment_summary(self, summary):
        return self.client.request("patch", f"experiment/{self.experiment_id}/summary", summary)

    def send_heartbeat(self):
        return self.client.request("post", f"experiment/{self.experiment_id}/record")

    def send_experiment_record(self, histories: List[Dict] = None, systems: List[Dict] = None, logs: List[Dict] = None):
        kwargs = locals()
        return self.client.request("post", f"experiment/{self.experiment_id}/record", kwargs)

    def artifacts(self, project_id=None):
        """
        Return artifacts list
        """
        project_id = project_id or self.project_id
        return self.client.request_json("get", f"project/{project_id}/artifact")["artifacts"]

    def detail_artifact(self, artifact_id):
        """
        Return artifact detail
        """
        return self.client.request_json("get", f"artifact/{artifact_id}")

    def get_artifact(self, project, experiment, name):
        # TODO
        project_id = project
        params = {"experimentId": experiment, "name": name}
        res = self.client.request_json("get", f"project/{project_id}/artifact", params=params)
        return res["artifacts"]

    def create_artifact(
        self,
        name: str,
        description: Optional[str] = None,
        group: Optional[str] = None,
        labels: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        project_id: Optional[str] = None,
        experiment_id: Optional[str] = None,
        project_only: bool = False,
    ):

        project_id = project_id or self.project_id
        if not project_only:
            experiment_id = experiment_id or self.experiment_id

        params = dict(
            experimentId=experiment_id,
            name=name,
            description=description,
            group=group,
            labels=labels,
            metadata=metadata,
        )
        res = self.client.request_json("post", f"project/{project_id}/artifact", params=params)
        return res["Id"]

    def update_artifact(self, *args, **kwargs):
        """
        Return artifact upsert
        TODO: need api implementation
        """
        return {}

    def delete_artifact(self, artifact_id):
        """
        Return artifact delete
        """
        return self.client.request("delete", f"artifact/{artifact_id}")

    def list_artifact_manifest(self, artifact_id):
        return self.client.request_json("get", f"artifact/{artifact_id}/manifest")["manifests"]

    def detail_artifact_manifest(self, artifact_id, manifest_id):
        """
        Return artifact manifest detail
        """
        return self.client.request_json("get", f"artifact/{artifact_id}/manifest/{manifest_id}")

    def create_artifact_manifest(self, artifact_id, name, size, digest, path, version=None, type="remote", **kwargs):
        # manifest_id is in kwargs but not using it
        params = dict(name=name, size=size, digest=digest, relativePath=path, version=version, type=type)
        res = self.client.request_json("post", f"artifact/{artifact_id}/manifest", params=params)
        return res["Id"]

    def update_artifact_manifest(self, artifact_id, name, version):
        """
        Return artifact manifest upsert

        We dont accept update manifest directly.
        delete artifact and create manifest again
        """
        self.delete_artifact_manifest(artifact_id, name, version)
        res = self.create_artifact_manifest(artifact_id, name, version)
        return res

    def manifest_upload_url(self, artifact_id, manifest_id):
        res = self.client.request_json("get", f"artifact/{artifact_id}/manifest/{manifest_id}/upload-url")
        return res["url"], res["fields"]

    def manifest_download_url(self, artifact_id, manifest_id):
        res = self.client.request_json("get", f"artifact/{artifact_id}/manifest/{manifest_id}/download-url")
        return res["url"]

    # TODO: no need for status maybe?
    def commit_artifact_manifest_uploaded(self, artifact_id, manifest_id, status="READY"):
        params = dict(
            status=status,
        )
        return self.client.request_json("patch", f"artifact/{artifact_id}/manifest/{manifest_id}/status", params)

    def delete_artifact_manifest(self, artifact_id, name, version="latest"):
        """
        Return artifact manifest delete
        """
        params = dict(name=name, version=version)
        return self.client.request("delete", f"artifact/{artifact_id}/artifactManifest", params)

    def reports(self, *args, **kwargs):
        """
        Return reports list
        """
        return {}

    def get_report(self, *args, **kwargs):
        """
        Return report detail
        """
        return {}

    def upsert_report(self, *args, **kwargs):
        """
        Return report upsert
        """
        return {}

    def delete_report(self, *args, **kwargs):
        """
        Return report delete
        """
        return {}

    def initiate_tune(self, config):
        import manta_lab as mc

        id = mc.util.generate_id()
        self.tune_repo[id] = config
        return id

    def register_agent(self, host, tune_id):
        return {"id": "register_agent_id"}

    def request_tune_schedule(self, agent_id, metric, run_states):
        return [
            {
                "type": "RUN",
                "experiment_id": "exp_id",
                "config": {
                    "name": "my-awesome-sweep",
                    "metric": {"name": "accuracy", "goal": "maximize"},
                    "method": "grid",
                    "parameters": {"a": {"values": [1, 2, 3, 4]}},
                },
            }
        ]

    def parse_artifact_path(self, path):
        """Returns project, entity and artifact name for project specified by path

        path: str,
            <artifact>
            <project>/<artifact>
            <entity>/<project>/<artifact>
            <entity>/<project>/<experiment>/<artifact>
        """
        entity = self._settings["entity"] or self.entity
        project = self._settings["project"]
        experiment = self._settings["experiment_name"]

        if path is None:
            return entity, project, experiment, None

        parts = path.split("/")
        if len(parts) == 1:
            return entity, project, experiment, path
        elif len(parts) == 2:
            return entity, parts[0], experiment, parts[1]
        elif len(parts) == 3:
            return parts[0], parts[1], experiment, parts[2]
        elif len(parts) == 4:
            return parts
        else:
            raise ValueError("Invalid artifact path: %s" % path)
