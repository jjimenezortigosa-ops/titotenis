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
    edad = int(float(age) + (datetime.date.today() - d0).days / 365.25) if age else 0
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
def cname(x): return canon.get(pk(x), None)
# campeones 2023-26 (campeones.json) y listas variadas
import collections as _cc
try: _camp = L('campeones.json')['t']
except Exception: _camp = []
_tit = _cc.Counter(cname(x['cam']) for x in _camp if x.get('cam') and cname(x['cam']))
add('tit3','Ha ganado 3 torneos ATP o más (desde 2023)',[n for n,c in _tit.items() if c>=3])
add('tit6','Ha ganado más de 5 torneos ATP (desde 2023)',[n for n,c in _tit.items() if c>5])
_pre_gs = ('Stan Wawrinka','Marin Cilic','Dominic Thiem','Daniil Medvedev','Andy Murray','Novak Djokovic','Rafael Nadal','Roger Federer')
_pre_1000 = ('Holger Rune','Marin Cilic','Stan Wawrinka','Dominic Thiem','Taylor Fritz','Karen Khachanov','Grigor Dimitrov','Hubert Hurkacz','Alexander Zverev','Stefanos Tsitsipas','Daniil Medvedev','Novak Djokovic','Andy Murray')
add('campGS','Campeón de un Grand Slam',[cname(x['cam']) for x in _camp if x.get('nv')=='GS' and x.get('cam') and cname(x['cam'])]+[cname(n) for n in _pre_gs if cname(n)])
add('camp1000','Campeón de un Masters 1000',[cname(x['cam']) for x in _camp if x.get('nv')=='1000' and x.get('cam') and cname(x['cam'])]+[cname(n) for n in _pre_1000 if cname(n)])
add('camp500','Campeón de un ATP 500 (desde 2023)',[cname(x['cam']) for x in _camp if x.get('nv')=='500' and x.get('cam') and cname(x['cam'])])
add('camp250','Campeón de un ATP 250 (desde 2023)',[cname(x['cam']) for x in _camp if x.get('nv')=='250' and x.get('cam') and cname(x['cam'])])
add('campTierra','Campeón en tierra batida (desde 2023)',[cname(x['cam']) for x in _camp if x.get('s')=='tierra' and x.get('cam') and cname(x['cam'])])
add('campHierba','Campeón en hierba (desde 2023)',[cname(x['cam']) for x in _camp if x.get('s')=='hierba' and x.get('cam') and cname(x['cam'])])
add('campDura','Campeón en pista dura (desde 2023)',[cname(x['cam']) for x in _camp if x.get('s')=='dura' and x.get('cam') and cname(x['cam'])])
add('sinTitulo','Sin ningún título ATP desde 2023',[p[0] for p in pool if p[0] not in _tit and p[5] and p[5]<=60])
def _g(*ns): return [cname(n) for n in ns if cname(n)]
add('gsHist','Ha ganado un Grand Slam (en toda su carrera)',_g('Novak Djokovic','Carlos Alcaraz','Jannik Sinner','Daniil Medvedev','Stan Wawrinka','Dominic Thiem','Marin Cilic','Andy Murray','Rafael Nadal','Roger Federer','Juan Martin Del Potro','Andy Roddick','Marat Safin','Gaston Gaudio','Albert Costa','Juan Carlos Ferrero','Carlos Moya','Thomas Johansson','Lleyton Hewitt','Gustavo Kuerten','Andre Agassi','Pete Sampras','Alexander Zverev'))
add('exNum1','Ha sido número 1 del mundo',_g('Novak Djokovic','Carlos Alcaraz','Jannik Sinner','Daniil Medvedev','Andy Murray','Rafael Nadal','Roger Federer','Juan Carlos Ferrero','Carlos Moya','Lleyton Hewitt','Marat Safin','Andy Roddick','Andre Agassi','Pete Sampras'))
add('reves1','Revés a una mano',_g('Stan Wawrinka','Lorenzo Musetti','Stefanos Tsitsipas','Denis Shapovalov','Grigor Dimitrov','Dominic Thiem','Richard Gasquet','Daniel Altmaier','Christopher Oconnell','Dusan Lajovic','Aleksandar Kovacevic','Christopher Eubanks','Daniel Evans','Giovanni Mpetshi Perricard','Andrea Vavassori','Marco Cecchinato'))
add('nordico','Nórdico (Suecia, Noruega, Dinamarca o Finlandia)',[p[0] for p in pool if p[1] in ('SWE','NOR','DEN','FIN')])
add('sudam','Sudamericano',[p[0] for p in pool if p[1] in ('ARG','CHI','BRA','COL','PER','BOL','ECU','URU','PAR')])
add('balcan','De los Balcanes',[p[0] for p in pool if p[1] in ('SRB','CRO','BIH','MNE','SLO','MKD','BUL')])
add('hispano','Habla español',[p[0] for p in pool if p[1] in ('ESP','ARG','CHI','COL','PER','MEX','ECU','BOL','URU','DOM','VEN','PAR')])
add('anglo','Anglosajón (EE. UU., Reino Unido, Australia, Canadá)',[p[0] for p in pool if p[1] in ('USA','GBR','AUS','CAN')])
# ganó a ... (2023-26)
J = base['j']; surfname = {'d':'en pista dura','t':'en tierra','h':'en hierba'}
wins = {}  # (perdedor) -> {None:set, surf:set}
for d, s, ti, rd, w, l, sc in base['m']:
    wn, ln = cname(J[w]), cname(J[l])
    if not wn or not ln: continue
    if d < '2026-01-01': continue
    wins.setdefault(ln, {}).setdefault('', set()).add(wn)
    wins[ln].setdefault(s, set()).add(wn)
for rv in ('Jannik Sinner','Carlos Alcaraz','Novak Djokovic','Alexander Zverev','Daniil Medvedev','Taylor Fritz','Casper Ruud','Stefanos Tsitsipas','Andrey Rublev','Ben Shelton'):
    if rv in wins:
        add('gana'+rv.split()[-1], 'Ha ganado a '+rv+' en 2026', wins[rv].get('', []))
        for s in 'dth':
            add('gana'+rv.split()[-1]+s, 'Ha ganado a '+rv+' '+surfname[s]+' en 2026', wins[rv].get(s, []))
json.dump({'actualizado': base.get('hasta',''), 'p': pool, 'c': crit}, open(out,'w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
print(len(pool), 'jugadores', len(crit), 'criterios')
for c in crit: print(c['id'], len(c['p']))
