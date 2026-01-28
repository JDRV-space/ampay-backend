# Definiciones de Categorias

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Este documento define las 15 categorias tematicas utilizadas para clasificar promesas de campana y votos parlamentarios en AMPAY (14 categorias generales + justicia).

---

## 1. Lista de Categorias

| # | Slug | Nombre Display | Icono Sugerido |
|---|------|----------------|----------------|
| 1 | `seguridad` | Seguridad | shield |
| 2 | `economia` | Economia | trending-up |
| 3 | `fiscal` | Fiscal | calculator |
| 4 | `social` | Social | users |
| 5 | `empleo` | Empleo | briefcase |
| 6 | `educacion` | Educacion | graduation-cap |
| 7 | `salud` | Salud | heart-pulse |
| 8 | `agricultura` | Agricultura | plant |
| 9 | `agua` | Agua/Saneamiento | droplet |
| 10 | `vivienda` | Vivienda | house |
| 11 | `transporte` | Transporte | truck |
| 12 | `energia` | Energia | lightning |
| 13 | `mineria` | Mineria | mountain |
| 14 | `ambiente` | Ambiente | tree |

---

## 2. Definiciones Detalladas

### 2.1 Seguridad

**Slug:** `seguridad`

**Alcance:**
- Seguridad ciudadana
- Policia Nacional del Peru (PNP)
- Sistema penitenciario / carceles
- Narcotrafico y crimen organizado
- Terrorismo y remanentes SL/MRTA
- Violencia domestica y genero
- Emergencias y desastres

**Keywords tipicos:**
```
PNP, policia, seguridad ciudadana, narcotrafico, crimen,
penal, carcel, terrorismo, VRAEM, delincuencia, robo,
extorsion, secuestro, homicidio, emergencia
```

**NO incluye:**
- Seguridad alimentaria (→ social)
- Seguridad laboral (→ empleo)
- Ciberseguridad pura (→ economia/otros)

---

### 2.2 Economia

**Slug:** `economia`

**Alcance:**
- Politica comercial y TLCs
- MYPES y emprendimiento
- Inversion privada nacional y extranjera
- Competitividad y productividad
- Mercados y regulacion economica
- Comercio exterior
- Turismo
- Industria manufacturera

**Keywords tipicos:**
```
MYPE, SUNAT, TLC, exportacion, importacion, aranceles,
inversion, competitividad, mercado, industria, turismo,
emprendimiento, empresa, comercio, produccion
```

**NO incluye:**
- Impuestos especificos (→ fiscal)
- Mineria (→ mineria)
- Agricultura (→ agricultura)

---

### 2.3 Fiscal

**Slug:** `fiscal`

**Alcance:**
- Presupuesto publico
- Impuestos y tributos
- Deuda publica
- Gasto corriente
- Deficit fiscal
- Transferencias a gobiernos regionales/locales
- Exoneraciones tributarias
- Canon y regalias (distribucion)

**Keywords tipicos:**
```
presupuesto, MEF, deficit, credito suplementario,
impuesto, IGV, IR, exoneracion, tributario, fiscal,
gasto, deuda, endeudamiento, tesoro, canon, regalias
```

**NO incluye:**
- Presupuestos sectoriales especificos (→ categoria del sector)
- Mineria como actividad (→ mineria)

---

### 2.4 Social

**Slug:** `social`

**Alcance:**
- Programas sociales (Juntos, Pension 65, Qali Warma, Cuna Mas)
- Lucha contra la pobreza
- Bonos y transferencias directas
- Sistema de pensiones (ONP, AFP)
- Proteccion social
- Discapacidad
- Adulto mayor
- Primera infancia

**Keywords tipicos:**
```
pension, ONP, AFP, bono, Qali Warma, Cuna Mas, Juntos,
Pension 65, pobreza, programa social, subsidio, MIDIS,
discapacidad, adulto mayor, vulnerable
```

**NO incluye:**
- Empleo formal (→ empleo)
- Salud especifica (→ salud)
- Educacion formal (→ educacion)

---

### 2.5 Empleo

**Slug:** `empleo`

