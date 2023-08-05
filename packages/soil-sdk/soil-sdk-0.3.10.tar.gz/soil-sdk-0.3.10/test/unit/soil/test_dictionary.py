# pylint: disable=missing-docstring,no-self-use,line-too-long

from typing import Any, Dict, Optional
import unittest
from unittest.mock import MagicMock, patch
from json import loads, dumps
from soil.dictionary import dictionary


TEST_DICT = {
    "_id": '609bdfe9f5e2c907fa353bca99',
    "content": {
      "a": 'b'
    },
    "created_at": 1620828137994,
    "language": 'es',
    "name": 'testdicaaddt'
}

TEST_CONTENT = {"a": "b"}


class MockResponse:  # pylint: disable=too-few-public-methods
    def __init__(self, text: str, status_code: int):
        self.text = text
        self.status_code = status_code

    # def text(self):
    #     return self._text


def mocked_requests_get(
        url: str,
        headers: Optional[Dict[str, str]] = None,
) -> MockResponse:
    # pylint: disable=unused-argument
    name, language = url.split('/')[-1].split('+')
    name = name.split("?")[0]
    if name == 'testdicaaddt' and language == 'ca':
        return MockResponse(dumps(TEST_DICT), 200)
    if name == 'testdicaaddt' and language == 'en':
        return MockResponse(dumps(TEST_DICT), 200)
    return MockResponse("Not found", 404)


def mocked_requests_post(*args: Any, **kwargs: Any) -> MockResponse:
    # pylint: disable=unused-argument
    data = loads(kwargs['data'])
    name = data['name']
    language = data['language']

    if name == 'testdicaaddt' and language == 'ca':
        return MockResponse(dumps({"status": "created"}), 200)
    if name == 'testdicaaddt' and language == 'en':
        response = {"message": "Dictionary " + name + " already exists in language " + language}
        return MockResponse(dumps(response), 400)
    return MockResponse(dumps({}), 404)


# Our test case class
class TestDictionary(unittest.TestCase):
    @patch('soil.api.requests.get', side_effect=mocked_requests_get)
    def test_get_dictionary(self, mock_get: MagicMock) -> None:

        response = dictionary('testdicaaddt', 'ca')
        self.assertEqual(response, TEST_DICT)
        response = dictionary('testdicaaddt', 'en')
        self.assertEqual(response, TEST_DICT)

        self.assertEqual(len(mock_get.call_args_list), 2)

    # TO DO: Test create new dict.
    @patch('soil.api.requests.post', side_effect=mocked_requests_post)
    def test_create_dictionary(self, mock_post: MagicMock) -> None:

        response = dictionary('testdicaaddt', 'ca', TEST_CONTENT)
        self.assertEqual(response, {"status": "created"})

        response = dictionary('testdicaaddt', 'en', TEST_CONTENT)
        self.assertEqual(response, {"status": 'Dictionary testdicaaddt already exists in language en'})

        self.assertEqual(len(mock_post.call_args_list), 2)
