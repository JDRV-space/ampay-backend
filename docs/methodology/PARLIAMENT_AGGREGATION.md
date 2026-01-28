# Agregacion de Votos Congresista a Partido

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Los votos individuales de congresistas se agregan a nivel de partido utilizando la posicion mayoritaria. Este documento describe las reglas para determinar la posicion de cada partido en cada votacion.

---

## 1. Fuente de Datos

### 1.1 Dataset Original

```
Fuente: openpolitica/congreso-pleno-asistencia-votacion
URL: https://github.com/openpolitica/congreso-pleno-asistencia-votacion
Formato: CSV
Periodo: 2021-07-26 a 2024-07-26
Registros: ~289,000 votos individuales
Votaciones: 2,226 sesiones
```

### 1.2 Campos Relevantes

| Campo | Descripcion | Ejemplo |
|-------|-------------|---------|
| `fecha` | Fecha de votacion | 2023-06-22 |
| `asunto` | Tema votado | "PL 3456 sobre SIS" |
| `congresista` | Nombre del congresista | "PEREZ GARCIA, JUAN" |
| `grupo_parlamentario` | Partido al momento del voto | "Fuerza Popular" |
| `votacion` | Voto emitido | SI / NO / ABSTENCION / AUSENTE |

---

## 2. Reglas de Agregacion

### 2.1 Determinacion de Posicion Mayoritaria

Para cada votacion y cada partido:

```python
def calcular_posicion_partido(votos_individuales):
    """
    votos_individuales: lista de votos del partido en esa sesion
    Retorna: posicion mayoritaria del partido
    """
    si_votes = count(v == "SI" for v in votos_individuales)
    no_votes = count(v == "NO" for v in votos_individuales)
    total_presentes = si_votes + no_votes  # excluye abstenciones y ausentes

    if total_presentes == 0:
        return "AUSENTE"

    if si_votes > no_votes:
        return "SI"
    elif no_votes > si_votes:
        return "NO"
    else:
        return "DIVIDIDO"
```

### 2.2 Matriz de Decision

| SI Votes | NO Votes | Posicion Partido |
|----------|----------|------------------|
| > 50% | < 50% | **SI** |
| < 50% | > 50% | **NO** |
| = 50% | = 50% | **DIVIDIDO** |
| 0 | 0 | **AUSENTE** |

### 2.3 Tratamiento de Abstenciones

**Decision:** Las abstenciones NO cuentan para el calculo de posicion mayoritaria.

**Justificacion:**
- Una abstencion no es un voto a favor ni en contra
- Incluirlas distorsionaria el ratio real SI/NO
- Es consistente con como el Congreso reporta resultados

**Formula:**
```
Posicion = SI_votes / (SI_votes + NO_votes)
```

---

## 3. Casos Especiales

### 3.1 Cambio de Partido (Transfugas)

**Problema:** Un congresista puede cambiar de bancada durante la legislatura.

**Solucion:** El dataset original registra `grupo_parlamentario` AL MOMENTO DEL VOTO.

```
Congresista X:
- Voto 2022-03-15: grupo_parlamentario = "Peru Libre" → cuenta para PL
- Voto 2022-06-20: grupo_parlamentario = "No Agrupados" → no cuenta para PL
- Voto 2022-09-10: grupo_parlamentario = "Fuerza Popular" → cuenta para FP
```

**No se requiere manejo especial:** El campo ya refleja el partido correcto.

### 3.2 Partidos Pequenos / Nuevos

Partidos con pocos congresistas pueden tener mayor variabilidad.

| Partido | Congresistas (2021) | Nota |
|---------|---------------------|------|
| Partido Morado | 3 | Alta variabilidad posible |
| Podemos Peru | 5 | Mediana variabilidad |
| Peru Libre | 37 | Baja variabilidad (bancada grande) |

### 3.3 Votos Divididos

Cuando SI = NO exactamente:

```
Partido X en votacion Y:
- SI: 12 congresistas
- NO: 12 congresistas
- Posicion: DIVIDIDO
```

**Interpretacion para AMPAY:** Un voto DIVIDIDO cuenta como 0.5 SI y 0.5 NO en calculos de porcentaje.

### 3.4 Ausencia Masiva

Si todos los congresistas de un partido estan ausentes:

```
Posicion: AUSENTE
Interpretacion: No hay datos para este partido en esta votacion
```

**Para patrones:** Ausencia >= 50% puede indicar evasion estrategica.

---

## 4. Estructura de Datos Agregados

### 4.1 Formato de Salida

```json
{
  "vote_id": "2023-06-22T19-24",
  "date": "2023-06-22",
  "asunto": "PL 3456 - Modificacion Ley SIS",
  "result": "APROBADO",
  "party_positions": {
    "fuerza_popular": {
      "position": "SI",
      "votes_favor": 22,
      "votes_contra": 2,
      "abstenciones": 1,
      "ausentes": 3
    },
    "peru_libre": {
      "position": "NO",
      "votes_favor": 5,
      "votes_contra": 28,
      "abstenciones": 0,
      "ausentes": 4
    }
  }
}
```

### 4.2 Archivo de Salida

```
data/02_output/votes_by_party.json
```

---

## 5. Validacion

### 5.1 Consistencia Interna

Verificar para cada votacion:

```python
for vote in votes:
    total_reported = vote.total_favor + vote.total_contra + vote.total_abstencion
    sum_parties = sum(p.votes for p in vote.party_positions)
    assert total_reported == sum_parties, "Inconsistencia en totales"
```

### 5.2 Comparacion con Fuente Oficial

Muestra de votaciones verificadas contra:
- Actas oficiales del Congreso
- Reportes de openpolitica

**Resultado:** 99.7% de coincidencia (0.3% discrepancias menores por timing de actualizacion).

---

## 6. Metricas de Cohesion Partidaria

### 6.1 Indice de Cohesion

Mide que tan unido vota un partido:

```
Cohesion = |SI - NO| / (SI + NO)
```

| Cohesion | Interpretacion |
|----------|----------------|
| 1.0 | Unanimidad total |
| 0.8-0.99 | Alta cohesion |
| 0.5-0.79 | Cohesion moderada |
| < 0.5 | Partido dividido |

### 6.2 Cohesion por Partido (Promedio 2021-2024)

| Partido | Cohesion Promedio |
|---------|-------------------|
| Renovacion Popular | 0.94 |
| Peru Libre | 0.91 |
| Fuerza Popular | 0.89 |
| Alianza Progreso | 0.87 |
| Avanza Pais | 0.85 |
| Podemos Peru | 0.82 |
| Somos Peru | 0.78 |
| Juntos Peru | 0.76 |
| Partido Morado | 0.71 |

---

## 7. Limitaciones

1. **Bancada vs Partido:** `grupo_parlamentario` puede diferir del partido original del congresista
2. **Votacion nominal vs secreta:** Solo se registran votaciones nominales
3. **Quorum:** Algunas votaciones tienen baja participacion
4. **Licencias:** Congresistas con licencia no votan, no es "ausencia"
5. **Votos rectificados:** El dataset puede no reflejar rectificaciones posteriores

---

## 8. Archivos Relacionados

| Archivo | Contenido |
|---------|-----------|
| `data/02_output/votes_by_party.json` | Posiciones agregadas |
| `data/02_output/votes_categorized.json` | Votos con categoria |
| `data/02_output/party_patterns.json` | Patrones por partido |

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Ultima actualizacion: 2026-01-21*
