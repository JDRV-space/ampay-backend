# Data Sources

**Version:** 1.0
**Date:** 2026-01-21
**Status:** ACTIVE

---

## Executive Summary

This document catalogs all data sources used in AMPAY, including URLs, access dates, and data formats.

---

## 1. Parliamentary Voting Data

### 1.1 Primary Source

| Field | Value |
|-------|-------|
| **Name** | openpolitica/congreso-pleno-asistencia-votacion |
| **URL** | https://github.com/openpolitica/congreso-pleno-asistencia-votacion |
| **Format** | CSV |
| **Period** | 2021-07-26 to 2024-07-26 |
| **Records** | ~289,000 individual votes |
| **Sessions** | 2,226 sessions (post-filtering) |
| **Last updated** | July 2024 |
| **Download date** | 2026-01-15 |
| **License** | Open Data |

### 1.2 Available Fields

| Field | Type | Description |
|-------|------|-------------|
| `fecha` | date | Date of the vote |
| `asunto` | string | Description of the subject voted on |
| `congresista` | string | Name of the legislator |
| `grupo_parlamentario` | string | Party at the time of the vote |
| `votacion` | enum | SI / NO / ABSTENCION / AUSENTE |

### 1.3 Complementary Official Source

| Field | Value |
|-------|-------|
| **Name** | Congress - Plenary Attendance and Votes |
| **URL** | https://www.congreso.gob.pe/AsistenciasVotacionesPleno/ |
| **Format** | PDF (unstructured) |
| **Usage** | Manual verification |

---

## 2. Bills (Metadata)

### 2.1 Primary Source

| Field | Value |
|-------|-------|
| **Name** | hiperderecho/proyectos_de_ley |
| **URL** | https://github.com/hiperderecho/proyectos_de_ley |
| **Format** | SQLite (leyes.db) |
| **Website** | https://github.com/hiperderecho/proyectos_de_ley |
| **Content** | Bill metadata |
| **Download date** | 2026-01-15 |

### 2.2 Relevant Fields

| Field | Type | Description |
|-------|------|-------------|
| `codigo` | string | Bill number |
| `titulo` | string | Official title |
| `fecha_presentacion` | date | Submission date |
| `autor` | string | Authoring legislator(s) |
| `estado` | enum | In committee / Approved / Archived |
| `comision` | string | Assigned committee |

---

## 3. Governance Plans

### 3.1 2021 Elections

| Field | Value |
|-------|-------|
| **Name** | JNE Historical Platform |
| **URL** | https://plataformahistorico.jne.gob.pe/OrganizacionesPoliticas/PlanesGobiernoTrabajo |
| **Format** | PDF |
| **Parties** | 9 major parties |
| **Download date** | 2026-01-15 |

**Verified direct links:**

| Party | 2021 Plan URL |
|-------|---------------|
| Juntos por el Peru | https://apisije-e.jne.gob.pe/TRAMITE/ESCRITO/1587/ARCHIVO/FIRMADO/5262.PDF |
| Accion Popular | https://declara.jne.gob.pe/ASSETS/PLANGOBIERNO/FILEPLANGOBIERNO/16511.pdf |

### 3.2 2026 Elections

| Field | Value |
|-------|-------|
| **Name** | JNE Electoral Platform |
| **URL** | https://plataformaelectoral.jne.gob.pe/candidatos/plan-gobierno-trabajo/buscar |
| **Format** | PDF |
| **Candidates** | 36 presidential candidates |
| **Download date** | 2026-01-18 |

### 3.3 JNE Comparative Report

| Field | Value |
|-------|-------|
| **URL** | https://saednef.jne.gob.pe/Content/PlanesGobierno/documentos/REPORTE%20F%20DE%20PLANES%20DE%20GOBIERNO.pdf |
| **Content** | Official comparison of proposals |

---

## 4. Official Government Portals

### 4.1 Congress of the Republic

| Resource | URL |
|----------|-----|
| Main Portal | https://www.congreso.gob.pe/ |
| Plenary Votes | https://www.congreso.gob.pe/AsistenciasVotacionesPleno/ |
| Bills | https://www.congreso.gob.pe/proyectosdeley/ |
| Congress in Numbers | https://www.congreso.gob.pe/GestionInformacionEstadistica/congreso-cifras/ |
| Rules of Procedure | https://www.congreso.gob.pe/reglamento/ |

