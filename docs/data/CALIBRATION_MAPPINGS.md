# Mapeos de Calibracion Ideologica

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Este documento detalla como se mapean los partidos politicos a los ejes de calibracion (economico y social) utilizados en el quiz de AMPAY para filtrar resultados segun la auto-identificacion del usuario.

---

## 1. Proposito del Sistema de Calibracion

### 1.1 Objetivo

El sistema de calibracion permite que usuarios vean primero partidos dentro de su "zona de confort" ideologica, evitando reacciones negativas cuando el match matematico sugiere partidos inesperados.

### 1.2 No Afecta el Calculo

**IMPORTANTE:** Las preguntas de calibracion NO afectan el calculo de distancia Manhattan. Solo filtran la PRESENTACION de resultados.

```
Calculo: 100% basado en preguntas Q01-Q08
Calibracion: Solo afecta orden y agrupacion del display
```

---

## 2. Ejes de Calibracion

### 2.1 Eje Economico (C1)

**Pregunta:**
> "En temas economicos, ordena del mas al menos identificado:"

**Opciones:**
1. Izquierda
2. Centro
3. Derecha

**Metodo de input:** Usuario RANKEA las 3 opciones (1 = mas identificado, 3 = menos identificado)

### 2.2 Eje Social (C2)

**Pregunta:**
> "En temas sociales y culturales, ordena del mas al menos identificado:"

**Opciones:**
1. Conservador
2. Moderado
3. Progresista

**Metodo de input:** Usuario RANKEA las 3 opciones (1 = mas identificado, 3 = menos identificado)

---

## 3. Mapeo Partidos por Eje

### 3.1 Eje Economico

| Posicion | Partidos | Justificacion |
|----------|----------|---------------|
| **Izquierda** | Peru Libre, Juntos por el Peru | Estatismo, nacionalizacion, control de precios |
| **Centro** | Partido Morado, Somos Peru, Alianza para el Progreso | Economia mixta, pragmatismo, sin posicion extrema |
| **Derecha** | Fuerza Popular, Renovacion Popular, Avanza Pais, Podemos Peru | Libre mercado, reduccion del estado, privatizacion |

### 3.2 Eje Social

| Posicion | Partidos | Justificacion |
|----------|----------|---------------|
| **Conservador** | Renovacion Popular, Peru Libre | Pro-familia tradicional, oposicion a enfoque de genero |
| **Moderado** | Fuerza Popular, Podemos Peru, Alianza para el Progreso, Avanza Pais, Somos Peru | Sin agenda social fuerte, posiciones pragmaticas |
| **Progresista** | Partido Morado, Juntos por el Peru | Derechos LGBTQ+, enfoque de genero, derechos civiles |

---

## 4. Matriz Completa de Mapeo

| Partido | Eje Economico | Eje Social |
|---------|---------------|------------|
| Peru Libre | Izquierda | Conservador |
| Juntos por el Peru | Izquierda | Progresista |
| Partido Morado | Centro | Progresista |
| Somos Peru | Centro | Moderado |
| Alianza para el Progreso | Centro | Moderado |
| Fuerza Popular | Derecha | Moderado |
| Renovacion Popular | Derecha | Conservador |
| Avanza Pais | Derecha | Moderado |
| Podemos Peru | Derecha | Moderado |

---

## 5. Logica de Filtrado

### 5.1 Reglas

```
Rank 1 → Partidos en este grupo: INCLUIDOS como "Dentro de tu perfil"
Rank 2 → Partidos en este grupo: INCLUIDOS como "Dentro de tu perfil"
Rank 3 → Partidos en este grupo: EXCLUIDOS de "Dentro de tu perfil"
```

### 5.2 Combinacion de Ejes

Un partido es EXCLUIDO si cae en Rank 3 de CUALQUIER eje.

**Ejemplo:**
```
Usuario:
  C1 (economico): Derecha (1), Centro (2), Izquierda (3)
  C2 (social): Moderado (1), Conservador (2), Progresista (3)

Excluidos:
  - Izquierda economica: Peru Libre, Juntos Peru
  - Progresista social: Partido Morado, Juntos Peru

Partido Morado: Excluido (progresista)
Peru Libre: Excluido (izquierda + conservador pero izquierda lo excluye)
Juntos Peru: Excluido (izquierda + progresista, ambos rank 3)
```

### 5.3 Display Final

