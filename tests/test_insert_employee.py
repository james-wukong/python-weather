import pytest
import src.database.mysql_crud as mysql_crud

def test_insert_employee():
    mysql_crud.insert_employee()

    assert 1 == 1

