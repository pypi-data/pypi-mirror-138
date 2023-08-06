from .BaseQuery import BaseQuery
from .Component import LimitOffset
from ..Builder import BaseBuilder, InsertBuilder
from ..Structure import Table, Value
from typing import Iterable

class Insert(BaseQuery, LimitOffset) :
    """INSERT query manipulation class.
    Components:
    - Table
    - Insert values
    - Limit query
    """

    def __init__(self, translator: int, bindingOption: int) :
        BaseQuery.__init__(self)
        self.builder = InsertBuilder()
        self.builder.builderType(BaseBuilder.INSERT)
        self.translator = translator
        self.bindingOption = bindingOption
        LimitOffset.__init__(self)

    def insert(self, table) :
        """INSERT INTO query query table input"""
        if table :
            tableObject = Table.create(table)
            self.builder.setTable(tableObject)
        else :
            raise Exception("Table name is not defined")
        return self

    def values(self, values) :
        """Add value and column pair list to builder object.
        
        Takes a dictionary with keys as column or list of two list with first item as column.
        """
        valueObject = Value.create(values)
        self.builder.addValue(valueObject)
        return self

    def multiValues(self, multiValues) :
        """Add multiple value and column pair list to builder object.
        
        Takes list of dictionary with keys as column.
        """
        valuesObjects = ()
        if isinstance(multiValues, Iterable) :
            for val in multiValues :
                valuesObjects += (Value.create(val),)
        for val in valuesObjects :
            self.builder.addValue(val)
        return self
