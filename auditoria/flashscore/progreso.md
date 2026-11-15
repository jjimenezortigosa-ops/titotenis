# Progreso de la auditoría con Flashscore

Orden: 2026, 2025, 2024 ... 2010. Una pasada = un año. Una pasada programada cada 2 horas.

- 2026: EN CURSO, lo hace la sesión principal con Javier. NO lo hagas tú, empieza por el siguiente año pendiente (2025).

## NOTAS IMPORTANTES PARA CADA PASADA (leer antes de empezar)
- Hay una receta probada en `auditoria/flashscore/metodo_flashscore.js`: lee Flashscore en iframes del mismo origen y compara contra nuestros datos dentro del navegador, devolviendo solo las diferencias. Úsala en vez de ir torneo a torneo.
- Nuestros datos se cargan con fetch a `https://raw.githubusercontent.com/jjimenezortigosa-ops/titotenis/main/campeones.json` (CORS permitido). El de workers.dev NO funciona.
- La herramienta javascript_tool corta a los 45 s: lanza el proceso en segundo plano y consulta `RES`, `LOG` y `DONE` cada 30 s.
- NO guardes las filas crudas de Flashscore en el repositorio (solo el informe con cifras y las discrepancias). Son datos de un tercero y la web no debe copiarlos.
- Las filas de clasificación (qualification) salen como `sin_nombre`: ignóralas, no son discrepancias.
- Para años pasados la página `/results/` solo muestra la última temporada: entra por `/archive/` del torneo y abre la temporada del año.
- 2023-2026 se comparan partido a partido con campeones.json. 2010-2022 solo tienen campeón, finalista y marcador de la final (campeones_2010_2022.json).
