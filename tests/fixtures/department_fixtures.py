import pytest
from tests.factories import department_factories


@pytest.fixture()
def department(db):
    department = department_factories.DepartmentFactory()
    db.session.commit()
    return department
