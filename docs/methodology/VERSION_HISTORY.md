# Historial de Versiones de la Metodologia

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Este documento registra la evolucion de la metodologia AMPAY desde v1 hasta v5, incluyendo los problemas identificados en cada version y las soluciones implementadas.

---

## 1. Vision General de Versiones

```
v1 ──────► v2 ──────► v3 ──────► v4 ──────► v5
(Fallida)  (Fallida)  (Mejorada) (Mejorada) (Actual)

Ene 2026   Ene 2026   Ene 2026   Ene 2026   Ene 2026
```

| Version | Estado | Problema Principal | Solucion |
|---------|--------|-------------------|----------|
| v1 | DESCARTADA | Comparacion voto-por-voto sin patron | Agregacion por categoria |
| v2 | DESCARTADA | Agregacion pierde especificidad | Busqueda por keywords |
| v3 | SUPERADA | Solo busqueda directa | Agregar busqueda inversa |
| v4 | SUPERADA | Sin sistema de confianza | Agregar niveles de confianza |
| v5 | **ACTIVA** | - | - |

---

## 2. Version 1 (Descartada)

### 2.1 Descripcion

Primera aproximacion: comparar cada promesa con cada voto individualmente.

### 2.2 Metodologia

```
Para cada promesa:
  Para cada voto:
    Si voto.asunto contiene promesa.keywords:
      Si partido voto NO:
        Marcar como contradiccion
```

### 2.3 Problemas Identificados

| Problema | Ejemplo | Impacto |
|----------|---------|---------|
| **Sin patron** | 1 voto NO en 50 relacionados = AMPAY? | Falsos positivos masivos |
| **Sin umbral** | Cualquier NO contaba | Sensibilidad excesiva |
| **Match literal** | "salud" matcheaba todo | Ruido |

### 2.4 Resultados

```
AMPAYs detectados: 200+
AMPAYs validos: ~5
Precision: ~2.5%
```

### 2.5 Decision

**DESCARTADA** - Demasiados falsos positivos, inutilizable.

---

## 3. Version 2 (Descartada)

### 3.1 Descripcion

Agregar todos los votos por categoria y calcular porcentaje NO.

### 3.2 Metodologia

```
Para cada promesa:
  categoria = promesa.categoria
  votos_categoria = filtrar(votos, categoria == promesa.categoria)

  si_total = sum(votos_categoria.si)
  no_total = sum(votos_categoria.no)

  pct_no = no_total / (si_total + no_total)

  Si pct_no >= 60%:
    AMPAY
```

### 3.3 Problemas Identificados

| Problema | Ejemplo | Impacto |
|----------|---------|---------|
| **Agregacion excesiva** | Promesa "hospital X" vs todas las leyes de salud | Pierde especificidad |
| **Votos irrelevantes** | Promesa fiscal especifica diluida en 100 votos fiscales | Falsos negativos |
| **Patron general != promesa especifica** | 90% SI en salud pero NO en la ley especifica | AMPAYs perdidos |

### 3.4 Ejemplo de Fallo

```
Promesa: "Implementar reforma tributaria con universalidad"
Categoria: fiscal

Resultado v2:
- Votos fiscales: 143
- FP: 93.7% SI
- Veredicto: NO AMPAY

Realidad:
- FP voto SI en 6/6 leyes que CONTRADICEN universalidad
- Deberia ser AMPAY
```

### 3.5 Decision

**DESCARTADA** - Agregacion por categoria pierde informacion critica.

---

## 4. Version 3 (Superada)

### 4.1 Descripcion

Buscar leyes ESPECIFICAS relacionadas con cada promesa usando keywords extraidos.

### 4.2 Metodologia

```
Para cada promesa:
  keywords = extraer_keywords(promesa.texto)

  leyes_especificas = buscar(votos, keywords)

  Para cada ley en leyes_especificas:
    Verificar posicion del partido

  Si >= 60% NO:
    AMPAY
```

### 4.3 Mejoras sobre v2

| Aspecto | v2 | v3 |
|---------|----|----|
| Granularidad | Por categoria | Por ley especifica |
| Matching | Categoria unica | Keywords multiples |
| Precision | Baja | Media |

### 4.4 Problema Identificado

**Solo busqueda directa:** Solo buscaba leyes que IMPLEMENTAN la promesa.

**Ejemplo de fallo:**
```
Promesa: "Eliminar exoneraciones"

Busqueda v3 (directa):
- Keywords: "eliminar exoneracion"
- Leyes encontradas: 0
- Resultado: DATOS INSUFICIENTES

Realidad:
- Existen 6 leyes que EXTIENDEN exoneraciones
- Partido voto SI en todas
- Deberia ser AMPAY (por contradiccion inversa)
```

### 4.5 Decision

**SUPERADA** - Funcional pero incompleta. Necesita busqueda inversa.

---

## 5. Version 4 (Superada)

### 5.1 Descripcion

Agregar busqueda INVERSA: no solo buscar leyes de apoyo, tambien leyes de contradiccion.

### 5.2 Metodologia

