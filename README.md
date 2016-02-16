# Guía de instalación de Pyomo

Guía traducida de instalación de Pyomo incluyendo solvers y tests.

## 0. Instalación de Python:
Lo primero que necesitamos para instalar Pyomo es Python. Nosotros recomendamos
instalar Anaconda con Python 3.5 ([descarga e instrucciones](https://www.continuum.io/downloads)).
Si lo necesitas, tienes un [vídeo de instalación para Windows 7](https://www.youtube.com/watch?v=x4xegDME5C0&feature=youtu.be&list=PLGBbVX_WvN7as_DnOGcpkSsUyXB1G_wqb).

Para comprobar que tienes la versión de Python correcta, una vez instalado abre una ventana de comandos, escribe `python` y dale a enter.

Deberás ver algo como:

```
Python 3.5.1 |Continuum Analytics, Inc.| (default, Jan 29 2016, 15:01:46) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> _
```

Nota: Fíjate que vamos a utilizar la versión de Python 3.5.1.
Si tienes instalada cualquier otra versión necesitas crear un entorno con conda. 
Para ello escribe una nueva ventana de comandos:

    conda create -n pyomo35 python=3.5 numpy matplotlib scipy jupyter ipython

Siempre que quieras trabajar con pyomo deberás de activar el entorno que has creado con
el siguientes comando:

* Windows:

    `activate pyomo35`

* Linux/Mac:

    `source activate pyomo35`

En [este vídeo](https://www.youtube.com/watch?v=cX6l3IzWewc&index=22&list=PLGBbVX_WvN7as_DnOGcpkSsUyXB1G_wqb)
explicamos con más detalle cómo gestionar una instalación de Python con Anconda/conda. 

## 1. Instalación de Pyomo:
Para instalar Pyomo sólo debes de escribir lo siguiente en la ventana de comandos
(cmd.exe) o terminal (linux o mac)

* Windows:

    `conda install -c https://conda.anaconda.org/cachemeorg pyomo`

* Linux/Mac:

    `pip install Pyomo`

Para comprobar que pyomo se ha instalado correctamente, cierra y abre una nueva
ventana de comandos y escribe:

    pyomo
Deberás de ver un mensaje similar a este:
```terminal
C:\>pyomo
usage: pyomo.exe [-h] [--version]
                 {check,convert,help,info,run,solve,test-solvers} ...

The 'pyomo' command is the top-level command for the Pyomo optimization software
.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

subcommands:
  {check,convert,help,info,run,solve,test-solvers}
    check               Check a model for errors.
    convert             Convert a Pyomo model to another format
    help                Print help information.
    info                Print information about installed packages that
                        support Pyomo.
    run                 Execute a command from the Pyomo bin (or Scripts)
                        directory.
    solve               Optimize a model
    test-solvers        Test Pyomo solvers

-------------------------------------------------------------------------
Pyomo supports a variety of modeling and optimization capabilities,
which are executed either as subcommands of 'pyomo' or as separate
commands.  Use the 'help' subcommand to get information about the
capabilities installed with Pyomo.  Additionally, each subcommand
supports independent command-line options.  Use the -h option to
print details for a subcommand.  For example, type

   pyomo solve -h
```

## 2. Instalación de Solvers
Pyomo por defecto viene sin solvers instalados. A continuación describiremos
cómo instalar algunos de los solvers que con los que Pyomo se comunica.
Para información más detallada recomendamos leer la
[documentación oficial](https://software.sandia.gov/downloads/pub/pyomo/PyomoInstallGuide.html#Solvers).
* __2a. Extras (NEOS Server)__
Lo primero que vamos a hacer es instalar algunos extras de forma similar a
como instalamos pyomo. Abrimos una ventana de comandos (cmd.exe) o terminal:

* Windows (python 3.5):

    `conda install -c https://conda.anaconda.org/cachemeorg pyomo.extras`

* Linux o Mac:

    `pip install pyomo.extras`

* __2b. Gurobi__
[Gurobi](https://www.gurobi.com/index) es un solver comercial que resuelve
problemas tipo LP, QP, MILP y MIQP. Sin embargo, Gurobi ofrece
una licencia académica sin coste que usaremos.

⋅⋅1. Para descargar e instalar gurobi podemos hacer uso de conda, el gestor de paquetes de
Anaconda que hemos instalado junto a Python:

    conda config --add channels http://conda.anaconda.org/gurobi
    conda install gurobi


⋅⋅2.  [Solicita una licencia haciendo uso de tu email
 de la universidad](http://user.gurobi.com/download/licenses/free-academic).
 Una vez registrado y aceptado los términos, se te mostrará tu número de licencia.

⋅⋅3. Para registrar la licencia basta utilizar el codigo generado en el paso anterior y
escribir lo siguiente en la ventana de comandos estando conectado en la red de tu universidad.

    grbgetkey xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx



* __2c. Otros solvers__
[GLPK](https://www.gnu.org/software/glpk/) es un solver gratuito y libre que
permite resolver problemas tipo LP y MIP. 

Para instalar GLPK en Windows ejecuta el siguiente comando:

    conda install -c https://conda.anaconda.org/snorfalorpagus glpk

Si estás en Linux o Mac utiliza este otro:

    conda install -c https://conda.anaconda.org/jjhelmus glpk
    
Otro solver libre y gratuito es 
[IPOPT](https://projects.coin-or.org/Ipopt) que permite resolver problemas NLP.
De nuevo, podemos instalarlo con conda:

* Windows:

`conda install -c https://conda.anaconda.org/juanlu001 ipopt_bin`

* Linux:

`conda install -c https://conda.anaconda.org/cachemeorg ipopt_bin`

Pyomo puede detectar los solvers que tienes disponibles con el siguiente comando:

    pyomo help -s

## 3. Probando la instalación
Vamos a resolver el problema de transporte para comprobar que hemos instalado
Pyomo y sus solvers correctamente. Para ello debemos de escribir el siguiente comando
estando en la ruta donde se encuentra el archivo transport.py

    pyomo solve --solver=glpk transport.py

Si has seguido los pasos correctamente, se habrá generado una archivo `results.yml`
con la solución de tu problema que puedes abrir con cualquier editor de texto.

De la misma forma, podemos probar el solver IPOPT para un problema no lineal. 
Recuerda que debes de escribir el siguiente comando
estando en la ruta donde se encuentra el archivo concrete.py

    pyomo solve --solver=ipopt concrete.py

### Errores de instalación
Pyomo hace uso de multitu de paquetes, en ocasiones es probable que durante
la instalación tengas algún que otro problema.

* __Errores de versiones:__

Si has tenido problemas durante la instalación, vamos a asegurarnos de que
disponemos de las últimas versiones de Python. Para ello, abrimos una ventana
de comandos (cmd.exe) o una terminal (linux o mac) y escribimos lo siguiente:

    conda udpdate conda
    conda update -all

* __Errores con Python:__

Para asegurarnos de que has instalado bien Python, abre una ventana de
comandos (cmd.exe) o una terminal (linux o mac) y escribe lo siguiente:
    python

Deberías de ver tu versión de Python como resultado:
 de haberse activado Python con información de la versión y distribución que estás usando:
 ```terminal
 Python 3.4.4 |Continuum Analytics, Inc.| (default, Jan 29 2016, 15:20:20) [MSC v
.1600 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> _
```

* __Error instalando pyomo.extras__

Si has obtenido un error en la ventana de comandos cuando instalabas pyomo.extras
no te preocupes. Estos paquetes no son imprescindibles para resolver
los problemas del curso. Por ejemplo, si recibes el error en Windows:

```
error: Microsoft Visual C++ 10.0 is required (Unable to find vcvarsall.bat).
```

Puedes instalar Visual Studio Community para tratar de solventarlo
([Descargar, 6Gb+](https://www.visualstudio.com/en-us/products/visual-studio-community-vs.aspx)).

* __Error instalando solvers__
Para instalar cualquier solver siempre es necesario descargar sus archivos
binarios más recientes para tu sistema operativo y añadirlos al PATH.
Si no entiendes muy bien qué es esto, puedes preguntarnos y/o leer una [explicación
del PATH para Windows](http://superuser.com/questions/284342/what-are-path-and-other-environment-variables-and-how-can-i-set-or-use-them).
