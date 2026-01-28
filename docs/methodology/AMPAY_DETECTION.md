# Deteccion de AMPAYs: Metodologia v5

**Version:** 5.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO
**Reemplaza:** v4 (busqueda dual), v3 (busqueda directa), v2 (agregacion por categoria)

---

## Resumen Ejecutivo

Un **AMPAY** es una contradiccion verificable entre una promesa de campana y el comportamiento de votacion del partido en el Congreso. La deteccion utiliza busqueda dual (directa + inversa) sobre leyes especificas.

---

## 1. Definicion de AMPAY

### 1.1 Que es un AMPAY

```
AMPAY = Partido voto de manera contraria a su promesa de campana
```

**Tipos de AMPAY:**

| Tipo | Descripcion | Ejemplo |
|------|-------------|---------|
| **Tipo A (Directo)** | Partido voto NO en leyes que implementarian su promesa | Prometio "aumentar presupuesto educacion", voto NO en ley de aumento |
| **Tipo B (Inverso)** | Partido voto SI en leyes que contradicen su promesa | Prometio "eliminar exoneraciones", voto SI en ley que las extiende |

### 1.2 Que NO es un AMPAY

- Un solo voto aislado (patron requerido, minimo 3 leyes)
- Voto por razones procedimentales documentadas
- Promesa vaga sin leyes relacionadas identificables
- Datos insuficientes (< 3 leyes encontradas)

---

## 2. Proceso de Deteccion

### 2.1 Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────┐
│                     PROMESA DE CAMPANA                          │
│  "Implementar reforma tributaria con universalidad"             │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────┴────────────────────┐
         │                                         │
         ▼                                         ▼
┌─────────────────────┐               ┌─────────────────────┐
│   BUSQUEDA A        │               │   BUSQUEDA B        │
│   (Directa)         │               │   (Inversa)         │
│                     │               │                     │
│ Leyes que           │               │ Leyes que           │
│ IMPLEMENTAN         │               │ CONTRADICEN         │
│ la promesa          │               │ la promesa          │
└──────────┬──────────┘               └──────────┬──────────┘
           │                                     │
           ▼                                     ▼
┌─────────────────────┐               ┌─────────────────────┐
│ ¿Partido voto NO    │               │ ¿Partido voto SI    │
│  en estas leyes?    │               │  en estas leyes?    │
└──────────┬──────────┘               └──────────┬──────────┘
           │                                     │
           ▼                                     ▼
    ┌──────┴──────┐                       ┌──────┴──────┐
    │ >= 60% NO   │                       │ >= 60% SI   │
    │ = AMPAY (A) │                       │ = AMPAY (B) │
    └─────────────┘                       └─────────────┘
```

### 2.2 Paso 1: Extraccion de Keywords

De cada promesa, extraer terminos buscables:

```
Promesa: "Formalizar un millon de nuevas MYPES"
Partido: Fuerza Popular
ID: FP-2021-002

Keywords extraidos:
├── Sustantivos: mype, mypes, micro empresa, pequena empresa
├── Verbos: formalizar, formalizacion
├── Sinonimos: microempresa, emprendimiento
└── Tecnicismos: RUC, RUS, regimen especial
```

### 2.3 Paso 2: Busqueda Dual

**Busqueda A (Directa):**
- Encontrar leyes que IMPLEMENTARIAN la promesa
- Verificar si el partido voto NO

**Busqueda B (Inversa):**
- Encontrar leyes que CONTRADICEN la promesa
- Verificar si el partido voto SI

```bash
# Ejemplo busqueda para "universalidad tributaria"

# Busqueda A: Leyes que eliminan exoneraciones (implementan)
jq '.votes[] | select(.asunto | contains("eliminar exoneracion"))'

