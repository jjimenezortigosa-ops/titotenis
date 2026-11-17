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

## Actualización 17-nov (mañana): 2022–2026 incluidos
- **2022**: 3.801 partidos de Flashscore (set a set), cuadro principal 2.529 y clasificación 1.272. Recuperados con otra dirección: US Open, Winston-Salem, Adelaide 2, NextGen Finals, Belgrado, Florencia, Gijón, San Diego, Seúl, Sídney, Tel Aviv. **Siguen sin datos: Melbourne y Nápoles** (Lyon descartado: la página sin año era de 2026). Sin segunda fuente.
- **2023–2026**: 10.592 partidos del cuadro principal tomados de `campeones.json` (los datos de la propia web), marcados `WEB_SITIO`. Nombre completo del jugador y fecha = inicio del torneo; sin clasificación. Comparados set a set con Flashscore en `auditoria/flashscore/informe_20xx_sets.md` (0 diferencias reales en 2023–2025).
- Los nombres de 2023–2026 (completos) no coinciden con los de 1990–2022 ("Apellido I."): para estadísticas por jugador hay que unificarlos antes.

## Actualización 17-nov (10:30): torneos recuperados de Wikipedia
- Fuente `WIKIPEDIA` (cuadro principal, nombre completo, sin fecha ni id): 2022 Lyon y Melbourne; 2021 Antalya, Singapur, Cagliari, Marbella, Lyon, Moscú y San Petersburgo (247 partidos). Comprobadas las finales: coinciden con los campeones reales que conozco (p. ej. Popyrin en Singapur, Sonego en Cagliari, Karatsev en Moscú, Nadal en Melbourne 2022).
- La final de Antalya 2021 solo trae sets ganados (0-2) en Wikipedia.
- Siguen sin datos 2021: Great Ocean Road Open, Murray River Open, Parma, NextGen Finals; 2022: Nápoles.

## Actualización 17-nov (tarde): 8 torneos más desde Wikipedia
Añadidos (224 partidos, fuente WIKIPEDIA): ATP Lyon 2017, 2018, 2019; Memphis 2017; Düsseldorf 2014; Bogotá 2015; Kuala Lumpur 2015; San Francisco 1992. Al revisar los avisos de "huecos", la mayoría (~230 de 282) eran el mismo torneo con otro nombre; quedan ~40 por comprobar a mano (Atlanta 1992–99, Génova 1992, Zaragoza 1994, Tashkent 2002, Parma/NextGen 2021, etc.). No es un 100% verificado.

## Actualización 17-nov (mediodía): barrido completo contra Wikipedia 1990–2021
Se leyeron 1.379 páginas "Singles" de Wikipedia (calendario ATP de cada año) y se comprobó que la final de cada torneo estuviera en el fichero. Resultado: 56 torneos con cuadro principal faltaban del todo (San Francisco 1990/91, Chevrolet Classic/Guarujá, Banespa, Maceió, US Clay Court, Hamlet Cup, Lyon 1991/99/2001/02/03/07, Kremlin Cup 93/02/03, Shanghai 98/99/01, Tata Open 2019, Istanbul/Shenzhen/Sibiu 2018, etc.). Añadidos desde Wikipedia (fuente WIKIPEDIA, nombres completos, sin fecha). Quedan por comprobar partidos sueltos dentro de torneos ya presentes.

## Actualización 17-nov (13:00): 178 torneos más desde Wikipedia (5.842 partidos)
Segundo barrido, esta vez partido a partido contra ~1.860 páginas de Wikipedia 1990–2026. Torneos de cuadro principal que no estaban en el fichero (sobre todo 1990–1997: Hamlet Cup, Tokyo Indoor, Kremlin Cup, Lyon, Newsweek/Indian Wells, Eurocard, Athens, Halle 1993, etc., y varios 2005–2010 y 2013–2021) añadidos con fuente WIKIPEDIA. Ya hay 251 torneos de Wikipedia (8.041 partidos). Pendiente: Great Ocean Road y Murray River 2021 (el lector falla), y unas 1.200 discrepancias dentro de torneos ya presentes (mayormente nombres escritos distinto, p.ej. Pashanski/Pašanski) que se listarán aparte.

## Actualización 17-nov (tarde): segunda fuente (Wikipedia) en TODO el fichero
- Se añadieron 3 torneos de 2011 (Johannesburgo, Costa do Sauípe, Kuala Lumpur), Great Ocean Road y Murray River 2021 (ya arreglados), 68 torneos de 1998–2004 y 178 de otros años. Total de torneos tomados de Wikipedia: ~320.
- 398 partidos sueltos que faltaban dentro de torneos de Flashscore se completaron con Wikipedia (fuente `WIKIPEDIA_COMPLEMENTO`).
- Nueva columna `segunda_fuente` en cada partido: "Wikipedia: mismo marcador" (83.313 partidos, set a set), "Wikipedia: marcador distinto (…)" (939: aquí Flashscore y Wikipedia no coinciden; revisar a mano), "solo Wikipedia" o vacío (sin comparar: qualy, rondas que Wikipedia no detalla, 2023–2026 que vienen de la web propia).
- Lista de las discrepancias: `auditoria/discrepancias_marcadores_wikipedia.json`.
- Qué NO está comprobado: ~33.600 partidos sin segunda fuente (principalmente clasificación y 2023–2026), y los partidos donde las dos fuentes se equivocan igual. Wikipedia no es infalible.

## Actualización 17-nov (tarde, final): nombres unificados y estadísticas rehechas
- Los nombres de 2023+ y de Wikipedia (nombre completo) se pasaron al formato de Flashscore "Apellido I." para poder sumar estadísticas del mismo jugador entre 1990 y 2026. El nombre original queda en la columna `nombres_originales`; el bloque `jugadores_alias` lista las variantes de cada jugador.
- Límite conocido: "Apellido I." no es un identificador único (p. ej. "Martin A." mezcla a Alberto, Andrej y Andrés Martín; "Silva J.", "Martin D."). Los 214 jugadores que no estaban en Flashscore se generaron con una regla (última palabra = apellido) y pueden tener errores.
- Se rehicieron `campeones_por_torneo` (2.581 finales), `campeones_grand_slam` (147, con 3 en 2020 por Wimbledon cancelado), `jugadores` (2.506) y `resumen_por_anio`. Comprobación rápida: Federer 20 Grand Slams, Nadal 22, Djokovic 24.
- No incluidos por no ser cuadros de eliminación directa o no ser ATP Tour: ATP Finals/Masters Cup (liguilla), NextGen Finals, Juegos Olímpicos, Copa Davis, Laver Cup, United Cup, Challengers. Por eso los títulos de Federer salen 97 (103 reales, 6 de ellos en ATP Finals).
