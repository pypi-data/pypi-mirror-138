import pytest

from typing import Dict, List

from relevanceai import Client

from tests.globals.constants import generate_dataset_id


@pytest.fixture(scope="session")
def pandas_dataset(
    test_client: Client,
    pandas_documents: List[Dict],
):
    test_dataset_id = generate_dataset_id()

    response = test_client._insert_documents(test_dataset_id, pandas_documents)

    yield response, len(pandas_documents)

    test_client.datasets.delete(test_dataset_id)
