from datetime import date, datetime

import pytest
from radis.reports.api.serializers import ReportSerializer
from radis.reports.models import Group

from radis_client.client import ReportData


@pytest.mark.django_db
def test_report_data_valid():
    group = Group.objects.create(name="Thoraxklinik")

    report_data = ReportData(
        document_id="synapse_3dfidii5858-6633i4-ii398841",
        language="en",
        groups=[group.id],
        pacs_aet="synapse",
        pacs_name="Synapse",
        patient_id="1234578",
        patient_birth_date=date(1976, 5, 23),
        patient_sex="M",
        study_description="CT of the Thorax",
        study_datetime=datetime(2000, 8, 10, 11, 37),
        modalities=["CT", "PET"],
        links=["http://synapse.net/34343-34343-34343"],
        metadata={
            "study_instance_uid": "34343-34343-34343",
            "accession_number": "345348389",
            "series_instance_uid": "34343-676556-3343",
            "sop_instance_uid": "35858-384834-3843",
        },
        body="This is the report",
    )

    report = ReportSerializer(data=report_data.to_dict())

    assert report.is_valid()
