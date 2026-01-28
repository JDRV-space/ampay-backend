# Registro de Auditoria (Audit Trail)

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Este documento registra todas las decisiones metodologicas, cambios de datos, y validaciones realizadas durante el desarrollo de AMPAY.

---

## 1. Decisiones Metodologicas

### 1.1 Seleccion de Algoritmo de Quiz

| Fecha | Decision | Alternativas Consideradas | Justificacion |
|-------|----------|---------------------------|---------------|
| 2026-01-19 | Manhattan distance | Euclidiana, Coseno | Estandar en VAAs, interpretacion intuitiva |
| 2026-01-19 | Escala 3 puntos | 5 puntos Likert | Simplicidad para quiz corto |
| 2026-01-19 | Sin ponderacion | Ponderacion por importancia | Evitar sesgos en seleccion de temas |

### 1.2 Criterios de AMPAY

| Fecha | Decision | Valor | Justificacion |
|-------|----------|-------|---------------|
| 2026-01-20 | Umbral AMPAY | >= 60% | Balance precision/recall |
| 2026-01-20 | Umbral potencial | 40-59% | Zona gris para revision |
| 2026-01-20 | Minimo de leyes | >= 3 | Evitar conclusiones de un solo dato |
| 2026-01-21 | Sistema de confianza | HIGH/MEDIUM/LOW | Transparencia en certeza |

### 1.3 Categorizacion

| Fecha | Decision | Valor | Justificacion |
|-------|----------|-------|---------------|
| 2026-01-18 | Numero de categorias | 13 | Balance granularidad/usabilidad |
| 2026-01-18 | Excluir digitalizacion | N/A | Es transversal, no categoria |
| 2026-01-18 | Una categoria por voto | N/A | Evitar doble conteo |

### 1.4 Fuentes de Posiciones

| Fecha | Decision | Alternativas | Justificacion |
|-------|----------|--------------|---------------|
| 2026-01-19 | Solo promesas 2026 | Promesas + votos | Quiz es para 2026, AMPAY cubre votos |
| 2026-01-19 | Silencio = 0 | Inferir posicion | Consistente con MARPOR |

---

## 2. Cambios de Datos

### 2.1 Dataset de Votaciones

| Fecha | Evento | Detalles |
|-------|--------|----------|
| 2026-01-15 | Descarga inicial | openpolitica, 289K votos |
| 2026-01-16 | Filtrado declarativos | 497 votos excluidos |
| 2026-01-16 | Filtrado procedurales | 847 votos excluidos |
| 2026-01-16 | Dataset final | 2,226 votos sustantivos |

### 2.2 Promesas Extraidas

| Fecha | Partido | Evento | Detalles |
|-------|---------|--------|----------|
| 2026-01-15 | Todos | Extraccion inicial | 372 promesas brutas |
| 2026-01-16 | Todos | Validacion | 345 promesas validas |
| 2026-01-17 | FP | Correccion | Promesa FP-2021-023 reclasificada |

### 2.3 AMPAYs

| Fecha | AMPAY ID | Evento | Detalles |
|-------|----------|--------|----------|
| 2026-01-20 | AMPAY-001 | Detectado | FP universalidad tributaria |
| 2026-01-20 | AMPAY-001 | Validado | 6 leyes, 100% SI, HIGH |
| 2026-01-20 | AMPAY-002 | Detectado | RP regimenes tributarios |
| 2026-01-20 | AMPAY-002 | Validado | 5 leyes, 100% SI, HIGH |
| 2026-01-21 | AMPAY-003 | Detectado | RP exportaciones |
| 2026-01-21 | AMPAY-003 | Validado | HIGH |
| 2026-01-21 | (varios) | Rechazados | 15 falsos positivos descartados |

---

## 3. Validaciones Realizadas

### 3.1 Calidad de Datos

| Fecha | Validacion | Resultado | Accion |
|-------|------------|-----------|--------|
| 2026-01-16 | Completitud votaciones | 99.7% | Aceptado |
| 2026-01-16 | Precision categorizacion | 94.8% | Aceptado |
| 2026-01-17 | Fuentes de promesas | 100% verificables | Aceptado |

### 3.2 AMPAYs

| Fecha | AMPAY | Revisor | Resultado |
|-------|-------|---------|-----------|
| 2026-01-20 | AMPAY-001 | JD | Aprobado (HIGH) |
| 2026-01-20 | AMPAY-002 | JD | Aprobado (HIGH) |
| 2026-01-21 | AMPAY-003 | JD | Aprobado (HIGH) |
| 2026-01-21 | AMPAY-004 | JD | Aprobado (HIGH) |
| 2026-01-21 | AMPAY-005 | JD | Aprobado (MEDIUM) |
| 2026-01-21 | AMPAY-006 | JD | Aprobado (MEDIUM) |
| 2026-01-21 | AMPAY-007 | JD | Aprobado (MEDIUM) |
| 2026-01-21 | AMPAY-008 | JD | Aprobado (MEDIUM) |

