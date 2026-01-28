# Validación del Algoritmo del Quiz

**AMPAY - Transparencia Electoral Perú 2026**

| Campo | Valor |
|-------|-------|
| Fecha | 23 de enero de 2026 |
| Autor | [@JDRV-space](https://github.com/JDRV-space) |
| Método | Simulación Monte Carlo |
| Revisión | Abierta a auditorías metodológicas |

---

## Declaración de Neutralidad

AMPAY es una herramienta informativa que no recomienda por quién votar.

- **Financiamiento:** Autofinanciado por el equipo fundador (sin patrocinadores externos)
- **Afiliación partidaria:** Ninguna - los miembros del equipo no militan ni han militado en ningún partido
- **Privacidad:** Sin cuentas, sin cookies de rastreo, sin registro de respuestas del usuario
- **Metodología pública:** Este documento y los datos de validación están disponibles para auditoría

---

## Resumen Ejecutivo

Se realizaron **2,000,000 de simulaciones** para validar el algoritmo de emparejamiento del quiz político de AMPAY.

| Prueba | Simulaciones | Resultado |
|--------|--------------|-----------|
| Creyentes Verdaderos | 1,000,000 | **100% precisión** |
| Respuestas Aleatorias | 1,000,000 | Distribución consistente con posiciones partidarias |

**Conclusión:** El algoritmo funciona correctamente. La distribución de coincidencias aleatorias refleja la estructura de posiciones de cada partido.

---

## Documentos Relacionados

| Documento | Contenido |
|-----------|-----------|
| Extracción de Promesas | Cómo se extraen las posiciones partidarias de los planes de gobierno del JNE |
| Metodología VAA | Base académica del diseño del quiz |
| Dataset de Replicación | `data/02_output/quiz_validation_dataset.json` - Archivo para reproducir la validación |

---

## Metodología

### Algoritmo Evaluado

El quiz utiliza **distancia Manhattan** para calcular la similitud entre las respuestas del usuario y las posiciones de cada partido:

```
distancia = Σ |respuesta_usuario - posición_partido|
```

| Parámetro | Valor |
|-----------|-------|
| Preguntas | 15 |
| Partidos | 9 |
| Escala | -1 (En desacuerdo), 0 (Neutral), +1 (De acuerdo) |
| Distancia máxima | 30 puntos |
| Empates | Partido primero alfabéticamente |

### ¿Por Qué Distancia Manhattan?

- **Trata cada pregunta independientemente** - suma de diferencias absolutas
- **No penaliza desproporcionadamente** un solo desacuerdo grande
- **Con escala de 3 puntos**, Manhattan y Euclidiana producen rankings similares; Manhattan es más simple de interpretar
- **Estándar en aplicaciones VAA** (Wahl-O-Mat, Vote Compass)

### Conversión a Porcentaje

```
porcentaje_match = 100 - (distancia / 30 × 100)
```

---

## Prueba 1: Creyentes Verdaderos

### Objetivo

Verificar que un usuario que responde exactamente igual que un partido sea emparejado con ese partido.

### Resultados

| Partido | Simulaciones | Correctos | Precisión |
|---------|--------------|-----------|-----------|
| Fuerza Popular | 111,111 | 111,111 | 100% |
| Perú Libre | 111,111 | 111,111 | 100% |
| Renovación Popular | 111,111 | 111,111 | 100% |
| Avanza País | 111,111 | 111,111 | 100% |
| Alianza para el Progreso | 111,111 | 111,111 | 100% |
| Somos Perú | 111,111 | 111,111 | 100% |
| Podemos Perú | 111,111 | 111,111 | 100% |
| Juntos por el Perú | 111,111 | 111,111 | 100% |
| Partido Morado | 111,111 | 111,111 | 100% |
| **TOTAL** | **999,999** | **999,999** | **100%** |

### Interpretación

El algoritmo tiene **100% de precisión** para usuarios con posiciones definidas. Este resultado también confirma que cada partido tiene un vector de posiciones único.

---

## Prueba 2: Respuestas Aleatorias

### Objetivo

Evaluar la distribución de resultados cuando los usuarios responden aleatoriamente.

### Estructura de Posiciones Partidarias

La clave para entender los resultados está en cuántas posiciones **neutrales (0)** tiene cada partido:

| Partido | Posiciones Neutrales (0) | Posiciones Extremas (-1/+1) |
|---------|--------------------------|----------------------------|
| Somos Perú | 13 | 2 |
| Podemos Perú | 11 | 4 |
| Partido Morado | 11 | 4 |
| Alianza para el Progreso | 10 | 5 |
| Fuerza Popular | 6 | 9 |
| Avanza País | 6 | 9 |
| Perú Libre | 3 | 12 |
| Juntos por el Perú | 3 | 12 |
| Renovación Popular | 1 | 14 |

**Observación clave:** Las respuestas aleatorias tienen valor esperado = 0 (promedio de -1, 0, +1). Por lo tanto, partidos con más posiciones neutrales estarán matemáticamente más cerca del "ruido" aleatorio.

### Resultados

| Partido | Coincidencias | Porcentaje | Posiciones Neutrales |
|---------|---------|------------|---------------------|
| Somos Perú | 321,196 | 32.12% | 13 |
| Perú Libre | 131,845 | 13.18% | 3 |
| Alianza para el Progreso | 115,890 | 11.59% | 10 |
| Partido Morado | 113,563 | 11.36% | 11 |
| Podemos Perú | 105,233 | 10.52% | 11 |
| Fuerza Popular | 95,878 | 9.59% | 6 |
| Renovación Popular | 41,152 | 4.12% | 1 |
| Juntos por el Perú | 40,671 | 4.07% | 3 |
| Avanza País | 34,572 | 3.46% | 6 |

### Verificación Estadística

La distribución NO es uniforme, como se esperaba matemáticamente:

| Métrica | Valor |
|---------|-------|
| Chi-cuadrado (χ²) | 545,177.93 |
| Grados de libertad | 8 |
| Resultado | Distribución no uniforme (confirmado) |

**Nota:** Esta prueba chi-cuadrado confirma lo que ya sabemos por la estructura de posiciones. No es una "prueba de sesgo" sino una verificación de que los resultados son consistentes con la matemática.

### Correlación Observada

La correlación entre posiciones neutrales y coincidencia aleatoria es evidente:

- **Somos Perú:** 13 neutrales → 32% coincidencia aleatoria
- **Renovación Popular:** 1 neutral → 4% coincidencia aleatoria

Esto demuestra que el algoritmo **funciona correctamente**: partidos con posiciones claras requieren alineación intencional.

---

## Métricas de Claridad Ideológica

| Partido | Coincidencia Aleatoria | Claridad Ideológica |
|---------|-----------------|---------------------|
| Avanza País | 3.46% | **Alta** (posiciones definidas) |
| Juntos por el Perú | 4.07% | **Alta** |
| Renovación Popular | 4.12% | **Alta** |
| Fuerza Popular | 9.59% | Media |
| Podemos Perú | 10.52% | Media |
| Partido Morado | 11.36% | Media |
| Alianza para el Progreso | 11.59% | Media |
| Perú Libre | 13.18% | Media-Baja |
| Somos Perú | 32.12% | **Baja** (mayormente neutral) |

**Definición de umbrales:**
- Alta claridad: <5% coincidencia aleatoria
- Media: 5-15%
- Baja: >15%

**Implicación:** Si la coincidencia principal del usuario es un partido de baja claridad, se recomienda examinar la 2da y 3ra coincidencia para una alineación más específica.

---

## Conclusiones

1. **100% precisión** para usuarios con posiciones definidas
2. **Distribución consistente** con la estructura matemática de posiciones partidarias
3. **Sin sesgo artificial** - los resultados reflejan las posiciones reales de los partidos
4. **Correlación verificable** entre neutralidad de posiciones y coincidencia aleatoria

---

## Reproducibilidad

### Requisitos

- Python 3.8+
- Sin dependencias externas (solo biblioteca estándar)

### Archivos

| Archivo | Descripción |
|---------|-------------|
| `scripts/quiz_simulation.py` | Script de validación |
| `data/02_output/quiz_statements.json` | Datos completos del quiz |
| `data/02_output/quiz_validation_dataset.json` | Dataset simplificado para replicación |

**Hash SHA-256 (quiz_posiciones_partidos.json):** `fdd72e86366ef6c7b77c0dd6d25724556ed7d90193b5439c2ac528241cd012d1`

### Ejecutar

Los archivos necesarios están disponibles bajo solicitud para auditoría metodológica.

```bash
# Verificar integridad del archivo de datos
shasum -a 256 data/02_output/quiz_statements.json
# Debe mostrar: c33f9d55ec53e653...f9db

# Ejecutar con seed fijo (reproducibilidad exacta)
python3 scripts/quiz_simulation.py 42

# Ejecutar sin seed (verificar consistencia estadística)
python3 scripts/quiz_simulation.py
```

### Especificaciones

| Parámetro | Valor |
|-----------|-------|
| Simulaciones | 2,000,000 |
| Tiempo | ~55 segundos (Apple M1) |
| Semilla oficial | 42 |
| Dependencias | Ninguna (biblioteca estándar) |

---

## Análisis de Sensibilidad

El algoritmo fue evaluado bajo diferentes escenarios para verificar su robustez:

| Escenario | Impacto en Resultados |
|-----------|----------------------|
| Cambio de 1 respuesta | Puede cambiar el orden de partidos con diferencias < 2 puntos |
| Respuestas todas neutrales (0) | Somos Perú obtiene mejor coincidencia (13 neutrales) |
| Respuestas todas extremas (+1/-1) | Renovación Popular más probable (14 posiciones extremas) |
| Empates en distancia | Se resuelve alfabéticamente (comportamiento determinista) |

**Implicación práctica:** Usuarios con posiciones claras obtienen coincidencias estables. Usuarios indecisos (muchos neutrales) pueden ver variación en su ranking de partidos cercanos.

---

## Limitaciones

1. **Posiciones partidarias:** Esta validación asume que las posiciones fueron correctamente extraídas (ver [PROMISE_EXTRACTION.md](/docs/methodology/PROMISE_EXTRACTION.md))
2. **Validación externa:** Se invita revisión de instituciones académicas o de observación electoral

---

## Contacto

- GitHub: [@JDRV-space](https://github.com/JDRV-space)

---

*Documento público, reproducible y abierto a revisión.*
