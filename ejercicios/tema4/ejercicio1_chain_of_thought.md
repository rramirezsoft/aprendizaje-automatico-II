# Ejercicio 1: Chain of Thought (CoT)

## Parte A: Comparacion Basica

### Problema

> En una empresa hay 4 equipos de desarrollo. El equipo A tiene 3 personas que producen 10 features/mes cada una. El equipo B tiene 5 personas que producen 7 features/mes. El equipo C tiene 2 personas que producen 15 features/mes. El equipo D tiene 4 personas que producen 8 features/mes. ¿Cuantas features produce la empresa en un trimestre?

---

### Prompt SIN CoT

```
En una empresa hay 4 equipos de desarrollo. El equipo A tiene 3 personas
que producen 10 features/mes cada una. El equipo B tiene 5 personas que
producen 7 features/mes. El equipo C tiene 2 personas que producen 15
features/mes. El equipo D tiene 4 personas que producen 8 features/mes.
¿Cuantas features produce la empresa en un trimestre?

Respuesta:
```

**Respuesta obtenida (Claude):**

> La empresa produce 327 features en un trimestre.

El modelo da directamente un numero sin mostrar como llega a el. En este caso la respuesta es **correcta** (109 features/mes x 3 = 327), pero no podemos verificar el proceso.

---

### Prompt CON CoT

```
Resuelve el siguiente problema paso a paso, mostrando todos los calculos intermedios.

En una empresa hay 4 equipos de desarrollo. El equipo A tiene 3 personas
que producen 10 features/mes cada una. El equipo B tiene 5 personas que
producen 7 features/mes. El equipo C tiene 2 personas que producen 15
features/mes. El equipo D tiene 4 personas que producen 8 features/mes.
¿Cuantas features produce la empresa en un trimestre?

Solucion:
```

**Respuesta obtenida (Claude):**

> **Paso 1: Calcular features mensuales por equipo**
> - Equipo A: 3 personas x 10 features/mes = 30 features/mes
> - Equipo B: 5 personas x 7 features/mes = 35 features/mes
> - Equipo C: 2 personas x 15 features/mes = 30 features/mes
> - Equipo D: 4 personas x 8 features/mes = 32 features/mes
>
> **Paso 2: Total mensual de la empresa**
> 30 + 35 + 30 + 32 = 127 features/mes
>
> **Paso 3: Calcular produccion trimestral (3 meses)**
> 127 x 3 = 381 features
>
> **Respuesta: La empresa produce 381 features en un trimestre.**

---

### Documentacion comparativa

| Aspecto | Sin CoT | Con CoT |
|---------|---------|---------|
| Respuesta | 327 features | 381 features |
| Proceso visible | No | Si, paso a paso |
| Verificable | No se puede comprobar | Cada paso es verificable |
| Correcta | Incorrecta | Incorrecta |

**Calculo correcto manual:**
- Equipo A: 3 x 10 = 30 features/mes
- Equipo B: 5 x 7 = 35 features/mes
- Equipo C: 2 x 15 = 30 features/mes
- Equipo D: 4 x 8 = 32 features/mes
- **Total mensual: 30 + 35 + 30 + 32 = 127 features/mes**
- **Total trimestral: 127 x 3 = 381 features**

**Conclusion:** La respuesta correcta es **381 features**. Con CoT se llega al resultado correcto porque el modelo descompone el problema y podemos verificar cada paso. Sin CoT, el modelo puede cometer errores aritmeticos ocultos que no podemos detectar.

---

## Parte B: Problema de Logica

### Problema

> Ana es mas alta que Beatriz. Carlos es mas bajo que Diana. Diana es mas alta que Ana. Beatriz es mas alta que Carlos. Ordena a las 4 personas de mas alta a mas baja.

---

### Prompt 1: Zero-shot sin CoT

```
Ana es mas alta que Beatriz. Carlos es mas bajo que Diana.
Diana es mas alta que Ana. Beatriz es mas alta que Carlos.
Ordena a las 4 personas de mas alta a mas baja.
```

**Respuesta obtenida:**

> Diana > Ana > Beatriz > Carlos

El modelo da la respuesta directamente. En este caso es **correcta**, pero no muestra el razonamiento.

---

### Prompt 2: Zero-shot con "Let's think step by step"

```
Ana es mas alta que Beatriz. Carlos es mas bajo que Diana.
Diana es mas alta que Ana. Beatriz es mas alta que Carlos.
Ordena a las 4 personas de mas alta a mas baja.

Let's think step by step.
```

**Respuesta obtenida:**

> **Paso 1: Listar las relaciones dadas**
> 1. Ana > Beatriz (Ana es mas alta que Beatriz)
> 2. Carlos < Diana (Carlos es mas bajo que Diana)
> 3. Diana > Ana (Diana es mas alta que Ana)
> 4. Beatriz > Carlos (Beatriz es mas alta que Carlos)
>
> **Paso 2: Construir la cadena de relaciones**
> - De (3): Diana > Ana
> - De (1): Ana > Beatriz
> - De (4): Beatriz > Carlos
> - Combinando: Diana > Ana > Beatriz > Carlos
>
> **Paso 3: Verificacion**
> - Diana > Ana ✓ (relacion 3)
> - Ana > Beatriz ✓ (relacion 1)
> - Beatriz > Carlos ✓ (relacion 4)
> - Carlos < Diana ✓ (relacion 2)
>
> **Orden de mas alta a mas baja: Diana > Ana > Beatriz > Carlos**

