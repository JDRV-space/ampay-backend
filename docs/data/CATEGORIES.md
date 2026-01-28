# AMPAY - Categories

## 15 Categories for Promise & Vote Classification

| # | Category | Spanish | Covers |
|---|----------|---------|--------|
| 1 | seguridad | Seguridad | Crimen, policía, cárceles, narcotráfico |
| 2 | economia | Economía | Impuestos, comercio, inversión, MYPE |
| 3 | fiscal | Fiscal | Déficit, presupuesto, deuda pública |
| 4 | social | Social | Pobreza, bonos, programas sociales, pensiones |
| 5 | empleo | Empleo | Trabajo, laboral, informalidad |
| 6 | educacion | Educación | Escuelas, universidades, becas |
| 7 | salud | Salud | Hospitales, medicamentos, anemia, SIS |
| 8 | agua | Agua/Saneamiento | Agua potable, desagüe, alcantarillado |
| 9 | vivienda | Vivienda | Déficit habitacional, urbanismo |
| 10 | transporte | Transporte | Puertos, aeropuertos, carreteras |
| 11 | energia | Energía | Electricidad, gas, petróleo |
| 12 | mineria | Minería | Minería formal/informal, canon |
| 13 | ambiente | Ambiente | Deforestación, residuos, contaminación |
| 14 | agricultura | Agricultura | Campo, riego, productores |
| 15 | justicia | Justicia/Anticorrupción | Tribunales, transparencia, corrupción |

## Notes

- **Digitalización** removed - it's a HOW, not a WHAT (cross-cutting)
- Categories derived from sampling Fuerza Popular plan de gobierno
- Same categories used for both:
  - Planes de gobierno (promises)
  - Asuntos de votación (congress votes)

## Usage

### For LLM Prompt (Promise Extraction):
```
Classify this promise into ONE of these categories:
seguridad, economia, fiscal, social, empleo, educacion, salud, agua, vivienda, transporte, energia, mineria, ambiente, agricultura, justicia

If unclear, choose the closest match. Never use "otros".
```

### For LLM Prompt (Vote Classification):
```
Classify this voting subject (asunto) into ONE of these categories:
seguridad, economia, fiscal, social, empleo, educacion, salud, agua, vivienda, transporte, energia, mineria, ambiente, agricultura, justicia

If unclear, choose the closest match. Never use "otros".
```

---

*Last updated: 2026-01-21*