```
"Dentro de tu perfil:"
  [Top 3 de partidos NO excluidos, ordenados por % match]

"Tus respuestas se alinean con:"
  [#1 match matematico, SIEMPRE mostrado]
  (Si es partido excluido, mostrar nota explicativa)
```

---

## 6. Justificacion de Mapeos

### 6.1 Peru Libre como Izquierda Economica + Conservador Social

**Evidencia:**
- Plan de gobierno 2021: Nacionalizacion de recursos, control estatal
- Plan de gobierno 2026: Economia planificada, estatismo
- Posiciones sociales: Oposicion a "ideologia de genero", valores andinos tradicionales

### 6.2 Partido Morado como Centro Economico + Progresista Social

**Evidencia:**
- Plan de gobierno: Economia mixta, regulacion inteligente
- Posiciones sociales: Derechos LGBTQ+, matrimonio igualitario, enfoque de genero

### 6.3 Renovacion Popular como Derecha Economica + Conservador Social

**Evidencia:**
- Plan de gobierno: Reduccion del estado, libre mercado
- Posiciones sociales: Pro-vida, pro-familia tradicional, oposicion a enfoque de genero

---

## 7. Casos Especiales

### 7.1 Peru Libre (Izquierda + Conservador)

Combinacion inusual en contexto occidental pero comun en izquierda latinoamericana andina.

### 7.2 Partidos con Posicion Ambigua

| Partido | Ambiguedad | Resolucion |
|---------|------------|------------|
| Somos Peru | Sin ideologia clara | Centro/Moderado (default pragmatico) |
| Alianza Progreso | Empresarial pero regional | Centro/Moderado |
| Podemos Peru | Pro-empresa pero flexible | Derecha/Moderado |

---

## 8. Representacion JSON

```json
{
  "calibration_questions": {
    "questions": [
      {
        "id": "C1",
        "text": "En temas economicos, ordena del mas al menos identificado:",
        "options": ["Izquierda", "Centro", "Derecha"],
        "maps_to_parties": {
          "Izquierda": ["peru_libre", "juntos_peru"],
          "Centro": ["partido_morado", "somos_peru", "alianza_progreso"],
          "Derecha": ["fuerza_popular", "renovacion_popular", "avanza_pais", "podemos_peru"]
        }
      },
      {
        "id": "C2",
        "text": "En temas sociales y culturales, ordena del mas al menos identificado:",
        "options": ["Conservador", "Moderado", "Progresista"],
        "maps_to_parties": {
          "Conservador": ["renovacion_popular", "peru_libre"],
          "Moderado": ["fuerza_popular", "podemos_peru", "alianza_progreso", "avanza_pais", "somos_peru"],
          "Progresista": ["partido_morado", "juntos_peru"]
        }
      }
    ]
  }
}
```

---

## 9. Algoritmo de Filtrado

```python
def filtrar_por_calibracion(partidos, c1_ranking, c2_ranking):
    """
    c1_ranking: dict { "Izquierda": 1, "Centro": 2, "Derecha": 3 }
    c2_ranking: dict { "Conservador": 1, "Moderado": 2, "Progresista": 3 }
    """
    excluidos = set()

    # Excluir partidos en rank 3 de C1
    for opcion, rank in c1_ranking.items():
        if rank == 3:
            excluidos.update(C1_MAPS[opcion])

    # Excluir partidos en rank 3 de C2
    for opcion, rank in c2_ranking.items():
        if rank == 3:
            excluidos.update(C2_MAPS[opcion])

    # Filtrar
    dentro_perfil = [p for p in partidos if p.slug not in excluidos]
    fuera_perfil = [p for p in partidos if p.slug in excluidos]

    return dentro_perfil, fuera_perfil
```

---

## 10. Validacion

### 10.1 Consistencia Interna

Verificar que:
- Cada partido aparece en exactamente 1 opcion de C1
- Cada partido aparece en exactamente 1 opcion de C2
- No hay partidos sin mapear

### 10.2 Validacion Externa

Comparar mapeos con:
- Chapel Hill Expert Survey (CHES) si disponible para Peru
- Clasificaciones de ciencia politica
- Auto-identificacion de partidos

---

## 11. Limitaciones

1. **Simplificacion:** 3 opciones no capturan matices ideologicos
2. **Estatico:** Mapeos pueden cambiar con el tiempo
3. **Subjetivo:** Clasificacion tiene componente interpretativo
4. **Sin validacion externa:** No hay CHES para Peru 2026

---

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Ultima actualizacion: 2026-01-21*
