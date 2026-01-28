# Validacion Cruzada de AMPAYs

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Cada AMPAY detectado automaticamente pasa por un proceso de validacion cruzada antes de publicarse. Este documento describe el proceso de verificacion, criterios de aceptacion, y ejemplos de falsos positivos rechazados.

---

## 1. Proceso de Validacion

### 1.1 Pipeline de Validacion

```
┌─────────────────────────────────────────┐
│      AMPAY DETECTADO AUTOMATICAMENTE    │
└────────────────────┬────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  VERIFICACION FUENTES │
         │  (promesa + votos)    │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  ANALISIS SEMANTICO   │
         │  (conexion logica)    │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  BUSQUEDA DE CONTEXTO │
         │  (explicaciones)      │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  DECISION FINAL       │
         │  (aprobar/rechazar)   │
         └───────────────────────┘
```

### 1.2 Criterios de Validacion

| Criterio | Pregunta | Peso |
|----------|----------|------|
| **Fuente verificable** | ¿Existe la promesa en el PDF de JNE? | Obligatorio |
| **Voto verificable** | ¿El dato de votacion es correcto? | Obligatorio |
| **Conexion semantica** | ¿La ley se relaciona con la promesa? | Alto |
| **Patron consistente** | ¿Hay multiples votos, no solo uno? | Medio |
| **Sin contexto exculpatorio** | ¿No hay explicacion razonable? | Medio |

---

## 2. Verificacion de Fuentes

### 2.1 Verificar Promesa

**Pasos:**
1. Obtener PDF original del JNE
2. Localizar pagina citada
3. Confirmar texto exacto
4. Verificar que es promesa (no contexto)

**Checklist:**
- [ ] PDF accesible en URL citada
- [ ] Pagina correcta
- [ ] Texto coincide
- [ ] Es compromiso, no descripcion

### 2.2 Verificar Votos

**Pasos:**
1. Consultar dataset openpolitica
2. Buscar por fecha + asunto
3. Confirmar posicion del partido
4. Verificar que es voto sustantivo

**Checklist:**
- [ ] Votacion existe en dataset
- [ ] Fecha correcta
- [ ] Asunto coincide
- [ ] Posicion del partido correcta
- [ ] No es voto procedural

---

## 3. Analisis Semantico

### 3.1 Conexion Promesa-Ley

**Pregunta clave:** ¿Votar SI/NO en esta ley afecta directamente el cumplimiento de la promesa?

**Matriz de Conexion:**

| Promesa | Ley | Voto | Conexion | Veredicto |
|---------|-----|------|----------|-----------|
| "Eliminar exoneraciones" | Ley que elimina exoneracion X | NO | DIRECTA | AMPAY |
| "Eliminar exoneraciones" | Ley que prorroga exoneracion X | SI | DIRECTA (inversa) | AMPAY |
| "Eliminar exoneraciones" | Ley de presupuesto general | NO | INDIRECTA | No AMPAY |

### 3.2 Errores Semanticos Comunes

| Error | Ejemplo | Por que es Error |
|-------|---------|------------------|
| **Falso homonimo** | Promesa "seguridad ciudadana" vs Ley "seguridad alimentaria" | Diferentes conceptos |
| **Categoria sin especificidad** | Promesa "mejorar salud" vs Cualquier ley de salud | Promesa muy vaga |
| **Oposicion tactica** | Votar NO por enmienda especifica, no por concepto | Contexto perdido |

---

## 4. Busqueda de Contexto

### 4.1 Fuentes de Contexto

| Fuente | Que Buscar | Donde |
|--------|------------|-------|
| Prensa | Declaraciones del partido sobre el voto | Google News |
| Actas | Fundamentacion de voto en sesion | Congreso.gob.pe |
| Comunicados | Posicion oficial del partido | Redes sociales |

### 4.2 Contexto Exculpatorio Valido

| Contexto | Ejemplo | Resultado |
|----------|---------|-----------|
| **Oposicion por forma, no fondo** | "Votamos NO porque la ley tenia errores tecnicos" | Evaluar caso |
| **Cambio de circunstancias** | Promesa 2021, realidad 2023 muy diferente | Evaluar caso |
| **Ley mixta** | Ley tiene partes alineadas y partes contradictorias | No AMPAY automatico |

### 4.3 Contexto NO Exculpatorio

| Excusa Invalida | Por que es Invalida |
|-----------------|---------------------|
| "Coherencia ideologica" | Si contradice ideologia, no debio prometerse |
| "Conveniencia politica" | Es precisamente lo que AMPAY detecta |
| "No habia recursos" | Promesas deben ser realistas |
| "La oposicion lo propuso" | El origen no invalida el contenido |

---

## 5. Ejemplos de Falsos Positivos Rechazados

### 5.1 Caso: FP-MYPE-NO

