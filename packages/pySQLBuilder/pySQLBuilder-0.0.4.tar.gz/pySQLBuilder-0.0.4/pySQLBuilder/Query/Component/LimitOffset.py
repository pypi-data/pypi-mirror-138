from ...Structure import Limit
from ...Builder import LimitBuilder

class LimitOffset :

    def limit(self, limit, offset = Limit.NOT_SET) :
        validLimit = Limit.NOT_SET
        validOffset = Limit.NOT_SET
        if isinstance(limit, int) :
            if limit > 0: validLimit = limit
        if isinstance(offset, int) :
            if offset > 0: validOffset = offset
        limitObject = Limit(validLimit, validOffset)
        if isinstance(self.builder, LimitBuilder) :
            self.builder.setLimit(limitObject)
        else :
            raise Exception('Builder object does not support LIMIT and OFFSET query')
        return self

    def offset(self, offset) :
        return self.limit(Limit.NOT_SET, offset)
