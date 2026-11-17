#!/usr/bin/env python3
"""Aplica auditoria/verificacion_manual.json al JSON unificado (idempotente)."""
import json,sys
R='/home/claude/repo-titotenis/'
d=json.load(open(R+'datos_unificados/titotenis_datos_unificados.json'))
c=d['columnas'];ix={n:i for i,n in enumerate(c)};P=d['partidos']
V=json.load(open(R+'auditoria/verificacion_manual.json'))
dele=set()
def find(k):
    a,t,r,l,v=k
    out=[]
    for i,p in enumerate(P):
        if p[0]==a and p[1]==t and p[2]==r and p[ix['cuadro']]=='principal' and ((p[3]==l and p[4]==v) or (p[3]==v and p[4]==l)) and i not in dele: out.append(i)
    return out
def sets_from(m):
    sl=sv=0
    for s in m.split(','):
        a,b=s.split('-'); sl+= int(a)>int(b); sv+= int(a)<int(b)
    return str(sl),str(sv)
log=[]
DEL=[(2026,'Madrid Masters',('Kjr N.',)),(2026,'Australian Open',('Kjr N.',))]
for i,p in enumerate(P):
    if p[0]==2026 and p[ix['cuadro']]=='principal' and 'Kjr N.' in (p[3],p[4]): dele.add(i)
# duplicados Next Gen
for i,p in enumerate(P):
    if p[0]==2017 and p[1]=='Next Gen Finals' and ((p[2]=='Final' and p[3]=='Rublev A.' and p[4]=='Chung H.') or (p[2]=='Semi-finals' and p[3]=='Coric B.' and p[4]=='Medvedev D.')): dele.add(i)
    if p[0]==2022 and p[1]=='NextGen Finals' and p[2]=='Final' and p[ix['verificacion']]=='CORREGIDO_VOTO': dele.add(i)
for i,p in enumerate(P):
    if p[0]==2017 and p[1]=='Rome Masters' and p[2]=='1/32-finals' and p[3]=='Isner J.' and p[4]=='Ramos A.' and not p[ix['id']]: dele.add(i)
sin=[]
for e in V:
    idx=find(e['clave'])
    if len(idx)!=1: sin.append((e['clave'],idx)); continue
    i=idx[0]
    if i in dele: continue
    p=P[i]
    if e['veredicto']=='corregido':
        m=e['marcador']
        if m:
            p[ix['detalle_sets']]=m; p[ix['sets_local']],p[ix['sets_visitante']]=sets_from(m) if p[3]==e['clave'][3] else sets_from(','.join('-'.join(reversed(s.split('-'))) for s in m.split(',')))
        else:
            p[ix['detalle_sets']]='';p[ix['sets_local']]=p[ix['sets_visitante']]='0'
        p[ix['estado']]=e['estado']
        win=e['estado'].split(' - ')[-1] if ' - ' in e['estado'] else (p[3] if int(p[ix['sets_local']])>int(p[ix['sets_visitante']]) else p[4])
        p[ix['ganador']]=win
    p[ix['verificacion']]='VERIFICADO_MANUAL'
    p[ix['fiabilidad']]='contrastado'
    extra=p[ix['fuentes_extra']] or ''
    if 'MANUAL=' not in extra: p[ix['fuentes_extra']]=(extra+';' if extra else '')+'MANUAL='+' '.join(e['fuentes'][:3])
    p[ix['nota']]=((p[ix['nota']] or '')+' | verificado a mano con '+str(len(e['fuentes']))+' fuentes ('+e['veredicto']+')').strip(' |')
# renombrar Martin D. -> Damm Jr. M. (2026)
for p in P:
    if p[0]==2026 and 'Martin D.' in (p[3],p[4]):
        for k in (3,4,ix['ganador'],ix['estado']):
            if p[k]: p[k]=p[k].replace('Martin D.','Damm Jr. M.')
d['partidos']=[p for i,p in enumerate(P) if i not in dele]
json.dump(d,open(R+'datos_unificados/titotenis_datos_unificados.json','w'),ensure_ascii=False,separators=(',',':'))
print('borradas',len(dele),'sin_localizar',sin)
