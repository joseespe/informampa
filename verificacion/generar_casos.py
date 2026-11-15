# -*- coding: utf-8 -*-
"""Genera 5 casos SIMULADOS de AMPA con resultado esperado conocido, para la
verificación técnica de InformAMPA. No son pacientes reales.

Protocolo simulado: 7 días, sesión de mañana y de tarde, 3 lecturas por sesión;
la 1.ª lectura se descarta y se promedian la 2.ª y la 3.ª.
El resultado esperado se calcula aquí de forma independiente, sin redondeos
intermedios, a partir de las definiciones de las guías (umbral AMPA 135/85;
objetivo óptimo <130/80; consulta elevada >=140/90).
"""
import json, random, statistics as stt, sys
from datetime import date, timedelta

random.seed(2026)
START = date(2026, 3, 2)

def sesion(d, ses, sys_, dia_, hr, alerta=7):
    """Devuelve una sesión con 3 lecturas. r1 lleva un efecto alerta (+alerta)."""
    j = lambda: random.randint(-2, 2)
    r2s, r2d = sys_ + j(), dia_ + j()
    r3s, r3d = sys_ + j(), dia_ + j()
    hh = "08" if ses == "morning" else "20"
    return dict(date=d.isoformat(), session=ses,
                r1sys=sys_ + alerta + j(), r1dia=dia_ + alerta // 2 + j(), r1time=f"{hh}:00",
                r2sys=r2s, r2dia=r2d, r2time=f"{hh}:02",
                r3sys=r3s, r3dia=r3d, r3time=f"{hh}:04", hr=hr + j())

def serie(m_sys, m_dia, t_sys, t_dia, hr=72, dias=7, sd=4, especiales=None):
    out = []
    for k in range(dias):
        d = START + timedelta(days=k)
        for ses, (bs, bd) in (("morning", (m_sys, m_dia)), ("afternoon", (t_sys, t_dia))):
            s, di = bs + random.randint(-sd, sd), bd + random.randint(-sd // 2, sd // 2)
            if especiales and (k, ses) in especiales:
                s, di = especiales[(k, ses)]
            out.append(sesion(d, ses, s, di, hr))
    return out

CASOS = [
 dict(id="S1", nombre="Control óptimo",
      descripcion="PA bien controlada, por debajo del objetivo óptimo",
      meas=serie(120, 75, 116, 72), clinic=("", ""), excluir_dia1=False,
      esperado_estado="ÓPTIMO"),
 dict(id="S2", nombre="Por encima de objetivos",
      descripcion="Media AMPA claramente elevada en ambas franjas",
      meas=serie(150, 94, 144, 90, hr=80), clinic=("", ""), excluir_dia1=False,
      esperado_estado="ATENCIÓN"),
 dict(id="S3", nombre="Elevación matutina aislada",
      descripcion="Media global controlada con media de mañana >=135/85",
      meas=serie(140, 86, 120, 76), clinic=("", ""), excluir_dia1=False,
      esperado_estado="ATENCIÓN PARCIAL"),
 dict(id="S4", nombre="Reacción de alerta el primer día",
      descripcion="Día 1 muy elevado; resto controlado. Se excluye el día 1 (ESH 2021)",
      meas=serie(124, 78, 120, 76, especiales={(0, "morning"): (162, 96), (0, "afternoon"): (150, 90)}),
      clinic=("", ""), excluir_dia1=True, esperado_estado="CONTROLADA u ÓPTIMO"),
 dict(id="S5", nombre="Sesión aislada elevada + bata blanca",
      descripcion="Una sesión vespertina elevada (simula omisión de dosis); PA en consulta 152/94",
      meas=serie(122, 77, 118, 74, especiales={(3, "afternoon"): (146, 90)}),
      clinic=("152", "94"), excluir_dia1=False, esperado_estado="BATA BLANCA"),
 # Caso adicional para la rama de HTA enmascarada (AMPA elevada, consulta normal)
 dict(id="S6", nombre="HTA enmascarada",
      descripcion="AMPA elevada con PA en consulta normal (128/80)",
      meas=serie(142, 88, 138, 86), clinic=("128", "80"), excluir_dia1=False,
      esperado_estado="ENMASCARADA"),
]

def esperado(caso):
    meas = caso["meas"]
    if caso["excluir_dia1"]:
        d1 = min(m["date"] for m in meas)
        meas = [m for m in meas if m["date"] != d1]
    sm = [((m["r2sys"] + m["r3sys"]) / 2, (m["r2dia"] + m["r3dia"]) / 2, m["session"], m["date"]) for m in meas]
    g = lambda xs: (stt.fmean(x[0] for x in xs), stt.fmean(x[1] for x in xs))
    mo = [x for x in sm if x[2] == "morning"]; af = [x for x in sm if x[2] == "afternoon"]
    G, M, A = g(sm), g(mo), g(af)
    el = lambda p: p[0] >= 135 or p[1] >= 85
    return dict(
        sesiones=len(sm), dias=len({x[3] for x in sm}),
        global_sys=round(G[0], 2), global_dia=round(G[1], 2),
        manana_sys=round(M[0], 2), manana_dia=round(M[1], 2),
        tarde_sys=round(A[0], 2), tarde_dia=round(A[1], 2),
        de_pas_muestral=round(stt.stdev([x[0] for x in sm]), 2),
        de_pas_poblacional=round(stt.pstdev([x[0] for x in sm]), 2),
        sesiones_elevadas=sum(1 for x in sm if el(x)),
        global_elevada=el(G), manana_elevada=el(M), tarde_elevada=el(A),
        optimo=G[0] < 130 and G[1] < 80,
        efecto_alerta_medio=round(stt.fmean(m["r1sys"] - (m["r2sys"] + m["r3sys"]) / 2 for m in meas), 2),
    )

for c in CASOS:
    c["esperado"] = esperado(c)

json.dump(CASOS, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for c in CASOS:
    e = c["esperado"]
    print(c["id"], c["nombre"], "|", e["sesiones"], "ses |", f'{e["global_sys"]}/{e["global_dia"]}',
          "| mañana", f'{e["manana_sys"]}/{e["manana_dia"]}', "| tarde", f'{e["tarde_sys"]}/{e["tarde_dia"]}',
          "| elevadas", e["sesiones_elevadas"], "| esperado:", c["esperado_estado"])