**Alcance:**
- Derechos laborales
- Salario minimo
- Formalizacion laboral
- Sindicatos y negociacion colectiva
- Seguridad y salud en el trabajo
- Tercerizacion
- CTS, gratificaciones, vacaciones
- Desempleo

**Keywords tipicos:**
```
laboral, SUNAFIL, salario minimo, CTS, gratificacion,
trabajador, empleo, contrato, despido, sindicato,
tercerizacion, informalidad, trabajo, vacaciones
```

**NO incluye:**
- Empleo publico/funcionarios (→ justicia/otros)
- Empleo agricola especifico (→ agricultura)

---

### 2.6 Educacion

**Slug:** `educacion`

**Alcance:**
- Educacion basica (inicial, primaria, secundaria)
- Educacion superior universitaria y tecnica
- Calidad educativa
- Docentes y magisterio
- Becas (Beca 18, etc.)
- Infraestructura educativa
- Curriculo y contenidos
- SUNEDU y acreditacion

**Keywords tipicos:**
```
MINEDU, educacion, universidad, docente, beca, SUNEDU,
escuela, colegio, estudiante, magisterio, curriculo,
inicial, primaria, secundaria, superior, tecnico
```

**NO incluye:**
- Capacitacion laboral puntual (→ empleo)
- Investigacion cientifica pura (→ economia/otros)

---

### 2.7 Salud

**Slug:** `salud`

**Alcance:**
- Sistema de salud publico (MINSA)
- ESSALUD
- SIS (Seguro Integral de Salud)
- Hospitales y centros de salud
- Medicamentos y farmacias
- Enfermedades especificas (anemia, TBC, VIH)
- Salud mental
- Vacunacion

**Keywords tipicos:**
```
MINSA, ESSALUD, SIS, hospital, medico, salud, vacuna,
medicamento, farmacia, anemia, TBC, enfermedad,
tratamiento, atencion, emergencia medica
```

**NO incluye:**
- Seguridad alimentaria/nutricion general (→ social)
- Agua potable (→ agua)

---

### 2.8 Agua/Saneamiento

**Slug:** `agua`

**Alcance:**
- Agua potable y acceso
- Saneamiento y alcantarillado
- SEDAPAL y empresas de agua
- Tratamiento de aguas residuales
- Infraestructura hidrica urbana

**Keywords tipicos:**
```
SEDAPAL, saneamiento, alcantarillado, desague, agua potable,
acueducto, tratamiento aguas, hidrico, abastecimiento
```

**NO incluye:**
- Riego agricola (→ agricultura)
- Represas para energia (→ energia)
- Inundaciones (→ seguridad/ambiente)

---

### 2.9 Vivienda

**Slug:** `vivienda`

**Alcance:**
- Deficit habitacional
- Programas de vivienda (Techo Propio, Mi Vivienda)
- Urbanismo y planificacion
- Titulacion y formalizacion de predios
- COFOPRI
- Construccion de viviendas sociales

**Keywords tipicos:**
```
vivienda, COFOPRI, Techo Propio, Mi Vivienda, urbanismo,
construccion, habilitacion urbana, predio, titulo,
habitacional, inmobiliario
```

**NO incluye:**
- Infraestructura de transporte (→ transporte)
- Espacios publicos (→ ambiente/otros)

---

### 2.10 Transporte

**Slug:** `transporte`

**Alcance:**
- Carreteras y vias
- Puertos y aeropuertos
- Ferrocarriles
- Transporte publico urbano
- MTC y regulacion
- Peajes y concesiones viales
- Aviacion civil

**Keywords tipicos:**
```
MTC, carretera, aeropuerto, puerto, ferrocarril, transporte,
via, peaje, concesion vial, metro, corredor, aviacion,
infraestructura vial
```

**NO incluye:**
- Vehiculos electricos (→ energia/ambiente)
- Logistica privada (→ economia)

---

### 2.11 Energia

**Slug:** `energia`

**Alcance:**
- Electricidad y distribucion
- Gas natural (Camisea, etc.)
- Petroleo e hidrocarburos
- Energias renovables (solar, eolica, hidroelectrica)
- PetroPeru
- OSINERGMIN
- Tarifas energeticas

**Keywords tipicos:**
```
OSINERGMIN, electricidad, gas, petroleo, hidrocarburo,
energia renovable, solar, eolica, PetroPeru, Camisea,
tarifa electrica, generacion, distribucion
```

