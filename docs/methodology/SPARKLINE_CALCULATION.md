# Calculo de Sparklines: Patrones de Votacion

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Los sparklines muestran el porcentaje de votos "SI" de cada partido por categoria y por mes. Se utilizan en los perfiles de partidos para visualizar tendencias de votacion.

---

## 1. Definicion de Sparkline

### 1.1 Que es un Sparkline

Un sparkline es una mini-grafica que muestra tendencia en poco espacio. En AMPAY:

```
Fuerza Popular - Economia: ▁▂▃▅▇▆▅▄▃▂ (94.2%)
```

Cada barra representa un periodo (mes o categoria).

### 1.2 Metricas Calculadas

| Metrica | Formula | Uso |
|---------|---------|-----|
| % SI por categoria | SI_votos / (SI_votos + NO_votos) * 100 | Comparar posiciones tematicas |
| % SI por mes | SI_votos_mes / Total_votos_mes * 100 | Ver evolucion temporal |

---

## 2. Calculo por Categoria

### 2.1 Formula

```python
def calcular_pct_categoria(partido, categoria, votos):
    """
    Calcula porcentaje de SI para un partido en una categoria
    """
    votos_partido_categoria = filter(
        votos,
        where partido == partido_input AND categoria == categoria_input
    )

    total_si = sum(v.votes_favor for v in votos_partido_categoria)
    total_no = sum(v.votes_contra for v in votos_partido_categoria)

    if total_si + total_no == 0:
        return None  # Sin datos

    return round(total_si / (total_si + total_no) * 100, 1)
```

### 2.2 Exclusiones

**Votos excluidos del calculo:**

| Tipo de Voto | Razon de Exclusion |
|--------------|-------------------|
| `declarativo` | Sin impacto politico real |
| `procedural` | Mecanica legislativa, no posicion |
| `justicia` (categoria) | Altamente contextual, distorsiona |

### 2.3 Ejemplo de Calculo

```
Partido: Fuerza Popular
Categoria: salud

Votos encontrados: 258
- SI: 1,581 votos individuales
- NO: 118 votos individuales
- Total: 1,699

Calculo:
% SI = 1,581 / 1,699 * 100 = 93.1%
```

---

## 3. Calculo por Mes

### 3.1 Formula

```python
def calcular_pct_mes(partido, mes, votos):
    """
    Calcula porcentaje de SI para un partido en un mes especifico
    """
    votos_partido_mes = filter(
        votos,
        where partido == partido_input
        AND extract_month(fecha) == mes_input
    )

    total_si = sum(v.votes_favor for v in votos_partido_mes)
    total_no = sum(v.votes_contra for v in votos_partido_mes)

    if total_si + total_no == 0:
        return None  # Sin datos para ese mes

    return round(total_si / (total_si + total_no) * 100, 1)
```

### 3.2 Normalizacion Temporal

**Problema:** Algunos meses tienen mas votaciones que otros.

**Solucion:** El porcentaje ya normaliza (ratio, no conteo absoluto).

**Periodo:** 2021-08 a 2024-07 (36 meses)

### 3.3 Meses con Pocos Votos

Si un mes tiene menos de 5 votaciones:
- Calcular el porcentaje normalmente
- Mostrar con indicador de "pocos datos"
- No excluir del sparkline

---

## 4. Estructura de Datos

### 4.1 Formato JSON

```json
{
  "fuerza_popular": {
    "by_category": {
      "salud": {
        "si": 1581,
        "total": 1699,
        "pct": 93.1
      },
      "economia": {
        "si": 2547,
        "total": 2705,
        "pct": 94.2
      }
    },
    "by_month": {
      "2021-08": {
        "si": 1,
        "total": 21,
        "pct": 4.8
      },
      "2021-09": {
        "si": 70,
        "total": 70,
        "pct": 100.0
      }
    }
  }
}
```

### 4.2 Archivo de Salida

```
data/02_output/party_patterns.json
```

---

## 5. Visualizacion

### 5.1 Mapeo Porcentaje a Barra

