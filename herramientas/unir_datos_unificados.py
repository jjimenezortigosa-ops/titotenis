"""Une las dos partes de datos_unificados en un solo JSON (para scripts de auditoría).
Uso: python3 herramientas/unir_datos_unificados.py  ->  datos_unificados/titotenis_datos_unificados.json (no se sube a Git, 35 MB)"""
import json,glob
ps=sorted(glob.glob('datos_unificados/titotenis_datos_unificados_parte*.json'))
d=json.load(open(ps[0]))
for p in ps[1:]: d['partidos']+=json.load(open(p))['partidos']
d['meta'].pop('parte',None)
json.dump(d,open('datos_unificados/titotenis_datos_unificados.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(d['partidos']),'partidos')
