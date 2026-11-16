# TitoTenis · Base de datos unificada (1990–2021)

Archivo único: `titotenis_datos_unificados.json` (17,8 MB). Generado la madrugada del 17-nov-2026.

## Qué contiene
- `partidos`: 103.469 partidos ATP individuales de Flashscore (columnas en `columnas`). 79.243 son del cuadro principal y 24.226 de clasificación (campo `cuadro`).
- `campeones_por_torneo`: 1.820 finales del cuadro principal. `campeones_grand_slam`: 127 finales de Grand Slam (4 por año, 3 en 2020).
- `jugadores`: victorias, derrotas, títulos, finales y Slams por jugador (solo cuadro principal).
- `resumen_por_anio`, `huecos`, `verificacion`, `comparacion_campeones`, `meta`.

## Qué está verificado y qué no (sin adornos)
- **Todo viene de una sola fuente (Flashscore)**, salvo 5 partidos contrastados con una segunda fuente (4 corregidos, 1 confirmado). **No está verificado al 100 %.**
- Comprobaciones internas: cero ids duplicados, cero nombres vacíos, sets coherentes con el detalle en todo el cuadro principal salvo 2 casos (Moya–Safin 2003, que es retirada y está bien, y Lapentti–Carlsen Wimbledon 2003, sin verificar).
- Sanity check: con estos datos Federer sale con 20 Slams, Nadal 20, Djokovic 20, Agassi 8 y Sampras 14, igual que en la realidad.
- El ganador de retiradas/walkovers es el jugador nombrado en el estado de Flashscore (comprobado: en 2.975 de 3.023 casos concluyentes ese jugador pasa de ronda).
- Comparado con `campeones_2010_2022.json` (lo que ya usa la web): de 740 finales 2010–2021, 676 coinciden en campeón, finalista y marcador; el resto se explica en `comparacion_campeones`.

## Lo que falta (huecos reales)
1. **304 torneos sin datos** (lista por año en `huecos.torneos_sin_datos_por_anio`; 2003 tiene 20 y 1990–2003 es lo peor).
2. Los 5 Grand Slams que faltaban se recuperaron (Australian Open 1995, Wimbledon 2001–2003, Roland Garros 2003).
3. **2022–2026 no están en este archivo.** De 2023–2026 solo existen informes de comparación y los datos de la web.
4. 554 partidos sin detalle de sets (casi todos walkovers y retiradas).
5. Ganador desconocido en 21 partidos.
6. Jugadores identificados por "Apellido I." (no hay id): puede mezclar homónimos.
7. Algunas fechas vienen vacías porque Flashscore puso otro texto (p. ej. "Limited number of spectators").

## Para arreglar en la web (campeones.json)
- Torneos que empiezan el 29–31 dic están en la temporada anterior: Brisbane 2012/2013/2018, Chennai 2012, Doha 2012/2018, Pune 2018.


Nota 17-nov: se recuperaron además Los Cabos 2018, New York Open 2019 y Belgrado (Serbia Open) 2021. Los otros torneos de 2017–2021 se probaron con varias direcciones y Flashscore no devuelve datos (probablemente no los tiene).
