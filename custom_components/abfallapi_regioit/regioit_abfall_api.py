#!/usr/bin/env python3
0
"""
Abfall-App RegioIT API
Based on:

* https://play.google.com/store/apps/details?id=de.regioit.abfallapp.awbgl&hl=de
* https://github.com/jensweimann/awb

Thanks to @jensweimann and 
"""
import sys
import logging
import json
import urllib.request

_LOGGER = logging.getLogger(__name__)

# Bergisch Gladbach
BASE_URL_BGL = 'https://aw-bgl2-abfallapp.regioit.de/abfall-app-aw-bgl2'
# Lindlar
BASE_URL_LINDLAR = 'https://lindlar-abfallapp.regioit.de/abfall-app-lindlar'
# ZEW
BASE_URL_ZEW = 'https://zew2-abfallapp.regioit.de/abfall-app-zew2'
# Dinslaken
BASE_URL_DIN = 'https://din-abfallapp.regioit.de/abfall-app-din'
# Pinneberg
BASE_URL_PI = 'https://pi-abfallapp.regioit.de/abfall-app-pi'
# Lüdenscheid
BASE_URL_STL = 'https://stl-abfallapp.regioit.de/abfall-app-stl'
# Bergischer Abfallwirtschaftverbund (Engelskirchen)
BASE_URL_BAV = 'https://bav-abfallapp.regioit.de/abfall-app-bav'
# WML (ESB)
BASE_URL_WML = 'https://wml2-abfallapp.regioit.de/abfall-app-wml2'
# KRWAF AWG / GEG
BASE_URL_KRWAF = 'https://krwaf-abfallapp.regioit.de/abfall-app-krwaf'
# Aachen
BASE_URL_AACHEN = 'https://aachen-abfallapp.regioit.de/abfall-app-aachen'
# Dorsten
BASE_URL_DORSTEN = 'https://dorsten-abfallapp.regioit.de/abfall-app-dorsten'
# Gütersloh
BASE_URL_GT2 = 'https://gt2-abfallapp.regioit.de/abfall-app-gt2'
# Halver
BASE_URL_HLV = 'https://hlv-abfallapp.regioit.de/abfall-app-hlv'
# Coesfeld
BASE_URL_COE = 'https://coe-abfallapp.regioit.de/abfall-app-coe'
# Norderstedt
BASE_URL_NDS = 'https://nds-abfallapp.regioit.de/abfall-app-nds'
# Nuernberg
BASE_URL_NBG = 'https://nuernberg-abfallapp.regioit.de/abfall-app-nuernberg'
CITIES = {
    'Bergisch Gladbach': BASE_URL_BGL,
    'Lindlar': BASE_URL_LINDLAR,
    'ZEW': BASE_URL_ZEW,
    'Dinslaken': BASE_URL_DIN,
    'Pinneberg': BASE_URL_PI,
    'Luedenscheid': BASE_URL_STL,
    'BAV': BASE_URL_BAV,
    'WML': BASE_URL_WML,
    'KRWAF': BASE_URL_KRWAF,
    'Aachen': BASE_URL_AACHEN,
    'Dorsten': BASE_URL_DORSTEN,
    'Guetersloh': BASE_URL_GT2,
    'Halver': BASE_URL_HLV,
    'Coesfeld': BASE_URL_COE,
    'Norderstedt': BASE_URL_NDS,
    'Nürnberg' : BASE_URL_NBG
}

class RegioItAbfallApi(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, endpoint):
        return urllib.request.urlopen(self.base_url + endpoint)

    def get_appdata(self):
        return self._request('/rest/appdata')

    def get_impressum(self, ort):
        return self._request('/rest/texte/ort/{}/impressum'.format(ort))

    def get_menuitems(self):
        return self._request('/rest/menue')

    def get_aktuelles(self, ort):
        return self._request('/rest/texte/aktuelles?ort={}'.format(ort))

    def get_orte(self):
        """
        Ruft alle verfügbaren Orte ab
        """
        return self._request('/rest/orte')
    
    def get_fraktionen(self):
        """
        Ruft alle Müll-Fraktionen (Müllarten) ab
        """
        return self._request('/rest/fraktionen')

    def get_kategorien(self):
        return self._request('/rest/kategorien')

    def get_lastimport(self):
        return self._request('/rest/appdata/lastimport')

    def get_preise(self, ort):
        return self._request('/rest/texte/ort/{}/preise'.format(ort))

    def get_push_notifications(self, ort, count=10):
        return self._request('/rest/pushnotifications/{}?count={}'.format(ort, count))

    def get_schadstoff_kategorien(self):
        return self._request('/rest/kategorien')

    def get_schadstoffe_stoffe(self):
        return self._request('/rest/stoffe')

    def get_standorte(self):
        return self._request('/rest/standorte')

    def get_services(self, ort):
        return self._request('/rest/texte/ort/{}/service'.format(ort))

    def get_standorte_by_id(self, standort_id):
        return self._request('/rest/standorte/{}'.format(standort_id))

    def get_standort_arten(self):
        return self._request('/rest/standorte/standortarten')

    def get_schadstoffmobil_termine(self, standort_id):
        return self._request('/rest/standorte/{}/mobiltermine'.format(standort_id))

    def get_strassen_all(self, ort):
        """
        Ruft alle Strassen eines Ortes ab
        """
        return self._request('/rest/orte/{}/strassen'.format(ort))

    def get_strasse_by_name(self, ort, strasse):
        return self._request('/rest/orte/{}/strassen?q={}'.format(ort, strasse))

    def get_hausnummern(self, strasse_id):
        return self._request('/rest/strassen/{}'.format(strasse_id))
    
    def get_bezirke(self, strasse_id):
        return self._request('/rest/hausnummern/{}/bezirke'.format(strasse_id))

    def get_termine_by_street(self, strasse_id):
        """
        Ruft Müllabfuhr Termine nach Straße ab
        """
        return self._request('/rest/strassen/{}/termine'.format(strasse_id))
    
    def get_termine_by_housenumber(self, housenumber_id):
        """
        Ruft Müllabfuhr Termine nach Haunummer ab
        """
        return self._request('/rest/hausnummern/{}/termine'.format(housenumber_id))

