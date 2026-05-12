# 📍 Inspecció de Camp PWA

Una aplicació web progressiva (PWA) lleugera i eficient dissenyada per a la recollida de dades georeferenciades sobre el terreny. Ideal per a inventaris, seguiment d'incidències o mostrejos ambientals.

## ✨ Característiques principal
- **📱 PWA Nativa:** Es pot instal·lar al mòbil com una aplicació sense necessitat de passar per l'App Store o Google Play.
- **🗺️ Mapes Interactius:** Suport per a capes de carrers, satèl·lit i OpenStreetMap mitjançant Leaflet.
- **🛰️ Geolocalització:** Utilitza el GPS del dispositiu per situar punts amb precisió o permet la selecció manual sobre el mapa.
- **📸 Integració amb Telegram:** Les fotografies es pugen automàticament a un bot de Telegram privat, estalviant espai al servidor i facilitant la consulta.
- **📂 Exportació compatible amb QGIS:** Exporta les dades en format GeoJSON (dins un fitxer ZIP) preparat per carregar directament a qualsevol SIG.
- **🔒 Privacitat:** Les dades s'emmagatzemen localment al navegador (`localStorage`). Res es puja a servidors externs excepte les fotos al teu propi bot.

## 🚀 Com començar

### 1. Configuració del Bot de Telegram (Obligatori)
Perquè les fotos funcionin, necessites el teu propi canal de recepció:
1. Parla amb [@BotFather](https://t.me/botfather) a Telegram i crea un nou bot per obtenir el **Token**.
2. Crea un grup o canal i afegeix el bot.
3. Obtingues el teu **Chat ID** (pots fer servir bots com [@userinfobot](https://t.me/userinfobot)).
4. En obrir l'App per primer cop, introdueix aquestes dades al panell de configuració.

### 2. Instal·lació al mòbil
1. Obre l'enllaç de GitHub Pages (o on tinguis allotjat l'HTML) al navegador del mòbil.
2. **Android:** Prem els tres punts i selecciona "Instal·lar aplicació".
3. **iOS (Safari):** Prem el botó "Compartir" i selecciona "Afegir a la pantalla d'inici".

## 🛠️ Flux de treball amb QGIS

L'aplicació està optimitzada per a professionals del territori:
1. **Camp:** Recull les dades i fes les fotos.
2. **Exportació:** Des de l'apartat "Gestió de Dades", descarrega el **ZIP (GeoJSON)**.
3. **Gabinet:** Arrossega el fitxer `.geojson` a QGIS.
4. **Visualització de fotos:** L'exportació inclou un camp anomenat `enllac_visor`. Si configures l'acció o el formulari a QGIS per obrir URLs, podràs veure les fotos directament al navegador sense que caduquin els enllaços de Telegram.

## 💻 Tecnologies utilitzades
- **HTML5/CSS3** (Tailwind CSS per als estils).
- **JavaScript ES6** (Sense dependències pesades).
- **Leaflet.js** per a la cartografia.
- **Proj4js** per a la conversió de coordenades a UTM 31N (EPSG:25831).
- **JSZip** per a la generació de paquets de dades.

## 📝 Notes
- **Emmagatzematge:** Com que les dades es guarden al navegador, si esborres la memòria cau (cache) o canvies de navegador, les dades que no hagis exportat es perdran. Es recomana exportar el ZIP al final de cada jornada.
- **Projecció:** L'aplicació calcula automàticament les coordenades X i Y en el sistema **EPSG:25831** (UTM 31N), molt utilitzat a Catalunya i Espanya.

---
Creat amb ❤️ per a treballs de camp eficients.