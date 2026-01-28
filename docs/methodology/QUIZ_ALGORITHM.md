# Algoritmo del Quiz: Compatibilidad Votante-Partido

**Version:** 3.3
**Fecha:** 2026-01-22
**Estado:** ACTIVO

---

## Disclaimer

> **Este quiz es una herramienta informativa basada en los planes de gobierno publicados. No constituye una recomendacion de voto. Los resultados muestran similitud entre tus respuestas y las posiciones declaradas de los partidos, no una evaluacion de su desempeño o integridad.**

---

## Resumen Ejecutivo

El quiz de AMPAY utiliza un algoritmo de **puntuacion combinada** basado en distancia Manhattan con ajuste por cobertura. Este enfoque combina la metodologia estandar de VAAs (Voting Advice Applications) con una penalizacion para partidos con pocas posiciones definidas.

**Version 3.3:** 15 preguntas con ratio balanceado 5:4 izquierda-derecha en eje economico, preguntas sociales y trans-ideologicas. Orden intercalado para prevenir sesgo de respuesta. Algoritmo validado con 2 millones de simulaciones.

**Validacion:** 1 millon de tests de creyentes (100% precision en identificacion de partidos) + 1 millon de tests aleatorios (ratio de balance 2.72:1).

---

## 1. Fundamento Teorico

### 1.1 Voting Advice Applications (VAAs)

Las VAAs son herramientas que ayudan a los votantes a identificar que partidos politicos se alinean mejor con sus preferencias. Funcionan mediante:

1. Recopilar posiciones de partidos sobre temas politicos
2. Preguntar al usuario su posicion sobre los mismos temas
3. Calcular la "distancia" entre usuario y partidos
4. Mostrar los partidos mas cercanos

**Referencias academicas:**

