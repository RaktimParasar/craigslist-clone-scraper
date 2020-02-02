import requests
from django.shortcuts import render, redirect
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

# Create your views here.

BASE_CRAGLIST_URL = 'https://bangalore.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def index(request):
    return render(request, 'my_app/base.html')


def search_result(request):
    search = request.POST.get('search')
    # Goes to Search model creates a search object and input search is feed to search argument
    models.Search.objects.create(search=search)

    # This concatenates base_url_link and what we search
    main_url = BASE_CRAGLIST_URL.format(quote_plus(search))
    response = requests.get(main_url)
    data = response.text
    # Parse the html data to soup object
    soup = BeautifulSoup(data, features='html.parser')
    # Find all the links where class is result-title
    result_lists = soup.find_all('li', {'class': 'result-row'})

    final_results = []

    for result in result_lists:
        result_title = result.find(class_='result-title').text
        result_url = result.find('a').get('href')

        if result.find(class_='result-price'):
            result_price = result.find(class_='result-price').text
        else:
            result_price = "N/A"

        if result.find(class_='result-image').get('data-ids'):
            result_image_id = result.find(
                class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            result_image_url = BASE_IMAGE_URL.format(result_image_id)
        else:
            result_image_url = 'https://craigslist.org/images/peace.jpg'
        
        final_results.append(
            (result_title, result_url, result_price, result_image_url))


    context = {
        'search': search,
        'final_results': final_results,
    }
    return render(request, 'my_app/search_result.html', context)