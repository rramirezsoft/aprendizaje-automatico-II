# Patron Strategy

## Categoria
Comportamiento.

## Proposito
Definir una familia de algoritmos intercambiables, encapsulando cada uno en una clase separada, de forma que puedan seleccionarse y cambiarse en tiempo de ejecucion sin modificar el codigo cliente que los usa.

## Cuando usarlo
- Cuando hay varias formas de realizar la misma tarea (ordenacion, calculo de impuestos, descuentos, validacion, compresion) y se quiere elegir cual aplicar segun el contexto.
- Cuando una clase tiene multiples ramas `if/elif/else` que dependen de un "modo" o "tipo" y se quiere eliminar esa estructura.
- Cuando se necesita inyectar el comportamiento desde fuera para facilitar el testing o permitir extensiones.

## Estructura
El cliente trabaja con una interfaz Strategy que declara un metodo comun (por ejemplo `ejecutar()` o `aplicar()`). Cada algoritmo concreto implementa esa interfaz. La clase Contexto recibe una Strategy por parametro (inyeccion de dependencias) y delega en ella la ejecucion del algoritmo.

## Ejemplo en Python
```python
from abc import ABC, abstractmethod

class EstrategiaPago(ABC):
    @abstractmethod
    def pagar(self, importe: float): ...

class PagoTarjeta(EstrategiaPago):
    def pagar(self, importe):
        print(f"Pagando {importe}€ con tarjeta")

class PagoPaypal(EstrategiaPago):
    def pagar(self, importe):
        print(f"Pagando {importe}€ con PayPal")

class Carrito:
    def __init__(self, estrategia: EstrategiaPago):
        self.estrategia = estrategia

    def finalizar(self, total):
        self.estrategia.pagar(total)

Carrito(PagoTarjeta()).finalizar(50)
Carrito(PagoPaypal()).finalizar(30)
```

## Ventajas
- Elimina condicionales largos basados en tipo o modo.
- Cada algoritmo queda aislado y es facilmente testeable de forma independiente.
- Permite añadir nuevas estrategias sin modificar el contexto (principio abierto/cerrado).
- El comportamiento puede cambiarse en tiempo de ejecucion.

## Desventajas
- Aumenta el numero de clases en el proyecto.
- El cliente debe conocer las estrategias disponibles para elegir una.
- Para casos triviales con una o dos opciones puede ser excesivo.

## Diferencia con State
Strategy y State tienen estructura similar (delegar comportamiento a otra clase), pero Strategy se usa cuando el cliente elige conscientemente un algoritmo, mientras que State modela transiciones automaticas entre estados de un objeto.
