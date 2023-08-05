import pytest

from typing import List, Dict

from relevanceai import Client

from tests.globals.constants import generate_dataset_id


@pytest.fixture(scope="session")
def assorted_nested_dataset_id(
    test_client: Client, assorted_nested_documents: List[Dict]
):
    test_dataset_id = generate_dataset_id()

    test_client._insert_documents(test_dataset_id, assorted_nested_documents)

    yield test_dataset_id

    test_client.datasets.delete(test_dataset_id)
