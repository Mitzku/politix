# poli-ticker

Notes
- Letzte Zeit um Bundestagswebseite zu scrapen:  2283.9095923900604 seconds
- Seid Einbau der img_rul auf /politiker ist die ladezeit merkbar angestiegen. könnte daran lieen, das ich auf politiker den ganzen df schicke und nicht nur werte?
- Profilseiten gehen nur manchmal weil scheinbar die Daten nicht in der db sind... dürfte am scrapen liegen. Ich habe lediglich 195 von 747 IDs in df_abstimmungen_selenium
- webscraper macht auf einmal issues ohne erkennbaren grund. ging vorhin noch mit demselben script...

Themen:
- Ausscheidende Politiktreibende
- Namenswechsel 
- Daten putzen (
  - landeslistenplätze (bisher none) und nicht erkannte wahlkreise
  - img_url wird beim scrapen scheinbar abgeschnitten manchmal 
- App vs Web fist
- functionalities?
  - recent tweets / social media ads
  - dashboard
  - boulevard
  - letzte headlines & news oder erwähnungen
  - geolocation & PLZ von wahlkreis abgeleitet
  - Facebook
    - Werbeeinköufe
    - letzte posts 
      - Erst die Page-ID holen, dann 
    - einbetten?
  - Twitter
    - tweets
    - connections
- wie automatisch jeden tag checken lassen?
- Filtern von Ergebnissen auf der Webpage
- URL verlinkt bei 'Keine auf Bundestagsseite'
- startseite carousel und snippets anzeigen
- improvements scraping: 
  - links zu redebeiträgen
  - bei manchen websiten werden die abstimmungen nicht mitausgelesen, e.g. https://www.bundestag.de/abgeordnete/biografien/G/gruender_nils-860540

