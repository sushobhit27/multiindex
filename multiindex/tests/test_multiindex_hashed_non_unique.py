import pytest
from ..multiindex import MultiIndexContainer
from ..indexed_by import OrderedUnique, HashedNonUnique


class Potus(object):
    def __init__(self,first_name, last_name, assumed_ofc_at):
        self.first_name = first_name
        self.last_name = last_name
        self.assumed_ofc_at = assumed_ofc_at

    def __str__(self):
        return '{} {}, {}'.format(self.first_name, self.last_name, self.assumed_ofc_at)


@pytest.fixture(scope='session')
def emp_seq():
    seq = [Potus('George', 'Washington', 57),
           Potus('Thomas', 'Jefferson', 58),
           Potus('Theodore', 'Roosevelt', 43),
           Potus('George', 'Bush', 55),
           Potus('Barack', 'Obama', 48),
           Potus('Franklin', 'Roosevelt', 51),
           ]
    return seq


@pytest.fixture(scope='session')
def mi(emp_seq):
    mi = MultiIndexContainer(HashedNonUnique('first_name'),
                             HashedNonUnique('last_name'),
                             HashedNonUnique('assumed_ofc_at')
                             )

    for emp in emp_seq:
        mi.insert(emp)
    return mi


def test_insert(mi, emp_seq):
    assert [emp_seq[4]] == mi.get('first_name', 'Barack')
    assert [emp_seq[2]] == mi.get('assumed_ofc_at', 43)
    assert None is mi.get('assumed_ofc_at', 0)
    assert None is mi.get('assumed_ofc_at', 786)
    assert [emp_seq[3]] == mi.get('last_name', 'Bush')
    assert [emp_seq[5]] == mi.get('first_name', 'Franklin')
    assert [emp_seq[1]] == mi.get('first_name', 'Thomas')

    for potus in mi.get('first_name', 'George'):
        assert potus in [emp_seq[3], emp_seq[0]]


def test_modify(mi):
    print(mi.get('assumed_ofc_at', 48))
    mi.modify('last_name', 'Obama', 'Hussain')
    print(mi.get('first_name', 'Thomas'))
    print(mi.get('assumed_ofc_at', 48))
    print(mi.get('first_name', 'George'))
    assert mi.get('assumed_ofc_at', 48)[0].last_name == 'Hussain'
#
#
def test_remove(mi):
    mi.remove('first_name', 'George')
    # print(mi.get('assumed_ofc_at', 786))
    assert len(mi.get('first_name', 'George')) == 1