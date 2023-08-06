from ...Structure import Order
from ...Builder import OrderByBuilder
from typing import Iterable, Mapping

class OrderBy :
    """ORDER BY manipulation component.
    """

    def oderBy(self, columns, orderType) :
        """ORDER BY query manipulation"""
        orderObjects = ()
        if isinstance(columns, str) :
            orderObjects += (Order.create(columns, orderType),)
        elif isinstance(columns, Mapping) :
            for key in columns.keys() :
                orderObjects += (Order.create({key: columns[key]}, orderType),)
        elif isinstance(columns, Iterable) :
            for col in columns :
                orderObjects += (Order.create(col, orderType),)
        for order in orderObjects :
            if isinstance(self.builder, OrderByBuilder) :
                self.builder.addOrder(order)
            else :
                raise Exception('Builder object does not support ORDER BY query')
        return self

    def orderByAsc(self, column) :
        """ORDER BY query with ASC order"""
        return self.oderBy(column, Order.ORDER_ASC)

    def orderByDesc(self, column) :
        """ORDER BY query with DESC order"""
        return self.oderBy(column, Order.ORDER_DESC)
