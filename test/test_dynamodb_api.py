import os
import sys

# resolves import conflicts between modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/src')))
import pytest
import json
import logging
import dynamodb_api as db


@pytest.fixture
def prepare_db():
    """
    Anything before yield executed before the test
    Anything after yield executed after the test
    """
    logging.info("Create table and load data")
    db.create_rules_table("TestRules")
    with open("test/mock_data/rules.json", 'rb') as f:
        fake_rules = json.load(f)
    db.load_rules(fake_rules, "TestRules")
    yield
    logging.info("Delete table")
    db.delete_table("TestRules")


@pytest.fixture
def clean_db():
    """
    Anything before yield executed before the test
    Anything after yield executed after the test
    """
    yield
    logging.info("Delete table")
    db.delete_table("TestRules")


def test_create_table(clean_db):
    table = "TestRules"
    db.create_rules_table(table)
    assert table in db.list_tables()


def test_delete_table():
    table = "TestRules"
    db.create_rules_table(table)
    db.delete_table(table)
    assert table not in db.list_tables()


def test_list_tables():
    assert type(db.list_tables()) == list


def test_get_rules(prepare_db):
    table = "TestRules"
    rules = db.get_rules(rule_id=1, table=table)
    with open("test/mock_data/rules.json", 'r') as f:
        expected_rules = json.load(f)[0]

    assert rules["RuleId"] == 1
    assert expected_rules == rules

