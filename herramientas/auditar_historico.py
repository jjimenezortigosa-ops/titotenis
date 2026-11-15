# Audita partidos ATP 2010-2022 (TML) y saca campeones por torneo. Uso: auditar_historico.py salida_json salida_md csv...
import csv, json, sys, re, collections as C
LV={'G':'GS','M':'1000','500':'500','250':'250','A':'500'}
rows=[]
for p in sys.argv[3:]:
    for r in csv.DictReader(open(p,encoding='utf-8')):
        if r.get('tourney_level') in LV: rows.append(r)
def sets(sc):
    out=[]
    for s in sc.replace('RET','').replace('DEF','').replace('W/O','').split():
        m=re.match(r'^(\d+)-(\d+)',s)
        if m: out.append((int(m.group(1)),int(m.group(2))))
    return out
prob=C.Counter(); ej=collections=C.defaultdict(list)
dup=set(); seen=set(); T=C.defaultdict(list)
for r in rows:
    T[r['tourney_id']].append(r)
    k=(r['tourney_id'],r['round'],r['winner_name'],r['loser_name'])
    if k in seen: prob['duplicado']+=1; ej['duplicado'].append(k)
    seen.add(k)
    sc=r['score']
    if any(x in sc for x in('RET','W/O','DEF')) or not sc: continue
    ss=sets(sc); w=sum(a>b for a,b in ss); l=sum(b>a for a,b in ss)
    bo=int(r['best_of'] or 0)
    if w<=l: prob['ganador sin ganar más sets']+=1; ej['ganador sin ganar más sets'].append((r['tourney_id'],r['winner_name'],r['loser_name'],sc))
    if bo and w!=(bo+1)//2: prob['sets ganados != best_of']+=1; ej['sets ganados != best_of'].append((r['tourney_id'],r['winner_name'],r['loser_name'],sc,bo))
champs=[]; nofinal=[]; multi=[]
for tid,ms in T.items():
    f=[m for m in ms if m['round']=='F']
    r0=ms[0]; y=r0['tourney_date'][:4]
    if len(f)!=1: (nofinal if not f else multi).append((tid,r0['tourney_name'],y,len(f))); continue
    champs.append({'a':int(y),'n':r0['tourney_name'],'nv':LV[r0['tourney_level']],'d':r0['tourney_date'],'cam':f[0]['winner_name'],'fin':f[0]['loser_name'],'sc':f[0]['score'],'pj':len(ms)})
champs.sort(key=lambda x:(x['a'],x['d'],x['n']))
json.dump(champs,open(sys.argv[1],'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
yrs=C.Counter(int(r['tourney_date'][:4]) for r in rows)
L=['# Auditoría de partidos ATP 2010-2022 (TML)','',f'Partidos: {len(rows)} · torneos: {len(T)} · campeones obtenidos: {len(champs)}','','## Partidos por año']
L+=[f'- {y}: {n}' for y,n in sorted(yrs.items())]
L+=['','## Problemas detectados']+[f'- {k}: {v}' for k,v in prob.items()] or ['- ninguno']
if not prob: L.append('- ninguno en marcadores')
L+=[f'- torneos sin final registrada: {len(nofinal)}',f'- torneos con más de una final: {len(multi)}']
for k,v in ej.items():
    L+=['',f'### Ejemplos: {k}']+[f'- {x}' for x in v[:15]]
L+=['','### Torneos sin final']+[f'- {x}' for x in nofinal[:40]]
open(sys.argv[2],'w',encoding='utf-8').write('\n'.join(L))
print('\n'.join(L[:30]))
