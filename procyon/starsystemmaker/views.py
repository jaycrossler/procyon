from procyon.starsystemmaker.test_helpers import *
from procyon.starsystemmaker.space_helpers import *
from procyon.starsystemmaker.models import *
from procyon.starcatalog.models import Star
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.core import exceptions
import json


def create_star_extended_data(request, pk):
    create_star_model(pk, True)
    result_info = "Done"

    return HttpResponse(result_info, content_type="text/html")


def create_star_extended_data_rerandomize(request, pk):
    create_star_model(pk, False)
    result_info = "Done"

    return HttpResponse(result_info, content_type="text/html")


def create_some_star_colors(request, force):
    for i in [7, 8, 9]:
        create_star_model(i, force)
    result_info = "Done"

    return HttpResponse(result_info, content_type="text/html")


def create_star_model(star_id, force=False):
    status = "Done"
    try:
        star = Star.objects.get(id=star_id)
        star_model, created = StarModel.objects.get_or_create(star=star)
        if created or force:
            star_model.build_model(star_id, forced=force)
            star_model.save()

    except exceptions.ObjectDoesNotExist:
        status = "{0} #{1} {2}".format(status, star_id, "star does not exist")

    return status


def lookup_star_info(request, pk):
    callback = request.GET.get('callback')

    try:
        star = get_object_or_404(StarModel, id=pk)
        dumps = star.get_params()

        star_prime = star.star
        if star_prime:
            dump2 = star_prime.get_params()
            dumps = dict(dump2.items()+dumps.items())

    except Exception as e:
        dumps = {'status': 'error', 'details': str(e)}

    output = json.dumps(dumps)
    if callback:
        output = '{0}({1});'.format(callback, output)

    return HttpResponse(output, content_type="application/json")


def lookup_star_info_prime(request, pk):
    #TODO: Maybe combine this with function above to DRY
    callback = request.GET.get('callback')

    try:
        star_prime = get_object_or_404(Star, id=pk)
        try:
            star = StarModel.objects.get(star=star_prime)
        except exceptions.ObjectDoesNotExist:
            star = StarModel.objects.create(star=star_prime)
            star.build_model(pk, star_prime)
            star = StarModel.objects.get(star=star_prime)

        dumps = star.get_params()
        dump2 = star_prime.get_params(['nearby_stars', ])
        dumps = dict(dump2.items()+dumps.items())

    except Exception as e:
        dumps = {'status': 'error', 'details': str(e)}

    output = json.dumps(dumps)
    if callback:
        output = '{0}({1});'.format(callback, output)

    return HttpResponse(output, content_type="application/json")
