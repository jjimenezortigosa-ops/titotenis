# Construye torneos.json, evolucion.json y estadisticas.json a partir de CSV de partidos ATP (formato TML/Sackmann).
# Uso: python3 -I construir_datos.py jugadores.json carpeta_salida 2025:a.csv 2026:b.csv 2026:ongoing.csv
import csv, json, sys, unicodedata, re, os
def norm(s): return unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower()
def pk(n):
    w = re.sub(r'[^a-z\s-]',' ',norm(n)).split()
    return w[-1]+'|'+w[0][0] if w else ''
jug = json.load(open(sys.argv[1],encoding='utf-8'))['jugadores']
mine = {pk(n) for n in jug}
out = sys.argv[2]
SURF = {'Hard':'dura','Carpet':'dura','Clay':'tierra','Grass':'hierba'}
LEVEL = {'G':'GS','M':'1000','500':'500','250':'250','F':'Finales'}
NO_TITLE = ('United Cup','Laver Cup')
rows, seen = [], set()
perfile_dates = {}
for arg in sys.argv[3:]:
    season, path = arg.split(':',1)
    season = int(season)
    for r in csv.DictReader(open(path,encoding='utf-8')):
        if r['tourney_name'].startswith('Davis Cup') or r['tourney_level']=='D': continue
        if r['surface'] not in SURF: continue
        k = (season, r['tourney_id'], r['match_num'])
        if k in seen: continue
        seen.add(k); r['_s'] = season; rows.append(r)
def iso(d): return d[:4]+'-'+d[4:6]+'-'+d[6:]
# ---------- torneos ----------
T = {}
for r in rows:
    k = (r['_s'], r['tourney_id'])
    t = T.setdefault(k, {'k':str(r['_s'])+'-'+r['tourney_id'],'a':r['_s'],'n':r['tourney_name'],'nv':LEVEL.get(r['tourney_level'],'Otros'),'s':SURF[r['surface']],'c':r['indoor']=='I','d1':r['tourney_date'],'d2':r['tourney_date'],'dr':r['draw_size'],'cam':'','fin':'','mar':'','np':0})
    t['d1'] = min(t['d1'], r['tourney_date']); t['d2'] = max(t['d2'], r['tourney_date']); t['np'] += 1
    if r['round']=='F' and r['tourney_name'] not in NO_TITLE and 'vs' not in r['tourney_name']:
        t['cam'], t['fin'], t['mar'] = r['winner_name'], r['loser_name'], r['score']
tor = sorted(T.values(), key=lambda t:(t['d1'], t['n']))
for t in tor:
    t['d1'] = iso(t['d1']); t['d2'] = iso(t['d2'])
    if t['d2'] == t['d1']: t['d2'] = ''
json.dump({'torneos':tor}, open(os.path.join(out,'torneos.json'),'w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
# ---------- cuadros (partidos de cada torneo) ----------
ORD = {'R128':0,'R64':1,'R32':2,'R16':3,'RR':3,'QF':4,'SF':5,'BR':5,'F':6}
C = {}
for r in rows:
    if r['score'] in ('', 'W/O') or 'W/O' in r['score'] or r['round'] not in ORD: continue
    C.setdefault(str(r['_s'])+'-'+r['tourney_id'], []).append([r['round'], r['winner_name'], r['loser_name'], r['score'], int(r['match_num'] or 0)])
for k in C: C[k].sort(key=lambda m:(ORD[m[0]], m[4]))
json.dump(C, open(os.path.join(out,'cuadros.json'),'w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
# ---------- evolución del ranking ----------
E = {}
first = {}
for r in rows:
    d = r['tourney_date']
    for side in ('winner','loser'):
        n = r[side+'_name']
        if pk(n) not in mine: continue
        rk = r[side+'_rank']
        if not rk: continue
        key = (n, r['_s'], r['tourney_id'])
        cur = first.get(key)
        cand = (d, int(r['match_num'] or 0), int(rk), int(r[side+'_rank_points'] or 0))
        if cur is None or cand[:2] < cur[:2]: first[key] = cand
for (n,s,tid),(d,_,rk,pt) in first.items():
    E.setdefault(n, []).append([iso(d), rk, pt])
for n in list(E):
    E[n].sort()
    # un punto por fecha (el último de la fecha)
    dd = {}
    for p in E[n]: dd[p[0]] = p
    E[n] = list(dd.values())
    if len(E[n]) < 2: del E[n]
json.dump({'j':E}, open(os.path.join(out,'evolucion.json'),'w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
# ---------- estadísticas de la temporada actual ----------
cur = max(r['_s'] for r in rows)
S = {}
def num(x):
    try: return int(x)
    except: return None
def P(n):
    return S.setdefault(n, {'pj':0,'g':0,'d':[0,0],'t':[0,0],'h':[0,0],'tit':0,'fin':0,'ps':0,'ac':0,'df':0,'sv':0,'i1':0,'w1':0,'w2':0,'bs':0,'bf':0,'rp':0,'rt':0,'bc':0,'bo':0})
for r in rows:
    if r['_s'] != cur: continue
    sf = SURF[r['surface']][0]
    W, L = r['winner_name'], r['loser_name']
    ok = all(num(r[c]) is not None for c in ('w_svpt','l_svpt','w_1stIn','l_1stIn','w_1stWon','l_1stWon','w_2ndWon','l_2ndWon','w_ace','l_ace','w_df','l_df','w_bpSaved','l_bpSaved','w_bpFaced','l_bpFaced'))
    for me, op, won, px in ((W,L,True,'w'),(L,W,False,'l')):
        if pk(me) not in mine: continue
        p = P(me); p['pj'] += 1
        if won: p['g'] += 1
        p[sf][0 if won else 1] += 1
        if r['round']=='F' and r['tourney_name'] not in NO_TITLE:
            p['fin'] += 1
            if won: p['tit'] += 1
        if ok:
            qx = 'l' if px=='w' else 'w'
            g = lambda s,c: num(r[s+'_'+c])
            p['ps'] += 1; p['ac'] += g(px,'ace'); p['df'] += g(px,'df'); p['sv'] += g(px,'svpt'); p['i1'] += g(px,'1stIn'); p['w1'] += g(px,'1stWon'); p['w2'] += g(px,'2ndWon')
            p['bs'] += g(px,'bpSaved'); p['bf'] += g(px,'bpFaced')
            p['rt'] += g(qx,'svpt'); p['rp'] += g(qx,'svpt') - g(qx,'1stWon') - g(qx,'2ndWon')
            p['bo'] += g(qx,'bpFaced'); p['bc'] += g(qx,'bpFaced') - g(qx,'bpSaved')
json.dump({'temporada':cur,'j':S}, open(os.path.join(out,'estadisticas.json'),'w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
print('torneos',len(tor),'evolucion',len(E),'estadisticas',len(S),'temporada',cur)
