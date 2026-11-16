# TitoTenis · Base de datos unificada (1990–2021)

Archivo único: `titotenis_datos_unificados.json` (17,8 MB). Generado la madrugada del 17-nov-2026.

## Qué contiene
- `partidos`: 102.160 partidos ATP individuales de Flashscore (columnas en `columnas`). 78.467 son del cuadro principal y 23.693 de clasificación (campo `cuadro`).
- `campeones_por_torneo`: 1.812 finales del cuadro principal. `campeones_grand_slam`: 122 finales de Grand Slam.
- `jugadores`: victorias, derrotas, títulos, finales y Slams por jugador (solo cuadro principal y partidos con estado "Finished").
- `resumen_por_anio`, `huecos`, `verificacion`, `comparacion_campeones`, `meta`.

## Qué está verificado y qué no (sin adornos)
- **Todo viene de una sola fuente (Flashscore)**, salvo 5 partidos contrastados con una segunda fuente (4 corregidos, 1 confirmado). **No está verificado al 100 %.**
- Comprobaciones internas: cero ids duplicados, cero nombres vacíos, sets coherentes con el detalle en todo el cuadro principal salvo 1 caso ya explicado (Moya–Safin 2003, retirada).
- Comparado con `campeones_2010_2022.json` (lo que ya usa la web): de 740 finales 2010–2021, 664 coinciden en campeón, finalista y marcador; el resto se explica en `comparacion_campeones`.

## Lo que falta (huecos reales)
1. **307 torneos sin datos** (lista por año en `huecos.torneos_sin_datos_por_anio`; 2003 tiene 20 y 1990–2003 es lo peor).
2. **5 Grand Slams ausentes**: Australian Open 1995, Wimbledon 2001, 2002 y 2003, Roland Garros 2003.
3. **2022–2026 no están en este archivo.** De 2023–2026 solo existen informes de comparación y los datos de la web.
4. 550 partidos sin detalle de sets (casi todos walkovers y retiradas).
5. Ganador solo si el estado es "Finished" (97 %). En retiradas/walkovers no se deduce.
6. Jugadores identificados por "Apellido I." (no hay id): puede mezclar homónimos.
7. Algunas fechas vienen vacías porque Flashscore puso otro texto (p. ej. "Limited number of spectators").

## Para arreglar en la web (campeones.json)
- Torneos que empiezan el 29–31 dic están en la temporada anterior: Brisbane 2012/2013/2018, Chennai 2012, Doha 2012/2018, Pune 2018.
- Revisar Stuttgart 2010 (Montañés–Monfils, retirada).
