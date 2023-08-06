from zcrmsdk.src.com.zoho.crm.api.notes import *
from zcrmsdk.src.com.zoho.crm.api.notes.note import Note
from zcrmsdk.src.com.zoho.crm.api.record import Record
from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs
from typing import Any

from ..client import ApiClient


class Create(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, log_path: str = "ZOHO_LOG_PATH", store_path: str = "ZOHO_STORE_PATH",
            resource_path: str = "ZOHO_RESOURCE_PATH", email: str = "ZOHO_USER_ID", env: str = "ZOHO_DATA_CENTER",
            client_id: str = "ZOHO_CLIENT_ID", client_secret: str = "ZOHO_CLIENT_SECRET",
            refresh_token: str = "ZOHO_REFRESH_TOKEN", body: dict = None):
        if log_path is None:
            raise ValueError("A log path must be provided.")

        if store_path is None:
            raise ValueError("A store path must be provided.")

        if resource_path is None:
            raise ValueError("A resource path must be provided.")

        if email is None:
            raise ValueError("An email must be provided.")

        if client_id is None:
            raise ValueError("A client id must be provided.")

        if client_secret is None:
            raise ValueError("A client secret must be provided")

        if refresh_token is None:
            raise ValueError("A refresh token must be provided")

        if body is None:
            raise ValueError("An object must be provided")

        if "data" not in body or not isinstance(body.get("data"), list):
            raise ValueError("An object must be provided")

        try:
            api_client = ApiClient(log_path, store_path, resource_path, email, env, client_id, client_secret,
                                   refresh_token)

            request = BodyWrapper()

            notes = []

            for elem in body.get("data"):
                note = Note()
                note.set_note_title(elem.get('title', ''))
                note.set_note_content(elem.get('content', ''))
                parent_record = Record()
                parent_record.set_id(elem.get('id', None))
                note.set_parent_id(parent_record)
                note.set_se_module(elem.get('module', None))
                notes.append(note)

            request.set_data(notes)

            response = NotesOperations().create_notes(request=request)
            return response
        except Exception as error:
            print(error)
            raise error


class List(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, log_path: str = "ZOHO_LOG_PATH", store_path: str = "ZOHO_STORE_PATH",
            resource_path: str = "ZOHO_RESOURCE_PATH", email: str = "ZOHO_USER_ID", env: str = "ZOHO_DATA_CENTER",
            client_id: str = "ZOHO_CLIENT_ID", client_secret: str = "ZOHO_CLIENT_SECRET",
            refresh_token: str = "ZOHO_REFRESH_TOKEN", headers_map: dict = None,
            params_map: dict = None):
        if log_path is None:
            raise ValueError("A log path must be provided.")

        if store_path is None:
            raise ValueError("A store path must be provided.")

        if resource_path is None:
            raise ValueError("A resource path must be provided.")

        if email is None:
            raise ValueError("An email must be provided.")

        if client_id is None:
            raise ValueError("A client id must be provided.")

        if client_secret is None:
            raise ValueError("A client secret must be provided")

        if refresh_token is None:
            raise ValueError("A refresh token must be provided")

        if headers_map is None:
            headers_map = {}

        if params_map is None:
            params_map = {}

        try:
            api_client = ApiClient(log_path, store_path, resource_path, email, env, client_id, client_secret,
                                   refresh_token)

            headers = HeaderMap()
            for key in headers_map:
                headers.add(getattr(GetNotesHeader, key), headers_map.get(key))

            """TODO: Should accept a list of ids"""
            params = ParameterMap()
            for key in params_map:
                params.add(getattr(GetNotesParam, key), params_map.get(key))

            response = NotesOperations().get_notes(param_instance=params, header_instance=headers)
            return response
        except Exception as error:
            print(error)
            raise error


