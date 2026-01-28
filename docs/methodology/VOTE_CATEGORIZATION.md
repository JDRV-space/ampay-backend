# Categorizacion de Votos Parlamentarios

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Cada voto del Congreso se clasifica en una de 15 categorias tematicas (14 categorias generales + justicia). La clasificacion combina analisis de keywords con verificacion por IA (Gemini/Claude).

---

## 1. Sistema de 15 Categorias

### 1.1 Lista de Categorias

| # | Categoria | Nombre Display | Alcance |
|---|-----------|----------------|---------|
| 1 | `seguridad` | Seguridad | Crimen, policia, carceles, narcotrafico, terrorismo |
| 2 | `economia` | Economia | Impuestos, comercio, inversion, MYPE, TLC |
| 3 | `fiscal` | Fiscal | Deficit, presupuesto, deuda publica, gasto corriente |
| 4 | `social` | Social | Pobreza, bonos, programas sociales, pensiones |
| 5 | `empleo` | Empleo | Trabajo, laboral, informalidad, salario minimo |
| 6 | `educacion` | Educacion | Escuelas, universidades, becas, docentes |
| 7 | `salud` | Salud | Hospitales, medicamentos, anemia, SIS, ESSALUD |
| 8 | `agricultura` | Agricultura | Agroindustria, riego, campesinos, precios agricolas |
| 9 | `agua` | Agua/Saneamiento | Agua potable, desague, alcantarillado |
| 10 | `vivienda` | Vivienda | Deficit habitacional, urbanismo, construccion |
| 11 | `transporte` | Transporte | Puertos, aeropuertos, carreteras, ferrocarriles |
| 12 | `energia` | Energia | Electricidad, gas, petroleo, renovables |
| 13 | `mineria` | Mineria | Mineria formal/informal, canon, regalias |
| 14 | `ambiente` | Ambiente | Deforestacion, residuos, contaminacion, areas protegidas |

**Nota:** La categoria 15 es "justicia/anticorrupcion", usada para AMPAYs y clasificacion de votos relacionados con el sistema judicial y anticorrupcion. No se incluye en analisis de patrones de votacion (sparklines).

### 1.2 Categoria Excluida

| Categoria | Razon de Exclusion |
|-----------|-------------------|
| `digitalizacion` | Es un COMO, no un QUE. Cruza todas las categorias |
| `otros` | No se permite. Forzar clasificacion en categoria existente |

---

## 2. Proceso de Categorizacion

### 2.1 Diagrama de Flujo

```
┌─────────────────────────────────────────┐
│         ASUNTO DEL VOTO                 │
│  "PL 3456 que modifica Ley del SIS"     │
└────────────────────┬────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  MATCHING DE KEYWORDS │
         │  (Primera pasada)     │
         └───────────┬───────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   Match unico   Match multiple  Sin match
        │            │            │
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ ASIGNAR │  │ IA para │  │ IA para │
   │ directo │  │ decidir │  │ clasificar │
   └─────────┘  └─────────┘  └─────────┘
                     │            │
                     └────┬───────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  VERIFICACION HUMANA  │
              │  (muestra aleatoria)  │
              └───────────────────────┘
```

### 2.2 Reglas de Keywords

**Prioridad de matching:**

1. **Terminos tecnicos especificos** (alta precision)
2. **Nombres de instituciones** (media precision)
3. **Terminos generales** (baja precision, requiere contexto)

### 2.3 Diccionario de Keywords por Categoria

```
SEGURIDAD:
├── Alta confianza: PNP, policia, narcotrafico, terrorismo, penal, crimen
├── Media confianza: detencion, seguridad ciudadana, requisitoria
└── Requiere contexto: ley, delito, sancion

ECONOMIA:
├── Alta confianza: MYPE, SUNAT, TLC, exportacion, importacion, aranceles
├── Media confianza: competitividad, inversion, mercado
└── Requiere contexto: empresa, comercio, fiscal

FISCAL:
├── Alta confianza: presupuesto, MEF, deficit, credito suplementario
├── Media confianza: endeudamiento, gasto publico, tesoro
└── Requiere contexto: recursos, financiamiento

SOCIAL:
├── Alta confianza: pension, ONP, AFP, bono, Qali Warma, Cuna Mas
├── Media confianza: programa social, subsidio, pobreza
└── Requiere contexto: beneficio, apoyo

EMPLEO:
├── Alta confianza: laboral, SUNAFIL, salario minimo, CTS, gratificacion
├── Media confianza: trabajador, contrato, despido, sindicato
└── Requiere contexto: empleo, trabajo

EDUCACION:
├── Alta confianza: MINEDU, universidad, docente, beca, SUNEDU
├── Media confianza: educacion, escuela, colegio, estudiante
└── Requiere contexto: formacion, capacitacion

SALUD:
├── Alta confianza: MINSA, ESSALUD, SIS, hospital, farmacia, vacuna
├── Media confianza: salud, medico, enfermedad, tratamiento
└── Requiere contexto: atencion, servicio

AGUA:
├── Alta confianza: SEDAPAL, saneamiento, alcantarillado, desague
├── Media confianza: agua potable, acueducto, tratamiento aguas
└── Requiere contexto: agua, hidrico

VIVIENDA:
├── Alta confianza: vivienda, urbanismo, COFOPRI, Techo Propio
├── Media confianza: construccion, habilitacion urbana
└── Requiere contexto: inmobiliario

TRANSPORTE:
├── Alta confianza: MTC, carretera, aeropuerto, puerto, ferrocarril
├── Media confianza: transporte, infraestructura vial, peaje
└── Requiere contexto: movilidad

ENERGIA:
├── Alta confianza: OSINERGMIN, electricidad, gas, petroleo, hidrocarburo
├── Media confianza: energia renovable, solar, eolica
└── Requiere contexto: energia

MINERIA:
├── Alta confianza: MINEM, mineria, canon minero, regalias mineras
├── Media confianza: concesion minera, exploracion, explotacion
└── Requiere contexto: extraccion, recursos

AMBIENTE:
├── Alta confianza: MINAM, SERNANP, area protegida, deforestacion
├── Media confianza: ambiental, contaminacion, residuos, reciclaje
└── Requiere contexto: conservacion, ecosistema
```

