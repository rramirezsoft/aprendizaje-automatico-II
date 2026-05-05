# Patron Observer

## Categoria
Comportamiento.

## Proposito
Definir una dependencia uno-a-muchos entre objetos de forma que, cuando uno (el sujeto) cambia su estado, todos los que dependen de el (los observadores) son notificados y actualizados automaticamente.

## Cuando usarlo
- Cuando un cambio en un objeto requiere cambios en otros y no se sabe de antemano cuantos seran.
- Para implementar sistemas de eventos, suscripciones o notificaciones push.
- Para desacoplar el productor de los datos de los consumidores que reaccionan a esos datos.
- Es la base de la programacion reactiva (RxJS, Redux, signals) y de los sistemas pub/sub.

## Estructura
Un Sujeto mantiene una lista de Observadores y expone metodos para registrarlos y desregistrarlos. Cuando su estado cambia, recorre la lista y llama al metodo `update()` de cada observador. Los observadores implementan una interfaz comun para que el sujeto pueda tratarlos uniformemente.

## Ejemplo en Python
```python
class Sujeto:
    def __init__(self):
        self._observadores = []
        self._estado = None

    def suscribir(self, observador):
        self._observadores.append(observador)

    def cambiar_estado(self, nuevo_estado):
        self._estado = nuevo_estado
        for o in self._observadores:
            o.actualizar(nuevo_estado)

class Observador:
    def __init__(self, nombre):
        self.nombre = nombre

    def actualizar(self, estado):
        print(f"{self.nombre} recibio: {estado}")

s = Sujeto()
s.suscribir(Observador("A"))
s.suscribir(Observador("B"))
s.cambiar_estado("nuevo dato")
```

## Ventajas
- Desacopla al sujeto de los observadores: no necesita conocer sus tipos concretos.
- Permite añadir o eliminar observadores en tiempo de ejecucion.
- Soporta comunicacion broadcast (uno publica, muchos reaccionan).

## Desventajas
- Si hay muchos observadores, las notificaciones pueden ser costosas.
- El orden de notificacion no esta garantizado.
- Las cadenas largas de observadores pueden producir actualizaciones inesperadas y bucles.

## Casos reales
Listeners de eventos del DOM en JavaScript, signals en Django, suscriptores de un topic en sistemas pub/sub como Kafka o Redis.