# Busqueda B: Leyes que extienden exoneraciones (contradicen)
jq '.votes[] | select(.asunto | contains("prorrogar") or contains("extender exoneracion"))'
```

### 2.4 Paso 3: Calculo de Ratios

**Ratio Directo:**
```
NO_votes_en_leyes_implementadoras / Total_leyes_implementadoras
>= 60% = AMPAY (TIPO A)
```

**Ratio Inverso:**
```
SI_votes_en_leyes_contradictorias / Total_leyes_contradictorias
>= 60% = AMPAY (TIPO B)
```

### 2.5 Paso 4: Matriz de Decision

| Busqueda A | Busqueda B | Veredicto Final |
|------------|------------|-----------------|
| AMPAY | AMPAY | **AMPAY (fuerte)** |
| AMPAY | NO | **AMPAY (directo)** |
| NO | AMPAY | **AMPAY (inverso)** |
| NO | NO | NO AMPAY |
| INSUF | AMPAY | **AMPAY (inverso)** |
| AMPAY | INSUF | **AMPAY (directo)** |
| INSUF | INSUF | DATOS INSUFICIENTES |

---

## 3. Umbrales y Filtros

### 3.1 Umbrales de Clasificacion

| Porcentaje | Estado | Accion |
|------------|--------|--------|
| >= 60% | **AMPAY** | Publicar con revision manual |
| 40-59% | **POTENCIAL AMPAY** | Requiere revision detallada |
| < 40% | **NO AMPAY** | No publicar |
| < 3 leyes | **DATOS INSUFICIENTES** | No evaluar |

### 3.2 Filtros Aplicados

1. **Solo votos sustantivos:** Excluir declarativos y procedimentales
2. **Relevancia semantica:** La ley debe relacionarse directamente con la promesa
3. **Verificacion humana:** Cada AMPAY revisado antes de publicar

---

## 4. Niveles de Confianza

### 4.1 Sistema de Confianza

| Nivel | Criterios | Accion |
|-------|-----------|--------|
| **HIGH** | >= 60% ratio + >= 5 leyes + clara conexion semantica | Auto-publicar con flag |
| **MEDIUM** | >= 60% ratio + 3-4 leyes O conexion semantica debil | Revision obligatoria |
| **LOW** | 40-59% ratio O datos limitados | No publicar sin investigacion adicional |

### 4.2 Ejemplos de Clasificacion

**AMPAY-001 (HIGH):**
```json
{
  "promise": "Universalidad tributaria",
  "inverse_search": {
    "laws_found": 6,
    "si_percentage": 100
  },
  "confidence": "HIGH",
  "reasoning": "6/6 votos SI en leyes que extienden regimenes especiales"
}
```

**AMPAY-006 (MEDIUM):**
```json
{
  "promise": "Fortalecer sistema electoral",
  "direct_search": {
    "laws_found": 2,
    "no_percentage": 100
  },
  "confidence": "MEDIUM",
  "reasoning": "Solo 2 mociones encontradas, pero patron claro"
}
```

---

## 5. Revision Manual

### 5.1 Checklist de Verificacion

Antes de publicar cualquier AMPAY:

- [ ] ¿La promesa es verificable y especifica?
- [ ] ¿Las leyes encontradas se relacionan directamente con la promesa?
- [ ] ¿El partido tuvo oportunidad real de votar (quorum)?
- [ ] ¿Existe contexto adicional que explique el voto?
- [ ] ¿El ratio cumple el umbral (>= 60%)?
- [ ] ¿Hay al menos 3 leyes analizadas?

### 5.2 Proceso de Revision

```
1. Analista revisa AMPAY automatico
2. Verifica fuentes (PDF de promesa, acta de votacion)
3. Confirma conexion semantica promesa-ley
4. Documenta reasoning
5. Aprueba o rechaza
6. Si aprobado, entra a publicacion
```

### 5.3 Documentacion de Rechazo

Si un AMPAY potencial es rechazado, documentar:
- Razon del rechazo
- Evidencia que lo descarta
- Fecha de revision
- Revisor responsable

---

## 6. Evolucion de la Metodologia

### 6.1 Historia de Versiones

| Version | Problema Identificado | Solucion Implementada |
|---------|----------------------|----------------------|
| v1 | Comparacion voto-por-voto sin patron | Agregacion por categoria |
| v2 | Agregacion perdio especificidad | Busqueda por keywords especificos |
| v3 | Solo buscaba leyes de apoyo | Agrego busqueda inversa |
| v4 | Busqueda dual incompleta | Matriz de decision completa |
| v5 | Umbrales arbitrarios | Sistema de confianza calibrado |

### 6.2 v3 vs v4 vs v5

| Aspecto | v3 | v4 | v5 |
|---------|----|----|----|-
| Direccion busqueda | Solo directa | Directa + inversa | Directa + inversa |
| Umbral AMPAY | 60% NO | 60% cualquier direccion | 60% + confianza |
| Leyes minimas | 3 | 3 | 3 con ajuste por tipo |
| Revision humana | No | Parcial | Obligatoria |
| Nivel confianza | No | No | Si |

---

## 7. Ejemplos Documentados

### 7.1 AMPAY Confirmado (Tipo B - Inverso)

```
ID: AMPAY-001
Partido: Fuerza Popular
Promesa: "Implementar reforma tributaria con principio de universalidad"

Busqueda A (Directa):
- Leyes encontradas: 0
- Estado: DATOS INSUFICIENTES

Busqueda B (Inversa):
- Keywords: "prorrogar exoneracion", "extender beneficio", "regimen especial"
- Leyes encontradas: 6
  1. PL 3740 - Prorrogar apendices IGV → FP voto SI
  2. PL 3195 - Devolucion IGV mineras/hidrocarburos → FP voto SI
  3. PL 3195 - Segunda votacion → FP voto SI
  4. PL 6473 - Prorrogar exoneracion valores → FP voto SI
  5. PL 3155 - Regimenes especiales depreciacion → FP voto SI
  6. PL 3671 - Incentivos fiscales fondos → FP voto SI
- SI votes: 6/6 = 100%
- Estado: AMPAY

Veredicto: AMPAY (TIPO B - INVERSO)
Confianza: HIGH
Reasoning: FP prometio universalidad tributaria pero voto SI en 6/6 leyes que extienden regimenes especiales.
```

### 7.2 NO AMPAY (Patron de Apoyo)

```
ID: NO-AMPAY-FP-002
Partido: Fuerza Popular
Promesa: "Formalizar un millon de nuevas MYPES"

Busqueda A (Directa):
- Keywords: "mype", "micro empresa", "formalizacion"
- Leyes encontradas: 26
- FP voto SI: 26/26 = 100%
- Estado: NO AMPAY

Veredicto: NO AMPAY
Reasoning: FP apoyo consistentemente legislacion MYPE.
```

---

## 8. Limitaciones

1. **Disponibilidad de datos:** Solo analiza periodo 2021-07 a 2024-07
2. **Ausencias:** No distingue entre ausencia justificada y evasion
3. **Contexto legislativo:** No captura negociaciones previas o compromisos
4. **Complejidad legal:** Leyes con multiples articulos pueden tener aspectos positivos y negativos
5. **Cambio de partido:** Congresistas transfugas afectan conteo por partido

---

## 9. Archivos Relacionados

| Archivo | Contenido |
|---------|-----------|
| `data/02_output/ampays.json` | AMPAYs confirmados |
| `data/02_output/AMPAY_CONFIRMED_2021.json` | Detalle de evidencia |
| `docs/methodology/archive/METHODOLOGY_V*.md` | Versiones anteriores |

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Ultima actualizacion: 2026-01-21*
