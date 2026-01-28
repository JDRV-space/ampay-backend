# Metodología de Detección AMPAY v4
## Búsqueda Dual: Directa + Inversa

**Versión:** 4.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO
**Reemplaza:** v3 (solo directa)

---

## INFORMACIÓN CRÍTICA

**Falla de v3:** Solo buscaba leyes que APOYARAN la promesa, verificaba si el partido votó NO.
**Problema:** A veces no existen leyes de apoyo, o el partido vota SÍ en todas ellas.
**Corrección v4:** TAMBIÉN buscar leyes que CONTRADIGAN la promesa, verificar si el partido votó SÍ.

---

## LAS DOS BÚSQUEDAS

### BÚSQUEDA A: Directa (v3)
```
Promesa: "X"
Pregunta: ¿Votó el partido NO en leyes que IMPLEMENTARÍAN X?
AMPAY si: >= 60% votos NO en leyes de implementación
```

### BÚSQUEDA B: Inversa (NUEVA)
```
Promesa: "X"
Pregunta: ¿Votó el partido SÍ en leyes que CONTRADECIRÍAN X?
AMPAY si: >= 60% votos SÍ en leyes contradictorias
```

**Ambas búsquedas deben ejecutarse para cada promesa.**

---

## EJEMPLO: FP-2021-005

**Promesa:** "Implementar reforma tributaria con principio de universalidad"

### Búsqueda A (Directa):
- Leyes que implementan "universalidad" (eliminando exoneraciones): **0 encontradas**
- Resultado: DATOS INSUFICIENTES

### Búsqueda B (Inversa):
- Leyes que CONTRADICEN "universalidad" (extendiendo exoneraciones): **4 encontradas**
  - PL 3740: Prorrogar apéndices IGV
  - PL 3195: Prorrogar devolución IGV mineras/hidrocarburos (x2 votos)
  - PL 6473: Prorrogar exoneración mercado valores
- FP votó SÍ en: **4/4 = 100%**
- Resultado: **AMPAY (INVERSO)**

### Veredicto Final: AMPAY
- Búsqueda directa: Datos insuficientes
- Búsqueda inversa: 100% contradicción
- Combinado: AMPAY confirmado vía inversa

---

## PASOS DE LA METODOLOGÍA

### PASO 1: Extraer Palabras Clave de la Promesa
```
Promesa: "Formalizar MYPES"
Palabras clave: mype, micro empresa, formalizar
```

### PASO 2: Definir Leyes de Apoyo vs Leyes Contradictorias

**Leyes de apoyo (para búsqueda Directa):**
- Leyes que AYUDARÍAN a lograr la promesa
- Ejemplo: Programas de formalización MYPE, beneficios tributarios MYPE

**Leyes contradictorias (para búsqueda Inversa):**
- Leyes que PERJUDICARÍAN o IMPEDIRÍAN la promesa
- Ejemplo: Más regulación para pequeñas empresas, impuestos a MYPES

### PASO 3: Buscar Leyes Específicas

```bash
# Directa: Leyes que apoyan la promesa
jq '.votes[] | select(.asunto | contains("PALABRA_CLAVE_APOYO"))'

# Inversa: Leyes que contradicen la promesa
jq '.votes[] | select(.asunto | contains("PALABRA_CLAVE_CONTRADICCION"))'
```

### PASO 4: Verificar Posición del Partido en CADA Ley

Para cada ley específica encontrada:
- Directa: Verificar si el partido votó NO (bloqueando su propia promesa)
- Inversa: Verificar si el partido votó SÍ (apoyando la contradicción)

### PASO 5: Calcular Proporciones

**Proporción directa:**
```
Votos NO en leyes de apoyo / Total leyes de apoyo
>= 60% = AMPAY (DIRECTO)
```

**Proporción inversa:**
```
Votos SÍ en leyes contradictorias / Total leyes contradictorias
>= 60% = AMPAY (INVERSO)
```

### PASO 6: Veredicto Final

| Directa | Inversa | Veredicto |
|---------|---------|-----------|
| AMPAY | AMPAY | AMPAY (fuerte) |
| AMPAY | NO | AMPAY (directo) |
| NO | AMPAY | AMPAY (inverso) |
| NO | NO | NO AMPAY |
| INSUF | AMPAY | AMPAY (inverso) |
| AMPAY | INSUF | AMPAY (directo) |
| INSUF | INSUF | DATOS INSUFICIENTES |

---

## PARES DE PALABRAS CLAVE POR TIPO DE PROMESA