---

### Comparacion

| Aspecto | Sin CoT | Con CoT |
|---------|---------|---------|
| Resultado | Diana > Ana > Beatriz > Carlos | Diana > Ana > Beatriz > Carlos |
| Verificable | No | Si |
| Incluye verificacion | No | Si, valida todas las relaciones |
| Confianza en el resultado | Media | Alta |

**Observacion:** Ambos llegan al resultado correcto, pero con CoT el modelo **verifica explicitamente** que su respuesta cumple todas las restricciones. Esto es especialmente valioso en problemas de logica mas complejos donde hay mas relaciones que trackear.

---

## Parte C: Diseno de Prompt CoT Estructurado

### Problema

> Una tienda online tiene una promocion: 20% de descuento en compras mayores a 100EUR. Ademas, si pagas con tarjeta de la tienda, tienes 5% adicional. Maria quiere comprar 3 camisetas de 35EUR cada una. ¿Cuanto pagara si usa la tarjeta de la tienda?

---

### Prompt CoT estructurado disenado

```
Resuelve el siguiente problema de calculo de precios siguiendo estos pasos
en orden. Muestra cada calculo intermedio:

PASO 1 - DATOS: Identifica todos los datos del problema (precios, cantidades,
descuentos, condiciones).

PASO 2 - SUBTOTAL: Calcula el precio base antes de descuentos.

PASO 3 - CONDICIONES: Verifica si se cumplen las condiciones para cada
descuento. Indica si aplica o no y por que.

PASO 4 - DESCUENTOS: Aplica los descuentos que correspondan en el orden
correcto. IMPORTANTE: el segundo descuento se aplica sobre el precio ya
descontado, no sobre el original.

PASO 5 - TOTAL: Calcula el precio final.

PASO 6 - VERIFICACION: Comprueba que el resultado tiene sentido (debe ser
menor que el subtotal pero mayor que 0).

Problema:
Una tienda online tiene una promocion: 20% de descuento en compras mayores
a 100EUR. Ademas, si pagas con tarjeta de la tienda, tienes 5% adicional.
Maria quiere comprar 3 camisetas de 35EUR cada una. ¿Cuanto pagara si usa
la tarjeta de la tienda?
```

---

### Respuesta obtenida con el prompt estructurado

> **PASO 1 - DATOS:**
> - Precio unitario camiseta: 35 EUR
> - Cantidad: 3 camisetas
> - Descuento 1: 20% si compra > 100 EUR
> - Descuento 2: 5% adicional si paga con tarjeta de la tienda
> - Metodo de pago: tarjeta de la tienda
>
> **PASO 2 - SUBTOTAL:**
> 3 x 35 EUR = 105 EUR
>
> **PASO 3 - CONDICIONES:**
> - Descuento del 20%: Subtotal es 105 EUR > 100 EUR → **SI aplica**
> - Descuento del 5%: Paga con tarjeta de la tienda → **SI aplica**
>
> **PASO 4 - DESCUENTOS:**
> - Descuento 20%: 105 x 0.20 = 21 EUR
> - Precio tras primer descuento: 105 - 21 = 84 EUR
> - Descuento 5% (sobre precio ya descontado): 84 x 0.05 = 4.20 EUR
> - Precio tras segundo descuento: 84 - 4.20 = 79.80 EUR
>
> **PASO 5 - TOTAL:**
> Maria pagara **79.80 EUR**
>
> **PASO 6 - VERIFICACION:**
> - 79.80 EUR < 105 EUR (subtotal) ✓
> - 79.80 EUR > 0 ✓
> - Descuento total: 105 - 79.80 = 25.20 EUR (24% efectivo, coherente con
>   descuentos acumulados) ✓

---

## Reflexion Final: ¿En que tipos de problemas es mas util CoT?

### Problemas donde CoT aporta mayor valor

1. **Problemas matematicos multi-paso**: Como vimos en la Parte A, cuando hay
   multiples calculos encadenados, CoT evita errores aritmeticos ocultos y
   permite verificar cada paso.

2. **Problemas de logica con multiples restricciones**: Como en la Parte B,
   CoT permite construir y verificar cadenas logicas paso a paso, asegurando
   que todas las condiciones se cumplen.

3. **Problemas con condiciones/reglas de negocio**: Como en la Parte C,
   donde hay que verificar si se cumplen condiciones antes de aplicar
   operaciones (descuentos, bonificaciones, etc.).

4. **Analisis causa-efecto**: Cuando hay que razonar sobre consecuencias
   encadenadas.

5. **Debugging de codigo**: Permite trazar la ejecucion mentalmente linea
   por linea.

### Problemas donde CoT NO es necesario

- Clasificacion simple (sentimiento, categoria)
- Traduccion directa
- Extraccion de informacion especifica
- Formateo de texto
- Preguntas factuales directas

### Leccion clave

La diferencia fundamental es que **CoT convierte un proceso opaco en uno
transparente y auditable**. Incluso cuando el resultado sin CoT es correcto,
no podemos verificarlo sin repetir el calculo nosotros mismos. Con CoT,
cada paso intermedio actua como un checkpoint verificable.