- Garzia, D. (2010). "The Methodological Challenges of Voting Advice Applications". *Representation*, 46(1), 89-102. DOI: [10.1080/00344890903510006](https://doi.org/10.1080/00344890903510006)
- Walgrave, S., Nuytemans, M., & Kriesi, H. (2009). "Who is taught by voters?". *Journal of Information Technology & Politics*, 6(3-4), 194-208. DOI: [10.1080/19331680903048992](https://doi.org/10.1080/19331680903048992)

### 1.2 Distancia Manhattan (City-Block Distance)

La distancia Manhattan mide la diferencia absoluta entre dos puntos en un espacio multidimensional. Es el metodo preferido por VAAs como Wahl-O-Mat (Alemania) y Smartvote (Suiza).

**Formula matematica:**

```
D(usuario, partido) = Σ |posicion_usuario_i - posicion_partido_i|
```

Donde:
- `D` = distancia total
- `i` = cada pregunta del quiz
- `posicion` = valor numerico (-1, 0, o +1)

**Por que Manhattan y no Euclidiana:**

| Metrica | Formula | Uso |
|---------|---------|-----|
| Manhattan | Σ\|x-y\| | VAAs tradicionales, interpretacion intuitiva |
| Euclidiana | √Σ(x-y)² | Penaliza mas las diferencias grandes |

La distancia Manhattan trata todas las diferencias por igual, lo cual es mas justo para comparaciones politicas donde no hay consenso sobre que diferencia es "peor".

---

## 2. Implementacion en AMPAY

### 2.1 Escala de Posiciones

**Entrada del usuario:**
```
+1 = De acuerdo
 0 = Neutral / No se
-1 = En desacuerdo
```

**Posiciones de partidos:**
```
+1 = Apoya (promesa explicita a favor)
 0 = Sin posicion clara (silencio o ambiguedad)
-1 = Se opone (promesa explicita en contra)
```

### 2.2 Calculo de Distancia

**Ejemplo con 15 preguntas:**

| Pregunta | Usuario | Fuerza Popular | Peru Libre |
|----------|---------|----------------|------------|
| Q01 (Impuestos mineras) | +1 | -1 | +1 |
| Q02 (Seguridad) | -1 | +1 | 0 |
| Q03 (TLCs) | +1 | -1 | +1 |
| Q04 (Flexibilidad laboral) | -1 | +1 | -1 |
| Q05 (Estado en energia) | +1 | -1 | +1 |
| ... | ... | ... | ... |
| Q15 (Descentralizacion) | +1 | 0 | +1 |

**Distancia:** Suma de |posicion_usuario - posicion_partido| para cada pregunta.

### 2.3 Puntuacion Combinada (Blended Score)

El algoritmo v3.3 utiliza una puntuacion combinada que considera dos factores:

1. **Distancia Manhattan (90%):** Que tan cerca estan las respuestas del usuario de las posiciones del partido
2. **Ajuste por cobertura (10%):** Penalizacion para partidos con pocas posiciones definidas

**Por que el ajuste por cobertura:**

Un partido que tiene posicion 0 (sin posicion clara) en muchas preguntas obtendria una distancia artificialmente baja, ya que estaria "cerca de todos". El ajuste penaliza esta ambiguedad para que los partidos con posiciones claras no se vean perjudicados.

```
Distancia maxima posible = 2 * numero_preguntas = 2 * 15 = 30

Puntuacion combinada = 0.9 * distancia + 0.1 * penalizacion_cobertura

Porcentaje = 100 - (puntuacion / maximo * 100)

Ejemplo:
Partido A: distancia=8, 12 posiciones definidas -> puntuacion baja -> alta afinidad
Partido B: distancia=6, 4 posiciones definidas -> penalizacion alta -> afinidad ajustada
```

**Interpretacion:** Menor puntuacion combinada = mayor compatibilidad real.

### 2.4 Validacion del Algoritmo

El algoritmo fue validado con 2 millones de simulaciones:

| Tipo de Test | Cantidad | Resultado |
|--------------|----------|-----------|
| Tests de creyentes | 1,000,000 | 100% precision (9/9 partidos correctos) |
| Tests aleatorios | 1,000,000 | Ratio de balance 2.72:1 |

**Tests de creyentes:** Usuarios simulados que responden exactamente como un partido. El algoritmo debe identificar ese partido como el mas afin.

**Tests aleatorios:** Respuestas generadas al azar para verificar que ningun partido sea favorecido sistematicamente. El ratio de balance mide la relacion entre el partido mas y menos seleccionado (ideal: 1:1, aceptable: <3:1).

**Mejora sobre versiones anteriores:** El ratio de balance mejoro de 7.6:1 (v3.2 Manhattan puro) a 2.72:1 (v3.3 puntuacion combinada).

---

## 3. Sistema de Calibracion (Filtro Ideologico)

### 3.1 Proposito

Las preguntas de calibracion NO afectan el calculo de distancia. Sirven para:
1. Filtrar partidos que el usuario considera fuera de su espectro
2. Evitar resultados que contradigan la auto-identificacion del usuario
3. Presentar resultados en dos secciones: "dentro de tu perfil" y "otros"

### 3.2 Preguntas de Calibracion

**C1: Eje Economico**
```
"En temas economicos, ordena del mas al menos identificado:"
Opciones: Izquierda, Centro, Derecha
Metodo: Usuario RANKEA 1-2-3
```

**C2: Eje Social**
```
"En temas sociales y culturales, ordena del mas al menos identificado:"
Opciones: Conservador, Moderado, Progresista
Metodo: Usuario RANKEA 1-2-3
```

### 3.3 Mapeo Calibracion-Partidos

| Calibracion | Partidos Mapeados |
|-------------|-------------------|
| Izquierda (economico) | Peru Libre, Juntos por el Peru |
| Centro (economico) | Partido Morado, Somos Peru, Alianza para el Progreso |
| Derecha (economico) | Fuerza Popular, Renovacion Popular, Avanza Pais, Podemos Peru |
| Conservador (social) | Renovacion Popular, Peru Libre |
| Moderado (social) | FP, Podemos, APP, Avanza Pais, Somos Peru |
| Progresista (social) | Partido Morado, Juntos por el Peru |

### 3.4 Logica de Filtrado

```
Rank 1 → Filtro primario (mejores matches)
Rank 2 → Filtro secundario (tambien mostrados)
Rank 3 → EXCLUIDO de "Dentro de tu perfil"
```

**Ejemplo:**
- Usuario rankea: Derecha (1), Centro (2), Izquierda (3)
- Resultado matematico: Peru Libre 80%, Fuerza Popular 65%
- Display: FP aparece en "Dentro de tu perfil", PL aparece en "Tambien podrias considerar"

---

## 4. Seleccion de Preguntas

### 4.1 Criterios de Inclusion

1. **Poder discriminatorio:** La pregunta debe generar variacion entre partidos
2. **Basada en promesas:** Cada posicion de partido debe tener respaldo documental
3. **Relevancia electoral:** El tema debe ser importante para votantes peruanos
4. **Claridad:** Redaccion sin ambiguedad

### 4.2 Criterios de Exclusion

1. **Consenso total:** Si todos los partidos tienen la misma posicion, la pregunta no discrimina
2. **Datos insuficientes:** Si menos de 5 partidos tienen posicion clara
3. **Temas secundarios:** Preguntas sobre temas marginales en el debate peruano

### 4.3 Preguntas Removidas por Consenso

Las siguientes preguntas fueron descartadas porque todos los partidos tenian posicion +1:

- "Proteger la intangibilidad de la Amazonia"
- "Garantizar cobertura universal de agua potable"
- "Eliminar trabas burocraticas para MYPES"

**Referencia:** Ver `quiz_statements.json` campo `removed_consensus_questions`

---

## 5. Presentacion de Resultados

### 5.1 Estructura de Display

```
╔═══════════════════════════════════════════════════════╗
║ DENTRO DE TU PERFIL:                                  ║
║   1. Fuerza Popular         78%                       ║
║   2. Avanza Pais            71%                       ║
║   3. Renovacion Popular     65%                       ║
╠═══════════════════════════════════════════════════════╣
║ TUS RESPUESTAS SE ALINEAN CON:                        ║
║   Peru Libre                82%                       ║
║   (Este partido esta fuera de tu perfil declarado)    ║
╠═══════════════════════════════════════════════════════╣
║ ⚠️ Esto NO es una recomendacion de voto.             ║
║    Compara los planes de gobierno antes de decidir.   ║
╚═══════════════════════════════════════════════════════╝
```

### 5.2 Logica de "Ver Detalle"

Al hacer click en un partido, mostrar:
- Que preguntas acercaron al usuario a ese partido
- Que preguntas alejaron al usuario de ese partido
- Fuente de la posicion del partido (ID de promesa)

---

## 6. Validacion Academica

### 6.1 Comparacion con VAAs Establecidas

| VAA | Algoritmo | Escala | Ponderacion |
|-----|-----------|--------|-------------|
| Wahl-O-Mat | Manhattan | 3 puntos | Opcional (2x) |
| Smartvote | Manhattan/Euclidiana | 5 puntos | Opcional |
| Vote Compass | Likert | 5 puntos | Automatica |
| **AMPAY** | Manhattan | 3 puntos | Sin ponderacion |

### 6.2 Justificacion de Decisiones

**Escala de 3 puntos (vs 5):**
- Simplifica la experiencia del usuario
- Reduce tiempo de completion
- Adecuado para 15 preguntas (quiz medio)

**Sin ponderacion:**
- Todas las preguntas tienen igual peso
- Evita sesgos en la seleccion de "temas importantes"
- Consistente con Wahl-O-Mat basico

**Balance ideologico (v3.3):**
- 5 preguntas economic-left coded
- 4 preguntas economic-right coded
- 3 preguntas social axis
- 3 preguntas cross-ideological
- Orden intercalado: Izq→Der→Izq→Der para prevenir sesgo de aquiescencia

---

## 7. Limitaciones

1. **Simplificacion:** 15 preguntas no capturan la complejidad politica completa
2. **Posiciones trinarias:** -1/0/+1 no permite matices finos
3. **Sesgo de disponibilidad:** Solo partidos con promesas documentadas
4. **Temporal:** Posiciones basadas en planes de gobierno 2021/2026
5. **Auto-reporte:** Depende de honestidad del usuario en calibracion
6. **Contexto:** Las posiciones reflejan promesas, no necesariamente acciones

---

## 8. Archivos Relacionados

| Archivo | Contenido |
|---------|-----------|
| `data/02_output/quiz_statements.json` | Preguntas y posiciones de partidos |
| `docs/research/03_QUIZ_ALGORITHM.md` | Investigacion VAA detallada |
| `docs/research/06_VAA_METHODOLOGY.md` | Comparacion de metodologias VAA |

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Ultima actualizacion: 2026-01-22 (v3.3 - 15 preguntas balanceadas, algoritmo combinado con ajuste por cobertura)*
