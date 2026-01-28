# Preguntas Frecuentes (FAQ)

**Version:** 1.0
**Fecha:** 2026-01-21
**Idioma:** Espanol

---

## Sobre AMPAY

### ¿Que es AMPAY?

AMPAY es una herramienta de transparencia politica que permite a los ciudadanos:
1. Descubrir que partidos se alinean con sus posiciones mediante un quiz
2. Ver contradicciones entre promesas de campana y votos en el Congreso
3. Explorar patrones de votacion por partido y categoria

### ¿Por que se llama "AMPAY"?

"Ampay" es una expresion coloquial peruana que significa atrapar a alguien in fraganti o descubrir algo oculto. Usamos este termino porque la herramienta "atrapa" a los partidos cuando votan de manera contraria a sus promesas.

### ¿Quien creo AMPAY?

AMPAY fue creado por el usuario de GitHub [JDRV-space](https://github.com/JDRV-space), un ciudadano peruano independiente interesado en mejorar la transparencia politica. No tenemos afiliacion con ningun partido politico.

---

## Sobre el Quiz

### ¿Como funciona el quiz?

El quiz te hace 8 preguntas sobre temas politicos. Comparamos tus respuestas con las posiciones de 9 partidos usando un algoritmo llamado "distancia Manhattan" (el mismo que usan herramientas similares en Alemania y Suiza). El partido con menor "distancia" es tu mayor coincidencia.

### ¿Las preguntas de calibracion afectan mi resultado?

No directamente. Las preguntas de calibracion (izquierda/derecha, conservador/progresista) solo filtran COMO se presentan los resultados. Tu match matematico siempre se calcula igual, pero te mostramos primero los partidos dentro de tu auto-identificacion ideologica.

### ¿Por que solo 8 preguntas?

Queremos que el quiz sea rapido y accesible. Mas preguntas aumentarian la precision pero reducirian la tasa de completion. Las 8 preguntas fueron seleccionadas para cubrir los temas mas diferenciadores entre partidos.

### ¿El quiz me dice por quien votar?

**NO.** AMPAY es informativo, no una recomendacion de voto. El quiz te muestra coincidencias basadas en posiciones declaradas en planes de gobierno. Siempre debes investigar mas antes de decidir tu voto.

### ¿Que significa el porcentaje de match?

El porcentaje indica que tan similar es tu posicion a la del partido. 100% seria coincidencia perfecta, 0% seria total oposicion. La mayoria de usuarios obtienen entre 50-80% con varios partidos.

---

## Sobre los AMPAYs

### ¿Que es exactamente un AMPAY?

Un AMPAY es cuando encontramos que un partido:
- Hizo una promesa especifica en su plan de gobierno
- Voto de manera contraria a esa promesa en el Congreso

Por ejemplo: prometer "eliminar exoneraciones tributarias" pero votar SI en leyes que las extienden.

### ¿Como verifican los AMPAYs?

Cada AMPAY pasa por:
1. Deteccion automatica (busqueda de patrones)
2. Verificacion de fuentes (promesa real, voto real)
3. Analisis de conexion logica (¿la ley se relaciona con la promesa?)
4. Revision manual antes de publicar

### ¿Por que hay pocos AMPAYs?

Solo publicamos AMPAYs con alta confianza. Muchos "candidatos a AMPAY" son descartados porque:
- La conexion entre promesa y ley era debil
- Solo habia 1-2 votos (no era patron)
- Existia contexto que explicaba el voto

### ¿Pueden los partidos disputar un AMPAY?

Si. Cualquier partido o ciudadano puede abrir un issue en nuestro repositorio de GitHub con evidencia que contradiga nuestro analisis. Revisaremos y corregiremos si corresponde.

### ¿Por que algunos partidos tienen mas AMPAYs que otros?

Las razones pueden ser varias:
- Hicieron promesas mas especificas (mas verificables)
- Tuvieron mas oportunidades de votar sobre sus promesas
- Realmente votaron de manera contraria con mas frecuencia

No significa necesariamente que un partido sea "peor" que otro.

---

## Sobre los Datos

### ¿De donde vienen los datos de votacion?

Usamos datos de Open Politica, una organizacion de la sociedad civil que recopila y publica votaciones del Congreso. Puedes verificar los datos originales en su repositorio de GitHub.

### ¿De donde vienen las promesas?

Las promesas se extraen de los Planes de Gobierno oficiales registrados ante el Jurado Nacional de Elecciones (JNE). Estos son documentos publicos disponibles en la plataforma electoral del JNE.

### ¿Por que los datos solo llegan hasta julio 2024?

El dataset de votaciones que usamos se actualizo por ultima vez en julio 2024. Votaciones mas recientes no estan incluidas. Planeamos actualizar cuando haya datos nuevos disponibles.

### ¿Puedo descargar los datos?

Si. Todos nuestros datos son abiertos y estan disponibles en GitHub. Queremos que periodistas, investigadores y ciudadanos puedan verificar y usar nuestros datos.

---

## Sobre la Metodologia

### ¿Que algoritmo usan para el quiz?

Usamos distancia Manhattan, el mismo algoritmo que usa Wahl-O-Mat en Alemania y Smartvote en Suiza. Es un estandar en Voting Advice Applications (VAAs) por su simplicidad e interpretabilidad.

### ¿Como asignan posiciones a los partidos?

Leemos los planes de gobierno y asignamos:
- +1 si hay promesa explicita a favor
- -1 si hay promesa explicita en contra
- 0 si no hay posicion clara o el partido guardo silencio

### ¿Por que usan solo promesas y no votos para el quiz?

El quiz es para las elecciones 2026, asi que usamos las propuestas 2026 de los partidos. Los votos son del periodo 2021-2024 y reflejan comportamiento historico, no propuestas actuales. Los votos se usan para la seccion de AMPAYs.

### ¿Han validado la metodologia academicamente?

Nuestra metodologia se basa en literatura academica sobre VAAs y cumplimiento de promesas electorales. Citamos todas nuestras fuentes en la documentacion. No hemos realizado validacion externa formal, pero nuestro codigo y datos son abiertos para escrutinio.

---

## Sobre Privacidad

### ¿Guardan mis respuestas del quiz?

No guardamos respuestas individuales ni datos personales. El calculo se hace en tu navegador y no se envia a ningun servidor.

### ¿Usan cookies?

Solo cookies tecnicas necesarias para el funcionamiento del sitio. No usamos cookies de tracking ni publicidad.

---

## Problemas y Errores

### Encontre un error en un AMPAY, ¿como lo reporto?

Abre un issue en nuestro repositorio de GitHub con:
- El ID del AMPAY
- Que crees que esta mal
- Evidencia que respalde tu reclamo

### El quiz no funciona en mi navegador

AMPAY funciona mejor en navegadores modernos (Chrome, Firefox, Safari, Edge actualizados). Si tienes problemas, intenta:
1. Actualizar tu navegador
2. Desactivar extensiones que bloqueen JavaScript
3. Limpiar cache del navegador

### ¿Por que mi partido favorito no aparece?

Solo incluimos partidos con representacion parlamentaria significativa en el periodo 2021-2026. Partidos nuevos o muy pequenos pueden no estar incluidos.

---

## Contacto

### ¿Como puedo contactar al creador?

- GitHub: https://github.com/JDRV-space (reportar errores, sugerencias, contribuciones)
- X (Twitter): https://x.com/JDRV_space

### ¿Puedo contribuir al proyecto?

Si. AMPAY es codigo abierto. Puedes:
- Reportar errores
- Sugerir mejoras
- Contribuir codigo
- Ayudar con verificacion de datos

---

## Disclaimers

### ¿AMPAY es neutral politicamente?

AMPAY es una herramienta informativa basada en datos publicos. No hacemos recomendaciones de voto ni apoyamos a ningun partido. Nuestro objetivo es transparencia, no promocion politica.

### ¿La informacion es 100% precisa?

Hacemos nuestro mejor esfuerzo para ser precisos, pero:
- Los datos pueden tener errores menores
- La interpretacion de promesas tiene componente subjetivo
- El contexto politico puede ser mas complejo de lo que mostramos

Siempre recomendamos verificar fuentes originales para decisiones importantes.

---

*Ultima actualizacion: 2026-01-21*
