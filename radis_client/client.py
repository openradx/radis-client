from datetime import date, datetime
from typing import Literal, TypedDict

import requests


class ReportData(TypedDict):
    document_id: str
    groups: list[int]
    pacs_aet: str
    pacs_name: str
    patient_id: str
    patient_birth_date: date
    patient_sex: Literal["F", "M", "U"]
    study_instance_uid: str
    accession_number: str
    study_description: str
    study_datetime: datetime
    series_instance_uid: str
    modalities_in_study: list[str]
    sop_instance_uid: str
    references: list[str]
    body: str


class RadisClient:
    def __init__(self, server_url: str, auth_token: str):
        self.server_url = server_url
        self.auth_token = auth_token

        self._reports_url = f"{self.server_url}/api/reports/"
        self._headers = {"Authorization": f"Token {self.auth_token}"}

    def add_report(self, data: ReportData) -> requests.Response:
        response = requests.post(self._reports_url, json=data, headers=self._headers)
        response.raise_for_status()
        return response

    def retrieve_report(self, document_id: str, full: bool = False) -> requests.Response:
        response = requests.get(
            f"{self._reports_url}{document_id}/",
            headers=self._headers,
            params={"full": full},
        )
        response.raise_for_status()
        return response

    def update_report(self, document_id: str, data: dict) -> requests.Response:
        response = requests.put(
            f"{self._reports_url}{document_id}/", json=data, headers=self._headers
        )
        response.raise_for_status()
        return response

    def delete_report(self, document_id: str) -> requests.Response:
        response = requests.delete(f"{self._reports_url}{document_id}/", headers=self._headers)
        response.raise_for_status()
        return response