### 4.2 National Elections Jury (JNE)

| Resource | URL |
|----------|-----|
| Main Portal | https://www.jne.gob.pe/ |
| Electoral Platform 2026 | https://plataformaelectoral.jne.gob.pe/ |
| Historical Platform | https://plataformahistorico.jne.gob.pe/ |
| 2026 Elections Info | https://portal.jne.gob.pe/portal/Pagina/Ver/979/page/Elecciones-Generales-2026 |

### 4.3 ONPE

| Resource | URL |
|----------|-----|
| Open Data | https://datosabiertos.gob.pe/users/onpedatos |

### 4.4 Other Entities

| Entity | URL | Content |
|--------|-----|---------|
| El Peruano | https://diariooficial.elperuano.pe/Normas | Official legal norms |
| MEF Transparency | https://www.mef.gob.pe/es/por-instrumento/decreto-de-urgencia | Emergency decrees |

---

## 5. Transparency Organizations

### 5.1 Open Politica

| Field | Value |
|-------|-------|
| **URL** | https://openpolitica.com/ |
| **Role** | Primary voting data provider |
| **Methodology** | Systematic compilation from official minutes |

### 5.2 Hiperderecho

| Field | Value |
|-------|-------|
| **URL** | https://hiperderecho.org/ |
| **Role** | Bill metadata |
| **Focus** | Digital rights and transparency |

### 5.3 Other Organizations

| Organization | URL | Focus |
|--------------|-----|-------|
| Directorio Legislativo | https://directoriolegislativo.org/en/categoria/ingles/peru-en/ | Regional legislative analysis |

---

## 6. Analysis and News Sources

### 6.1 Cited Articles

| Source | URL | Content |
|--------|-----|---------|
| Gestion | https://gestion.pe/economia/mas-de-7500-proyectos-de-ley-en-el-congreso-de-peru-los-que-mas-preocupan-videnza-populismo-noticia/ | 7,500+ bills |
| Ojo Publico | https://ojo-publico.com/politica/congreso-publico-mas-100-leyes-por-insistencia-pesar-alertas | 107+ laws passed by override |
| Ojo Publico | https://ojo-publico.com/4925/congresistas-impulsaron-497-proyectos-ley-declarativos-el-2023 | 497 declaratory bills in 2023 |
| Agencia Andina | https://andina.pe/agencia/noticia-congreso-90-leyes-fueron-promulgadas-durante-primera-legislatura-20242025-1012947.aspx | 90 laws enacted in 2024 |

### 6.2 Academic Studies

| Institution | URL | Content |
|-------------|-----|---------|
| PUCP | https://gobierno.pucp.edu.pe/wp-content/uploads/2024/08/poder-congresal.pdf | Study on congressional power |

---

## 7. Update Schedule

| Dataset | Frequency | Next Update |
|---------|-----------|-------------|
| openpolitica voting data | Quarterly | Q2 2026 (if available) |
| 2026 governance plans | Once | Completed |
| Bills | Monthly | Not planned |

---

## 8. Data Limitations

### 8.1 Known Gaps

| Gap | Description | Impact |
|-----|-------------|--------|
| Period 2024-07 to 2026-01 | Votes not included in dataset | Recent AMPAYs not detected |
| New 2026 parties | No voting history | Promise analysis only |
| Secret votes | Not recorded | Underestimation of participation |

### 8.2 Data Quality

| Source | Completeness | Accuracy | Notes |
|--------|-------------|----------|-------|
| openpolitica | 99%+ | 99.7% | Verified against Congress |
| JNE PDFs | 100% | Variable | OCR may fail |
| hiperderecho | 95% | 98% | Some bills missing |

---

## 9. URL Verification

**Last verified:** 2026-01-21

| URL | Status | Notes |
|-----|--------|-------|
| github.com/openpolitica | OK | |
| github.com/hiperderecho | OK | |
| plataformaelectoral.jne.gob.pe | OK | |
| plataformahistorico.jne.gob.pe | OK | |
| congreso.gob.pe | OK | |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-01-21*
