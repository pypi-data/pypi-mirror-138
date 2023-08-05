from .Structure import Table, Column, Value, Clause, Order, Limit

class BaseBuilder :

    SELECT = 1
    INSERT = 2
    UPDATE = 3
    DELETE = 4
    SELECT_DISTINCT = 5
    SELECT_UNION = 6
    SELECT_INTERSECT = 7
    SELECT_MINUS = 8
    INSERT_COPY = 9

    def __init__(self) :
        self.__builderType = 0
        self.__table = None
        self.__columns = ()
        self.__values = ()

    def builderType(self, type: int = 0) -> int :
        if (type > 0 and type <= 9) :
            self.__builderType = type
        return self.__builderType

    def getTable(self) -> Table :
        return self.__table

    def setTable(self, table: Table) :
        self.__table = table

    def getColumns(self) -> tuple :
        return self.__columns

    def countColumns(self) -> int :
        return len(self.__columns)

    def addColumn(self, column) :
        if isinstance(column, Column) :
            self.__columns = self.__columns + (column,)

    def getValues(self) -> tuple :
        return self.__values

    def countValues(self) -> int :
        return len(self.__values)

    def addValue(self, value : Value) :
        self.__values = self.__values + (value,)

class SelectBuilder(BaseBuilder) :

    def __init__(self) :
        BaseBuilder.__init__(self)
        self.__where = ()
        self.__having = ()
        self.__groupBy = ()
        self.__orderBy = ()
        self.__limit = None

    def getWhere(self) -> tuple:
        return self.__where

    def lastWhere(self) -> Clause :
        count = len(self.__where)
        if count > 0 :
            return self.__where[count-1]
        return None

    def countWhere(self) -> int :
        return len(self.__where)

    def addWhere(self, where: Clause) :
        self.__where += (where,)

    def editWhereNested(self, nestedLevel: int) :
        count = len(self.__where)
        if count > 0 :
            self.__where[count-1].nestedLevel(nestedLevel)

    def getHaving(self) -> tuple :
        return self.__having

    def lastHaving(self) -> Clause :
        count = len(self.__having)
        if count > 0 :
            return self.__having[count-1]
        return None

    def countHaving(self) -> int :
        return len(self.__having)

    def addHaving(self, having: Clause) :
        self.__having += (having,)

    def editHavingNested(self, nestedLevel: int) :
        count = len(self.__having)
        if count > 0 :
            self.__having[count-1].nestedLevel(nestedLevel)

    def getGroup(self) -> tuple :
        return self.__groupBy

    def countGroup(self) -> int :
        return len(self.__groupBy)

    def addGroup(self, groupBy: Column) :
        self.__groupBy = self.__groupBy + (groupBy,)

    def getOrder(self) -> tuple :
        return self.__orderBy

    def countOrder(self) -> int :
        return len(self.__orderBy)

    def addOrder(self, orderBy: Order) :
        self.__orderBy = self.__orderBy + (orderBy,)

    def getLimit(self) -> tuple :
        return self.__limit

    def hasLimit(self) -> bool :
        if self.__limit is None : return False
        else : return True

    def setLimit(self, limit: Limit) :
        self.__limit = limit

class InsertBuilder(BaseBuilder) :

    def __init__(self) :
        BaseBuilder.__init__(self)
        self.__limit = None

    def getLimit(self) -> tuple :
        return self.__limit

    def hasLimit(self) -> bool :
        if self.__limit is None : return False
        else : return True

    def setLimit(self, limit: Limit) :
        self.__limit = limit

class UpdateBuilder(BaseBuilder) :

    def __init__(self) :
        BaseBuilder.__init__(self)
        self.__where = ()
        self.__limit = None

    def getWhere(self) -> tuple:
        return self.__where

    def lastWhere(self) -> Clause :
        count = len(self.__where)
        if count > 0 :
            return self.__where[count-1]
        return None

    def countWhere(self) -> int :
        return len(self.__where)

    def addWhere(self, where: Clause) :
        self.__where += (where,)

    def editWhereNested(self, nestedLevel: int) :
        count = len(self.__where)
        if count > 0 :
            self.__where[count-1].nestedLevel(nestedLevel)

    def getLimit(self) -> tuple :
        return self.__limit

    def hasLimit(self) -> bool :
        if self.__limit is None : return False
        else : return True

    def setLimit(self, limit: Limit) :
        self.__limit = limit

class DeleteBuilder(BaseBuilder) :

    def __init__(self) :
        BaseBuilder.__init__(self)
        self.__where = ()
        self.__limit = None

    def getWhere(self) -> tuple:
        return self.__where

    def lastWhere(self) -> Clause :
        count = len(self.__where)
        if count > 0 :
            return self.__where[count-1]
        return None

    def countWhere(self) -> int :
        return len(self.__where)

    def addWhere(self, where: Clause) :
        self.__where += (where,)

    def editWhereNested(self, nestedLevel: int) :
        count = len(self.__where)
        if count > 0 :
            self.__where[count-1].nestedLevel(nestedLevel)

    def getLimit(self) -> tuple :
        return self.__limit

    def hasLimit(self) -> bool :
        if self.__limit is None : return False
        else : return True

    def setLimit(self, limit: Limit) :
        self.__limit = limit
