from tests.factories import *
from dartplan.models import Term


class TermFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Term

    id = factory.Sequence(lambda n: n)
    year = factory.Sequence(lambda n: u'201%d' % n)
    season = factory.Iterator(['F', 'W', 'S', 'X'])
