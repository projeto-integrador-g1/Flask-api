from satstac import Catalog, Collection, Item
import urllib.request, json

cat = Catalog.open('https://landsat-stac.s3.amazonaws.com/landsat-8-l1/catalog.json')
col = Collection.open('https://landsat-stac.s3.amazonaws.com/landsat-8-l1/catalog.json')

subcat = [c for c in cat.children()][0]
print(subcat)