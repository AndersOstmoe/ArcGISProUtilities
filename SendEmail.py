import sys
sys.path.append(r'C:\Users\torbjorn.boe\Google Drive\Python\AV_agol')
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
    return f"""\
Subject: Bekreftelse mottatt innspill

Til {navn}

Innspillet er mottatt.

Denne e-posten kan ikke besvares. Videre kommunikasjon angående prosjektet
kan gjøres via de kanalene som er oppgitt på Nye Veier sine sider.

Vennlig hilsen
Prosjektgruppa for ny E18 Dørdal - Grimstad
""".encode('latin-1')


brukernavn = "agostmoe"
Onlinepwd = "1Fairlane1"
gis = GIS("https://www.arcgis.com/home/signin.html", brukernavn, Onlinepwd)

Innspill_feature_layer = FeatureLayer('https://services.arcgis.com/whQdER0woF1J7Iqk/arcgis/rest/services/E18DG_TilbakemeldingerEksternt_Ver3_20190404/FeatureServer/0', gis)
adm_table = Table('https://services.arcgis.com/whQdER0woF1J7Iqk/arcgis/rest/services/E18DG_epost_sendt_runtime/FeatureServer/0', gis)

epost = 'Epost'
OBJECTID = 'OBJECTID'
Navn = 'Navn'  # innspillstekst
innspill_id = 'innspill_id'  # kolonne i adm tabell

all_features = Innspill_feature_layer.query()
all_adm_table = adm_table.query()  # kan sansynligvis forenkle med å sette as_df = True

innspill_pandas_dataframe = all_features.sdf
adm_pandas_dataframe = all_adm_table.sdf

if not is_editable(adm_table):
    print(f'{adm_table} not editable')
    raise ValueError

gmail = Av_gmail('e18dgav@gmail.com', "TilGrimstadPaa123")

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
            print (f'email sendt to {receiver}')
        except smtplib.SMTPRecipientsRefused:
            print(f'could not send to {receiver}')