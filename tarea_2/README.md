# Tarea 2. Optimización de la función de Rastrigin con algoritmos genéticos

## Problema

Minimizar la función de Rastrigin en dos variables, con x, y ∈ [-5.12, 5.12]:

```
f(x, y) = 20 + (x² − 10·cos(2πx)) + (y² − 10·cos(2πy))
```

El óptimo global es f(0, 0) = 0. La función tiene muchos mínimos locales (uno por
cada valle alrededor de los enteros), así que sirve para ver si el AG mantiene
suficiente exploración.

## Algoritmo (`main.py`)

| Componente | Implementación |
|---|---|
| Codificación | Binaria; 5 decimales de precisión → 20 bits por variable (40 por individuo) |
| Selección | Torneo binario (dos permutaciones de la población) |
| Cruzamiento | Dos puntos, con probabilidad `pc` por pareja |
| Mutación | Cambio de un bit aleatorio por individuo, con probabilidad `pm` |
| Sustitución | Extintiva con elitismo: la descendencia reemplaza a toda la población y el mejor individuo anterior sustituye a un hijo elegido al azar |
| Generaciones | 200 |

Cómo se ejecuta (el entorno usa `uv`):

```bash
uv run main.py            # 10 ejecuciones de 200 generaciones + indicadores
uv run experimentos.py    # barridos de sintonización (tarda ~35 s)
```

## Sintonización de parámetros

`experimentos.py` ejecuta cada configuración 10 veces (200 generaciones) y cuenta
como "óptimo" una ejecución con f < 1e-3. Valores en notación científica;
`desv` es la desviación estándar poblacional (`np.std`).

### Tamaño de población (pc = 0.7, pm = 0.02)

| población | mejor | mediana | media | peor | desv | óptimo |
|---|---|---|---|---|---|---|
| 10 | 1.02e+00 | 2.40e+00 | 3.21e+00 | 6.71e+00 | 1.90e+00 | 0/10 |
| 20 | 9.87e-05 | 1.61e+00 | 1.67e+00 | 3.98e+00 | 1.03e+00 | 1/10 |
| 50 | 9.46e-09 | 9.95e-01 | 7.45e-01 | 2.23e+00 | 7.02e-01 | 4/10 |
| 100 | 9.46e-09 | 9.46e-09 | 2.98e-01 | 1.99e+00 | 6.37e-01 | 8/10 |
| 512 | 9.46e-09 | 9.46e-09 | 9.46e-09 | 9.46e-09 | 0.00e+00 | 10/10 |

### Tasa de cruzamiento (pm = 0.02, población = 50)

| pc | mejor | mediana | media | peor | desv | óptimo |
|---|---|---|---|---|---|---|
| 0.1 | 9.95e-01 | 2.11e+00 | 2.31e+00 | 4.99e+00 | 1.19e+00 | 0/10 |
| 0.3 | 9.95e-01 | 1.24e+00 | 1.62e+00 | 4.00e+00 | 9.18e-01 | 0/10 |
| 0.5 | 9.46e-09 | 4.97e-01 | 7.45e-01 | 2.23e+00 | 8.59e-01 | 5/10 |
| 0.7 | 9.46e-09 | 9.97e-01 | 1.12e+00 | 2.04e+00 | 7.03e-01 | 2/10 |
| 0.9 | 9.46e-09 | 9.46e-09 | 4.23e-01 | 1.24e+00 | 5.22e-01 | 6/10 |

### Tasa de mutación (pc = 0.7, población = 50)

| pm | mejor | mediana | media | peor | desv | óptimo |
|---|---|---|---|---|---|---|
| 0.0 | 8.78e-04 | 1.01e+00 | 8.92e-01 | 2.65e+00 | 7.42e-01 | 1/10 |
| 0.01 | 9.46e-09 | 9.95e-01 | 7.04e-01 | 1.05e+00 | 4.60e-01 | 2/10 |
| 0.02 | 9.46e-09 | 9.95e-01 | 8.28e-01 | 1.99e+00 | 7.57e-01 | 4/10 |
| 0.1 | 9.46e-09 | 4.97e-01 | 7.97e-01 | 1.99e+00 | 8.68e-01 | 5/10 |
| 0.3 | 9.46e-09 | 9.95e-01 | 1.12e+00 | 4.97e+00 | 1.46e+00 | 4/10 |
| 0.6 | 9.46e-09 | 9.46e-09 | 5.22e-01 | 2.23e+00 | 8.50e-01 | 7/10 |

### pc × pm (población = 20)

