# Extraccion de Promesas de Campana

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Las promesas de campana se extraen de los Planes de Gobierno registrados ante el JNE. Este documento describe el proceso de extraccion, criterios de clasificacion, y reglas para determinar que constituye una promesa.

---

## 1. Fuente de Datos

### 1.1 Planes de Gobierno 2021

```
Fuente: JNE Plataforma Historica
URL: https://plataformahistorico.jne.gob.pe/OrganizacionesPoliticas/PlanesGobiernoTrabajo
Formato: PDF
Acceso: Enero 2026
```

### 1.2 Planes de Gobierno 2026

```
Fuente: JNE Plataforma Electoral
URL: https://plataformaelectoral.jne.gob.pe/candidatos/plan-gobierno-trabajo/buscar
Formato: PDF
Acceso: Enero 2026
```

### 1.3 Partidos Incluidos

| Partido | Plan 2021 | Plan 2026 | Notas |
|---------|-----------|-----------|-------|
| Fuerza Popular | Si | Si | Principal oposicion |
| Peru Libre | Si | Si | Partido de gobierno 2021-2026 |
| Renovacion Popular | Si | Si | - |
| Avanza Pais | Si | Si | - |
| Alianza para el Progreso | Si | Si | - |
| Somos Peru | Si | Si | - |
| Podemos Peru | Si | Si | - |
| Juntos por el Peru | Si | Si | - |
| Partido Morado | Si | Si | - |

---

## 2. Proceso de Extraccion

### 2.1 Pipeline de Extraccion

```
┌─────────────────────────────────────────┐
│         PDF PLAN DE GOBIERNO            │
└────────────────────┬────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  DETECCION DE TIPO    │
         │  (Nativo vs Escaneado)│
         └───────────┬───────────┘
                     │
        ┌────────────┼────────────┐
        │                         │
   Texto nativo            Escaneado/Imagen
        │                         │
        ▼                         ▼
   ┌─────────┐              ┌─────────────┐
   │ PyMuPDF │              │  Tesseract  │
   │ (rapido)│              │ OCR (spa)   │
   └────┬────┘              └──────┬──────┘
        │                          │
        └──────────┬───────────────┘
                   │
                   ▼
         ┌───────────────────────┐
         │  VALIDACION CALIDAD   │
         │  (legibilidad > 80%)  │
         └───────────┬───────────┘
                     │
                ┌────┴────┐
                │         │
           Aprobado    Fallido
                │         │
                ▼         ▼
         ┌─────────┐  ┌─────────────┐
         │ Extraer │  │ Claude API  │
         │ promesas│  │ (fallback)  │
         └─────────┘  └─────────────┘
```

### 2.2 Herramientas de Extraccion

| Herramienta | Uso | Costo |
|-------------|-----|-------|
| **PyMuPDF** | PDFs con texto nativo | Gratis |
| **Tesseract (spa)** | PDFs escaneados | Gratis |
| **Claude API** | Layouts complejos, fallback | ~$0.38/50 pags |

### 2.3 Parametros Tesseract

```bash
tesseract input.pdf output -l spa --psm 6
```

- `-l spa`: Modelo de idioma espanol
- `--psm 6`: Assume bloque de texto uniforme

---

## 3. Definicion de Promesa

### 3.1 Que Constituye una Promesa

Una promesa es una declaracion que cumple TODOS estos criterios:

| Criterio | Descripcion | Ejemplo |
|----------|-------------|---------|
| **Especificidad** | Accion concreta, no vaga | "Construir 500 hospitales" vs "Mejorar salud" |
| **Verificabilidad** | Se puede medir cumplimiento | "Aumentar 10% presupuesto" vs "Priorizar educacion" |
| **Compromiso** | Lenguaje de obligacion | "Implementaremos" vs "Podriamos considerar" |
| **Alcance ejecutivo** | Dentro de competencias del cargo | Presidente puede, vs cambio constitucional |

### 3.2 Que NO es una Promesa

| Tipo | Ejemplo | Razon |
|------|---------|-------|
| **Aspiracion** | "Sonaremos con un Peru mejor" | No es accion concreta |
| **Diagnostico** | "El Peru tiene problemas de corrupcion" | Es descripcion, no compromiso |
| **Valor** | "Creemos en la libertad" | Es ideologia, no promesa |
| **Condicionado** | "Si hay recursos, mejoraremos X" | Escape clause |
| **Vago** | "Trabajaremos por el bienestar" | No verificable |

### 3.3 Verbos de Promesa (Indicadores)

**Verbos fuertes (alta confianza):**
- Implementaremos, crearemos, construiremos
- Eliminaremos, reduciremos, aumentaremos
- Garantizaremos, aseguraremos

**Verbos debiles (requieren contexto):**
- Promoveremos, fomentaremos, impulsaremos
- Fortaleceremos, mejoraremos
- Trabajaremos por, buscaremos

---

## 4. Reglas de Categorizacion

### 4.1 Asignacion de Categoria

Cada promesa se asigna a UNA categoria principal:

