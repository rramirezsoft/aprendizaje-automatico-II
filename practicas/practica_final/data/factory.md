# Patron Factory Method

## Categoria
Creacional.

## Proposito
Definir una interfaz para crear objetos pero permitir que las subclases decidan que clase concreta instanciar. Encapsula la logica de creacion de objetos detras de un metodo, desacoplando al cliente del tipo concreto que se construye.

## Cuando usarlo
- Cuando el codigo cliente no debe conocer las clases concretas que necesita instanciar.
- Cuando una clase quiere delegar a sus subclases la decision de que tipo de objeto crear.
- Cuando se trabaja con familias de productos relacionados y se quiere centralizar su creacion.
- Para frameworks o librerias que deben permitir extensiones por terceros sin modificar su nucleo.

## Estructura
Una clase abstracta (Creator) define un metodo factoria, normalmente llamado `crearProducto()`. Cada subclase concreta implementa ese metodo devolviendo una instancia del producto especifico. El cliente usa el metodo del Creator sin saber que tipo concreto recibe.

## Ejemplo en Python
```python
from abc import ABC, abstractmethod

class Notificacion(ABC):
    @abstractmethod
    def enviar(self, mensaje): ...

class NotificacionEmail(Notificacion):
    def enviar(self, mensaje):
        print(f"Email: {mensaje}")

class NotificacionSMS(Notificacion):
    def enviar(self, mensaje):
        print(f"SMS: {mensaje}")

class FabricaNotificaciones:
    @staticmethod
    def crear(tipo: str) -> Notificacion:
        if tipo == "email":
            return NotificacionEmail()
        if tipo == "sms":
            return NotificacionSMS()
        raise ValueError(f"Tipo desconocido: {tipo}")

n = FabricaNotificaciones.crear("email")
n.enviar("Hola")
```

## Ventajas
- Desacopla al cliente de las clases concretas, que pueden cambiar sin afectarlo.
- Centraliza la logica de construccion en un unico lugar.
- Facilita extender el sistema con nuevos productos sin tocar codigo existente (principio abierto/cerrado).

## Desventajas
- Puede aumentar el numero de clases si hay muchos productos.
- Anade un nivel de indireccion que dificulta el seguimiento del codigo en proyectos pequeños.

## Diferencia con Abstract Factory
Factory Method crea **un** producto. Abstract Factory crea **familias completas de productos relacionados** mediante varios metodos factoria agrupados.
