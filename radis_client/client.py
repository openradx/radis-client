from datetime import date, datetime
from typing import Any, Literal, TypedDict

import requests


class ReportData(TypedDict):
    document_id: str
    language: str
    groups: list[int]
    pacs_aet: str
    pacs_name: str
    patient_id: str
    patient_birth_date: date
    patient_sex: Literal["M", "F", "O"]
    study_instance_uid: str
    accession_number: str
    study_description: str
    study_datetime: datetime
    series_instance_uid: str
    modalities_in_study: list[str]
    sop_instance_uid: str
    links: list[str]
    body: str


def _sanitize_data(data: ReportData) -> dict[str, Any]:
    sanitized_data = {**data}
    if isinstance(sanitized_data["patient_birth_date"], date):
        sanitized_data["patient_birth_date"] = sanitized_data["patient_birth_date"].isoformat()
    if isinstance(sanitized_data["study_datetime"], datetime):
        sanitized_data["study_datetime"] = sanitized_data["study_datetime"].isoformat()
    return sanitized_data


class RadisClient:
    def __init__(self, server_url: str, auth_token: str):
        self.server_url = server_url
        self.auth_token = auth_token

        self._reports_url = f"{self.server_url}/api/reports/"
        self._headers = {"Authorization": f"Token {self.auth_token}"}

    def create_report(self, data: ReportData) -> dict[str, Any]:
        """
        Create a report using the provided data and return the response as a dictionary.

        Args:
            data (ReportData): The data to be used for creating the report.

        Returns:
            dict[str, Any]: The response from the report creation request.
        """
        response = requests.post(
            self._reports_url, json=_sanitize_data(data), headers=self._headers
        )
        response.raise_for_status()
        return response.json()

    def retrieve_report(self, document_id: str, full: bool = False) -> dict[str, Any]:
        """
        Retrieve a report with the given document ID.

        Args:
            document_id (str): The ID of the document to retrieve.
            full (bool, optional): Whether to retrieve also document data from Vespa.
                Defaults to False.

        Returns:
            dict[str, Any]: The retrieved report in dictionary format.
        """
        response = requests.get(
            f"{self._reports_url}{document_id}/",
            headers=self._headers,
            params={"full": full},
        )
        response.raise_for_status()
        return response.json()

    def update_report(self, document_id: str, data: ReportData, upsert=False) -> dict[str, Any]:
        """
        Update a report with the given document ID and report data.
        Partial updates are not supported.

        Args:
            document_id (str): The ID of the document to be updated.
            data (ReportData): The report data to be updated.
            upsert (bool): Whether to perform an upsert if the document is not found.

        Returns:
            dict[str, Any]: The response as JSON.
        """
        response = requests.put(
            f"{self._reports_url}{document_id}/",
            json=_sanitize_data(data),
            headers=self._headers,
            params={"upsert": upsert},
        )
        response.raise_for_status()
        return response.json()

    def delete_report(self, document_id: str) -> None:
        """
        Deletes a report with the given document_id.

        Args:
            document_id (str): The ID of the document to be deleted.

        Returns:
            None
        """
        response = requests.delete(f"{self._reports_url}{document_id}/", headers=self._headers)
        response.raise_for_status()