class Fetch(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, log_path: str = "ZOHO_LOG_PATH", store_path: str = "ZOHO_STORE_PATH",
            resource_path: str = "ZOHO_RESOURCE_PATH", email: str = "ZOHO_USER_ID", env: str = "ZOHO_DATA_CENTER",
            client_id: str = "ZOHO_CLIENT_ID", client_secret: str = "ZOHO_CLIENT_SECRET",
            refresh_token: str = "ZOHO_REFRESH_TOKEN", note_id: int = None, headers_map: dict = None,
            params_map: dict = None):
        if log_path is None:
            raise ValueError("A log path must be provided.")

        if store_path is None:
            raise ValueError("A store path must be provided.")

        if resource_path is None:
            raise ValueError("A resource path must be provided.")

        if email is None:
            raise ValueError("An email must be provided.")

        if client_id is None:
            raise ValueError("A client id must be provided.")

        if client_secret is None:
            raise ValueError("A client secret must be provided")

        if refresh_token is None:
            raise ValueError("A refresh token must be provided")

        if note_id is None:
            raise ValueError("A note ID must be provided")

        if headers_map is None:
            headers_map = {}

        if params_map is None:
            params_map = {}

        try:
            api_client = ApiClient(log_path, store_path, resource_path, email, env, client_id, client_secret,
                                   refresh_token)

            headers = HeaderMap()
            for key in headers_map:
                headers.add(getattr(GetNoteHeader, key), headers_map.get(key))

            params = ParameterMap()
            for key in params_map:
                params.add(getattr(GetNoteParam, key), params_map.get(key))

            response = NotesOperations().get_note(id=note_id, param_instance=params, header_instance=headers)
            return response
        except Exception as error:
            print(error)
            raise error


class Update(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, log_path: str = "ZOHO_LOG_PATH", store_path: str = "ZOHO_STORE_PATH",
            resource_path: str = "ZOHO_RESOURCE_PATH", email: str = "ZOHO_USER_ID", env: str = "ZOHO_DATA_CENTER",
            client_id: str = "ZOHO_CLIENT_ID", client_secret: str = "ZOHO_CLIENT_SECRET",
            refresh_token: str = "ZOHO_REFRESH_TOKEN", body: dict = None, headers_map: dict = None):
        if log_path is None:
            raise ValueError("A log path must be provided.")

        if store_path is None:
            raise ValueError("A store path must be provided.")

        if resource_path is None:
            raise ValueError("A resource path must be provided.")

        if email is None:
            raise ValueError("An email must be provided.")

        if client_id is None:
            raise ValueError("A client id must be provided.")

        if client_secret is None:
            raise ValueError("A client secret must be provided")

        if refresh_token is None:
            raise ValueError("A refresh token must be provided")

        if body is None:
            raise ValueError("An object must be provided")

        if "data" not in body or not isinstance(body.get("data"), list):
            raise ValueError("An object must be provided")

        try:
            api_client = ApiClient(log_path, store_path, resource_path, email, env, client_id, client_secret,
                                   refresh_token)

            request = BodyWrapper()

            notes = []

            for elem in body.get("data"):
                note = Note()
                note.set_id(elem.get("id"))
                elem.pop("id")
                note.set_note_title(elem.get('title', ''))
                note.set_note_content(elem.get('content', ''))
                parent_record = Record()
                parent_record.set_id(elem.get('id', None))
                note.set_parent_id(parent_record)
                note.set_se_module(elem.get('module', None))
                notes.append(note)

            request.set_data(notes)

            response = NotesOperations().update_notes(request=request)
            return response
        except Exception as error:
            print(error)
            raise error


class Delete(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, log_path: str = "ZOHO_LOG_PATH", store_path: str = "ZOHO_STORE_PATH",
            resource_path: str = "ZOHO_RESOURCE_PATH", email: str = "ZOHO_USER_ID", env: str = "ZOHO_DATA_CENTER",
            client_id: str = "ZOHO_CLIENT_ID", client_secret: str = "ZOHO_CLIENT_SECRET",
            refresh_token: str = "ZOHO_REFRESH_TOKEN", module_name: str = None, record_ids: list = None,
            params_map: dict = None, headers_map: dict = None):
        if log_path is None:
            raise ValueError("A log path must be provided.")

        if store_path is None:
            raise ValueError("A store path must be provided.")

        if resource_path is None:
            raise ValueError("A resource path must be provided.")

        if email is None:
            raise ValueError("An email must be provided.")

        if client_id is None:
            raise ValueError("A client id must be provided.")

        if client_secret is None:
            raise ValueError("A client secret must be provided")

        if refresh_token is None:
            raise ValueError("A refresh token must be provided")

        if module_name is None:
            raise ValueError("A module name must be provided")

        if record_ids is None or not isinstance(record_ids, list):
            raise ValueError("A list of record IDs must be provided")

        try:
            api_client = ApiClient(log_path, store_path, resource_path, email, env, client_id, client_secret,
                                   refresh_token)

            params = ParameterMap()
            for record_id in record_ids:
                params.add(DeleteNotesParam.ids, record_id)

            response = NotesOperations().delete_notes(param_instance=params)
            return response
        except Exception as error:
            print(error)
            raise error