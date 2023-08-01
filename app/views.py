from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
import requests

CRAIGSLIST_BASE_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def search(request):
    search_text = request.POST.get('search')
    url = CRAIGSLIST_BASE_URL.format(quote_plus(search_text))
    response = requests.get(url)
    site_html_data =  response.text
    soup = BeautifulSoup(site_html_data, features='html.parser')
    posts_list= soup.find_all('li', {'class': 'cl-static-search-result'})
    final_posts = []
    # split posts lists bcz it's too large and took a lot of time in webscraping while getting images
    posts_list = posts_list[:6]
    for post in posts_list:
        post_title = post.find(class_='title').text
        post_link = post.find('a').get('href')
        post_price = post.find(class_='price').text

        if not post_price:
            post_price = 'N/A'
        post_location = post.find(class_= 'location').text

        if not post_location:
            post_location = 'N/A'

        #getting image from the other page which opens on the link
        post_image_url = 'https://craigslist.org/images/peace.jpg' # default image url
        site_html_data = requests.get(post_link).text
        soap_for_image = BeautifulSoup(site_html_data, features='html.parser')
        image_div = soap_for_image.find(class_='visible')
        if image_div:
            post_image_url= image_div.find('img').get('src')
        print(post_image_url)
        post_title = get_prettier_text(post_title)
        post_location = get_prettier_text(post_location)
        final_posts.append((post_title, post_link, post_price, post_location, post_image_url))
    print(final_posts)
    search_content = {'search': search_text, 'final_posts': final_posts}
    return render(request, 'app/search.html', search_content)

def get_prettier_text(text):
    text = text.replace('  ', '')
    text = text.replace('\n', '')
    text = text.replace('(', '')
    text = text.replace(')', '')
    text = text.replace('*', '')
    text = text.replace('★', '')
    return text
