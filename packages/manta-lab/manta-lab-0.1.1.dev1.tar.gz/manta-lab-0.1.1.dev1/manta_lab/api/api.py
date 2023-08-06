import os
from typing import Any, Dict, List, Optional, Sequence, Union
from urllib.parse import quote as urlquote

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
        self._run = None
        self._run_id = None

    @property
    def api_key(self):
        return self._client.api_key

    @property
    def client(self):
        return self._client

    @property
    def app_url(self):
        return self._settings.base_url

    @property
    def api_url(self):
        return self._client.api_url

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
    def run(self):
        return self._run or self._settings.run_name

    @property
    def run_id(self):
        #
        return self._run_id or self._settings.run_id

    def cli_setup(self):
        """
        set team by using settings.entity
        """
        s = self._settings

        self._team_id = None
        self._project_id = None
        self._run_id = None

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
        self._run_id = None

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

        if self._project_id is None and not self._settings.cli_only:
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

    def _update_run(self, run):
        if run == self._run:
            return
        # update run_id
        for e in self.runs():
            if e["name"] == run:
                self._run_id = e["Id"]
                self._run = run
                return
        raise AttributeError("Couldn't find run name in your run list")

    def update_settings(self, s: Settings):
        # TODO: do we need singleton update ?
        self._settings.update_settings(s)

        # while update, name should be changed to id
        if s.entity:
            self._update_entity(s.entity)
        if s.project:
            self._update_project(s.project)
        if s.run_name:
            self._update_run(s.run_name)

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

    def runs(self, project_id: str = None):
        """
        Return runs list
        """
        project_id = project_id or self.project_id
        return self.client.request_json("get", f"project/{project_id}/run")["runs"]

    def get_run(self, run_id: str = None):
        """
        Return run detail
        """
        run_id = run_id or self.run_id

        return self.client.request_json("get", f"run/{run_id}")

    def create_run(
        self,
        name: str = None,
        memo: str = None,
        config: Dict = None,
        metadata: Dict = None,
        hyperparameter: Dict = None,
        tags: Sequence = None,
    ):
        """
        Return run upsert
        """
        project_id = self.project_id

        kwargs = locals()
        res = self.client.request_json("post", f"project/{project_id}/run", kwargs)
        self._run = name
        self._run_id = res["Id"]
        return self._run_id

    def delete_run(self, *args, **kwargs):
        """
        Return run delete
        """
        return {}

    def update_run_status(self, status):
        status = status.lower()
        assert status in ["pending", "running", "done", "error", "aborted"]
        return self.client.request("patch", f"run/{self.run_id}/status", {"status": status})

    def update_run_meta(self, metadata):
        return self.client.request("patch", f"run/{self.run_id}/metadata", metadata)

    def update_run_config(self, config):
        return self.client.request("patch", f"run/{self.run_id}/config", config)

    def update_run_summary(self, summary):
        return self.client.request("patch", f"run/{self.run_id}/summary", summary)

    def send_heartbeat(self):
        return self.client.request("post", f"run/{self.run_id}/record")

    def send_run_record(self, histories: List[Dict] = None, systems: List[Dict] = None, logs: List[Dict] = None):
        kwargs = locals()
        return self.client.request("post", f"run/{self.run_id}/record", kwargs)

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

    def get_artifact(self, artifact_id):
        res = self.client.request_json("get", f"artifact/{artifact_id}")
        return res

    def create_artifact(
        self,
        name: str,
        version: Optional[str] = None,
        description: Optional[str] = None,
        group: Optional[str] = None,
        labels: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        project_only: bool = False,
    ):

        project_id = self.project_id
        run_id = self.run_id if not project_only else None

        params = dict(
            name=name,
            version=version,
            runId=run_id,
            description=description,
            group=group,
            labels=labels,
            metadata=metadata,
        )
        res = self.client.request_json("post", f"project/{project_id}/artifact", params=params)
        return res

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

    def list_artifact_files(self, artifact_id):
        return self.client.request_json("get", f"artifact/{artifact_id}/file")["files"]

    def detail_artifact_file(self, artifact_id, file_id):
        """
        Return artifact file detail
        """
        return self.client.request_json("get", f"artifact/{artifact_id}/file/{file_id}")

    def create_artifact_file(
        self,
        artifact_id,
        name,
        path,
        size,
        digest,
        version=None,
        ref=None,
        local_path=None,
        **kwargs,
    ):
        if ref:
            _type = "ref"
        else:
            _type = "remote"

        params = dict(
            type=_type,
            name=name,
            relativePath=path,
            size=size,
            digest=digest,
            version=version,
            ref=ref,
            localPath=local_path,
        )
        res = self.client.request_json("post", f"artifact/{artifact_id}/file", params=params)
        return res["Id"]

    def artifact_file_upload_url(self, artifact_id, file_id):
        res = self.client.request_json("get", f"artifact/{artifact_id}/file/{file_id}/upload-url")
        return res["url"], res["fields"]

    def artifact_file_download_url(self, artifact_id, file_id):
        res = self.client.request_json("get", f"artifact/{artifact_id}/file/{file_id}/download-url")
        return res["url"]

    def commit_artifact_file_uploaded(self, artifact_id, file_id):
        params = dict(
            status="READY",
        )
        return self.client.request_json("patch", f"artifact/{artifact_id}/file/{file_id}/status", params)

    def delete_artifact_file(self, artifact_id, name, version="latest"):
        """
        Return artifact manifest delete
        """
        # TODO: implement here
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
        import manta_lab as ml

        id = ml.util.generate_id()
        self.tune_repo[id] = config
        return id

    def register_agent(self, host, tune_id):
        return {"id": "register_agent_id"}

    def request_tune_schedule(self, agent_id, metric, run_states):
        return [
            {
                "type": "RUN",
                "run_id": "run_id",
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
            <entity>/<project>/<run>/<artifact>
        """
        entity = self._settings["entity"] or self.entity
        project = self._settings["project"]
        run = self._settings["run_name"]

        if path is None:
            return entity, project, run, None

        parts = path.split("/")
        if len(parts) == 1:
            return entity, project, run, path
        elif len(parts) == 2:
            return entity, parts[0], run, parts[1]
        elif len(parts) == 3:
            return parts[0], parts[1], run, parts[2]
        elif len(parts) == 4:
            return parts
        else:
            raise ValueError("Invalid artifact path: %s" % path)

    # get url functions
    def get_project_url(self, run_dict) -> str:
        if run_dict is None:
            return ""
        entity = urlquote(run_dict["entity"])
        project = urlquote(run_dict["project"])

        url = f"{self.app_url}/{entity}/{project}"
        return url

    def get_run_url(self, run_dict) -> str:
        if run_dict is None:
            return ""
        entity = urlquote(run_dict["entity"])
        project = urlquote(run_dict["project"])
        run_id = urlquote(run_dict["run_id"])

        url = f"{self.app_url}/{entity}/{project}/run/{run_id}"
        return url

    def get_tune_url(self, run_dict) -> str:
        return ""

    def get_run_name(sel, run_dict) -> str:
        return run_dict["run_name"]