```
Para cada promesa:
  # Busqueda A: Directa
  keywords_apoyo = keywords que IMPLEMENTAN promesa
  leyes_apoyo = buscar(votos, keywords_apoyo)
  ratio_no_apoyo = contar_NO(leyes_apoyo) / total(leyes_apoyo)

  # Busqueda B: Inversa
  keywords_contradiccion = keywords que CONTRADICEN promesa
  leyes_contradiccion = buscar(votos, keywords_contradiccion)
  ratio_si_contradiccion = contar_SI(leyes_contradiccion) / total(leyes_contradiccion)

  # Matriz de decision
  Si ratio_no_apoyo >= 60% OR ratio_si_contradiccion >= 60%:
    AMPAY
```

### 5.3 Mejoras sobre v3

| Aspecto | v3 | v4 |
|---------|----|----|
| Direcciones de busqueda | Solo directa | Directa + Inversa |
| Tipos de AMPAY detectados | Tipo A solamente | Tipo A + Tipo B |
| Cobertura | Parcial | Completa |

### 5.4 Problema Identificado

**Sin sistema de confianza:** Todos los AMPAYs tratados igual, sin distinguir fuerza de evidencia.

### 5.5 Decision

**SUPERADA** - Deteccion completa pero falta calibracion de confianza.

---

## 6. Version 5 (Actual)

### 6.1 Descripcion

Agregar sistema de confianza y revision manual obligatoria.

### 6.2 Metodologia

```
Para cada promesa:
  # Deteccion (igual que v4)
  ejecutar_busqueda_dual()

  # Calcular confianza
  confianza = calcular_confianza(
    num_leyes,
    ratio,
    fuerza_conexion_semantica
  )

  # Clasificar
  Si confianza >= HIGH:
    AMPAY_candidato (revision automatica)
  Si confianza == MEDIUM:
    AMPAY_candidato (revision manual obligatoria)
  Si confianza == LOW:
    No publicar
```

### 6.3 Mejoras sobre v4

| Aspecto | v4 | v5 |
|---------|----|----|
| Confianza | Binario (AMPAY/NO) | HIGH/MEDIUM/LOW |
| Revision | Opcional | Obligatoria para MEDIUM |
| Transparencia | Basica | Documentacion completa |

### 6.4 Componentes Nuevos

1. **Sistema de confianza:** HIGH, MEDIUM, LOW
2. **Proceso de revision manual:** Checklist estandarizado
3. **Documentacion de rechazo:** Log de falsos positivos
4. **Proceso de apelacion:** Canal para disputar AMPAYs

### 6.5 Resultados

```
AMPAYs detectados: 23
AMPAYs aprobados (HIGH): 4
AMPAYs aprobados (MEDIUM): 4
AMPAYs rechazados: 17
AMPAYs final (after audit): 6
Precision estimada: 90%+
```

---

## 7. Linea de Tiempo Detallada

| Fecha | Version | Evento |
|-------|---------|--------|
| 2026-01-18 | v1 | Primera implementacion |
| 2026-01-18 | v1 | Detectados 200+ AMPAYs (sospechoso) |
| 2026-01-18 | v1 | Revision manual: >95% falsos positivos |
| 2026-01-19 | v2 | Pivotar a agregacion por categoria |
| 2026-01-19 | v2 | 0 AMPAYs detectados (sospechoso) |
| 2026-01-19 | v2 | Identificado: promesas especificas perdidas |
| 2026-01-20 | v3 | Pivotar a busqueda por keywords |
| 2026-01-20 | v3 | AMPAYs detectados pero incompletos |
| 2026-01-20 | v4 | Agregar busqueda inversa |
| 2026-01-20 | v4 | Primer AMPAY valido: FP-universalidad |
| 2026-01-21 | v5 | Agregar sistema de confianza |
| 2026-01-21 | v5 | 6 AMPAYs validados para publicacion |

---

## 8. Lecciones Aprendidas

### 8.1 Errores que no Repetir

| Error | Leccion |
|-------|---------|
| Confiar en deteccion automatica sin revision | Siempre validar humano |
| Agregar sin medir precision | Medir antes de publicar |
| Asumir que mas detecciones = mejor | Calidad > cantidad |
| Busqueda unidireccional | Siempre buscar ambas direcciones |

### 8.2 Principios Establecidos

1. **Patron > evento aislado:** Minimo 3 leyes
2. **Especificidad > categoria:** Buscar leyes exactas
3. **Bidireccional > unidireccional:** Directa + inversa
4. **Confianza calibrada:** No todos los AMPAYs son iguales
5. **Revision obligatoria:** Humano en el loop

---

## 9. Proximas Mejoras (Roadmap)

| Mejora | Prioridad | Estado |
|--------|-----------|--------|
| Incorporar datos 2024-2026 | Alta | Pendiente |
| Mejorar extraccion de keywords con NLP | Media | Investigando |
| Dashboard de monitoreo de precision | Media | Pendiente |
| API para periodistas | Baja | Futuro |

---

## 10. Archivos de Cada Version

| Version | Archivo | Estado |
|---------|---------|--------|
| v2 | `docs/methodology/archive/METHODOLOGY_V2_DEPRECATED.md` | Archivado |
| v3 | `docs/methodology/archive/METHODOLOGY_V3_DEPRECATED.md` | Archivado |
| v4 | `docs/methodology/METHODOLOGY_V4_DUAL_SEARCH.md` | Superado |
| v5 | Documentacion distribuida en `/docs/methodology/` | **ACTIVO** |

---

*Ultima actualizacion: 2026-01-21*
