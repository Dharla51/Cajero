# 🏧 Cajero Automático

Aplicación desktop desarrollada en Python con Tkinter para simular un cajero con validación de cuentas, cálculo de retiros, recorrido del algoritmo de acarreo y control del inventario real del cajero.

## 📌 ¿Qué hace el proyecto?

La aplicación permite:

- realizar retiros por NEQUI, ahorro a la mano y cuenta de ahorros
- validar los datos del usuario según reglas específicas
- calcular la entrega de billetes por denominación
- mostrar la matriz de intentos del acarreo
- proyectar cuántos retiros adicionales puede soportar la caja
- descontar y recargar el inventario real del cajero según el retiro realizado

## 🧩 Reglas de validación del usuario

### 1) NEQUI
- longitud: 10 dígitos
- primer dígito obligatorio: `3`
- ejemplo válido: `3001234567`

### 2) Ahorro a la mano
- longitud: 11 dígitos
- primer dígito: `0` o `1`
- segundo dígito obligatorio: `3`
- ejemplo válido: `03345678901`

### 3) Cuenta de ahorros
- longitud: 11 dígitos
- solo admite números
- ejemplo válido: `50123456789`

### 4) PIN / clave
- 4 dígitos exactos
- no se muestran en pantalla al escribir

> El dinero no está asociado a la cuenta del usuario; la cuenta solo valida la identidad y la clave. El saldo real del sistema corresponde al efectivo físico que hay en la caja del cajero.

## 💵 Denominaciones del cajero

El sistema trabaja con estas denominaciones:

- $10.000
- $20.000
- $50.000
- $100.000

El orden del recorrido del cajero queda definido como:

```text
10.000 -> 20.000 -> 50.000 -> 100.000
```

## 🔄 Lógica del acarreo

El algoritmo no depende de una matriz rígida de valores fija en todo el código, sino del recorrido del monto con la secuencia de denominaciones. La app genera la secuencia de intentos y contabiliza cómo se va cubriendo el valor solicitado.

La salida final devuelve:

- la cantidad exacta de billetes por denominación
- el total de billetes entregados
- la matriz de intentos del acarreo
- el valor verificado del retiro
- la cantidad de combinaciones posibles para ese monto

### Ejemplo de recorrido

Para un monto de 300.000, la matriz generada por la lógica del proyecto queda así:

```text
Intento 1: {10000:1, 20000:1, 50000:1, 100000:1}
Intento 2: {10000:0, 20000:1, 50000:1, 100000:0}
Intento 3: {10000:0, 20000:0, 50000:1, 100000:0}
```

Esto es lo que la interfaz muestra como la matriz de intentos del acarreo.

## 🧮 Predicción y caja

La aplicación adicionalmente muestra:

- cuántos retiros podrían realizarse con el efectivo restante
- la cantidad disponible del cajero por denominación
- el inventario real de billetes en la caja
- la recarga automática cuando el inventario queda muy bajo

La lógica del inventario realiza una resta real de billetes por cada retiro ejecutado y persiste los cambios en archivo JSON.

## ▶️ Cómo ejecutar el proyecto

Requisitos:

- Python 3.10+
- Tkinter

```bash
cd cajero_automatico
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

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
│   │   ├── inventario_view.py
│   │   ├── main_window.py
│   │   ├── retiro_view.py
│   │   └── result_view.py
│   ├── utils/
│   │   ├── constantes.py
│   │   └── helpers.py
│   └── validators/
│       └── validadores.py
├── tests/
│   └── test_validadores.py
└── .gitignore
```

## ✅ Estado actual

El proyecto ya está funcionando con:

- validación correcta de NEQUI, ahorro a la mano y cuenta de ahorros
- denominaciones 10k, 20k, 50k y 100k
- cálculo del acarreo con recorrido de matriz de intentos
- inventario real de la caja con decremento por retiro
- recarga automática del cajero cuando hace falta efectivo
- pantalla final con resultado, predicción y control visual del inventario

## 🧪 Verificación

Se validó con:

```bash
python -m pytest -q
```

Resultado esperado:

```text
3 passed
```

## 🚀 Futuras mejoras

- historial de retiros en archivo externo
- exportación de reportes
- interfaz más avanzada para gestión del inventario
- empaquetado ejecutable para distribución