def main():
    api = RegioItAbfallApi(CITIES['Nürnberg'])
    
    choice = 0

    orte = None
    strassen = None
    fraktionen = None
    bezirke = None
    termine = None

    ort_name = ''
    ort_id = 0
    strassen_name = ''
    strassen_id = 0

    _LOGGER.info('Getting list of FRAKTIONEN')
    with api.get_fraktionen() as resp:
        print('FRAKTIONEN:')
        try:
            fraktionen = json.loads(resp.read().decode())
            for entry in fraktionen:
                print(entry)
        except:
            _LOGGER.error('Failed to get list of FRAKTIONEN')
            sys.exit(3)

    _LOGGER.info('Getting list of ORTE')
    with api.get_orte() as resp:
        print('ORTE:')
        try:
            orte = json.loads(resp.read().decode())
            for index, entry in enumerate(orte):
                print('{}: Id: {} => {}'.format(index, entry['id'], entry['name']))
        except:
            _LOGGER.error('Failed to get list of ORTE')
            sys.exit(1)

    try:
        choice = int(input("Choose ORTE Id: "))
        if choice > len(orte):
            raise IndexError()
    except:
        _LOGGER.error('Invalid choice on ORTE')
        sys.exit(1)

    ort_name = orte[choice]['name']
    ort_id = orte[choice]['id']
    _LOGGER.info('Choosing first Ort: {} => {}'.format(ort_name, ort_id))

    _LOGGER.info('Getting list of STRASSEN')
    with api.get_strassen_all(ort_id) as resp:
        print('STRASSEN:')
        try:
            strassen = json.loads(resp.read().decode())
            for index, entry in enumerate(strassen):
                hausnummern = entry['hausNrList']
                print('{}: id: {} => {} {}'.format(index, entry['id'], entry['name'], '(hausnr: {})'.format(hausnummern)
                    if hausnummern else ''))
        except:
            _LOGGER.error('failed to get list of strassen')
            sys.exit(2)

    try:
        choice = int(input("choose strassen id: "))
        if choice > len(strassen):
            raise indexerror()
    except:
        _LOGGER.error('invalid choice on strassen')
        sys.exit(2)

    strassen_name = strassen[choice]['name']
    strassen_id = strassen[choice]['id']
    _LOGGER.info('choosing first strasse: {} => {}'.format(strassen_name, strassen_id))


    try:
        with api.get_hausnummern(strassen_id) as url:
            numbers = json.loads(url.read().decode())
            numbers = numbers['hausNrList']
    except Exception as e:
        _LOGGER.error('API call error: Hausnummern , error: {}'.format(e))
        return
    
    _LOGGER.info('getting list of hausnummern')
    with api.get_hausnummern(strassen_id) as resp:
        try:
            print('hausnummern:')
            strasse = json.loads(resp.read().decode())
            hausNummern = strasse['hausNrList']
            for index, entry in enumerate(hausNummern):
                print('{}: id: {} => {} '.format(index, entry['id'], entry['nr']))
        except:
            _LOGGER.error('failed to get list of hausnummern')
            sys.exit(2)    
        
    try:
        choice = int(input("choose hausnummer Id: "))
        if choice > len(hausNummern):
            raise IndexError()
    except:
        _LOGGER.error('Invalid choice on STRASSEN')
        sys.exit(2)
    
    strassen_name += " " + hausNummern[choice]['nr']
    strassen_id = hausNummern[choice]['id']
    _LOGGER.info('choosing first strasse: {} => {}'.format(strassen_name, strassen_id))

    # _LOGGER.info('Getting list of BEZIRKE')
    # with api.get_bezirke(strassen_id) as resp:
    #     print('BEZIRKE:')
    #     try:
    #         bezirke = json.loads(resp.read().decode())
    #         for entry in bezirke:
    #             print(entry)
    #     except:
    #         _LOGGER.error('Failed to get list of BEZIRKE')
    #         sys.exit(3)

    _LOGGER.info('Getting list of TERMINE')
    with api.get_termine_by_housenumber(strassen_id) as resp:
        print('TERMINE:')
        try:
            termine = json.loads(resp.read().decode())
            for entry in termine:
                print(entry)
        except:
            _LOGGER.error('Failed to get list of TERMINE')
            sys.exit(3)
    
    fraktionen = {entry['id']:entry for entry in fraktionen}

    abholtermine = dict()
    for entry in termine:
        datum = entry['datum']
        del entry['datum']

        if datum not in abholtermine:
            abholtermine[datum] = list()

        abholtermine[datum].append(entry)
    
    print(abholtermine)
    for k, v in sorted(abholtermine.items()):
        muell = None
        for abfuhr in v:
            fraktion = abfuhr['bezirk']['fraktionId']
            muell_typ = fraktionen.get(fraktion)['name']
            muell = muell_typ if not muell else ', '.join([muell, muell_typ])
        print('{} => {}'.format(k, muell))


if __name__ == '__main__':
    main()
