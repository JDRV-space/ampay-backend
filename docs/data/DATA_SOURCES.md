# Fuentes de Datos

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Este documento cataloga todas las fuentes de datos utilizadas en AMPAY, incluyendo URLs, fechas de acceso, y formato de los datos.

---

## 1. Datos de Votacion Parlamentaria

### 1.1 Fuente Principal

| Campo | Valor |
|-------|-------|
| **Nombre** | openpolitica/congreso-pleno-asistencia-votacion |
| **URL** | https://github.com/openpolitica/congreso-pleno-asistencia-votacion |
| **Formato** | CSV |
| **Periodo** | 2021-07-26 a 2024-07-26 |
| **Registros** | ~289,000 votos individuales |
| **Votaciones** | 2,226 sesiones (post-filtrado) |
| **Ultima actualizacion** | Julio 2024 |
| **Fecha de descarga** | 2026-01-15 |
| **Licencia** | Open Data |

### 1.2 Campos Disponibles

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `fecha` | date | Fecha de la votacion |
| `asunto` | string | Descripcion del tema votado |
| `congresista` | string | Nombre del congresista |
| `grupo_parlamentario` | string | Partido al momento del voto |
| `votacion` | enum | SI / NO / ABSTENCION / AUSENTE |

### 1.3 Fuente Oficial Complementaria

| Campo | Valor |
|-------|-------|
| **Nombre** | Congreso - Asistencias y Votaciones Pleno |
| **URL** | https://www.congreso.gob.pe/AsistenciasVotacionesPleno/ |
| **Formato** | PDF (no estructurado) |
| **Uso** | Verificacion manual |

---

## 2. Proyectos de Ley (Metadata)

### 2.1 Fuente Principal

| Campo | Valor |
|-------|-------|
| **Nombre** | hiperderecho/proyectos_de_ley |
| **URL** | https://github.com/hiperderecho/proyectos_de_ley |
| **Formato** | SQLite (leyes.db) |
| **Website** | https://github.com/hiperderecho/proyectos_de_ley |
| **Contenido** | Metadata de proyectos de ley |
| **Fecha de descarga** | 2026-01-15 |

### 2.2 Campos Relevantes

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `codigo` | string | Numero de proyecto de ley |
| `titulo` | string | Titulo oficial |
| `fecha_presentacion` | date | Fecha de ingreso |
| `autor` | string | Congresista/s autores |
| `estado` | enum | En comision / Aprobado / Archivado |
| `comision` | string | Comision asignada |

---

## 3. Planes de Gobierno

### 3.1 Elecciones 2021

| Campo | Valor |
|-------|-------|
| **Nombre** | JNE Plataforma Historica |
| **URL** | https://plataformahistorico.jne.gob.pe/OrganizacionesPoliticas/PlanesGobiernoTrabajo |
| **Formato** | PDF |
| **Partidos** | 9 partidos principales |
| **Fecha de descarga** | 2026-01-15 |

**Links directos verificados:**

| Partido | URL Plan 2021 |
|---------|---------------|
| Juntos por el Peru | https://apisije-e.jne.gob.pe/TRAMITE/ESCRITO/1587/ARCHIVO/FIRMADO/5262.PDF |
| Accion Popular | https://declara.jne.gob.pe/ASSETS/PLANGOBIERNO/FILEPLANGOBIERNO/16511.pdf |

### 3.2 Elecciones 2026

| Campo | Valor |
|-------|-------|
| **Nombre** | JNE Plataforma Electoral |
| **URL** | https://plataformaelectoral.jne.gob.pe/candidatos/plan-gobierno-trabajo/buscar |
| **Formato** | PDF |
| **Candidatos** | 36 candidatos presidenciales |
| **Fecha de descarga** | 2026-01-18 |

### 3.3 Reporte Comparativo JNE

| Campo | Valor |
|-------|-------|
| **URL** | https://saednef.jne.gob.pe/Content/PlanesGobierno/documentos/REPORTE%20F%20DE%20PLANES%20DE%20GOBIERNO.pdf |
| **Contenido** | Comparacion oficial de propuestas |

---

## 4. Portales Gubernamentales Oficiales

### 4.1 Congreso de la Republica

| Recurso | URL |
|---------|-----|
| Portal Principal | https://www.congreso.gob.pe/ |
| Votaciones Pleno | https://www.congreso.gob.pe/AsistenciasVotacionesPleno/ |
| Proyectos de Ley | https://www.congreso.gob.pe/proyectosdeley/ |
| Congreso en Cifras | https://www.congreso.gob.pe/GestionInformacionEstadistica/congreso-cifras/ |
| Reglamento | https://www.congreso.gob.pe/reglamento/ |

