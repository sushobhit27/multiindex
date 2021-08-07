import pytest
from ..multiindex import MultiIndexContainer
from ..indexed_by import OrderedUnique


class Employee(object):
    def __init__(self,first_name, last_name, emp_id):
        self.first_name = first_name
        self.last_name = last_name
        self.emp_id = emp_id

    def __str__(self):
        return '{} {}, {}'.format(self.first_name, self.last_name, self.emp_id)


@pytest.fixture(scope='session')
def emp_seq():
    seq = [Employee('Steve', 'Austin', 786),
           Employee('Bret', 'Hart', 345),
           Employee('Razor', 'Ramon', 8732),
           Employee('Shawn', 'Michaels', 1234)]
    return seq


@pytest.fixture(scope='session')
def mi(emp_seq):
    mi = MultiIndexContainer(OrderedUnique('first_name'),
                             OrderedUnique('last_name'),
                             OrderedUnique('emp_id')
                             )

    for emp in emp_seq:
        mi.insert(emp)
    return mi


def test_insert(mi, emp_seq):
    assert emp_seq[3] == mi.get('first_name', 'Shawn')
    assert emp_seq[0] == mi.get('emp_id', 786)
    assert mi.get('emp_id', 321) is None
    assert emp_seq[0] == mi.get('first_name', 'Steve')
    assert emp_seq[1] == mi.get('last_name', 'Hart')
    assert emp_seq[2] == mi.get('last_name', 'Ramon')


def test_insert_overwrite(mi, emp_seq):
    assert emp_seq[3] == mi.get('first_name', 'Shawn')
    assert emp_seq[0] == mi.get('emp_id', 786)
    assert mi.get('emp_id', 321) is None
    assert emp_seq[0] == mi.get('first_name', 'Steve')
    assert emp_seq[1] == mi.get('last_name', 'Hart')
    assert emp_seq[2] == mi.get('last_name', 'Ramon')
    mi.insert(Employee('Steve', 'Austin', 123), overwrite=True)
    assert mi.get('first_name', 'Steve').emp_id == 123
    mi.insert(Employee('Razor', 'Topaz', 8732), overwrite=True)
    assert mi.get('emp_id', 8732).last_name == 'Topaz'
    assert mi.get('first_name', 'Razor').emp_id == 8732
    mi.insert(emp_seq[0], overwrite=True)


def test_modify(mi):
    mi.modify('emp_id', 786, 666)
    assert mi.get('emp_id', 666).first_name == 'Steve'
    assert mi.get('emp_id', 666).last_name == 'Austin'
    assert mi.get('first_name', 'Steve').emp_id == 666
    assert mi.get('last_name', 'Austin').emp_id == 666


def test_remove(mi):
    mi.remove('emp_id', 666)
    assert mi.get('emp_id', 666) is None


def test_get_by(mi):
    assert mi.get_by_emp_id(1234).first_name == 'Shawn'
    assert mi.get_by_first_name('Shawn').emp_id == 1234
    assert mi.get_by_last_name('Hart').first_name == 'Bret'