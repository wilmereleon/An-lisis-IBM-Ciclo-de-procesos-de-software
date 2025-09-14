# 📋 PLANTILLA FUNCIONAL DE CASOS DE PRUEBA
## Basada en ISO/IEC 29119 - Sistema de Registro de Usuario

---

## 📌 INFORMACIÓN BÁSICA

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre** | Validación de Login de Usuario en Sistema de Banca Virtual |
| **Autor** | Federico Toledo / Equipo QA IBM |
| **Fecha** | 09/01/2024 |
| **Descripción** | Un usuario debe registrarse para hacer uso del sistema, y para ello debe hacer "login" con su usuario y password. Si no cuenta con él, debe registrarse en el sistema creando así su usuario |

---

## 👥 ACTORES DEL SISTEMA

- **Usuario a través de la interfaz web**

---

## ✅ PRE-CONDICIONES

- El usuario debe estar registrado en el sistema

---

## 🔄 FLUJO NORMAL

| **Paso** | **Acción** |
|----------|------------|
| **1** | El usuario accede al sistema con la URL principal |
| **2** | El sistema solicita credenciales |
| **3** | El usuario ingresa proporcionando usuario y password |
| **4** | El sistema valida las credenciales del usuario |
| **5** | El sistema da la bienvenida |

---

## 🔀 FLUJO ALTERNATIVO 1

| **Paso** | **Acción** |
|----------|------------|
| **3** | El usuario no recuerda su password por lo que solicita que se le envíe por e-mail |
| **4** | El sistema solicita el e-mail y envía una clave temporal |

---

## 🔀 FLUJO ALTERNATIVO 2

| **Paso** | **Acción** |
|----------|------------|
| **3** | El usuario no está registrado en el sistema por lo que solicita crear una cuenta |
| **4** | El sistema solicita los datos necesarios para crear la cuenta |
| **5** | El usuario ingresa los datos y confirma |
| **6** | El sistema crea la cuenta del usuario |

---

## ⚠️ EXCEPCIONES

| **ID** | **Descripción** |
|--------|-----------------|
| **E1** | **Usuario y password incorrectos:** Si esto sucede tres veces consecutivas la cuenta del usuario se bloquea por seguridad |
| **E2** | **[E4]: El e-mail proporcionado no está registrado en el sistema.** El sistema notifica el error |

---

## ✅ POST-CONDICIONES

- El usuario accede al sistema y se registra su acceso en la tabla de registro de actividad

---

# 🧪 TABLA DE EJECUCIÓN DE CASOS DE PRUEBA

## 📊 Información del Caso

| **Campo** | **Valor** |
|-----------|-----------|
| **ID** | mt01 |
| **Target Description** | Ingreso a banca virtual |
| **Type** | Funcional |
| **Priority** | Media |
| **Pre-Conditions** | 1) Creación de cuenta<br>2) Ingreso banca virtual |

---

## 📝 Matriz de Ejecución

| **#** | **Steps / Expected Result** | **Pass** | **Fail** | **Bug Report ID** |
|-------|----------------------------|----------|----------|-------------------|
| **1** | **Acceso a banca digital**<br>• Ingresar datos solicitados<br>• (tipo: nombre, documento, contraseña)<br>**Expected:** Se visualiza correctamente | ✅ | | |
| **2** | **Seleccionar opción ingreso**<br>**Expected:** Acceso correcto a la Banca virtual | ✅ | | |
| **3** | | | | |
| **4** | | | | |
| **5** | | | | |
| **6** | | | | |

---

## 👤 Información del Ejecutor

| **Campo** | **Valor** |
|-----------|-----------|
| **Executor** | Mercurio Avellaneda Vargas |
| **Date** | __________ |
| **ID** | kt-23 |

---

## 📋 PLANTILLA EN BLANCO PARA USO

### Copiar y completar esta sección para nuevos casos de prueba:

```markdown
# CASO DE PRUEBA

## INFORMACIÓN BÁSICA
- **Nombre:** ________________________________
- **Autor:** ________________________________
- **Fecha:** ________________________________
- **Descripción:** ________________________________

## ACTORES DEL SISTEMA
- ________________________________

## PRE-CONDICIONES
- ________________________________

## FLUJO NORMAL
1. ________________________________
2. ________________________________
3. ________________________________
4. ________________________________
5. ________________________________

## FLUJO ALTERNATIVO
3. ________________________________
4. ________________________________

## EXCEPCIONES
- **E1:** ________________________________
- **E2:** ________________________________

## POST-CONDICIONES
- ________________________________

## TABLA DE EJECUCIÓN
| # | Steps / Expected Result | Pass | Fail | Bug Report ID |
|---|------------------------|------|------|---------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

**Executor:** _____________ | **Date:** _______ | **ID:** _____
```

---

> **Nota:** Esta plantilla está basada en los estándares ISO/IEC 29119 para documentación de casos de prueba y puede ser utilizada como formato estándar para el proyecto de análisis de calidad de software en IBM.