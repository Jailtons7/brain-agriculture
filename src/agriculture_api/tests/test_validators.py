import os
import csv
import pytest
from typing import List

from django.core.validators import ValidationError
from src.agriculture_api.validators import (
    validate_cpf, validate_cnpj, validate_document, validate_areas
)


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


def load_fixture(filename):
    path = os.path.join(FIXTURES_DIR, filename)
    with open(path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return list(reader)


def load_documents(cpf_file, cnpj_file):
    """ Load CPFs and CNPJ given their respective file names """
    cpfs = load_fixture(cpf_file)
    cnpjs = load_fixture(cnpj_file)
    return cpfs + cnpjs


def load_cpf_cnpj(filename: str) -> List[str]:
    """ Load data from a csv file given a file name in 'fixtures' folder. """
    data = load_fixture(filename)
    return [row[0] for row in data]


def load_areas(filename: str) -> List[tuple[str, str, str]]:
    """ Load data from a csv file given a filename in 'fixtures' folder. """
    data = load_fixture(filename)
    return [(row[0], row[1], row[2]) for row in data]


@pytest.mark.parametrize("cpf", load_cpf_cnpj('valid_cpfs.csv'))
def test_valid_cpf(cpf):
    assert validate_cpf(cpf) == cpf


@pytest.mark.parametrize("cpf", load_cpf_cnpj('invalid_cpfs.csv'))
def test_invalid_cpf(cpf):
    with pytest.raises(ValidationError):
        validate_cnpj(cpf)


@pytest.mark.parametrize("areas", load_areas('valid_areas.csv'))
def test_valid_areas(areas):
    assert validate_areas(float(areas[0] or 0.0), float(areas[1] or 0.0), float(areas[2] or 0.0)) is None


@pytest.mark.parametrize("areas", load_areas('invalid_areas.csv'))
def test_invalid_areas(areas):
    with pytest.raises(ValidationError):
        validate_areas(float(areas[0] or 0.0), float(areas[1] or 0.0), float(areas[2] or 0.0))


@pytest.mark.parametrize("document", load_documents('valid_cnpjs.csv', 'valid_cpfs.csv'))
def test_valid_documents(document):
    try:
        document = document[0]
    except KeyError:
        document = ''

    assert validate_document(document) == document


@pytest.mark.parametrize("document", load_documents('invalid_cnpjs.csv', 'invalid_cpfs.csv'))
def test_invalid_documents(document):
    try:
        document = document[0]
    except IndexError:
        document = ''

    with pytest.raises(ValidationError):
        validate_document(document)
