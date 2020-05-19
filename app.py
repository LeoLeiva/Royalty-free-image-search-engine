from flask import Flask, render_template, request
import requests
import json
from itertools import zip_longest

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template("buscador.html")


@app.route('/procesar', methods=['POST'])
def procesar():
    #Recupero el valor de la busqueda
    busqueda = request.form.get("busqueda")

    #Llave de API Pixabay
    keypixabay = '<--Api Key de Pixabay-->'

    #Llave de API Flickr
    keyflickr = '<--Api Key de Flickr-->'

    #Llave de API Pexels
    keypexels = '<--Api Key de Pexels-->'

    #Llave de API Unsplash
    keyunsplash = '<--Api Key de Unsplash-->'

    #Links de las APIs
    pixabay = 'https://pixabay.com/api/?key={}&q={}&image_type=photo&per_page=200'.format(keypixabay, busqueda).replace(" ", "+")
    flickr = 'https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key={}&text={}&license=4%2C5%2C9%2C10&sort=relevance&privacy_filter=1&safe_search=3&content_type=7&media=photo&is_commons=true&in_gallery=true&extras=media%2C+url_q%2C+url_o%2C+original_format&per_page=500&format=json&nojsoncallback=1'.format(keyflickr, busqueda)
    wikimedia = 'https://commons.wikimedia.org/w/api.php?action=query&generator=images&prop=imageinfo&gimlimit=500&redirects=1&titles={}&iiprop=url|size|dimensions&iilimit=1&iiprop=url&iiurlwidth=200&iiurlheight=200&format=json'.format(busqueda).replace(" ", "%20")
    pexels = requests.get("http://api.pexels.com/v1/search?query={}&per_page=80".format(busqueda).replace(" ", "%20"), headers={
    "Authorization": "{}".format(keypexels)})
    unsplash = 'https://api.unsplash.com/search/photos/?client_id={}&query={}&per_page=500'.format(keyunsplash, busqueda)

    #Saco datos de API Pixabay
    response = requests.get(pixabay)
    data = response.text
    parsed = json.loads(data)

    #Saco datos de API Flickr
    responseflickr = requests.get(flickr)
    dataflickr = responseflickr.text
    parsedflickr = json.loads(dataflickr)

    #Saco datos de API Wikimedia
    Rwiki = requests.get(wikimedia)
    DATA = Rwiki.json()
    try:
        PAGES = DATA["query"]["pages"]
    except KeyError:
        PAGES = False

    #Saco datos de API Pexels
    datapexels = pexels.text
    parsedpexels = json.loads(datapexels)

    #Api de Unsplash
    Runsplash = requests.get(unsplash)
    parsedunsplash = Runsplash.json()


    listpixa = []
    listflickr =[]
    listwikimedia =[]
    listpexels =[]
    listunsplash =[]

    #Bucle de Pixabay
    for product in parsed['hits']:
        idimg = product['id']
        pageURL = product['pageURL']
        tags = product['tags']
        previewURL = product['previewURL']
        ImageWidth = product['previewWidth']
        listpixa.append([idimg, pageURL, tags, previewURL])

    #Bucle de Flickr
    for productflickr in parsedflickr['photos']['photo']:
        idflickr = productflickr['id']
        owner = productflickr['owner']
        url_q = productflickr['url_q']
        listflickr.append([idflickr, owner, url_q])

    #Bucle de Wikimedia
    if PAGES != False:
        for page in PAGES.values():
            if 'imageinfo' in page:
                thumburl = page['imageinfo'][0]['thumburl']
                descriptionurl = page['imageinfo'][0]['descriptionurl']
                listwikimedia.append([thumburl, descriptionurl])

    #Bucle de Pexels
    for productpexels in parsedpexels['photos']:
        photourl = productpexels['url']
        imgview = productpexels['src']['small']
        listpexels.append([photourl, imgview])

    #Bucle de Unsplash
    for productunsplash in parsedunsplash['results']:
        thumbunsplash = productunsplash['urls']['thumb']
        urlunsplash = productunsplash['links']['html']
        listunsplash.append([thumbunsplash, urlunsplash])



    zipped_list = list(zip_longest(listpixa,listflickr, listwikimedia, listpexels, listunsplash, fillvalue='?'))
    return render_template("mostrar.html", listimg=zipped_list, busqueda=busqueda)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)