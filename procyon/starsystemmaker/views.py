from procyon.starsystemmaker.test_helpers import *
from procyon.starsystemmaker.space_helpers import *
from procyon.starsystemmaker.texture_generator import *
from procyon.starsystemmaker.models import *
from procyon.starcatalog.models import Star
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render_to_response
from django.core import exceptions
import json
from django.template import RequestContext


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


def star_viewer(request, pk):
    """
    View used for visualizing star clusters.
    """
    star = get_object_or_404(Star, id=pk)

    try:
        star = get_object_or_404(Star, id=pk)
        star_model = get_object_or_404(StarModel, star=star)
    except:
        star_model = {}

    return render_to_response('star_viewer.html', {'item': star_model, 'star': star}, RequestContext(request))


def lookup_star_info(request, pk):
    callback = request.GET.get('callback')

    try:
        star_model = get_object_or_404(StarModel, id=pk)
        dumps = star_model.get_params()

        star_prime = star_model.star
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
        star_initialized = True
        try:
            star_model = StarModel.objects.get(star=star_prime)
            if star_model.guessed_age == 0 or star_model.guessed_age == None or star_model.guessed_mass == 0:
                star_initialized = False
        except exceptions.ObjectDoesNotExist:
            StarModel.objects.create(star=star_prime)
            star_model = StarModel.objects.get(star=star_prime)
            star_initialized = False

        if not star_initialized:
            star_model.build_model(pk, star_prime)

        dumps = star_model.get_params()
        dump2 = star_prime.get_params()
        dumps = dict(dump2.items()+dumps.items())

    except Exception as e:
        dumps = {'status': 'error', 'details': str(e)}

    output = json.dumps(dumps)
    if callback:
        output = '{0}({1});'.format(callback, output)

    return HttpResponse(output, content_type="application/json")


def system_builder(request):
    """
    View used for designing a star system.
    """
    rand = request.GET.get('rand')
    stellar = request.GET.get('stellar')
    temp = request.GET.get('temp')
    mass = request.GET.get('mass')
    radius = request.GET.get('radius')
    age = request.GET.get('age')
    planets = request.GET.get('planets')

    options = {'rand_seed': rand, 'stellar': stellar, 'temp': temp, 'mass': mass, 'radius': radius, 'age': age, 'planets': planets}
    settings = star_variables(options)

    settings = planet_from_variables(settings)

    settings = json.dumps(settings, ensure_ascii=True)

    return render_to_response('system_builder.html', {'settings': settings}, RequestContext(request))


def create_planet_texture_png(request):
    try:
        return generate_texture(request, 'PNG')
    except:
        return image_with_random_color('PNG')


def create_planet_texture_jpeg(request):
    try:
        return generate_texture(request, 'JPEG')
    except:
        return image_with_random_color('JPEG')
