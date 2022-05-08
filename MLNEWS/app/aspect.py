from django.shortcuts import render
from app.models import *
from random import shuffle

def aspect(request):
    search_type = request.POST.get('searchType')

    search_value = request.POST.get('search_value')

    co_search_value = request.POST.get('co_search_value')

    search_type = 'city'

    if co_search_value:
        values = co_search_value.split(":")
        if len(values) > 1:
            search_type = values[0]
            search_value = values[1]
        else:
            search_value = values[0]
    else:
        co_search_value = '北京'
        search_value = '北京'

    safe = {}
    if not search_value:

        return render(request,'aspect.html',locals())

    all_sights = Sight.objects.all()

    hot_sights = Sight.objects.filter(city = search_value).order_by('-hot')[:60]

    hot_sight_x = [item.name for item in hot_sights][:20]
    hot_sight_y = [item.hot for item in hot_sights][:20]

    hot_restaurants = Restaurant.objects.filter(city= search_value).order_by('-comments')[:60]
    hot_restaurant_x = [item.name[:5] for item in hot_restaurants][:20]
    hot_restaurant_y1 = [item.comments for item in hot_restaurants][:20]
    hot_restaurant_y2 = [item.score for item in hot_restaurants][:20]

    love_restaurants = Restaurant.objects.filter(city= search_value, comments__gte=10).order_by('-score', '-comments')[:60]
    love_restaurant_x = [item.name[:5] for item in love_restaurants][:20]
    love_restaurant_y1 = [item.score for item in love_restaurants][:20]
    love_restaurant_y2 = [item.comments for item in love_restaurants][:20]

    main5 = [{'name':item.name, 'value':item.comments }for item in hot_sights][:60]
    shuffle(main5)
    main5 = main5[:20]

    love_sights = Sight.objects.filter(city = search_value).order_by('-sales')[:60]
    love_sight_x = [item.name for item in love_sights][:20]
    love_sight_y1 = [item.sales for item in love_sights][:20]
    love_sight_y2 = [item.price for item in love_sights][:20]


    main6 = [{'name':item.name, 'value':item.comments }for item in love_sights][:60]
    shuffle(main6)
    main6 = main6[:20]

    return  render(request,'aspect.html',locals())
