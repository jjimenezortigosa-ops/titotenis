# Construye juegos.json (datos para los juegos de TitoTenis) a partir de CSV de partidos ATP, jugadores.json,
# ranking.json, torneos.json e historial_base.json.
# Uso: python3 -I construir_juegos.py carpeta_repo salida.json a.csv b.csv ...
import csv, json, sys, unicodedata, re, os, datetime
def norm(s): return unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower()
ALIAS = {'yunchaokete bu':'bu yunchaokete','daniel merida':'daniel merida aguilar'}
def pk(n):
    s = re.sub(r'\s+',' ',norm(n).replace("'",'').replace('-',' ')).strip(); s = ALIAS.get(s,s)
    w = re.sub(r'[^a-z\s]',' ',s).split()
    return w[-1]+'|'+w[0][0] if w else ''
repo, out = sys.argv[1], sys.argv[2]
L = lambda f: json.load(open(os.path.join(repo,f),encoding='utf-8'))
jug = L('jugadores.json')['jugadores']; rk = L('ranking.json')['j']; tor = L('torneos.json')['torneos']; base = L('historial_base.json')
import collections as _c
_cnt = _c.Counter(pk(n) for n in jug)
canon = {}
for n in jug:
    if _cnt[pk(n)] == 1: canon[pk(n)] = n  # se excluyen apellido+inicial repetidos
info = {}  # pk -> (fecha, ioc, hand, ht, age)
for path in sys.argv[3:]:
    for r in csv.DictReader(open(path,encoding='utf-8')):
        for side in ('winner','loser'):
            k = pk(r[side+'_name'])
            if k not in canon: continue
            d = r['tourney_date']
            if k not in info or d >= info[k][0]:
                age = r[side+'_age']; ht = r[side+'_ht']
                old = info.get(k)
                info[k] = (d, r[side+'_ioc'] or (old[1] if old else ''), r[side+'_hand'] or (old[2] if old else ''),
                           ht or (old[3] if old else ''), age or (old[4] if old else ''))
rank = {canon.get(pk(x['n']), x['n']): x['r'] for x in rk if pk(x['n']) in canon}
try:
    for _n, _r in L('excepciones_ranking.json')['r'].items():
        if pk(_n) in canon and canon[pk(_n)] not in rank: rank[canon[pk(_n)]] = _r
except FileNotFoundError: pass
pool, idx = [], {}
for k, n in canon.items():
    if k not in info: continue
    _d, ioc, hand, ht, age = info[k]
    if not ioc: continue
    idx[n] = len(pool)
    d0 = datetime.date(int(_d[:4]), int(_d[4:6]), int(_d[6:8]))
    edad = round(float(age) + (datetime.date.today() - d0).days / 365.25) if age else 0
    pool.append([n, ioc, hand if hand in ('L','R') else '', int(float(ht)) if ht else 0, edad, rank.get(n, 0)])
crit = []
def add(cid, txt, names):
    ps = sorted({idx[n] for n in names if n in idx})
    if len(ps) >= 5: crit.append({'id': cid, 't': txt, 'p': ps})
# país
FLAG = {'ESP':'España','USA':'Estados Unidos','FRA':'Francia','ITA':'Italia','ARG':'Argentina','GER':'Alemania','AUS':'Australia','GBR':'Reino Unido','CAN':'Canadá','RUS':'Rusia','BRA':'Brasil','CZE':'Chequia','JPN':'Japón','CHI':'Chile','SRB':'Serbia','NED':'Países Bajos','POR':'Portugal','BEL':'Bélgica'}
for c, t in FLAG.items(): add('pais'+c, 'De '+t, [p[0] for p in pool if p[1]==c])
add('zurdo','Zurdo',[p[0] for p in pool if p[2]=='L'])
add('alto','Mide 1,95 m o más',[p[0] for p in pool if p[3]>=195])
add('bajo','Mide 1,80 m o menos',[p[0] for p in pool if 0<p[3]<=180])
add('top10','Top 10 actual',[p[0] for p in pool if 0<p[5]<=10])
add('top30','Top 30 actual',[p[0] for p in pool if 0<p[5]<=30])
add('top100','Top 100 actual',[p[0] for p in pool if 0<p[5]<=100])
add('joven','23 años o menos',[p[0] for p in pool if 0<p[4]<=23])
add('vet','30 años o más',[p[0] for p in pool if p[4]>=30])
# campeones (2025-26)
def cname(x): return canon.get(pk(x), None)
for lvl, t, mn in (('GS','Campeón de un Grand Slam (2025-26)',1),('1000','Campeón de un Masters 1000 (2025-26)',1),('500','Campeón de un ATP 500 (2025-26)',1),('250','Campeón de un ATP 250 (2025-26)',1)):
    add('camp'+lvl, t, [cname(x['cam']) for x in tor if x['nv']==lvl and x['cam'] and cname(x['cam'])])
add('campTierra','Campeón en tierra batida (2025-26)',[cname(x['cam']) for x in tor if x['s']=='tierra' and x['nv'] in ('GS','1000','500','250') and x['cam'] and cname(x['cam'])])
add('campHierba','Campeón en hierba (2025-26)',[cname(x['cam']) for x in tor if x['s']=='hierba' and x['cam'] and cname(x['cam'])])
add('campDura','Campeón en pista dura (2025-26)',[cname(x['cam']) for x in tor if x['s']=='dura' and x['cam'] and cname(x['cam'])])
add('finalista','Finalista de un Masters 1000 o Grand Slam (2025-26)',[cname(x['fin']) for x in tor if x['nv'] in ('GS','1000') and x['fin'] and cname(x['fin'])])
# ganó a ... (2023-26)
J = base['j']; surfname = {'d':'en pista dura','t':'en tierra','h':'en hierba'}
wins = {}  # (perdedor) -> {None:set, surf:set}
for d, s, ti, rd, w, l, sc in base['m']:
    wn, ln = cname(J[w]), cname(J[l])
    if not wn or not ln: continue
    wins.setdefault(ln, {}).setdefault('', set()).add(wn)
    wins[ln].setdefault(s, set()).add(wn)
for rv in ('Jannik Sinner','Carlos Alcaraz','Novak Djokovic','Alexander Zverev','Daniil Medvedev','Taylor Fritz','Casper Ruud','Stefanos Tsitsipas','Andrey Rublev','Ben Shelton'):
    if rv in wins:
        add('gana'+rv.split()[-1], 'Ha ganado a '+rv+' (desde 2023)', wins[rv].get('', []))
        for s in 'dth':
            add('gana'+rv.split()[-1]+s, 'Ha ganado a '+rv+' '+surfname[s], wins[rv].get(s, []))
json.dump({'actualizado': base.get('hasta',''), 'p': pool, 'c': crit}, open(out,'w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
print(len(pool), 'jugadores', len(crit), 'criterios')
for c in crit: print(c['id'], len(c['p']))
