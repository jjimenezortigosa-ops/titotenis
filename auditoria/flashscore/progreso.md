
## MÉTODO RÁPIDO set a set (flashscore.mobi) — usar en las siguientes pasadas
- `https://www.flashscore.mobi/match/<mid>/` (fetch mismo origen, ~0,3 s/partido, 4 en paralelo ≈ 10 partidos/s). La cabecera `<div class="detail"><b>2-1</b> (6-2,4-6,7-6)</div>` da juegos por set (local primero; sin puntos de tie-break). Los `mid` salen de `?mid=` en los enlaces de resultados de flashscore.com.
- Pasar datos entre orígenes: `window.name` sobrevive a la navegación .com → .mobi.
- Retiradas: FS muestra el set parcial (0-0), nosotros 'RET'; no es error.
- 2026: 1.005 partidos de 24 torneos comparados set a set: 1.002 coinciden, 2 retiradas (formato), 1 error real corregido (Alcaraz-Hanfmann AO R2: 7-6(4) 6-3 6-2, confirmado por ATP/AO/Sky). Faltan 34 torneos de 2026 por recopilar enlaces.
