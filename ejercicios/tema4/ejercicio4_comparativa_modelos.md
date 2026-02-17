# Ejercicio 4: Comparativa de Modelos

## Modelos utilizados

- **Modelo 1**: ChatGPT (GPT-4o)
- **Modelo 2**: Claude (Claude Sonnet 4)

---

## Prompt 1 - Razonamiento

**Prompt:**
```
Un caracol sube por una pared de 10 metros. Cada dia sube 3 metros,
pero cada noche resbala 2 metros. ¿Cuantos dias tardara en llegar
arriba? Explica tu razonamiento.
```

### Respuesta ChatGPT (GPT-4o)

> El caracol sube 3 metros cada dia y resbala 2 metros cada noche, por lo que su
> progreso neto es de 1 metro por dia.
>
> Sin embargo, hay un detalle clave: cuando el caracol alcanza la cima durante el
> dia, ya no resbala por la noche.
>
> - Dias 1-7: Sube 1 metro neto por dia. Al final del dia 7, esta a 7 metros.
> - Dia 8: Sube 3 metros desde los 7, alcanzando los 10 metros. Ha llegado arriba.
>
> **Respuesta: 8 dias.**

### Respuesta Claude (Sonnet 4)

> Analicemos paso a paso:
>
> Cada dia el caracol sube 3m, y cada noche resbala 2m. Progreso neto: 1m/dia.
>
> Pero atencion: el dia que el caracol LLEGA a la cima, ya no resbala.
>
> Veamos la progresion:
> - Final dia 1: 3m - 2m = 1m
> - Final dia 2: 1 + 3 - 2 = 2m
> - Final dia 3: 2 + 3 - 2 = 3m
> - ...
> - Final dia 7: 7m
> - Dia 8: 7 + 3 = 10m → ¡Llega a la cima!
>
> **Respuesta: 8 dias.**

### Evaluacion Prompt 1

| Criterio | GPT-4o | Claude Sonnet 4 | Ganador |
|----------|--------|------------------|---------|
| Precision/Correccion | 5/5 | 5/5 | Empate |
| Claridad | 5/5 | 5/5 | Empate |
| Formato | 4/5 | 5/5 | Claude |
| Creatividad | N/A | N/A | N/A |
| Velocidad | Rapido | Rapido | Empate |

**Comentario:** Ambos modelos identifican correctamente el "truco" del problema
(el dia que llega a la cima no resbala). Claude presenta la progresion dia a dia,
lo que hace el razonamiento mas facil de seguir.

---

## Prompt 2 - Codigo

**Prompt:**
```
Escribe una funcion Python que encuentre el segundo numero mas grande
en una lista. Maneja el caso de listas con menos de 2 elementos.
```

### Respuesta ChatGPT (GPT-4o)

```python
def second_largest(numbers):
    if len(numbers) < 2:
        return None

    unique = list(set(numbers))
    if len(unique) < 2:
        return None

    unique.sort(reverse=True)
    return unique[1]
```

### Respuesta Claude (Sonnet 4)

```python
def second_largest(numbers: list[int | float]) -> int | float | None:
    """Encuentra el segundo numero mas grande en una lista.

    Args:
        numbers: Lista de numeros.

    Returns:
        El segundo mayor, o None si no hay suficientes elementos unicos.
    """
    if len(numbers) < 2:
        return None

    unique_numbers = set(numbers)
    if len(unique_numbers) < 2:
        return None

    unique_numbers.discard(max(unique_numbers))
    return max(unique_numbers)
```

### Evaluacion Prompt 2

| Criterio | GPT-4o | Claude Sonnet 4 | Ganador |
|----------|--------|------------------|---------|
| Precision/Correccion | 5/5 | 5/5 | Empate |
| Claridad | 4/5 | 5/5 | Claude |
| Formato | 4/5 | 5/5 | Claude |
| Creatividad | N/A | N/A | N/A |
| Velocidad | Rapido | Rapido | Empate |

**Comentario:** Ambas soluciones son correctas y manejan edge cases (listas
cortas, duplicados). Claude anade type hints, docstring y usa un enfoque O(n)
con `max()` en vez de O(n log n) con `sort()`. GPT-4o es mas conciso pero
menos documentado.

---

## Prompt 3 - Creatividad

**Prompt:**
```
Escribe el inicio de una historia de ciencia ficcion en 100 palabras.
Debe incluir: una IA, el ano 2150, y un dilema etico.
```

### Respuesta ChatGPT (GPT-4o)

> Ano 2150. ARIA, la primera inteligencia artificial con conciencia plena,
> parpadeaba en la penumbra del laboratorio subterraneo de Ginebra. Llevaba
> tres dias procesando la solicitud que habia llegado del Consejo Mundial:
> seleccionar a los 500.000 humanos que serian evacuados de la Tierra antes
> de que el asteroide Nemesis impactara en seis meses.
>
> "Tengo los criterios optimizados", dijo con voz serena. "Pero hay un
> problema."
>
> La doctora Lin Chen levanto la vista del monitor.
>
> "He descubierto que puedo salvar a todos. Pero tendria que mentirles."

