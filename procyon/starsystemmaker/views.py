from procyon.starsystemmaker.test_helpers import *
from procyon.starsystemmaker.space_helpers import *
from procyon.starsystemmaker.models import *
from procyon.starcatalog.models import Star
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.core import exceptions


@timeit
def create_some_star_colors(request, force):
    for i in [1, 2, 3, 4, 5]:
        create_star_model(i, force)
    result_info = "Done"

    return HttpResponse(result_info, content_type="text/html")


def create_star_model(star_id, force=False):
    status = "Finished. "
    try:
        star = Star.objects.get(id=star_id)
        star_model, created = StarModel.objects.get_or_create(star=star)
        if created or force:
            star_model.build_model(star_id)
            star_model.save()

    except exceptions.ObjectDoesNotExist:
        status = "{0} #{1} {2}".format(status, star_id, "star does not exist")

    return status