---

## 3. Clasificacion por IA

### 3.1 Prompt de Clasificacion

```
Clasifica el siguiente asunto de votacion del Congreso peruano en UNA de estas categorias:
seguridad, economia, fiscal, social, empleo, educacion, salud, agua, vivienda, transporte, energia, mineria, ambiente

ASUNTO: "[texto del asunto]"

Reglas:
1. Elegir la categoria PRINCIPAL, no secundaria
2. Si hay duda, elegir la categoria mas especifica
3. NUNCA usar "otros" o inventar categorias
4. Responder SOLO con el nombre de la categoria en minusculas

Categoria:
```

### 3.2 Modelo Utilizado

| Modelo | Uso | Costo |
|--------|-----|-------|
| Claude Opus | Clasificacion final, AMPAYs | Alto |
| Gemini Flash | Pre-clasificacion masiva | Bajo |

### 3.3 Umbrales de Confianza

```
Confianza >= 0.95  → Aceptar directamente
Confianza 0.80-0.94 → Revisar si hay keyword conflictivo
Confianza < 0.80   → Revision humana obligatoria
```

---

## 4. Casos Especiales

### 4.1 Votos Multi-Categoria

Algunos votos tocan multiples temas. Regla: **elegir categoria principal**.

**Ejemplo:**
```
Asunto: "Ley que promueve la mineria formal para reducir la pobreza"
Categorias posibles: mineria, social
Clasificacion: mineria (es el objeto de la ley, pobreza es el objetivo)
```

### 4.2 Presupuestos Sectoriales

Leyes de presupuesto se clasifican por SECTOR, no como "fiscal".

**Ejemplo:**
```
Asunto: "Presupuesto del sector salud 2024"
Clasificacion: salud (no fiscal)

Asunto: "Ley de equilibrio financiero del sector publico"
Clasificacion: fiscal (es transversal)
```

### 4.3 Reformas Institucionales

Reformas de entidades se clasifican por FUNCION de la entidad.

**Ejemplo:**
```
Asunto: "Ley que reestructura SEDAPAL"
Clasificacion: agua

Asunto: "Ley que reorganiza la PNP"
Clasificacion: seguridad
```

---

## 5. Estadisticas de Categorizacion

### 5.1 Distribucion por Categoria (2,226 votos)

| Categoria | Votos | % del Total |
|-----------|-------|-------------|
| economia | 412 | 18.5% |
| seguridad | 298 | 13.4% |
| salud | 258 | 11.6% |
| educacion | 245 | 11.0% |
| social | 198 | 8.9% |
| empleo | 187 | 8.4% |
| agricultura | 156 | 7.0% |
| fiscal | 143 | 6.4% |
| transporte | 121 | 5.4% |
| ambiente | 89 | 4.0% |
| agua | 67 | 3.0% |
| vivienda | 31 | 1.4% |
| mineria | 21 | 0.9% |

### 5.2 Precision de Clasificacion

Basado en revision manual de muestra (n=200):

| Metodo | Precision |
|--------|-----------|
| Keywords unicos | 98.2% |
| Keywords + IA | 95.7% |
| Solo IA | 91.3% |
| Promedio ponderado | **94.8%** |

---

## 6. Validacion

### 6.1 Proceso de QA

1. **Muestra aleatoria:** 5% de votos revisados manualmente
2. **Casos frontera:** Todos los casos con confianza < 0.85 revisados
3. **Consistencia:** Votos similares deben tener misma categoria

### 6.2 Metricas de Calidad

| Metrica | Umbral Aceptable | Actual |
|---------|------------------|--------|
| Precision | >= 90% | 94.8% |
| Casos sin clasificar | 0% | 0% |
| Tiempo promedio/voto | < 2s | 0.8s |

---

## 7. Limitaciones

1. **Ambiguedad inherente:** Algunos votos genuinamente cruzan categorias
2. **Evolucion del lenguaje:** Terminos nuevos pueden no estar en diccionario
3. **Contexto perdido:** Solo se analiza el "asunto", no el texto completo de la ley
4. **Sesgos del modelo:** IA puede tener sesgos en clasificacion

---

## 8. Archivos Relacionados

| Archivo | Contenido |
|---------|-----------|
| `data/02_output/votes_categorized.json` | Votos con categoria asignada |
| `docs/CATEGORIES.md` | Definiciones de categorias |

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Ultima actualizacion: 2026-01-21*
