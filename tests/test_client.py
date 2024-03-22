import pytest
from pytest_mock import MockerFixture
from radis.reports.api.serializers import ReportSerializer

from radis_client.client import RadisClient


@pytest.mark.django_db
def test_report_data_valid(report_data):
    report = ReportSerializer(data=report_data.to_dict())

    assert report.is_valid()


@pytest.mark.django_db
def test_report_data_post(
    live_server,
    mocker: MockerFixture,
    admin_with_group_and_token,
    report_data,
):
    # Make sure it won't try to save created reports to any full text search database
    # as those are not available during test
    mocker.patch("radis.reports.api.viewsets.reports_created_handlers", return_value=[])

    _, _, token = admin_with_group_and_token

    client = RadisClient(live_server, token)
    response = client.create_report(report_data)

    assert response