**NO incluye:**
- Mineria de carbon (→ mineria)
- Biocombustibles agricolas (→ agricultura)

---

### 2.12 Mineria

**Slug:** `mineria`

**Alcance:**
- Mineria formal (gran, mediana, pequena)
- Mineria informal y artesanal
- Canon y regalias mineras (origen)
- Conflictos mineros
- MINEM
- Concesiones mineras
- Exploracion y explotacion

**Keywords tipicos:**
```
MINEM, mineria, canon minero, regalias mineras, concesion minera,
exploracion, explotacion, mineral, cobre, oro, plata, zinc,
formalizacion minera, minero artesanal
```

**NO incluye:**
- Impacto ambiental de mineria (→ ambiente si es tema principal)
- Distribucion del canon (→ fiscal)

---

### 2.13 Ambiente

**Slug:** `ambiente`

**Alcance:**
- Proteccion ambiental
- Areas naturales protegidas
- Deforestacion y reforestacion
- Contaminacion y remediacion
- Residuos solidos y reciclaje
- Cambio climatico
- MINAM y SERNANP
- Consulta previa
- Biodiversidad

**Keywords tipicos:**
```
MINAM, SERNANP, area protegida, deforestacion, contaminacion,
ambiental, residuos, reciclaje, cambio climatico, biodiversidad,
conservacion, ecosistema, EIA, impacto ambiental
```

**NO incluye:**
- Mineria ilegal como crimen (→ seguridad)
- Agricultura sostenible (→ agricultura)

---

## 3. Categoria Especial: Justicia/Anticorrupcion

**Slug:** `justicia`

**Uso:** Solo para AMPAYs relacionados con sistema de justicia y anticorrupcion. NO se usa para categorizacion general de votos.

**Alcance:**
- Sistema judicial
- Poder Judicial y Ministerio Publico
- Anticorrupcion
- Transparencia
- Reforma constitucional
- Sistema electoral

---

## 4. Categorias Excluidas

| Categoria | Razon de Exclusion |
|-----------|-------------------|
| `digitalizacion` | Es transversal, cruza todas las categorias |
| `genero` | Es transversal, se refleja en varias categorias |
| `descentralizacion` | Se refleja en fiscal y otras |
| `otros` | No permitido, forzar clasificacion |

---

## 5. Reglas de Asignacion

### 5.1 Principio General

**Una categoria por item.** Si un tema cruza categorias, elegir la MAS ESPECIFICA.

### 5.2 Jerarquia de Decision

1. ¿Hay categoria con match exacto? → Usar esa
2. ¿Hay multiples matches? → Elegir la del OBJETO principal
3. ¿No hay match claro? → Revisar keywords expandidos
4. ¿Sigue ambiguo? → IA + revision humana

### 5.3 Ejemplos de Resolucion

| Tema | Categorias Posibles | Asignacion | Razon |
|------|---------------------|------------|-------|
| "Presupuesto de salud 2024" | fiscal, salud | **salud** | Presupuesto sectorial |
| "Canon minero para educacion" | mineria, educacion, fiscal | **fiscal** | Es transferencia fiscal |
| "Empleo en sector agricola" | empleo, agricultura | **agricultura** | Sector especifico |
| "Violencia contra la mujer" | seguridad, social | **seguridad** | Es tema de seguridad |

---

## 6. Mapeo a Estandares Externos

### 6.1 Manifesto Project (MARPOR)

| AMPAY | MARPOR Codes |
|-------|--------------|
| seguridad | 605 (Law and Order) |
| economia | 401-412 (Free Market, Incentives) |
| fiscal | 414 (Economic Orthodoxy) |
| social | 503-506 (Social Welfare) |
| empleo | 701-706 (Labour Groups) |
| educacion | 506 (Education) |
| salud | 504 (Health Care) |
| ambiente | 501 (Environmental Protection) |

---

## 7. Estadisticas de Uso

### 7.1 Distribucion en Votos (2,226 votos sustantivos)

| Categoria | Votos | % |
|-----------|-------|---|
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

---

*Ultima actualizacion: 2026-01-21*
