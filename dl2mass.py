from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.utils.data import download_file
import requests #to make get-requests in web
import time #to make pauses
from lxml import etree
import re
import os

#folder to download, ra,de are both in degree, j,k,h - 2mass bands to download, default: download all bands
def dl2mass (folder,ra, de,j=False, k=False, h=False):
    a = b = d = 'name'
    if j:
        a = b = d = 'name=j'
        if k:
            b = 'name=k'
        if h:
            d = 'name=h'
    else:
        if k:
            a = b = d = 'name=k'
            if h:
                d = 'name=h'
        else:
            if h:
                a = b = d = 'name=h'
    c = SkyCoord(ra, de,  unit="deg")
    u2mass = ('http://irsa.ipac.caltech.edu/cgi-bin/2MASS/IM/nph-im_sia?'
              'POS=%f,%f&SIZE=%f&FORMAT=image/fits' % (c.ra.degree, c.dec.degree, 0.1))  # 0.1 - field size in arcmin
    rsuccess = False
    while (not rsuccess):
        try:
            r2mass = requests.get(u2mass).text.encode("utf-8")
            rsuccess = True
        except Exception:  # protection from web-interruption
            rsuccess = False
            print('request failed')
            time.sleep(10)
    root = etree.fromstring(bytes(r2mass))
    for element in root.iter():
        e=str(element.text)
        if (re.search("\.fits", e) and (re.search(a, e) or re.search(b, e) or re.search(d, e))):
            print(e)
            fitssucess = False
            while (not fitssucess):
                try:
                    fitsfile = download_file(e, cache=True)
                    hdulist = fits.open(fitsfile)
                    hdulist[0].writeto(os.path.join(folder, re.split("name=", e)[1] + '.bz2'))
                    hdulist.close()
                    fitssucess = True
                except:
                    fitssucess = False
                    time.sleep(10)

ra=4 #degree
de=19#degree
folder='./2mass-dwnl'#should exist
dl2mass (folder,ra, de, k=True, h=True)