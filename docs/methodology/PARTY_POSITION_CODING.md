# Codificacion de Posiciones de Partidos

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Las posiciones de los partidos politicos se codifican en una escala de +1/0/-1 basandose en sus promesas de campana documentadas. El silencio se interpreta como posicion neutral (0).

---

## 1. Sistema de Codificacion

### 1.1 Escala de Posiciones

| Valor | Significado | Criterio |
|-------|-------------|----------|
| **+1** | APOYA | Promesa explicita a favor del tema |
| **0** | NEUTRAL | Sin promesa clara o silencio sobre el tema |
| **-1** | SE OPONE | Promesa explicita en contra del tema |

### 1.2 Fuente de Posiciones

**Fuente unica:** Planes de gobierno 2026 registrados en JNE

```
URL: https://plataformaelectoral.jne.gob.pe/candidatos/plan-gobierno-trabajo/buscar
Formato: PDF
Acceso: Enero 2026
```

**Por que solo 2026 (no voting records):**
1. El quiz es para elecciones 2026 → usar propuestas 2026
2. Registros de votacion son 2021-2024 (datos historicos)
3. La feature AMPAY ya cubre discrepancias promesa-voto
4. Simplifica el desarrollo

---

## 2. Reglas de Codificacion

### 2.1 Criterios para +1 (APOYA)

Una posicion se codifica +1 cuando el plan de gobierno contiene:

1. **Compromiso explicito:** "Implementaremos X", "Crearemos Y"
2. **Mencion favorable repetida:** El tema aparece 3+ veces positivamente
3. **Verbo de accion positivo:** aumentar, expandir, crear, fortalecer, garantizar
4. **Prioridad declarada:** El tema aparece en prioridades o ejes principales

**Ejemplos:**
```
"Implementaremos la nacionalizacion del gas de Camisea" → +1 en energia
"Fortaleceremos los sindicatos" → +1 en empleo/derechos laborales
"Expandiremos el sistema publico de salud" → +1 en salud publica
```

### 2.2 Criterios para -1 (SE OPONE)

Una posicion se codifica -1 cuando el plan de gobierno contiene:

1. **Oposicion explicita:** "Eliminaremos X", "Rechazamos Y"
2. **Mencion negativa:** El tema se presenta como problema a corregir
3. **Verbo de accion negativo:** reducir, eliminar, recortar, privatizar (en contexto)
4. **Propuesta contraria:** Alternativa incompatible con la posicion +1

**Ejemplos:**
```
"Reduciremos la intervencion estatal en la economia" → -1 en economia estatista
"Eliminaremos exoneraciones tributarias" → -1 en beneficios fiscales
"Privatizaremos servicios ineficientes" → -1 en servicios publicos
```

### 2.3 Criterios para 0 (NEUTRAL)

Una posicion se codifica 0 cuando:

1. **Silencio total:** El tema no aparece en el plan de gobierno
2. **Mencion ambigua:** Lenguaje vago sin compromiso claro
3. **Posicion contradictoria:** El plan contiene afirmaciones en ambas direcciones
4. **Condicionamiento excesivo:** "Estudiaremos", "Si es posible", "Evaluaremos"

**Ejemplos:**
```
(Tema no mencionado) → 0
"Evaluaremos la posibilidad de reformar el sistema tributario" → 0
"Mejoraremos la economia" (sin especificar como) → 0
```

---

## 3. Proceso de Codificacion

### 3.1 Flujo de Trabajo

```
┌─────────────────────────────────────────┐
│      PDF PLAN DE GOBIERNO (JNE)         │
└────────────────────┬────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  EXTRACCION DE TEXTO  │
         │  (PyMuPDF/Tesseract)  │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  IDENTIFICAR PROMESAS │
         │  RELEVANTES AL QUIZ   │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  ASIGNAR POSICION     │
         │  (+1 / 0 / -1)        │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  DOCUMENTAR FUENTE    │
         │  (ID promesa + pagina)│
         └───────────────────────┘
```

### 3.2 Documentacion de Fuentes

Cada posicion codificada debe tener:

```json
{
  "party": "peru_libre",
  "question": "Q01",
  "position": 1,
  "source_promises": ["PL-2026-024", "PL-2026-049"],
  "evidence": "Plan de gobierno p.47: 'Nacionalizaremos el gas de Camisea'",
  "confidence": "HIGH"
}
```

---

## 4. Tratamiento del Silencio

### 4.1 Logica de Silencio = 0

**Justificacion academica:**

El Manifesto Project (MARPOR) distingue entre SALIENCIA (cuanto enfatiza un tema) y POSICION (que opina del tema). Cuando un partido no menciona un tema:

1. No podemos inferir su posicion real
2. El silencio puede ser estrategico o por omision
3. Asignar +1 o -1 seria especulacion

