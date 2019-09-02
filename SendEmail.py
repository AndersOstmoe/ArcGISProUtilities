# -*- coding: UTF-8 -*-
import sys
sys.path.append(r'C:\Program Files\ArcGIS\Pro\Resources\ArcPy\arcpy')
sys.path.append(r'C:\Program Files\ArcGIS\Pro\Resources\ArcPy\arcpy\arcpy')
sys.path.append(r'C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\DLLs')
sys.path.append(r'C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\lib')
sys.path.append(r'C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3')
sys.path.append(r'C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\lib\site-packages')
sys.path.append(r'C:\Program Files\ArcGIS\Pro\bin')

import logging


from av_email import Av_gmail

from arcgis.gis import GIS
from arcgis.features import FeatureLayer
from arcgis.features import Table

import getpass, smtplib

def is_editable(lyr):
    l = lyr.properties.capabilities.split(',')
    if 'Editing' in l:
        return True
    else:
        return False

def create_msg(navn):
    the_message = f"""\
Subject: Bekreftelse mottatt innspill

Til {navn}

Innspillet er mottatt.

Denne e-posten kan ikke besvares. Videre kommunikasjon angående prosjektet
kan gjøres via de kanalene som er oppgitt på medvirkningsportalen.

Vennlig hilsen
Prosjektgruppa for ny E6 Moelv-Storhove"""

    # the_message = "Subject: Bekreftelse mottatt innspill \n" + \
    #     "\n" + \
    #     "Til " + navn + "\n" +\
    #     "\n" + \
    #     "Innspillet er mottatt. \n" + \
    #     "\n" + \
    #     "Denne e-posten kan ikke besvares. Videre kommunikasjon angående prosjektet\n" + \
    #     "kan gjøres via de kanalene som er oppgitt på medvirkningsportalen.\n" + \
    #     "\n" + \
    #     "\n" + \
    #     "Vennlig hilsen\n" + \
    #     "Prosjektgruppa for ny E6 Moelv-Storhove"

    return the_message.encode('latin-1')


logging.basicConfig(filename="C:/DiskTemp/E6Innlandet/Email.log", level=logging.INFO, format='%(asctime)-15s %(message)s')
logging.info("Sjekker tabellen for nye innspill.")

brukernavn = "agostmoe"
Onlinepwd = "1Fairlane1"
gis = GIS("https://www.arcgis.com/home/signin.html", brukernavn, Onlinepwd)

Innspill_feature_layer = FeatureLayer('https://services.arcgis.com/whQdER0woF1J7Iqk/arcgis/rest/services/TilbakemeldingerEksterntOriginal_E6_1/FeatureServer/0', gis)
adm_table = Table('https://services.arcgis.com/whQdER0woF1J7Iqk/arcgis/rest/services/E6Innlandet_epost_sendt_runtime/FeatureServer/0', gis)

epost = 'Epost'
OBJECTID = 'OBJECTID'
Navn = 'Navn'  # innspillstekst
innspill_id = 'innspill_id'  # kolonne i adm tabell

all_features = Innspill_feature_layer.query()
all_adm_table = adm_table.query()  # kan sansynligvis forenkle med å sette as_df = True

innspill_pandas_dataframe = all_features.sdf
adm_pandas_dataframe = all_adm_table.sdf

if not is_editable(adm_table):
    print(str(adm_table) + "not editable")
    raise ValueError

gmail = Av_gmail('e6innlandetsvar@gmail.com', "1Fairlane1")

epost_objectid = innspill_pandas_dataframe[[epost, OBJECTID, Navn]][innspill_pandas_dataframe[epost].notna()]  # utvalg av innspill med epostadresse
receivers = list(epost_objectid['Epost'])  # liste epost adr
objids = list(epost_objectid['OBJECTID'])  # liste objid
navn_liste = list(epost_objectid['Navn'])  # liste innspillstekst
allready_sendt = list(adm_pandas_dataframe['innspill_id'])  # get list of innspillsid that has recieved email

for receiver, objid, navn in zip(receivers, objids, navn_liste):
    if objid not in allready_sendt:  # If email has not been sendt previously
        try:
            gmail.sendmails(receivers= receiver, message = create_msg(navn))
            adm_table.edit_features(adds=[{"attributes":{"innspill_id": objid,"sendt":"ja"}}])  # add objid to innspill_id col.
            print ("email sendt til " + receiver)
            logging.info("email sendt til " + receiver)
        except smtplib.SMTPRecipientsRefused:
            print("Ikke akseptert adresse " + receiver)
            logging.info("Ikke akseptert adresse " + receiver)
        except UnicodeEncodeError:
            print("Kunne ikke enkode " + receiver)
            logging.info("Kunne ikke enkode " + receiver)