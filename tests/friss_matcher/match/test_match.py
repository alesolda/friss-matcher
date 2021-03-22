"""Test match main login.

This module exercises the ".match" method in Person model.
"""
import pytest

import datetime as dt

from friss_matcher.match.models import Person


@pytest.mark.parametrize("p1, p2, result", (
    ({"bsn": 1}, {"bsn": 1}, 100),
    ({"bsn": 0}, {"bsn": 1}, 0),
    ({"last_name": "lname"}, {"last_name": "lname"}, 40),
    ({"first_name": "fname"}, {"first_name": "fname"}, 20),
    ({"birth_date": dt.date(1900, 1, 1)}, {"birth_date": dt.date(1900, 1, 1)}, 40),
    ({"birth_date": dt.date(2000, 1, 1)}, {"birth_date": dt.date(1900, 1, 1)}, 0),
))
def test_match_individual_rules(p1, p2, result):
    """Test taking in account each rule separately."""
    p1 = Person(**p1)
    p2 = Person(**p2)
    assert p1.match(p2) == result


@pytest.mark.parametrize("p1, p2", (
    (
        {"first_name": "a", "last_name": "b", "birth_date": dt.date(1900, 1, 1)},
        {"first_name": "a", "last_name": "b", "birth_date": dt.date(1900, 1, 1)},
    ),
    (
        {"first_name": "a", "last_name": "b", "birth_date": dt.date(1900, 1, 1), "bsn": 1},
        {"first_name": "a", "last_name": "b", "birth_date": dt.date(1900, 1, 1)},
    ),
    (
        {"first_name": "a", "last_name": "b", "birth_date": dt.date(1900, 1, 1)},
        {"first_name": "a", "last_name": "b", "birth_date": dt.date(1900, 1, 1), "bsn": 1},
    ),

))
def test_match_100(p1, p2):
    """Test a score of 100 without matching the BSNs."""
    p1 = Person(**p1)
    p2 = Person(**p2)
    assert p1.match(p2) == 100


@pytest.mark.parametrize("p1, p2", (
    (
        {"last_name": "b", "birth_date": dt.date(1900, 1, 1)},
        {"last_name": "b", "birth_date": dt.date(1900, 1, 1)},
    ),
    (
        {"last_name": "b", "birth_date": dt.date(1900, 1, 1)},
        {"last_name": "b", "birth_date": dt.date(1900, 1, 1), "bsn": 1},
    ),
    (
        {"first_name": "a", "last_name": "b", "birth_date": dt.date(1900, 1, 1)},
        {"last_name": "b", "birth_date": dt.date(1900, 1, 1)},
    ),
    (
        {"first_name": "a", "last_name": "b", "birth_date": dt.date(1900, 1, 1)},
        {"first_name": "b", "last_name": "b", "birth_date": dt.date(1900, 1, 1)},
    ),
))
def test_match_80(p1, p2):
    """Test a score of 80.

    If the last name is the same +40%
    If the date of birth matches + 40%
    """
    p1 = Person(**p1)
    p2 = Person(**p2)
    assert p1.match(p2) == 80


@pytest.mark.parametrize("p1, p2", (
    (
        {"first_name": "a", "last_name": "b"},
        {"first_name": "a", "last_name": "b",},
    ),
    (
        {"first_name": "a", "last_name": "b", "birth_date": dt.date(1900, 1, 1)},
        {"first_name": "a", "last_name": "b"},
    ),
    (
        {"first_name": "a", "last_name": "b"},
        {"first_name": "a", "last_name": "b", "birth_date": dt.date(1900, 1, 1)},
    ),
))
def test_match_60(p1, p2):
    """Test a score of 60.

    If the last name is the same +40%
    If the first name is the same +20%
    """
    p1 = Person(**p1)
    p2 = Person(**p2)
    assert p1.match(p2) == 60


@pytest.mark.parametrize("p1, p2, result", (
    (
        {"first_name": "Andrew", "last_name": "Craw", "birth_date": dt.date(1985, 2, 20)},
        {"first_name": "Andrew", "last_name": "Craw"},
        60
    ),
    (
        {"first_name": "Andrew", "last_name": "Craw", "birth_date": dt.date(1985, 2, 20)},
        {"first_name": "Petty", "last_name": "Smith", "birth_date": dt.date(1985, 2, 20)},
        40
    ),
    # (
    #     {"first_name": "Andrew", "last_name": "Craw", "birth_date":dt.date(1985, 2, 20)},
    #     {"first_name": "A.", "last_name": "Craw", "birth_date":dt.date(1985, 2, 20)},
    #     95
    # ),
    (
        {"first_name": "Andrew", "last_name": "Craw", "birth_date": dt.date(1985, 2, 20)},
        {"first_name": "Andrew", "last_name": "Craw", "birth_date": dt.date(1985, 2, 20)},
        100
    )))
def test_match_assigment_values(p1, p2, result):
    """Test match logic against dataset provided by the assigment."""
    p1 = Person(**p1)
    p2 = Person(**p2)
    assert p1.match(p2) == result