```
AMPAY DETECTADO:
- Promesa: "Formalizar un millon de MYPES"
- Ley: "Ley de pago de facturas MYPE"
- Voto FP: NO

INVESTIGACION:
- FP voto NO en esta ley especifica
- PERO voto SI en otras 25 leyes MYPE
- Este NO fue por oposicion a clausula de penalidades

DECISION: RECHAZADO
RAZON: Patron general es de apoyo (25 SI vs 1 NO)
```

### 5.2 Caso: PL-EXONERACION-SI

```
AMPAY DETECTADO:
- Promesa: "Eliminar exoneraciones tributarias"
- Ley: "Prorrogar exoneracion Amazonia"
- Voto PL: SI

INVESTIGACION:
- PL tiene base electoral en Amazonia
- La exoneracion beneficia a pequenos productores
- PL distingue entre exoneraciones "corporativas" y "populares"

DECISION: ACEPTADO con nota
RAZON: Contradiccion real pero con matiz (HIGH → MEDIUM confidence)
```

### 5.3 Caso: RP-EXPORTACION-NO

```
AMPAY DETECTADO:
- Promesa: "Fomentar exportaciones"
- Ley: "Comision investigadora Puerto Chancay"
- Voto RP: NO

INVESTIGACION:
- Conexion semantica: Puerto = exportaciones
- Pero: Comision investigadora ≠ promover exportaciones
- Votar NO en investigar no es votar NO en exportar

DECISION: RECHAZADO
RAZON: Conexion semantica debil. Investigar infraestructura no es lo mismo que oponerse a ella.
```

**Nota:** Este caso fue posteriormente reclasificado como AMPAY valido despues de revision adicional.

---

## 6. Metricas de Validacion

### 6.1 Resultados del Proceso

| Metrica | Valor |
|---------|-------|
| AMPAYs detectados automaticamente | 23 |
| AMPAYs aprobados tras validacion cruzada | 8 |
| AMPAYs rechazados en validacion cruzada | 15 |
| AMPAYs eliminados en auditoria manual | 2 |
| **AMPAYs finales confirmados** | **6** |
| Tasa de falsos positivos (validacion) | 65.2% |

> **Nota de auditoria:** De los 8 AMPAYs aprobados en validacion cruzada, 2 fueron posteriormente eliminados durante la auditoria manual final (AMPAY-006 y AMPAY-007 de Alianza para el Progreso, y AMPAY-008 de Juntos por el Peru) por interpretacion incorrecta de votos. El total final confirmado es 6 AMPAYs.

### 6.2 Razones de Rechazo

| Razon | Cantidad | % |
|-------|----------|---|
| Conexion semantica debil | 7 | 46.7% |
| Patron no consistente (1 solo voto) | 4 | 26.7% |
| Contexto exculpatorio valido | 2 | 13.3% |
| Error en datos fuente | 2 | 13.3% |

---

## 7. Documentacion de Revision

### 7.1 Formato de Registro

```json
{
  "ampay_candidate_id": "AC-001",
  "detection_date": "2026-01-20",
  "reviewer": "JD",
  "review_date": "2026-01-21",
  "decision": "APPROVED",
  "confidence_adjustment": "HIGH → HIGH",
  "notes": "Verificado en PDF pagina 47. Patron claro con 6 leyes.",
  "sources_checked": [
    "https://plataformahistorico.jne.gob.pe/...",
    "https://github.com/openpolitica/..."
  ]
}
```

### 7.2 Archivo de Auditoria

```
data/02_output/ampays.json
```

---

## 8. Proceso de Apelacion

### 8.1 Como Apelar un AMPAY

Si un partido o ciudadano cree que un AMPAY publicado es incorrecto:

1. Abrir issue en GitHub: `github.com/ampay/issues`
2. Proveer evidencia de contexto exculpatorio
3. Equipo AMPAY revisa en 7 dias
4. Decision documentada publicamente

### 8.2 Criterios de Apelacion Exitosa

| Evidencia | Resultado |
|-----------|-----------|
| Error factual demostrado | Correccion inmediata |
| Contexto exculpatorio nuevo | Re-evaluacion |
| Interpretacion alternativa razonable | Agregar nota, mantener AMPAY |
| Opinion sin evidencia | Rechazar apelacion |

---

## 9. Limitaciones

1. **Sesgo de revisor:** Validacion manual puede tener sesgos
2. **Informacion asimetrica:** Partidos tienen mas contexto que revisores
3. **Tiempo limitado:** No se puede investigar exhaustivamente cada caso
4. **Fuentes incompletas:** Algunas declaraciones no estan documentadas

---

## 10. Archivos Relacionados

| Archivo | Contenido |
|---------|-----------|
| `data/02_output/ampays.json` | AMPAYs aprobados |
| `data/02_output/ampays.json` | AMPAYs aprobados (includes audit log) |

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Ultima actualizacion: 2026-01-21*
