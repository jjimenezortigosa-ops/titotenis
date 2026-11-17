
## MÉTODO RÁPIDO set a set (flashscore.mobi) — usar en las siguientes pasadas
- `https://www.flashscore.mobi/match/<mid>/` (fetch mismo origen, ~0,3 s/partido, 4 en paralelo ≈ 10 partidos/s). La cabecera `<div class="detail"><b>2-1</b> (6-2,4-6,7-6)</div>` da juegos por set (local primero; sin puntos de tie-break). Los `mid` salen de `?mid=` en los enlaces de resultados de flashscore.com.
- Pasar datos entre orígenes: `window.name` sobrevive a la navegación .com → .mobi.
- Retiradas: FS muestra el set parcial (0-0), nosotros 'RET'; no es error.
- 2026: 1.005 partidos de 24 torneos comparados set a set: 1.002 coinciden, 2 retiradas (formato), 1 error real corregido (Alcaraz-Hanfmann AO R2: 7-6(4) 6-3 6-2, confirmado por ATP/AO/Sky). Faltan 34 torneos de 2026 por recopilar enlaces.
- Para 2025 y años pasados la URL de resultados es `https://www.flashscore.com/tennis/atp-singles/<torneo>-<año>/results/` (ej. `australian-open-2025`). Se comprobó que funciona.
- Problema visto: con iframes en paralelo (4) Flashscore devuelve páginas vacías y se atasca; en secuencial va a ~1 torneo cada 5 min (2025 entero = más de 4 h). Guardar cada torneo leído en localStorage del navegador (`RAW25`) por si la página se recarga: ya perdí una hora de lectura una vez porque la página se recargó. Una sola pasada de 2 h no basta para un año completo: reanudar leyendo localStorage y seguir donde se quedó.
- En la comparación, los partidos 'Retired'/WO salen con 0-0 en Flashscore: no son discrepancias. Las filas de clasificación no traen cabecera 'Qualification' en esta temporada: se distinguen por fecha anterior al primer partido del cuadro principal.

## Estado set a set
- 2026: HECHO (2.547 partidos, 2 errores corregidos). Informe: informe_2026_sets.md
- 2025: HECHO salvo Marseille, Atenas, Metz, Canada Masters (0 errores en 2.443 partidos). Informe: informe_2025_sets.md
- Siguiente: 2024 (URLs de temporada pasada: /tennis/atp-singles/<slug>-<año>/results/; Canada Masters -> toronto-<año>/montreal-<año> según año). Recoger 1 torneo ≈ 1 min en iframe (uno a uno; en paralelo se satura). Comparar luego en flashscore.mobi (10 partidos/s). Pasar datos .com -> .mobi con window.name.
- 2024: HECHO salvo Córdoba, Lyon, Newport, Atlanta, Amberes, Belgrado (0 errores en 2.507 partidos). Informe: informe_2024_sets.md

2023 set a set: HECHO salvo Adelaide-1, Pune, Banja Luka, Lyon, Sofia, Astana, Zhuhai. 0 errores reales.

## Descarga histórica Flashscore (2004–2021) — copia de seguridad 16-nov-2026
- Fichero: datos/flashscore_2004_2021.json (clave por año; cada año: slugs, err, t{torneo:[[ronda,local,visitante,sh,sa,sets,estado,fecha,mid]]}). 2003 solo parcial (clave 2003_parcial_F, formato de fase 1, sin sets).
- Partidos por año (con sets): 2004 2904, 2005 2953, 2006 3046, 2007 3054, 2008 2821, 2009 3165, 2010 3515, 2011 4404, 2012 4336, 2013 4171, 2014 4229, 2015 4206, 2016 3806, 2017 3825, 2018 3704, 2019 3626, 2020 1731, 2021 3293.
- Torneos con error (0 filas) por reintentar al final: ver campo err de cada año. Incluye 2005: Milán, Salvador, Scottsdale, Ho Chi Minh, Lyon, Masters Cup.
- Las filas pueden incluir clasificación (tras la 2ª 'Final'). Retiradas: ganador no derivable de sh/sa.
- PENDIENTE: terminar 2003 y bajar hasta 1990; reintentos; comparar finales con campeones_2010_2022.json; informe de discrepancias.

## 16 nov 2026 (noche) – Descarga completa 1990–2021
- `datos/flashscore_1990_2021.json`: 102.160 partidos ATP individuales con sets (Flashscore), 32 años. Formato por año: `{year,slugs,err,t:{torneo:[[ronda,local,visitante,sets_l,sets_v,sets,estado,fecha,id],...]}}`.
- Torneos sin datos (campo `err`): por año ~2–22 (sobre todo 1990–2003, nombres/torneos que Flashscore no tiene). Pendiente: reintento con otros nombres + 2ª fuente.
- Avisos: filas de clasificación mezcladas (tras el segundo "Final"), algunos partidos sin sets (5–18/año). Aún NO verificado contra segunda fuente.

## 17 nov 2026 (madrugada) – Archivo único
- `datos_unificados/titotenis_datos_unificados.json` + `LEEME.md`: partidos 1990–2021 con cuadro principal/clasificación separados, campeones, Slams, jugadores, huecos y comparación con campeones.json. 4 marcadores corregidos con 2ª fuente (Indian Wells 2001/2005/2006, Vienna 2003).
- Hallazgos: 5 Grand Slams ausentes (AO 1995, W 2001/2002/2003, RG 2003); campeones.json pone en la temporada anterior los torneos que empiezan 29–31 dic.
- Pendiente: reintentar los 307 torneos sin datos y los 5 Slams (necesita el navegador), añadir 2022–2026, verificar con 2ª fuente el resto.

- CORRECCIÓN 17-nov: en el estado `Finished / retired - X` y `Walkover - X`, X es el GANADOR (no el que se retira). Comprobado con el cuadro: 2.975 vs 48. El aviso anterior de que el ganador de retiradas no es derivable era erróneo.
- 5 Grand Slams ausentes recuperados: `datos/flashscore_5slams_ausentes.json` (AO 1995, W 2001/2002/2003, RG 2003). Con ellos Federer 20, Nadal 20, Djokovic 20, Agassi 8, Sampras 14 Slams.
- 17 nov: recuperados Los Cabos 2018, New York Open 2019, Serbia Open 2021 (datos/flashscore_recuperados_2018_2021.json). Probados sin éxito (0 filas): Chennai/Memphis/Lyon 2017, Quito/Istanbul/Lyon/Shenzhen 2018, Sao Paulo/Budapest/Lyon 2019, New York/Cologne 1-2/Sardinia 2020, Antalya/Great Ocean Road/Murray River/Singapore/Cagliari/Marbella/Lyon/Parma/Moscow/St. Petersburg/NextGen 2021. Truco de transferencia: los blobs descargados quedan completos como .tmp en Descargas y se pueden leer sin pulsar nada.

## 17 nov 2026 (mañana) – 2022 y 2023-2026 en el unificado
- `datos/flashscore_2022.json` ahora tiene los 3.215 partidos con sets (antes solo 110 filas). `flashscore_2022_reintentos.json`: US Open, Winston-Salem, Adelaide-2, NextGen + Belgrado, Florencia, Gijón, San Diego, Seúl, Sídney, Tel Aviv.
- Truco: las últimas ediciones de algunos torneos están en la dirección SIN año (`/tennis/atp-singles/tel-aviv/`). Hay que comprobar el año por las fechas (Lyon sin año = 2026, descartado).
- Sigue sin cargar: Melbourne, Nápoles 2022.
- Descarga a Descargas: solo funciona con el nombre `flashscore_2022.json`; otros nombres no llegaban.
