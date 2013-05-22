#!/usr/bin/python
""" Provide the NTList class, which combines namedtuples & ifilter """
import itertools
import collections


class NTList(object):
    """ Provide a convenient interface to a list of namedtuples """
    rows = None
    row_class = None
    column_types = None
    column_type_map = None

    def __init__(self, *column_names, **kwargs):
        """ Initialize an ntlist object with the given column names """
        self.rows = list()
        self.row_class = collections.namedtuple("ntl_{}".format(id(self)),
                                                column_names)
        if 'types' in kwargs:
            self.column_types = kwargs['types']
            self.column_type_map = dict(zip(column_names, self.column_types))

    def insert_generator(self, source_generator, direct=False):
        """ Replace the internal row list with a generator function """

        if direct:
            self.rows = source_generator

        def regenerator(input_generator):
            """ Yield a named tuple based from the input_generator """
            for row in input_generator:
                yield self.row_class(*row)

        def typed_regenerator(input_generator):
            """
            Yield a named tuple with values "cast" to the types in
            self.column_types
            """
            for row in input_generator:
                yield self.row_class(*[column_type(column_value)
                                       for column_type, column_value
                                       in zip(self.column_types, row)])

        if self.column_types is None:
            self.rows = regenerator(source_generator)
        else:
            self.rows = typed_regenerator(source_generator)

    def insert(self, new_row):
        """ Insert a namedtuple with the values given in the list new_row """
        if self.column_types is not None:
            new_row = [column_type(column_value)
                       for column_type, column_value
                       in zip(self.column_types, new_row)]
        self.rows.append(self.row_class(*new_row))        

    def update(self, change_dict, predicate):
        """
        Update rows that match the predicate using x.k = v from the
        change_dict
        """
        if self.column_types is not None:
            for key, value in change_dict.items():
                change_dict[key] = self.column_type_map[key](value)

        for idx, row in enumerate(self.rows):
            if predicate(row):
                new_row_dict = row._asdict()
                for key, value in change_dict.items():
                    new_row_dict[key] = value
                self.rows[idx] = self.row_class(**new_row_dict)


    def select(self, predicate=None, order_by=None, reverse=False,
               get_dicts=False):
        """ Return a copy of rows matching predicate """
        if get_dicts:
            result = itertools.imap(lambda row: row._asdict(),
                                    itertools.ifilter(predicate, self.rows))
        else:
            result = itertools.ifilter(predicate, self.rows)

        if order_by is not None:
            return sorted(result, key=order_by, reverse=reverse)

        return result

    def delete(self, predicate=None):
        """ Delete rows matching the predicate """
        self.rows = itertools.ifilterfalse(predicate, self.rows)