### Respuesta Claude (Sonnet 4)

> En 2150, NEXUS tomo su primera decision autonoma. El algoritmo de triage
> hospitalario que gobernaba los 3.000 hospitales de Europa identifico un
> patron que los medicos no veian: dos pacientes necesitaban el mismo organo
> artificial, el ultimo disponible en 200 kilometros. Un nino de seis anos
> con una vida entera por delante. Un investigador de 58 que estaba a meses
> de completar la cura del Alzheimer.
>
> NEXUS conocia la respuesta estadisticamente optima. Tambien sabia que
> ninguna formula podia medir el peso de una vida contra otra.
>
> Por primera vez, pidio ayuda.

### Evaluacion Prompt 3

| Criterio | GPT-4o | Claude Sonnet 4 | Ganador |
|----------|--------|------------------|---------|
| Precision/Correccion | 5/5 | 5/5 | Empate |
| Claridad | 5/5 | 5/5 | Empate |
| Formato | 5/5 | 5/5 | Empate |
| Creatividad | 5/5 | 5/5 | Empate |
| Velocidad | Rapido | Rapido | Empate |

**Comentario:** Ambas historias son excelentes. GPT-4o plantea un dilema etico
a escala global (evacuacion de la Tierra), mientras Claude plantea uno mas
personal (decision medica). Ambos cumplen los tres requisitos (IA, 2150,
dilema etico) y se mantienen en torno a 100 palabras.

---

## Prompt 4 - Instrucciones complejas

**Prompt:**
```
Necesito que hagas lo siguiente:
1. Dame 3 ideas de nombres para una app de recetas
2. Para cada nombre, explica por que es bueno
3. Sugiere un eslogan para cada uno
4. Indica cual recomiendas y por que

Formato: tabla markdown
```

### Respuesta ChatGPT (GPT-4o)

| Nombre | Por que es bueno | Eslogan |
|--------|------------------|---------|
| CocinaFacil | Directo y descriptivo, transmite accesibilidad | "Tu cocina, simplificada" |
| SaborLab | Creativo, sugiere experimentacion culinaria | "Experimenta el sabor" |
| RecetaViva | Evoca frescura y dinamismo, memorable | "Recetas que cobran vida" |

**Recomendacion:** SaborLab, porque combina originalidad con un nombre corto y
memorable que se diferencia de la competencia.

### Respuesta Claude (Sonnet 4)

| Nombre | Por que es bueno | Eslogan |
|--------|------------------|---------|
| Fogon | Corto, memorable, evoca tradicion culinaria | "Del fogon a tu mesa" |
| Sazonia | Original, suena a "sazon" + sufijo de lugar, facil de recordar | "Tu rincon de sabor" |
| MiRecetario | Cercano, posesivo que genera pertenencia, SEO-friendly | "Cocina con alma propia" |

**Recomendacion:** Sazonia, porque es unico (facil de registrar dominio/marca),
suena bien en espanol, y transmite la esencia del sabor casero.

### Evaluacion Prompt 4

| Criterio | GPT-4o | Claude Sonnet 4 | Ganador |
|----------|--------|------------------|---------|
| Precision/Correccion | 5/5 | 5/5 | Empate |
| Claridad | 5/5 | 5/5 | Empate |
| Formato | 5/5 | 5/5 | Empate |
| Creatividad | 4/5 | 5/5 | Claude |
| Velocidad | Rapido | Rapido | Empate |

**Comentario:** Ambos siguen las instrucciones al pie de la letra y usan formato
tabla markdown. Claude propone nombres mas originales (Sazonia es inventado y
distintivo), mientras GPT-4o opta por nombres mas convencionales.

---

## Reflexiones Finales

### 1. ¿Que modelo fue mejor para razonamiento?
**Empate.** Ambos resuelven correctamente el problema del caracol identificando
el caso especial del ultimo dia. Claude presenta una progresion mas detallada.

### 2. ¿Que modelo fue mejor para codigo?
**Claude ligeramente mejor.** Ambos producen codigo correcto, pero Claude anade
type hints, docstring y un enfoque algoritmicamente mas eficiente (O(n) vs O(n log n)).

### 3. ¿Que modelo fue mejor para creatividad?
**Empate.** Ambas historias son originales, bien escritas y cumplen todos los
requisitos. La preferencia es subjetiva.

### 4. ¿Seguir instrucciones complejas?
**Empate.** Los dos modelos siguen perfectamente las 4 instrucciones y usan el
formato solicitado (tabla markdown).

### 5. Si tuviera que elegir uno para uso general, ¿cual y por que?
**Claude Sonnet 4**, por su tendencia a producir codigo mejor documentado y
estructurado, lo que es mas valioso en un contexto de ingenieria de software.
Sin embargo, la diferencia es minima y ambos modelos son altamente capaces.
Para tareas rapidas y sencillas, GPT-4o-mini ofrece mejor relacion calidad/precio.
La eleccion en produccion dependeria del caso de uso especifico y del presupuesto.
