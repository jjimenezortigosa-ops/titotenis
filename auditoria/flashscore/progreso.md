
## MÉTODO RÁPIDO set a set (flashscore.mobi) — usar en las siguientes pasadas
- `https://www.flashscore.mobi/match/<mid>/` (fetch mismo origen, ~0,3 s/partido, 4 en paralelo ≈ 10 partidos/s). La cabecera `<div class="detail"><b>2-1</b> (6-2,4-6,7-6)</div>` da juegos por set (local primero; sin puntos de tie-break). Los `mid` salen de `?mid=` en los enlaces de resultados de flashscore.com.
- Pasar datos entre orígenes: `window.name` sobrevive a la navegación .com → .mobi.
- Retiradas: FS muestra el set parcial (0-0), nosotros 'RET'; no es error.
- 2026: 1.005 partidos de 24 torneos comparados set a set: 1.002 coinciden, 2 retiradas (formato), 1 error real corregido (Alcaraz-Hanfmann AO R2: 7-6(4) 6-3 6-2, confirmado por ATP/AO/Sky). Faltan 34 torneos de 2026 por recopilar enlaces.
- Para 2025 y años pasados la URL de resultados es `https://www.flashscore.com/tennis/atp-singles/<torneo>-<año>/results/` (ej. `australian-open-2025`). Se comprobó que funciona.
- Problema visto: con iframes en paralelo (4) Flashscore devuelve páginas vacías y se atasca; en secuencial va a ~1 torneo cada 5 min (2025 entero = más de 4 h). Guardar cada torneo leído en localStorage del navegador (`RAW25`) por si la página se recarga: ya perdí una hora de lectura una vez porque la página se recargó. Una sola pasada de 2 h no basta para un año completo: reanudar leyendo localStorage y seguir donde se quedó.
- En la comparación, los partidos 'Retired'/WO salen con 0-0 en Flashscore: no son discrepancias. Las filas de clasificación no traen cabecera 'Qualification' en esta temporada: se distinguen por fecha anterior al primer partido del cuadro principal.
