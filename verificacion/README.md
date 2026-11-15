# Verificación técnica de InformAMPA con casos simulados

Esta carpeta contiene seis casos **simulados** (no son pacientes reales) cuyo resultado correcto se conoce de antemano. Sirven para comprobar que la herramienta calcula y clasifica bien.

| Caso | Escenario | Estado esperado |
|---|---|---|
| S1 | Control óptimo | ÓPTIMO |
| S2 | Por encima de objetivos | ATENCIÓN |
| S3 | Elevación matutina aislada | ATENCIÓN PARCIAL |
| S4 | Reacción de alerta el primer día (se excluye el día 1) | ÓPTIMO |
| S5 | Sesión aislada elevada + PA en consulta 152/94 | BATA BLANCA |
| S6 | AMPA elevada + PA en consulta 128/80 | ENMASCARADA |

Cada caso tiene 7 días, con sesión de mañana y de tarde y 3 lecturas por sesión. Se descarta la 1.ª lectura y se promedian la 2.ª y la 3.ª.

## Reproducir

```bash
python generar_casos.py casos_simulados.json
node informes_node.js ../informampa.html casos_simulados.json .
```

- `generar_casos.py` crea los casos y calcula el resultado esperado de forma independiente, sin redondeos intermedios.
- `informes_node.js` ejecuta el motor de cálculo de la herramienta, guarda sus resultados en `resultados_herramienta.json` y genera un informe HTML por caso.

## Resultado (v1.1.1 y v1.1.2)

En los seis casos, las medias globales y por franja coinciden con las esperadas, con una diferencia máxima de 0,04 mmHg (por el redondeo a una décima). La desviación estándar coincide también, y los seis estados se clasifican correctamente.

La verificación de la v1.1.0 detectó tres problemas, que se corrigieron en la v1.1.1:
1. **HTA enmascarada:** este estado nunca se mostraba.
2. **Sesgo de redondeo:** la herramienta redondeaba cada sesión antes de promediar, lo que sobrestimaba la PAS media entre 0,2 y 0,3 mmHg.
3. **Desviación estándar:** se calculaba la poblacional (n) en lugar de la muestral (n−1).
