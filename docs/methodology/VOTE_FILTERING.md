# Filtrado de Votos Parlamentarios

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

No todos los votos del Congreso tienen igual relevancia para analisis politico. Este documento describe los criterios para filtrar votos sustantivos de procedimentales y declarativos.

---

## 1. Tipos de Votos

### 1.1 Clasificacion Tripartita

| Tipo | Definicion | Incluido en Analisis |
|------|------------|---------------------|
| **Sustantivo** | Votos sobre legislacion con impacto politico real | **SI** |
| **Procedural** | Votos sobre mecanica legislativa | NO |
| **Declarativo** | Votos simbolicos sin efecto legal | NO |

### 1.2 Ejemplos por Tipo

**SUSTANTIVO (incluir):**
```
- "Ley que modifica el Codigo Penal"
- "Presupuesto del Sector Publico 2024"
- "Ley de reforma del sistema de pensiones"
- "Credito suplementario para el sector salud"
```

**PROCEDURAL (excluir):**
```
- "Mocion de orden del dia"
- "Aprobacion del acta de sesion anterior"
- "Cuestion previa"
- "Cuestion de orden"
- "Dispensa de segunda votacion"
- "Ampliacion de agenda"
```

**DECLARATIVO (excluir):**
```
- "Declarar de interes nacional el Festival de X"
- "Declarar heroe de la patria a Y"
- "Saludo por el dia de Z"
- "Reconocimiento a la labor de..."
```

---

## 2. Criterios de Filtrado

### 2.1 Reglas de Exclusion Automatica

**Por palabras clave en asunto:**

```python
EXCLUIR_SI_CONTIENE = [
    # Procedural
    "orden del dia",
    "acta de sesion",
    "cuestion previa",
    "cuestion de orden",
    "dispensa de",
    "ampliacion de agenda",
    "reconsideracion",
    "votacion en bloque",

    # Declarativo
    "declarar de interes nacional",
    "declarar heroe",
    "declarar patrimonio",
    "saludo por",
    "reconocimiento a",
    "dia nacional de",
    "dia del",
    "semana de",
    "mes de",
    "año de"
]
```

### 2.2 Reglas de Inclusion Forzada

Aunque contenga palabras de exclusion, INCLUIR si:

```python
INCLUIR_SI_CONTIENE = [
    "ley",
    "proyecto de ley",
    "presupuesto",
    "credito suplementario",
    "decreto",
    "reforma",
    "modificacion",
    "deroga"
]
```

### 2.3 Matriz de Decision

| Contiene Exclusion | Contiene Inclusion | Resultado |
|--------------------|-------------------|-----------|
| NO | SI | **INCLUIR** |
| NO | NO | **INCLUIR** (default) |
| SI | NO | **EXCLUIR** |
| SI | SI | **REVISION MANUAL** |

---

## 3. Proceso de Clasificacion

### 3.1 Pipeline Automatico

```
┌─────────────────────────────────────────┐
│         ASUNTO DEL VOTO                 │
└────────────────────┬────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  REGLAS DE EXCLUSION  │
         │  (palabras clave)     │
         └───────────┬───────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   No match     Match excl   Match ambos
        │            │            │
        ▼            │            ▼
   ┌─────────┐       │      ┌───────────┐
   │ INCLUIR │       │      │ REVISION  │
   │ como    │       │      │ MANUAL    │
   │sustantivo│      │      └───────────┘
   └─────────┘       │
                     ▼
         ┌───────────────────────┐
         │  REGLAS DE INCLUSION  │
         │  (palabras clave)     │
         └───────────┬───────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   Match incl               No match
        │                         │
        ▼                         ▼
   ┌─────────┐              ┌─────────┐
   │ INCLUIR │              │ EXCLUIR │
   │ como    │              │ como    │
   │sustantivo│             │ declarativo/
   └─────────┘              │ procedural │
                            └─────────┘
```

### 3.2 Clasificacion por IA

Para casos ambiguos, usar Claude:

```
Prompt:
"Clasifica este asunto de votacion del Congreso peruano:

ASUNTO: [texto]

Clasificacion (elegir UNA):
1. SUSTANTIVO - Ley o decision con impacto politico real
2. PROCEDURAL - Mecanica legislativa sin contenido politico
3. DECLARATIVO - Reconocimiento simbolico sin efecto legal

Responde SOLO con: SUSTANTIVO, PROCEDURAL, o DECLARATIVO"
```