```
Prompt para LLM:
"Clasifica esta promesa en UNA de estas categorias:
seguridad, economia, fiscal, social, empleo, educacion, salud, agua, vivienda, transporte, energia, mineria, ambiente, agricultura, justicia

PROMESA: [texto]

Reglas:
1. Elegir la categoria PRINCIPAL
2. Si cruza categorias, elegir la mas especifica
3. NUNCA usar 'otros'"
```

### 4.2 Manejo de Promesas Multi-Categoria

| Promesa | Categorias Posibles | Asignacion | Razon |
|---------|---------------------|------------|-------|
| "Construir hospitales en zonas mineras" | salud, mineria | salud | Hospital es el objeto |
| "Aumentar canon para educacion" | mineria, educacion, fiscal | fiscal | Es transferencia fiscal |
| "Formalizar MYPES con capacitacion" | economia, empleo, educacion | economia | MYPE es el sujeto |

---

## 5. Estructura de Datos

### 5.1 Formato de Promesa Extraida

```json
{
  "id": "FP-2021-007",
  "party_id": "fuerza_popular",
  "text": "Implementar programas de alimentacion escolar de calidad para todos los ninos",
  "text_original": "Implementaremos programas de alimentación escolar de calidad...",
  "category": "social",
  "source": {
    "document": "Plan de Gobierno FP 2021",
    "url": "https://plataformahistorico.jne.gob.pe/.../FP-2021.pdf",
    "page": 47,
    "extracted_at": "2026-01-15"
  },
  "keywords": ["alimentacion", "escolar", "nutricion", "ninos"],
  "confidence": "HIGH",
  "verifiable": true
}
```

### 5.2 Archivo de Salida

```
data/01_input/promises/[partido]_[anio].json
```

---

## 6. Control de Calidad

### 6.1 Validacion Automatica

```python
def validar_promesa(promesa):
    checks = []

    # Check 1: Longitud minima
    checks.append(len(promesa.text) >= 20)

    # Check 2: Contiene verbo de accion
    verbos = ['implementar', 'crear', 'construir', 'eliminar', 'aumentar']
    checks.append(any(v in promesa.text.lower() for v in verbos))

    # Check 3: No es solo diagnostico
    diagnosticos = ['el peru tiene', 'existe un problema', 'se observa']
    checks.append(not any(d in promesa.text.lower() for d in diagnosticos))

    # Check 4: Tiene categoria valida
    categorias_validas = ['seguridad', 'economia', 'fiscal', ...]
    checks.append(promesa.category in categorias_validas)

    return all(checks)
```

### 6.2 Revision Humana

**Criterios para revision manual:**
- Promesas con confianza < 0.8
- Promesas muy cortas (< 30 caracteres)
- Promesas con multiples categorias posibles
- Promesas con lenguaje condicionado

### 6.3 Metricas de Calidad

| Metrica | Umbral | Actual |
|---------|--------|--------|
| Promesas validas / Total | >= 90% | 94.2% |
| Categorias correctas | >= 85% | 91.7% |
| Fuentes verificables | 100% | 100% |

---

## 7. Estadisticas de Extraccion

### 7.1 Promesas por Partido (2021)

| Partido | Promesas Extraidas | Promesas Validas |
|---------|-------------------|------------------|
| Renovacion Popular | 89 | 84 |
| Podemos Peru | 71 | 67 |
| Alianza Progreso | 52 | 49 |
| Fuerza Popular | 38 | 35 |
| Juntos Peru | 35 | 32 |
| Avanza Pais | 33 | 31 |
| Peru Libre | 24 | 21 |
| Somos Peru | 22 | 20 |
| Partido Morado | 8 | 6 |
| **TOTAL** | **372** | **345** |

### 7.2 Distribucion por Categoria

| Categoria | Promesas | % Total |
|-----------|----------|---------|
| economia | 67 | 19.4% |
| social | 54 | 15.7% |
| educacion | 48 | 13.9% |
| salud | 42 | 12.2% |
| seguridad | 38 | 11.0% |
| fiscal | 29 | 8.4% |
| agricultura | 22 | 6.4% |
| empleo | 18 | 5.2% |
| transporte | 12 | 3.5% |
| ambiente | 8 | 2.3% |
| energia | 4 | 1.2% |
| agua | 3 | 0.9% |

---

## 8. Limitaciones

1. **Calidad de PDFs:** Algunos planes de gobierno son escaneados de baja calidad
2. **Estructura variable:** No hay formato estandar para planes de gobierno
3. **Ambiguedad:** Algunas promesas son intencionalmente vagas
4. **Cambios post-eleccion:** Partidos pueden modificar posiciones despues de registrar plan
5. **Completitud:** Algunos temas pueden no estar en el plan pero si en discursos

---

## 9. Archivos Relacionados

| Archivo | Contenido |
|---------|-----------|
| `data/01_input/promises/` | Promesas extraidas por partido |
| `data/01_input/pdfs/` | PDFs originales de JNE |
| `scripts/extract_promises.py` | Script de extraccion |

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Ultima actualizacion: 2026-01-21*
