from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from procyon.starcatalog.models import Star



class StarCatalog(TestCase):
    
    def setUp(self):
        star1 = Star.objects.create(**{"HR": None, "spectrum": "G5", "Y": -28.6581, "VY": 5.7579e-05, "HD": None, "HIP": 70767, "RV": None, "proper_name": 'Kelda', "RA": 14.47259311, "distance_parsecs": 73.8007380073801, "abs_mag": 5.52969647605212, "gliese": None, "PMDec": -28.21, "mag": 9.87, "color_index": 0.753, "VX": -3.3849e-05, "X": -37.90807, "VZ": -6.498e-06, "Z": -56.46449, "PMRA": -185.44, "bayer_flamsteed": None, "dec": -49.91535182})
        star2 = Star.objects.create(**{"HR": None, "spectrum": "F5V", "Y": -37.48622, "VY": 2.3793e-05, "HD": 126819, "HIP": 70768, "RV": None, "proper_name": 'Chloe', "RA": 14.47315865, "distance_parsecs": 67.5219446320054, "abs_mag": 3.76277529260604, "gliese": None, "PMDec": -50.55, "mag": 7.91, "color_index": 0.506, "VX": -9.883e-06, "X": -49.57038, "VZ": -1.5229e-05, "Z": -26.39644, "PMRA": -76.19, "bayer_flamsteed": None, "dec": -23.01246733})
        star3 = Star.objects.create(**{"HR": None, "spectrum": "M3/M4III", "Y": -232.61189, "VY": 1.4617e-05, "HD": 126743, "HIP": 70769, "RV": None, "proper_name": 'Jasper', "RA": 14.47365036, "distance_parsecs": 500.0, "abs_mag": -0.414850021680092, "gliese": None, "PMDec": -17.82, "mag": 8.08, "color_index": 1.465, "VX": 2.3422e-05, "X": -307.515, "VZ": -3.3309e-05, "Z": -318.31781, "PMRA": 1.02, "bayer_flamsteed": None, "dec": -39.54140198})

    def test_search_view(self):
        """
        Tests the search view.
        """
        c = Client()

        term = 'kelda'
        db_lookup = Star.objects.filter(proper_name__icontains=term)
        response = c.get(reverse('star-list-no-id') + '?q={term}'.format(term=term))

        for i in db_lookup:
            self.assertTrue(i in response.context['items'])