**Referencia:** Werner, A., et al. (2023). "Manifesto Project Codebook v6". DOI: [10.25522/manifesto.v6](https://doi.org/10.25522/manifesto.v6)

### 4.2 Casos Especiales de Silencio

| Situacion | Codificacion | Razon |
|-----------|--------------|-------|
| Tema no mencionado | 0 | Sin datos |
| Mencion sin posicion | 0 | Ambiguedad |
| Promesa + contra-promesa | 0 | Contradiccion interna |
| "Evaluaremos" / "Estudiaremos" | 0 | No es compromiso |

---

## 5. Mapeo Partidos-Ideologia

### 5.1 Eje Economico

| Partido | Posicion Economica | Evidencia |
|---------|-------------------|-----------|
| Peru Libre | Izquierda | Nacionalizacion, control estatal |
| Juntos por el Peru | Izquierda | Impuestos progresivos, gasto social |
| Partido Morado | Centro | Economia mixta, regulacion |
| Somos Peru | Centro | Pragmatismo, sin ideologia fija |
| Alianza para el Progreso | Centro | Empresarial pero social |
| Fuerza Popular | Derecha | Libre mercado, reduccion estado |
| Renovacion Popular | Derecha | Conservador fiscal |
| Avanza Pais | Derecha | Liberal economico |
| Podemos Peru | Derecha | Pro-empresa |

### 5.2 Eje Social

| Partido | Posicion Social | Evidencia |
|---------|----------------|-----------|
| Renovacion Popular | Conservador | Pro-familia tradicional, anti-genero |
| Peru Libre | Conservador | Tradicionalismo andino |
| Fuerza Popular | Moderado | Sin posiciones sociales extremas |
| Podemos Peru | Moderado | Pragmatico |
| Alianza Progreso | Moderado | Sin agenda social fuerte |
| Avanza Pais | Moderado | Liberal economico, moderado social |
| Somos Peru | Moderado | Sin posiciones definidas |
| Partido Morado | Progresista | Derechos civiles, diversidad |
| Juntos por el Peru | Progresista | Derechos humanos, genero |

---

## 6. Validacion de Posiciones

### 6.1 Proceso de Auditoria

Para cada pregunta del quiz:

1. **Revisar promesa fuente:** Verificar que el texto citado existe en el PDF
2. **Confirmar interpretacion:** La codificacion refleja el contenido
3. **Cross-check:** Comparar con otras fuentes (noticias, entrevistas)
4. **Peer review:** Segunda persona revisa casos dudosos

### 6.2 Archivo de Auditoria

```
data/02_output/quiz_position_audit.json
```

Contiene:
- Cada posicion codificada
- ID de promesa fuente
- Texto citado
- Pagina del PDF
- Fecha de revision
- Revisor

---

## 7. Preguntas Removidas

### 7.1 Por Consenso Total

Preguntas donde todos los partidos tienen +1:

| Pregunta Original | Razon de Remocion |
|-------------------|-------------------|
| Intangibilidad Amazonia | 9/9 partidos +1 |
| Cobertura universal agua | 9/9 partidos +1 |
| Eliminar burocracia MYPES | 9/9 partidos +1 |

**Logica:** Preguntas sin variacion no discriminan entre partidos.

### 7.2 Por Datos Insuficientes

Preguntas donde menos de 5 partidos tienen posicion clara:

| Pregunta Original | Partidos con Datos |
|-------------------|-------------------|
| (ninguna en v2.1) | N/A |

---

## 8. Comparacion con Otros Enfoques

### 8.1 AMPAY vs Vote Compass

| Aspecto | AMPAY | Vote Compass |
|---------|-------|--------------|
| Fuente posiciones | Solo promesas | Promesas + expertos |
| Escala | 3 puntos (-1/0/+1) | 5 puntos |
| Validacion | Interna | Partidos revisan |
| Silencio | = 0 | Puede inferirse |

### 8.2 AMPAY vs Wahl-O-Mat

| Aspecto | AMPAY | Wahl-O-Mat |
|---------|-------|-----------|
| Quien codifica | Equipo AMPAY | Partidos directamente |
| Fuente | PDFs publicos | Cuestionario a partidos |
| Escala | 3 puntos | 3 puntos |
| Supervision | Sin expertos externos | Panel de expertos |

---

## 9. Limitaciones

1. **Subjetividad:** Interpretacion de promesas vagas
2. **Silencio estrategico:** Partidos evitan temas controversiales
3. **Evolucion de posiciones:** Promesas 2026 pueden cambiar durante campana
4. **Promesas vs intencion real:** Planes de gobierno pueden ser aspiracionales

---

## 10. Archivos Relacionados

| Archivo | Contenido |
|---------|-----------|
| `data/02_output/quiz_statements.json` | Posiciones codificadas |
| `data/02_output/quiz_position_audit.json` | Auditoria de fuentes |
| `data/01_input/promises/` | PDFs originales |

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Ultima actualizacion: 2026-01-21*