### 4.2 Jurado Nacional de Elecciones (JNE)

| Recurso | URL |
|---------|-----|
| Portal Principal | https://www.jne.gob.pe/ |
| Plataforma Electoral 2026 | https://plataformaelectoral.jne.gob.pe/ |
| Plataforma Historica | https://plataformahistorico.jne.gob.pe/ |
| Elecciones 2026 Info | https://portal.jne.gob.pe/portal/Pagina/Ver/979/page/Elecciones-Generales-2026 |

### 4.3 ONPE

| Recurso | URL |
|---------|-----|
| Datos Abiertos | https://datosabiertos.gob.pe/users/onpedatos |

### 4.4 Otras Entidades

| Entidad | URL | Contenido |
|---------|-----|-----------|
| El Peruano | https://diariooficial.elperuano.pe/Normas | Normas legales oficiales |
| MEF Transparencia | https://www.mef.gob.pe/es/por-instrumento/decreto-de-urgencia | Decretos de urgencia |

---

## 5. Organizaciones de Transparencia

### 5.1 Open Politica

| Campo | Valor |
|-------|-------|
| **URL** | https://openpolitica.com/ |
| **Rol** | Proveedor principal de datos de votacion |
| **Metodologia** | Recopilacion sistematica de actas |

### 5.2 Hiperderecho

| Campo | Valor |
|-------|-------|
| **URL** | https://hiperderecho.org/ |
| **Rol** | Metadata de proyectos de ley |
| **Enfoque** | Derechos digitales y transparencia |

### 5.3 Otras Organizaciones

| Organizacion | URL | Enfoque |
|--------------|-----|---------|
| Directorio Legislativo | https://directoriolegislativo.org/en/categoria/ingles/peru-en/ | Analisis legislativo regional |

---

## 6. Fuentes de Analisis/Noticias

### 6.1 Articulos Citados

| Fuente | URL | Contenido |
|--------|-----|-----------|
| Gestion | https://gestion.pe/economia/mas-de-7500-proyectos-de-ley-en-el-congreso-de-peru-los-que-mas-preocupan-videnza-populismo-noticia/ | 7,500+ proyectos de ley |
| Ojo Publico | https://ojo-publico.com/politica/congreso-publico-mas-100-leyes-por-insistencia-pesar-alertas | 107+ leyes por insistencia |
| Ojo Publico | https://ojo-publico.com/4925/congresistas-impulsaron-497-proyectos-ley-declarativos-el-2023 | 497 proyectos declarativos 2023 |
| Agencia Andina | https://andina.pe/agencia/noticia-congreso-90-leyes-fueron-promulgadas-durante-primera-legislatura-20242025-1012947.aspx | 90 leyes promulgadas 2024 |

### 6.2 Estudios Academicos

| Institucion | URL | Contenido |
|-------------|-----|-----------|
| PUCP | https://gobierno.pucp.edu.pe/wp-content/uploads/2024/08/poder-congresal.pdf | Estudio del poder congresal |

---

## 7. Calendario de Actualizacion

| Dataset | Frecuencia | Proxima Actualizacion |
|---------|------------|----------------------|
| Votaciones openpolitica | Trimestral | Q2 2026 (si disponible) |
| Planes de gobierno 2026 | Una vez | Completado |
| Proyectos de ley | Mensual | No planeado |

---

## 8. Limitaciones de Datos

### 8.1 Gaps Conocidos

| Gap | Descripcion | Impacto |
|-----|-------------|---------|
| Periodo 2024-07 a 2026-01 | Votaciones no incluidas en dataset | AMPAYs recientes no detectados |
| Partidos nuevos 2026 | Sin historial de votacion | Solo analisis de promesas |
| Votos secretos | No registrados | Subestimacion de participacion |

### 8.2 Calidad de Datos

| Fuente | Completitud | Precision | Notas |
|--------|-------------|-----------|-------|
| openpolitica | 99%+ | 99.7% | Verificado contra Congreso |
| JNE PDFs | 100% | Variable | OCR puede fallar |
| hiperderecho | 95% | 98% | Algunos proyectos faltantes |

---

## 9. Verificacion de URLs

**Ultima verificacion:** 2026-01-21

| URL | Estado | Notas |
|-----|--------|-------|
| github.com/openpolitica | OK | |
| github.com/hiperderecho | OK | |
| plataformaelectoral.jne.gob.pe | OK | |
| plataformahistorico.jne.gob.pe | OK | |
| congreso.gob.pe | OK | |

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Ultima actualizacion: 2026-01-21*
