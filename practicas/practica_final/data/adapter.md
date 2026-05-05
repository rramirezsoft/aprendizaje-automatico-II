# Patron Adapter

## Categoria
Estructural.

## Proposito
Permitir que dos clases con interfaces incompatibles colaboren entre si envolviendo una de ellas con un objeto adaptador que traduce las llamadas de una interfaz a la otra. Tambien se conoce como "Wrapper".

## Cuando usarlo
- Cuando se quiere usar una clase existente cuya interfaz no coincide con la que espera el codigo cliente.
- Para integrar codigo legado con un sistema nuevo sin reescribir el codigo legado.
- Para usar librerias o APIs externas detras de una fachada propia, de forma que un cambio de libreria no obligue a tocar todo el codigo cliente.
- Cuando varias clases tienen funcionalidad similar pero interfaces distintas y se quiere unificarlas.

## Estructura
El cliente trabaja con una interfaz Target que define los metodos que espera. La clase Adaptee es la clase existente con interfaz incompatible. El Adapter implementa la interfaz Target y mantiene una referencia al Adaptee, traduciendo cada llamada de Target en una o varias llamadas a Adaptee.

## Ejemplo en Python
```python
class CalculadoraVieja:
    def operar(self, a, b, simbolo):
        if simbolo == "+":
            return a + b
        if simbolo == "-":
            return a - b

class CalculadoraNueva:
    def sumar(self, a, b): ...
    def restar(self, a, b): ...

class AdaptadorCalculadora(CalculadoraNueva):
    def __init__(self, vieja: CalculadoraVieja):
        self.vieja = vieja

    def sumar(self, a, b):
        return self.vieja.operar(a, b, "+")

    def restar(self, a, b):
        return self.vieja.operar(a, b, "-")

calc = AdaptadorCalculadora(CalculadoraVieja())
print(calc.sumar(3, 4))  # 7
```

## Ventajas
- Permite reutilizar codigo existente sin modificarlo.
- Aisla al cliente de los detalles de la clase adaptada.
- Cumple el principio de responsabilidad unica al separar la conversion de interfaces de la logica de negocio.

## Desventajas
- Aumenta la complejidad del codigo al introducir clases intermedias.
- Si hay muchos metodos a adaptar puede generar mucho codigo repetitivo.

## Diferencia con Decorator
Decorator añade nuevas responsabilidades manteniendo la misma interfaz. Adapter cambia la interfaz pero no añade nueva funcionalidad: solo traduce.

## Casos reales
Drivers de bases de datos que adaptan distintos motores SQL a una interfaz comun (DBAPI en Python, JDBC en Java), wrappers que adaptan APIs antiguas a interfaces modernas, conectores entre sistemas heterogeneos en arquitecturas hexagonales.
