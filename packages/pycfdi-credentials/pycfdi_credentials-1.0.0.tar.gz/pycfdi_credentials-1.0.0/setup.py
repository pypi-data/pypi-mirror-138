# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycfdi_credentials']

package_data = \
{'': ['*']}

install_requires = \
['pyOpenSSL>=22.0.0,<23.0.0']

setup_kwargs = {
    'name': 'pycfdi-credentials',
    'version': '1.0.0',
    'description': 'Library to manage CSD and FIEL files from SAT. Use this to sign, verify and get certificate data.',
    'long_description': '# pyCFDI/credentials\n:us: The documentation of this project is in spanish as this is the natural language for intended audience.\n\n:mexico: La documentación del proyecto está en español porque ese es el lenguaje principal de los usuarios.\n\nEste proyecto está inspirado en [phpcfdi/credentials](https://github.com/phpcfdi/credentials/)\n\n## Descripción\nEsta librería ha sido creada para poder trabajar con los archivos CSD y FIEL del SAT. De esta forma, se simplifica el proceso de firmar, verificar firma y obtener datos particulares del archivo de certificado así como de la llave pública.\n\nPara ver el detalle de como funcionan los certificados y las llaves privadas, echa un vistazo al archivo [manejo_de_archivos.md](doc/manejo_de_archivos.md), en él encontrarás como, a partir de los archivos provistos por el sat, generar todos los archivos necesario mediante la herramienta [OpenSSL](openssl.org)\n\n## Roadmap\n- [x] Cargar certificados y llaves desde archivos del SAT\n- [x] Firmar y verificar contenido\n- [ ] Determinar si el certificado cargado es FIEL, CSD u otro\n- [x] Obtener información del certificado (RFC, nombre, etc)\n- [x] Cambiar la contraseña de la llave privada\n- [x] Convertir a formato PEM el certificado\n- [x] Convertir a formato PEM la llave privada (mantener la llave encriptada)\n\n## TODOS\n- [ ] Badges\n- [ ] Ilustraciones de procesamiento de certificado y llaves\n- [ ] Manual de instalación\n- [ ] Manual de uso\n- [ ] Mecanismo de contribución\n- [ ] Licencia\n- [ ] Crear pipeline\n  - [ ] Creacion de virtualenv (poetry)\n  - [ ] Analsisis estático\n  - [ ] Analisis de vulnerabilidades\n  - [ ] black\n  - [ ] mypy\n  - [ ] tests\n- [ ] Publicar en pip de forma automática al crear una nueva versión (si pasó el pipeline)\n',
    'author': 'Moises Navarro',
    'author_email': 'moisalejandro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