| % SI | Barra | Significado |
|------|-------|-------------|
| 0-12.5% | ▁ | Muy bajo |
| 12.5-25% | ▂ | Bajo |
| 25-37.5% | ▃ | Medio-bajo |
| 37.5-50% | ▄ | Medio |
| 50-62.5% | ▅ | Medio-alto |
| 62.5-75% | ▆ | Alto |
| 75-87.5% | ▇ | Muy alto |
| 87.5-100% | █ | Maximo |

### 5.2 Codigo de Colores

```css
/* CSS Variables para sparklines */
--sparkline-low: #ff6b6b;      /* < 40% - Oposicion */
--sparkline-mid: #ffd93d;      /* 40-60% - Dividido */
--sparkline-high: #6bff6b;     /* > 60% - Apoyo */
```

### 5.3 Ejemplo Visual

```
FUERZA POPULAR - Votacion por Categoria

salud      ████████▇ 93%
economia   █████████ 94%
seguridad  █████████ 96%
educacion  ████████▇ 91%
empleo     ████████▆ 89%
```

---

## 6. Interpretacion

### 6.1 Patrones Tipicos

| Patron | Significado |
|--------|-------------|
| Todos altos (>80%) | Partido oficialista o muy cohesionado |
| Todos bajos (<40%) | Oposicion sistematica |
| Variable por categoria | Posiciones diferenciadas por tema |
| Caida temporal | Cambio de posicion o crisis interna |

### 6.2 Alertas

**Alerta de coherencia:** Si un partido tiene >80% SI en una categoria pero promete lo contrario, puede indicar AMPAY potencial.

---

## 7. Limitaciones

1. **Sesgo de votaciones:** No todos los temas llegan a votacion
2. **Agregacion excesiva:** 15 categorias pueden ocultar matices
3. **Peso igual:** Votos importantes y menores tienen mismo peso
4. **Sin contexto:** El numero no explica POR QUE votaron asi
5. **Periodo fijo:** 2021-2024, no incluye legislatura actual

---

## 8. Validacion

### 8.1 Verificacion de Totales

```python
# Para cada partido, verificar:
total_by_category = sum(cat.total for cat in party.by_category)
total_by_month = sum(month.total for month in party.by_month)

assert total_by_category == total_by_month, "Inconsistencia en totales"
```

### 8.2 Comparacion con Fuentes

- Contrastar con reportes de transparencia del Congreso
- Verificar meses con anomalias (0% o 100%)
- Revisar categorias con pocos datos

---

## 9. Script de Generacion

```python
# scripts/compute_patterns.py

import json
from collections import defaultdict

def compute_party_patterns(votes_categorized):
    patterns = defaultdict(lambda: {
        'by_category': defaultdict(lambda: {'si': 0, 'total': 0}),
        'by_month': defaultdict(lambda: {'si': 0, 'total': 0})
    })

    for vote in votes_categorized:
        category = vote['category']
        month = vote['date'][:7]  # YYYY-MM

        for party, position in vote['party_positions'].items():
            if position['position'] in ['SI', 'NO']:
                patterns[party]['by_category'][category]['total'] += 1
                patterns[party]['by_month'][month]['total'] += 1

                if position['position'] == 'SI':
                    patterns[party]['by_category'][category]['si'] += 1
                    patterns[party]['by_month'][month]['si'] += 1

    # Calcular porcentajes
    for party in patterns:
        for cat in patterns[party]['by_category']:
            data = patterns[party]['by_category'][cat]
            data['pct'] = round(data['si'] / data['total'] * 100, 1) if data['total'] > 0 else None

        for month in patterns[party]['by_month']:
            data = patterns[party]['by_month'][month]
            data['pct'] = round(data['si'] / data['total'] * 100, 1) if data['total'] > 0 else None

    return patterns
```

---

## 10. Archivos Relacionados

| Archivo | Contenido |
|---------|-----------|
| `data/02_output/party_patterns.json` | Datos de sparklines |
| `data/02_output/votes_categorized.json` | Votos fuente |
| `scripts/compute_patterns.py` | Script de generacion |

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Ultima actualizacion: 2026-01-21*