### 3.3 Falsos Positivos Rechazados

| Fecha | Candidato | Razon de Rechazo |
|-------|-----------|------------------|
| 2026-01-20 | AC-FP-001 | Conexion semantica debil |
| 2026-01-20 | AC-FP-002 | Solo 1 voto (patron insuficiente) |
| 2026-01-20 | AC-PL-001 | Contexto exculpatorio (Amazonia) |
| 2026-01-21 | (varios) | Ver archivo ampay_review_log.json |

---

## 4. Cambios de Metodologia

### 4.1 Evolucion de Versiones

| Fecha | Version | Cambio | Razon |
|-------|---------|--------|-------|
| 2026-01-18 | v1 → v2 | Agregacion por categoria | v1 tenia muchos falsos positivos |
| 2026-01-19 | v2 → v3 | Busqueda por keywords | v2 perdia especificidad |
| 2026-01-20 | v3 → v4 | Agregar busqueda inversa | v3 solo detectaba tipo A |
| 2026-01-21 | v4 → v5 | Sistema de confianza | v4 no distinguia certeza |

### 4.2 Archivos Afectados por Cambios

| Cambio | Archivos Regenerados |
|--------|---------------------|
| v1 → v2 | Ninguno (metodologia rechazada) |
| v2 → v3 | ampays.json |
| v3 → v4 | ampays.json |
| v4 → v5 | ampays.json, documentacion |

---

## 5. Incidentes y Correcciones

### 5.1 Errores Detectados

| Fecha | Error | Severidad | Correccion |
|-------|-------|-----------|------------|
| 2026-01-17 | Promesa duplicada | Baja | Eliminada FP-2021-023b |
| 2026-01-19 | Categoria incorrecta | Media | Reclasificados 12 votos |
| 2026-01-20 | AMPAY falso positivo publicado | Alta | Retirado antes de QA |

### 5.2 Gaps de Datos Conocidos

| Gap | Identificado | Estado |
|-----|--------------|--------|
| Votaciones 2024-07 a 2026-01 | 2026-01-15 | Documentado, sin resolucion |
| Votos secretos | 2026-01-15 | Limitacion inherente |
| Partidos sin plan 2026 detallado | 2026-01-18 | Documentado |

---

## 6. Revisiones de Calidad

### 6.1 Muestreo de Votaciones

| Fecha | Muestra | Precision |
|-------|---------|-----------|
| 2026-01-16 | 200 votos | 94.8% |
| 2026-01-17 | 50 votos frontera | 91.0% |

### 6.2 Muestreo de Promesas

| Fecha | Muestra | Precision |
|-------|---------|-----------|
| 2026-01-17 | 100 promesas | 91.7% |

### 6.3 Verificacion de Fuentes

| Fecha | Verificacion | Resultado |
|-------|--------------|-----------|
| 2026-01-21 | URLs en bibliografia | 100% funcionando |
| 2026-01-21 | DOIs academicos | 100% resuelven |
| 2026-01-21 | PDFs de JNE | 100% accesibles |

---

## 7. Responsables

| Rol | Persona | Tareas |
|-----|---------|--------|
| Lider del proyecto | JD | Decisiones metodologicas, validacion |
| Desarrollador | JD | Implementacion, datos |
| Revisor AMPAY | JD | Validacion manual de AMPAYs |

---

## 8. Proximos Pasos

| Fecha Objetivo | Tarea | Estado |
|----------------|-------|--------|
| 2026-01-22 | Soft launch | Pendiente |
| 2026-01-25 | Feedback inicial | Pendiente |
| 2026-02-01 | Correccion de errores post-launch | Pendiente |
| 2026-Q2 | Actualizacion datos 2024-2026 | Planeado |

---

## 9. Control de Versiones

### 9.1 Archivos Versionados

| Archivo | Version Actual | Ultima Modificacion |
|---------|----------------|---------------------|
| quiz_statements.json | 2.1 | 2026-01-21 |
| ampays.json | 1.0 | 2026-01-21 |
| votes_categorized.json | 1.0 | 2026-01-21 |
| party_patterns.json | 1.0 | 2026-01-21 |

### 9.2 Git History

```
Commits relevantes:
- 2026-01-15: Initial data import
- 2026-01-18: Methodology v1-v2
- 2026-01-20: Methodology v3-v4, first AMPAYs
- 2026-01-21: Methodology v5, documentation complete
```

---

*Ultima actualizacion: 2026-01-21*
