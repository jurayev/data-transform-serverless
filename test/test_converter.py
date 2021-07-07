import os
import sys

# resolves import conflicts between modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/src')))

import pytest
import json
import converter
import mock_data.data as mock_data
from typing import List

@pytest.mark.parametrize('depth_level, expected_flatten',
                         [(3, [{'currency': 'EUR', 'value': '49.95'}, {'currency': 'DKK', 'value': '445.60'}]),
                          (0, [{"prices": {"price": [{"currency": "EUR", "value": "49.95"},
                                                     {"currency": "DKK", "value": "445.60"}]}}]),
                          (6, []),
                          (4, ['EUR', '49.95', 'DKK', '445.60']),
                          ])
def test_flatten_list(depth_level: int, expected_flatten: List[dict]):
    input_data = {"prices": {
        "price": [
            {
                "currency": "EUR",
                "value": "49.95"
            },
            {
                "currency": "DKK",
                "value": "445.60"
            }
        ]
    }
    }
    flatten = []\

    converter.flatten_list(input_data, depth_level, 0, flatten)
    assert flatten == expected_flatten


@pytest.mark.parametrize('depth_level, expected_flatten',
                         [(1, {'currency_1': 'EUR', 'value_1': '49.95', 'currency_2': 'DKK', 'value_2': '445.60'}),
                          (0, {"prices": [{"currency": "EUR", "value": "49.95"}, {"currency": "DKK", "value": "445.60"}]}),
                          (6, {}),
                          ])
def test_flatten_dict(depth_level: int, expected_flatten: dict):
    input_data = {
        "prices": [
            {
                "currency": "EUR",
                "value": "49.95"
            },
            {
                "currency": "DKK",
                "value": "445.60"
            }
        ]
    }
    flatten = {}
    converter.flatten_dict(input_data, depth_level, 0, flatten)
    assert flatten == expected_flatten


def test_convert():
    input_data = mock_data.RAW_DICT
    rules = mock_data.RULES
    actual_dict = converter.convert(input_data, rules)
    assert actual_dict == mock_data.FORMATTED_DICT


def test_xml_to_json():
    with open("test/mock_data/data.xml", 'rb') as f:
        data = f.read().decode('utf-8')
    rules = mock_data.RULES
    json_string = converter.xml_to_json(data, rules)
    json_string_formatted = json.dumps(mock_data.FORMATTED_DICT_TWO_PRODUCTS, indent=4)
    assert json_string == json_string_formatted
