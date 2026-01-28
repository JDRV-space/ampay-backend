# Limitaciones de los Datos

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Este documento transparenta las limitaciones conocidas de los datos utilizados en AMPAY, incluyendo gaps temporales, sesgos potenciales, y areas de incertidumbre.

---

## 1. Limitaciones Temporales

### 1.1 Periodo de Cobertura

| Dataset | Inicio | Fin | Gap |
|---------|--------|-----|-----|
| Votaciones | 2021-07-26 | 2024-07-26 | 2024-07 a 2026-01 no incluido |
| Promesas 2021 | 2021-04 | 2021-04 | Solo plan registrado |
| Promesas 2026 | 2026-01 | 2026-01 | Solo plan registrado |

### 1.2 Impacto del Gap 2024-2026

| Implicacion | Detalle |
|-------------|---------|
| AMPAYs recientes | Contradicciones de los ultimos 18 meses no detectadas |
| Cambios de posicion | Partidos pueden haber cambiado comportamiento |
| Contexto incompleto | Patrones 2021-2024 pueden no reflejar 2024-2026 |

### 1.3 Mitigacion

- Disclaimer explicito en la aplicacion
- Fecha de corte mostrada claramente
- Actualizacion planeada si datos disponibles

---

## 2. Limitaciones de Votaciones

### 2.1 Datos No Capturados

| Tipo de Votacion | Incluido | Razon |
|------------------|----------|-------|
| Votacion nominal | SI | Registrada en actas |
| Votacion secreta | NO | No hay registro publico |
| Comisiones | NO | Solo pleno incluido |
| Mesa Directiva | PARCIAL | Algunas decisiones sin votacion |

### 2.2 Contexto Perdido

| Elemento | Disponible | No Disponible |
|----------|------------|---------------|
| Resultado del voto | SI | - |
| Fundamentacion de voto | - | NO |
| Negociaciones previas | - | NO |
| Presion politica | - | NO |
| Votos condicionados | - | NO |

### 2.3 Calidad de los Datos

| Metrica | Valor | Fuente |
|---------|-------|--------|
| Completitud | 99%+ | openpolitica |
| Precision | 99.7% | Verificacion muestral |
| Errores conocidos | < 0.3% | Mayormente typos |

---

## 3. Limitaciones de Promesas

### 3.1 Problemas de Extraccion

| Problema | Frecuencia | Mitigacion |
|----------|------------|------------|
| PDFs escaneados baja calidad | 15% | OCR + revision manual |
| Estructura no estandar | 100% | Adaptacion por documento |
| Promesas vagas | 30% | Exclusion si no verificable |
| Lenguaje condicionado | 20% | Codificacion como 0 |

### 3.2 Sesgo de Documentacion

| Partido | Paginas Plan 2021 | Promesas Extraidas | Notas |
|---------|-------------------|-------------------|-------|
| Renovacion Popular | 120+ | 84 | Plan muy detallado |
| Peru Libre | 60 | 21 | Plan mas general |
| Partido Morado | 25 | 6 | Plan corto |

**Implicacion:** Partidos con planes mas detallados tienen mas promesas analizables.

### 3.3 Promesas No Incluidas

| Tipo | Razon de Exclusion |
|------|-------------------|
| Promesas verbales | No documentadas en plan JNE |
| Entrevistas de campana | Fuera de alcance |
| Redes sociales | Verificabilidad cuestionable |
| Promesas post-registro | No en version oficial |

---

## 4. Limitaciones de Categorizacion

### 4.1 Precision de Clasificacion

| Metodo | Precision Estimada | Casos Problematicos |
|--------|-------------------|---------------------|
| Keywords automaticos | 98% | Homonimos |
| IA (Claude/Gemini) | 95% | Temas fronterizos |
| Revision manual | 99%+ | Subjetividad residual |

### 4.2 Categorias Fronterizas

| Ejemplo | Categorias Posibles | Asignacion |
|---------|---------------------|------------|
| "Canon minero para educacion" | mineria, educacion, fiscal | fiscal |
| "Hospitales en zonas mineras" | salud, mineria | salud |
| "Empleo en agricultura" | empleo, agricultura | agricultura |

### 4.3 Evolucion de Categorias