---

## 4. Estadisticas de Filtrado

### 4.1 Resultados del Filtrado (2021-2024)

| Tipo | Cantidad | % del Total |
|------|----------|-------------|
| **Sustantivo** | 2,226 | 62.4% |
| Procedural | 847 | 23.8% |
| Declarativo | 497 | 13.9% |
| **TOTAL** | 3,570 | 100% |

### 4.2 Votos Declarativos por Año

| Año | Declarativos | % del Año | Notas |
|-----|--------------|-----------|-------|
| 2021 | 89 | 11.2% | Inicio legislatura |
| 2022 | 142 | 14.8% | Normal |
| 2023 | 178 | 15.6% | Aumento pre-electoral |
| 2024 | 88 | 12.1% | Parcial (hasta julio) |

**Fuente:** Analisis Ojo Publico sobre proyectos declarativos: [URL](https://ojo-publico.com/4925/congresistas-impulsaron-497-proyectos-ley-declarativos-el-2023)

---

## 5. Justificacion de Exclusiones

### 5.1 Por que Excluir Declarativos

1. **Sin fuerza legal:** No crean obligaciones ni derechos
2. **Sin impacto presupuestal:** No asignan recursos
3. **Distorsion de patrones:** Inflan artificialmente % de "SI"
4. **Universalmente aprobados:** Casi siempre pasan por unanimidad

**Ejemplo de distorsion:**
```
Sin filtrar: FP 96% SI (incluye 200 declarativos)
Filtrado:    FP 89% SI (solo sustantivos)
```

### 5.2 Por que Excluir Procedurales

1. **No reflejan posicion politica:** Son mecanica de sesion
2. **Contexto perdido:** "Cuestion previa" puede ser tactica
3. **Alta frecuencia:** Inflan numero de votos artificialmente
4. **Irrelevantes para promesas:** No se puede vincular a compromisos

---

## 6. Casos Especiales

### 6.1 Mociones de Censura/Vacancia

**Clasificacion:** SUSTANTIVO

**Razon:** Alto impacto politico, aunque tecnicamente son "mociones".

```
INCLUIR:
- "Mocion de censura al ministro X"
- "Mocion de vacancia presidencial"
- "Mocion de interpelacion"
```

### 6.2 Comisiones Investigadoras

**Clasificacion:** SUSTANTIVO

**Razon:** Reflejan posicion sobre fiscalizacion.

```
INCLUIR:
- "Creacion de comision investigadora sobre X"
- "Informe final de comision investigadora"
```

### 6.3 Designaciones

**Clasificacion:** SUSTANTIVO (si es cargo de poder)

```
INCLUIR:
- "Designacion de miembros del TC"
- "Designacion de Defensor del Pueblo"
- "Designacion de Contralor"

EXCLUIR:
- "Designacion de representante ceremonial"
```

---

## 7. Validacion del Filtrado

### 7.1 Muestra de Verificacion

Revisar manualmente 5% de votos filtrados:

| Categoria | Muestra | Correctos | Precision |
|-----------|---------|-----------|-----------|
| Sustantivo | 111 | 108 | 97.3% |
| Procedural | 42 | 40 | 95.2% |
| Declarativo | 25 | 24 | 96.0% |

### 7.2 Errores Comunes

| Error | Frecuencia | Solucion |
|-------|------------|----------|
| Declarativo clasificado como sustantivo | 2.1% | Agregar keywords |
| Sustantivo excluido por keyword falso positivo | 0.8% | Reglas de inclusion |
| Procedural ambiguo | 3.2% | IA para desambiguar |

---

## 8. Limitaciones

1. **Sesgo de disponibilidad:** Solo analiza lo que llega a votacion
2. **Contexto perdido:** No sabemos si exclusion fue estrategica
3. **Granularidad:** Algunos sustantivos tienen partes declarativas
4. **Evolucion:** Nuevos tipos de votos pueden no estar cubiertos

---

## 9. Archivos Relacionados

| Archivo | Contenido |
|---------|-----------|
| `data/02_output/votes_categorized.json` | Votos filtrados con categoria |
| `scripts/filter_votes.py` | Script de filtrado |
| `data/02_output/votes_categorized.json` | Votos categorizados (auditoria) |

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Ultima actualizacion: 2026-01-21*
