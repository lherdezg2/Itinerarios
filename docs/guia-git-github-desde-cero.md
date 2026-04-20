# Guia Git y GitHub desde cero (paso a paso)

Esta guia esta pensada para simular trabajo en equipo con 2 desarrolladores y rama principal `main`.

## 1) Crear cuenta en GitHub

1. Entrar a https://github.com
2. Crear cuenta personal.
3. Verificar correo.

## 2) Instalar Git en Windows

1. Descargar instalador: https://git-scm.com/download/win
2. Ejecutar instalador con opciones por defecto.
3. Cerrar y abrir de nuevo la terminal.
4. Verificar instalacion:

```bash
git --version
```

## 3) Configurar Git por primera vez

Ejecutar en terminal (una sola vez):

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"
git config --global init.defaultBranch main
```

Verificar configuracion:

```bash
git config --list
```

## 4) Crear repositorio remoto en GitHub

1. En GitHub, clic en "New repository".
2. Nombre sugerido: `itinerarios-microservicios`.
3. Elegir "Public" o "Private" segun indicacion del profesor.
4. No marcar README en GitHub (ya existe localmente).
5. Crear repositorio.

## 5) Conectar proyecto local con GitHub

Dentro de la carpeta raiz del proyecto ejecutar:

```bash
git init
git add .
git commit -m "chore: estructura base de microservicios"
git remote add origin <URL_DEL_REPOSITORIO>
git push -u origin main
```

## 6) Crear ramas de trabajo (2 desarrolladores)

Ramas sugeridas:

- `dev-estudiante-a`
- `dev-estudiante-b`

Crearlas y publicarlas:

```bash
git checkout -b dev-estudiante-a
git push -u origin dev-estudiante-a

git checkout main
git checkout -b dev-estudiante-b
git push -u origin dev-estudiante-b

git checkout main
```

## 7) Flujo diario por cada HU

Ejemplo para desarrollador A:

```bash
git checkout dev-estudiante-a
git pull origin dev-estudiante-a
# hacer cambios de una HU

git add .
git commit -m "feat(HU-123): crear endpoint de consulta de aeropuertos"
git push
```

Luego en GitHub:

1. Abrir Pull Request desde `dev-estudiante-a` hacia `main`.
2. Solicitar revision (tu companera o tu profesor).
3. Hacer merge cuando este aprobado.

Despues del merge:

```bash
git checkout main
git pull origin main
```

Y sincronizar rama de desarrollo:

```bash
git checkout dev-estudiante-a
git merge main
git push
```

Repetir lo mismo para `dev-estudiante-b`.

## 8) Reglas practicas para su equipo

- Una HU por commit o por pequeno grupo de commits.
- Mensajes de commit claros con ID de HU.
- No trabajar directo sobre `main`.
- Siempre hacer Pull Request hacia `main`.
- Si hay conflicto, resolverlo en la rama de desarrollo antes del merge.

## 9) Comandos utiles de consulta

```bash
git status
git branch
git branch -a
git log --oneline --graph --decorate --all
```

## 10) Convencion simple de commits recomendada

- `chore:` configuracion o infraestructura.
- `feat:` nueva funcionalidad de HU.
- `fix:` correccion de error.
- `docs:` cambios en documentacion.

Ejemplos:

- `chore: agregar docker-compose del MVP`
- `feat(HU-201): crear caso de uso para crear itinerario`
- `docs: actualizar arquitectura hexagonal`

## 11) Errores comunes y solucion rapida

- Error `fatal: not a git repository`:
  - Estas fuera de la carpeta del proyecto. Entra a la carpeta raiz y repite.
- Error de autenticacion en push:
  - Usar GitHub Desktop o configurar token personal (PAT).
- Error por cambios sin commit al cambiar de rama:
  - Ejecutar commit o stash antes de hacer checkout.

Con esto ya puedes trabajar en paralelo con tu companera y simular el flujo real de desarrollo solicitado.
