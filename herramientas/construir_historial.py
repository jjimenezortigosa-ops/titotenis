# Construye historial_base.json a partir de CSV de partidos ATP (formato TML/Sackmann).
# Uso: python3 -I construir_historial.py jugadores.json salida.json 2023.csv 2024.csv ... ongoing.csv
import csv, json, sys, unicodedata, re
def norm(s): return unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower()
def pk(n):
    w = re.sub(r'[^a-z\s-]',' ',norm(n)).split()
    return w[-1]+'|'+w[0][0] if w else ''
jug = json.load(open(sys.argv[1],encoding='utf-8'))['jugadores']
mine = {pk(n) for n in jug}
SURF = {'Hard':'d','Carpet':'d','Clay':'t','Grass':'h'}
ROUND = {'F':'Final','SF':'Semifinal','QF':'Cuartos','R16':'Octavos','R32':'1/16','R64':'1/32','R128':'1/64','RR':'Fase de grupos','BR':'Bronce'}
rows, seen = [], set()
for f in sys.argv[3:]:
    for r in csv.DictReader(open(f,encoding='utf-8')):
        t = r['tourney_name']
        if t.startswith('Davis Cup') or 'W/O' in r['score'] or 'Walkover' in r['score'] or not r['score'].strip(): continue
        if pk(r['winner_name']) not in mine and pk(r['loser_name']) not in mine: continue
        if r['surface'] not in SURF: continue
        k = (r['tourney_id'], r['match_num'])
        if k in seen: continue
        seen.add(k)
        d = r['tourney_date']
        rows.append((d, SURF[r['surface']], t, ROUND.get(r['round'], r['round']), r['winner_name'], r['loser_name'], r['score'].strip(), r['tourney_id'], int(r['match_num'] or 0)))
rows.sort(key=lambda x:(x[0], x[7], x[8]))
names, tours = {}, {}
def idx(d, v): 
    if v not in d: d[v] = len(d)
    return d[v]
m = []
for d,s,t,rd,w,l,sc,_,_ in rows:
    m.append([d[:4]+'-'+d[4:6]+'-'+d[6:], s, idx(tours,t), rd, idx(names,w), idx(names,l), sc])
out = {'hasta': m[-1][0] if m else '', 'fuente': 'TML-Database (Tennismylife), uso no comercial', 'j': list(names), 't': list(tours), 'm': m}
json.dump(out, open(sys.argv[2],'w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
print(len(m), 'partidos', len(names), 'jugadores', out['hasta'])
