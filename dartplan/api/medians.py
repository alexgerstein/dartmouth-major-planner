from flask_restful import Resource
from dartplan.login import login_required

MEDIANS = ['A', 'A/A-', 'A-', 'A-/B+', 'B+', 'B+/B', 'B',
           'B/B-', 'B-', 'B-/C+', 'C+', 'C+/C', 'C']


class MedianListAPI(Resource):
    def get(self):
        return {'medians': [{'id': index, 'value': median} for index, median in enumerate(MEDIANS)]}
