# pyCFDI/credentials
:us: The documentation of this project is in spanish as this is the natural language for intended audience.

:mexico: La documentación del proyecto está en español porque ese es el lenguaje principal de los usuarios.

Este proyecto está inspirado en [phpcfdi/credentials](https://github.com/phpcfdi/credentials/)

## Descripción
Esta librería ha sido creada para poder trabajar con los archivos CSD y FIEL del SAT. De esta forma, se simplifica el proceso de firmar, verificar firma y obtener datos particulares del archivo de certificado así como de la llave pública.

Para ver el detalle de como funcionan los certificados y las llaves privadas, echa un vistazo al archivo [manejo_de_archivos.md](doc/manejo_de_archivos.md), en él encontrarás como, a partir de los archivos provistos por el sat, generar todos los archivos necesario mediante la herramienta [OpenSSL](openssl.org)

## Roadmap
- [x] Cargar certificados y llaves desde archivos del SAT
- [x] Firmar y verificar contenido
- [ ] Determinar si el certificado cargado es FIEL, CSD u otro
- [x] Obtener información del certificado (RFC, nombre, etc)
- [x] Cambiar la contraseña de la llave privada
- [x] Convertir a formato PEM el certificado
- [x] Convertir a formato PEM la llave privada (mantener la llave encriptada)

## TODOS
- [ ] Badges
- [ ] Ilustraciones de procesamiento de certificado y llaves
- [ ] Manual de instalación
- [ ] Manual de uso
- [ ] Mecanismo de contribución
- [ ] Licencia
- [ ] Crear pipeline
  - [ ] Creacion de virtualenv (poetry)
  - [ ] Analsisis estático
  - [ ] Analisis de vulnerabilidades
  - [ ] black
  - [ ] mypy
  - [ ] tests
- [ ] Publicar en pip de forma automática al crear una nueva versión (si pasó el pipeline)