Las 15 categorias actuales pueden no capturar:
- Temas emergentes (ej: IA, criptomonedas)
- Temas transversales (ej: genero, digitalizacion)
- Matices dentro de categorias (ej: mineria formal vs informal)

---

## 5. Limitaciones del Quiz

### 5.1 Simplificacion Inherente

| Aspecto | Realidad | Quiz |
|---------|----------|------|
| Espectro politico | Multidimensional | 2 ejes |
| Posiciones | Matizadas | -1/0/+1 |
| Temas | Miles | 8 preguntas |
| Ponderacion | Variable por votante | Igual para todos |

### 5.2 Sesgos Potenciales

| Sesgo | Descripcion | Mitigacion |
|-------|-------------|------------|
| Seleccion de preguntas | Temas elegidos por equipo | Diversidad de ejes |
| Redaccion | Framing afecta respuestas | Lenguaje neutral |
| Orden | Primeras preguntas anclan | Aleatorizar en futuro |

### 5.3 Validacion Pendiente

| Test | Estado | Prioridad |
|------|--------|-----------|
| Test-retest reliability | No realizado | Media |
| Validez de constructo | No realizado | Alta |
| Comparacion con encuestas | No realizado | Media |

---

## 6. Limitaciones de AMPAYs

### 6.1 Falsos Negativos

Contradicciones que podemos PERDER:

| Tipo | Razon |
|------|-------|
| Sin leyes relacionadas | Promesa sin legislacion en periodo |
| Keywords no detectados | Sinonimos no incluidos |
| Contradiccion sutil | Conexion semantica debil |
| Voto por delegacion | Lider vota, bancada ausente |

### 6.2 Incertidumbre Residual

| AMPAY | Confianza | Fuente de Incertidumbre |
|-------|-----------|------------------------|
| AMPAY-001 | HIGH | Contexto de negociacion desconocido |
| AMPAY-005 | MEDIUM | Distincion "corporativo" vs "popular" |
| AMPAY-006 | MEDIUM | Solo 2 mociones encontradas |

### 6.3 Contexto No Capturado

- Presion de ejecutivo
- Acuerdos de bancada
- Votos "estrategicos"
- Cambios en texto de ley entre versiones

---

## 7. Limitaciones de Agregacion

### 7.1 Congresista vs Partido

| Situacion | Tratamiento | Limitacion |
|-----------|-------------|------------|
| Voto unanime | Posicion = posicion partido | Ninguna |
| Voto dividido | Posicion = mayoria | Pierde matiz |
| Transfuga | Usa partido al momento | Historia perdida |
| Bancada de 1 | Posicion = individuo | No es "partido" |

### 7.2 Pesos Iguales

Todos los votos tienen igual peso, pero:
- Algunos votos son mas relevantes (presupuesto)
- Algunos congresistas tienen mas influencia (lideres)
- Algunos temas son mas importantes para votantes

---

## 8. Recomendaciones de Uso

### 8.1 AMPAY Esta Disenado Para

- Informar votantes sobre patrones generales
- Identificar contradicciones claras
- Promover transparencia politica
- Ser punto de partida para investigacion

### 8.2 AMPAY NO Esta Disenado Para

- Predecir comportamiento futuro con certeza
- Ser unica fuente de decision de voto
- Reemplazar analisis periodistico
- Afirmar intencion o motivacion de politicos

---

## 9. Niveles de Confianza por Seccion

| Seccion | Confianza | Justificacion |
|---------|-----------|---------------|
| Datos de votacion | **ALTA** | Fuente oficial, verificada |
| Categorizacion de votos | **ALTA** | Proceso multiple, QA |
| Posiciones de partidos | **MEDIA** | Basado en promesas, no votos |
| Match del quiz | **MEDIA** | Simplificacion necesaria |
| AMPAYs | **VARIABLE** | Depende de evidencia especifica |

---

## 10. Actualizaciones Futuras

| Mejora | Impacto en Limitaciones |
|--------|------------------------|
| Datos 2024-2026 | Elimina gap temporal |
| Validacion externa | Aumenta confianza |
| Mas preguntas quiz | Reduce simplificacion |
| Categorias granulares | Mejora precision |

---

*Ultima actualizacion: 2026-01-21*
