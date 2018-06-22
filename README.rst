==========
Multiindex
==========

Multiindex is a container created along the lines of C++ boost::multi_index. Although similar but many
aspects/interfaces in this container will be different from boost's version.

The basic premise for having multi_index container is to have access to the object based on its different properties,
just like accessing a row from a SQL table based on different column value.

.. code-block:: python

    import multiindex as mi

    class Employee(object):
        def __init__(self, emp_id, name, contact_number, department):
            self.emp_id = emp_id
            self.name = name
            self.contact_number = contact_number
            self.department = department

        def __str__(self):
            return '{},{},{},{}'.format(self.emp_id, self.name, self.contact_number, self.department)


    emp_container = mi.MultiIndexContainer(mi.HashedUnique('emp_id'),
                                           mi.HashedNonUnique('name'),
                                           mi.HashedUnique('contact_number'),
                                           mi.HashedNonUnique('department'))

    emp_container.insert(Employee(1234, 'Bret Hart', 5678, 'HR'))
    emp_container.insert(Employee(1235, 'Steve Austin', 3343431, 'Sales'))
    emp_container.insert(Employee(1236, 'Hulk Hogan', 892784, 'Marketing'))
    emp_container.insert(Employee(1237, 'Triple H', 937261, 'HR'))

    print(emp_container.get('emp_id', 1235))
    print(emp_container.get('contact_number', 937261))
    for emp in emp_container.get('department', 'HR'):
        print(emp)


Above will generate following output:

.. code-block::

    1235,Steve Austin,3343431,Sales
    1237,Triple H,937261,HR
    1234,Bret Hart,5678,HR
    1237,Triple H,937261,HR


------------------------
Installation
------------------------
Currently this package can be installed using setup.py only.

.. code-block::

  python setup.py install

------------------------
TODO
------------------------
- [] Make package pip installable.
- [] Ordered index is based on OrderedDict, therefore order indexes based on the insertion order which is not quite 
     useful and is not same as boost::ordered_unique/ ordered_non_unique. To have similar behaviour, SortedDict 
     will be required, which can be used from sortedcontainers package.

