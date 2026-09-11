# 🏧 Cajero Automático

Proyecto de escritorio en Python con interfaz gráfica en Tkinter para simular un cajero automático con validaciones, algoritmo de acarreo y cálculo de inventario real.

## ✨ Descripción

Este sistema permite:

- realizar retiros por NEQUI, ahorro a la mano y cuenta de ahorros
- validar datos del usuario con reglas específicas
- calcular la entrega exacta de billetes por denominación
- mostrar la matriz de intentos del algoritmo de acarreo
- proyectar cuántos retiros adicionales podría soportar el cajero
- consultar el inventario actual de billetes y su recarga automática

## 🧩 Tipos de retiro

| Tipo | Identificación | Clave |
|---|---|---|
| NEQUI | Celular de 10 dígitos y debe iniciar en `3` | Clave temporal de 6 dígitos |
| Ahorro a la mano | Vector de 11 dígitos, con primer dígito `0` o `1` y segundo `3` | PIN de 4 dígitos |
| Cuenta de ahorros | Vector de 11 dígitos | PIN de 4 dígitos |

> El dinero no pertenece a la cuenta, sino al cajero. El saldo real del sistema corresponde al efectivo físico disponible en la caja.

## 🏷️ Denominaciones soportadas

Solo se usan billetes de:

- $10.000
- $20.000
- $50.000
- $100.000

## ▶️ Cómo ejecutar

Requiere Python 3.10+

```bash
cd cajero_automatico
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

> En Windows, `tkinter` suele venir integrado con Python. En Linux puede requerirse instalar `python3-tk`.

## 🧪 Cómo probarlo

- NEQUI: usa un celular válido que empiece en `3`.
- Ahorro a la mano: usa un vector de 11 dígitos con primer dígito `0` o `1` y segundo `3`.
- Cuenta de ahorros: usa un vector válido y un PIN de 4 dígitos.

La primera vez que se usa un vector válido, el sistema lo crea automáticamente como cuenta demo.

## 🔄 Lógica de acarreo

El algoritmo trabaja por niveles de denominaciones y genera una matriz de intentos con reinicios cuando el ciclo completa una secuencia y vuelve a comenzar.

### Orden de niveles

```text
Nivel 1: 100k, 50k, 20k, 10k
Nivel 2: 100k, 50k, 20k
Nivel 3: 100k, 50k
Nivel 4: 100k
```

Esto permite evaluar qué combinación de billetes puede cubrir un monto y detectar reinicios cuando la secuencia llega a su límite.

## 📊 Predicción y disponibilidad

La aplicación muestra:

- la cantidad exacta de billetes entregados
- la matriz de intentos del acarreo
- combinaciones posibles para el monto solicitado
- el efectivo restante del cajero
- la cantidad de retiros adicionales que podría continuar entregando

## 🗂️ Estructura del proyecto

```text
cajero_automatico/
├── main.py
├── requirements.txt
├── README.md
├── data/
│   ├── cuentas.json
│   ├── inventario.json
│   └── configuracion.json
├── src/
│   ├── algorithms/
│   │   └── acarreo.py
│   ├── controller/
│   │   └── cajero.py
│   ├── repositories/
│   │   ├── cuenta_repository.py
│   │   └── inventario_repository.py
│   ├── services/
│   │   ├── caja_service.py
│   │   └── retiro_service.py
│   ├── ui/
│   │   ├── home_view.py
│   │   ├── main_window.py
│   │   ├── retiro_view.py
│   │   └── result_view.py
│   ├── utils/
│   │   ├── constantes.py
│   │   └── helpers.py
│   └── validators/
│       └── validadores.py
└── tests/
```

## ✅ Estado del proyecto

La aplicación ya permite:

- realizar retiros válidos
- validar entradas con reglas específicas
- procesar el algoritmo de acarreo
- calcular la predicción de disponibilidad del cajero
- descontar y reabastecer el inventario según el movimiento real del cajero

## 🚀 Mejoras futuras

- persistir historial de transacciones en archivo externo
- agregar pruebas automáticas más extensas
- empaquetar la app como ejecutable para distribución
