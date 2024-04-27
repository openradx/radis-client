from datetime import date, datetime

import pytest
from adit_radis_shared.accounts.models import User
from adit_radis_shared.common.utils.auth_utils import add_user_to_group
from adit_radis_shared.token_authentication.models import Token
from radis.reports.models import Group

from radis_client.client import ReportData


@pytest.fixture
def admin_with_group_and_token():
    user: User = User.objects.create_superuser("admin")
    group = Group.objects.create(name="Staff")
    add_user_to_group(user, group)
    _, token = Token.objects.create_token(user, "", None)
    return user, group, token


@pytest.fixture
def report_data():
    group = Group.objects.create(name="Thoraxklinik")

    return ReportData(
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