| pc | pm | mejor | mediana | media | peor | desv | óptimo |
|---|---|---|---|---|---|---|---|
| 0.3 | 0.02 | 9.95e-01 | 2.36e+00 | 2.80e+00 | 5.59e+00 | 1.50e+00 | 0/10 |
| 0.3 | 0.2 | 9.46e-09 | 1.99e+00 | 2.61e+00 | 7.98e+00 | 2.14e+00 | 1/10 |
| 0.7 | 0.02 | 9.46e-09 | 2.11e+00 | 3.11e+00 | 9.54e+00 | 3.02e+00 | 1/10 |
| 0.7 | 0.2 | 9.46e-09 | 9.97e-01 | 1.25e+00 | 5.24e+00 | 1.46e+00 | 3/10 |
| 0.9 | 0.02 | 9.46e-09 | 1.02e+00 | 1.75e+00 | 4.99e+00 | 1.56e+00 | 2/10 |
| 0.9 | 0.2 | 9.46e-09 | 1.12e+00 | 1.54e+00 | 3.98e+00 | 1.02e+00 | 1/10 |

Con solo 10 repeticiones por celda hay ruido: diferencias de uno o dos aciertos
no son concluyentes.

**Configuración elegida:** pc = 0.7, pm = 0.02, población = 512. Son los valores
habituales (pc alto, pm bajo) y la población grande es el factor que más pesa.

## Resultado final: 10 ejecuciones × 200 generaciones

Salida de `uv run main.py` con pc = 0.7, pm = 0.02, población = 512:

| Ejecución | x | y | f(x, y) |
|---|---|---|---|
| 1 | 0.00000 | 0.00000 | 9.460091e-09 |
| 2 | 0.00000 | 0.00000 | 9.460091e-09 |
| 3 | 0.00000 | -0.00000 | 9.460091e-09 |
| 4 | 0.00000 | 0.00000 | 9.460091e-09 |
| 5 | 0.00000 | -0.00000 | 9.460091e-09 |
| 6 | -0.00000 | 0.00000 | 9.460091e-09 |
| 7 | 0.00000 | 0.00000 | 9.460091e-09 |
| 8 | 0.00000 | -0.00000 | 9.460091e-09 |
| 9 | 0.00000 | -0.00000 | 9.460091e-09 |
| 10 | -0.00000 | 0.00000 | 9.460091e-09 |

| Indicador | Resultado |
|---|---|
| Mejor | 9.460091e-09 |
| Mediana | 9.460091e-09 |
| Media | 9.460091e-09 |
| Peor | 9.460091e-09 |
| Desv. estándar | 0 |

El valor 9.46e-09 no es error del algoritmo: con 5 decimales el punto de la
malla más cercano al origen no cae exactamente en 0 (la malla tiene paso
≈ 9.8e-6), y ese es el mejor valor que se puede representar.

## Discusión

**Efecto de pc y pm.** Con población pequeña (50) una pc baja (0.1–0.3) nunca
llegó al óptimo, mientras que pc ≥ 0.5 sí lo hizo (hasta 6/10 con pc = 0.9): sin
cruzamiento suficiente, la información de los buenos individuos casi no se
recombina. La pm tuvo un efecto mucho menor: sin mutación (pm = 0) solo 1/10
llegó al óptimo y con valores entre 0.01 y 0.6 se obtuvieron 2–7/10, sin una
tendencia monótona clara; incluso pm altas funcionaron razonablemente porque el
elitismo conserva siempre al mejor individuo. Con población 512 las diferencias
desaparecen: cualquier combinación razonable converge al óptimo. En esta función
el tamaño de población es el factor dominante.

**Estabilidad.** Con la configuración elegida (512 individuos) el algoritmo fue
completamente estable: las 10 ejecuciones dieron el mismo resultado y desviación
estándar nula. Con poblaciones de 100 o menos la estabilidad baja: con 100 hubo
8/10 aciertos y con 20 solo 1/10.

**Ejecuciones que no llegaron al óptimo.** Los valores finales no óptimos se
agrupan cerca de 0.995, 1.99, 2.98… Corresponden a que una, dos o tres variables
quedaron atrapadas en un valle vecino (x ≈ ±1, ±2), que son mínimos locales de
Rastrigin. Con pocos individuos la población pierde diversidad antes de
encontrar el valle central, y una vez convergida la mutación con probabilidad
baja rara vez salta a otro valle. El elitismo evita retrocesos pero tampoco
permite escapar de ese mínimo local.

> Nota: en las pruebas previas se observó que con poblaciones ≤ 100 el valor deja
> de converger a 0, y que pc y pm extremos funcionaron bien con población grande.
> Con población 50 sí se nota el efecto de una pc baja (ver tablas), así que
> conviene aclarar en el reporte que esa observación aplica solo para población 512.

## Archivos

- `main.py`: AG, función de Rastrigin y las 10 ejecuciones con indicadores.
- `experimentos.py`: barridos de sintonización.
- `requesitos.pdf`: enunciado.