### Promesas Tributarias
| Tipo de Promesa | Palabras Clave de Apoyo | Palabras Clave Contradictorias |
|-----------------|-------------------------|--------------------------------|
| Universalidad | eliminar exoneración, derogar beneficio | prorrogar, extender exoneración, régimen especial |
| Simplificación | simplificar, unificar | nuevo impuesto, nuevo régimen |
| Reducir impuestos | reducir, eliminar impuesto | aumentar, crear impuesto |

### Promesas Sociales
| Tipo de Promesa | Palabras Clave de Apoyo | Palabras Clave Contradictorias |
|-----------------|-------------------------|--------------------------------|
| Reducir pobreza | programa social, bono, subsidio | recortar, eliminar programa |
| Proteger trabajadores | derechos laborales, salario mínimo | flexibilizar, tercerizar |
| Formalizar MYPES | formalizar, mype, micro empresa | fiscalizar mype, sancionar informal |

### Promesas Ambientales
| Tipo de Promesa | Palabras Clave de Apoyo | Palabras Clave Contradictorias |
|-----------------|-------------------------|--------------------------------|
| Proteger ambiente | protección ambiental, conservar | exonerar minería, prorrogar formalización minera |
| Reducir conflictos | diálogo, consulta previa | acelerar concesión, simplificar EIA |

---

## UMBRALES AMPAY

| Proporción | Estado |
|------------|--------|
| >= 60% | **AMPAY** |
| 40-59% | **AMPAY POTENCIAL** |
| < 40% | **NO AMPAY** |
| < 3 leyes encontradas | **DATOS INSUFICIENTES** |

**Nota:** Aplicar los mismos umbrales tanto para búsquedas Directas como Inversas.

---

## FORMATO DE SALIDA

```json
{
  "promise_id": "FP-2021-005",
  "promise_text": "Implementar reforma tributaria con principio de universalidad",
  "party": "Fuerza Popular",

  "direct_search": {
    "keywords": ["eliminar exoneración", "universalidad tributaria"],
    "laws_found": 0,
    "si_votes": 0,
    "no_votes": 0,
    "no_percentage": null,
    "status": "DATOS_INSUFICIENTES"
  },

  "inverse_search": {
    "keywords": ["prorrogar exoneración", "extender beneficio", "régimen especial"],
    "laws_found": 4,
    "laws_detail": [
      {"asunto": "PL 3740 prorrogar IGV", "position": "SI"},
      {"asunto": "PL 3195 devolución IGV mineras", "position": "SI"},
      {"asunto": "PL 3195 segunda votación", "position": "SI"},
      {"asunto": "PL 6473 prorrogar exoneración valores", "position": "SI"}
    ],
    "si_votes": 4,
    "no_votes": 0,
    "si_percentage": 100,
    "status": "AMPAY"
  },

  "final_verdict": "AMPAY",
  "ampay_type": "INVERSO",
  "reasoning": "FP prometió 'universalidad tributaria' pero votó SÍ en el 100% de las leyes que extienden tratamiento tributario especial para corporaciones."
}
```

---

## LISTA DE VERIFICACIÓN

Antes de marcar AMPAY:

- [ ] ¿Buscamos leyes ESPECÍFICAS (no agregación por categoría)?
- [ ] ¿Ejecutamos AMBAS búsquedas Directa e Inversa?
- [ ] ¿Verificamos la posición del partido en CADA ley específica?
- [ ] ¿Verificamos que la ley realmente apoya/contradice la promesa (no solo coincidencia de palabras clave)?
- [ ] ¿Es la proporción >= 60%?

---

## COMPARACIÓN: v3 vs v4

| Aspecto | v3 | v4 |
|---------|----|----|
| Dirección de búsqueda | Solo directa | Directa + Inversa |
| Pregunta formulada | ¿Votaron NO en leyes de apoyo? | TAMBIÉN: ¿Votaron SÍ en leyes contradictorias? |
| Detecta | Oposición activa | Oposición activa + Contradicción activa |
| Resultado FP-2021-005 | DATOS INSUFICIENTES | **AMPAY (inverso)** |

---

## ARCHIVOS

- v2 (obsoleto): `METHODOLOGY_V2_DEPRECATED.md`
- v3 (superado): `METHODOLOGY_V3.md`
- v4 (actual): `METHODOLOGY_V4.md`
- Línea base de categorías: `CATEGORY_VOTING_PATTERNS.md`

---

## PRIMER AMPAY ENCONTRADO

**FP-2021-005:** "Implementar reforma tributaria con principio de universalidad"
- **Tipo:** AMPAY INVERSO
- **Evidencia:** Votó SÍ en 4/4 leyes que extienden tratamiento tributario especial
- **Validación:** Perú Libre votó NO en las mismas leyes (consistente con su promesa anti-exoneración)

---

**FIN DE METODOLOGÍA v4**
