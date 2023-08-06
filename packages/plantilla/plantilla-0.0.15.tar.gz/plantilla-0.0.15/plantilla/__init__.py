def importar_style():

  import os
  import matplotlib

  from pkg_resources import resource_string

  files = [
    'styles\\mecon.mplstyle',
  ]

  for fname in files:
    path = os.path.join(matplotlib.get_configdir(),fname)
    text = resource_string(__name__,fname).decode()
    open(path,'w').write(text)


def plantilla(proyecto=None, subproyecto=None, path_proyectos=None):
    
    import os
    import matplotlib
    import matplotlib.pyplot as plt
    from pathlib import Path

    try:
        plt.style.use('mecon.mplstyle')
    except:
        from site import getsitepackages
        site_packages = getsitepackages()
        for folder in site_packages:
            try:
                path_style = os.path.join(folder, 'plantilla', 'styles', 'mecon.mplstyle')
                path_stylelib = os.path.join(matplotlib.get_configdir(), 'stylelib')
                path_end_style = os.path.join(path_stylelib, 'mecon.mplstyle')
                Path(path_style).rename(path_end_style)
                plt.style.use(path_end_style)
            except:
                pass

    else:
        path_stylelib = os.path.join(matplotlib.get_configdir(), 'stylelib')
        path_end_style = os.path.join(path_stylelib, 'mecon.mplstyle')
        print(f'No se pudo importar el estilo. Mover a mano a el archivo "mecon.mplstyle" desde la carpeta de plantilla (ruta de python/Lib/site-packages/plantilla/styles) a {path_end_style} y activarlo con "plt.style.use("mecon.mplstyle")"')
            
    
    # from sfi import Macro

    # proyecto = Macro.getGlobal("proyecto")

    try:
        from sfi import Macro
        proyecto = Macro.getGlobal("proyecto")
        subproyecto = Macro.getGlobal("subproyecto")
    except:
        if proyecto==None:
            raise NameError("Error. Globales no definidas.")
        else:   
            proyecto = proyecto
            subproyecto = subproyecto

    path_user = ''
    
    test_path = fr"C:\Users\Administrador\Documents\MECON\{proyecto}"


    if os.path.isdir(test_path):
        path_user = test_path

    elif path_proyectos:
        path_user = path_proyectos + '\\' + str(proyecto)

    else:
        path = os.path.normpath(os.getcwd() + os.sep + os.pardir) # Get padre de la ruta del archivo

        path_user = path + '\\' + str(proyecto)

        if os.path.isdir(path_user)==False:
            raise NameError("Error 404. Directorio no encontrado, revisar nombre del proyecto")
    
    folders = []

    print(path_user + fr'\scripts\{subproyecto}')

    if os.path.isdir(path_user + fr'\scripts\{subproyecto}'):
        
        print("El directorio en scripts existe. Creando carpetas.")
        
        try:
            folders = [r'\data',
                        r'\data\data_in',
                        r'\data\data_out',
                        fr'\data\data_out\{subproyecto}',
                        r'\docs',
                        r'\scripts',
                        fr'\scripts\{subproyecto}',
                        r'\outputs',
                        r'\outputs\figures',
                        fr'\outputs\figures\{subproyecto}',
                        r'\outputs\maps',
                        fr'\outputs\maps\{subproyecto}',
                        r'\outputs\tables',
                        fr'\outputs\tables\{subproyecto}']

        except:
            folders = [ r'\data',
                        r'\data\data_in',
                        r'\data\data_out',
                        r'\docs',
                        r'\scripts',
                        r'\outputs',
                        r'\outputs\figures',
                        r'\outputs\maps',
                        r'\outputs\tables']


        for folder in folders:

            mkdir = path_user + folder
            if os.path.isdir(mkdir)==False:
                os.mkdir(mkdir)
                print(mkdir, 'Creado')
            else:
                print(mkdir, 'ya existe')

    else:
        raise NameError("El directorio en scripts no existe. Por favor, crear una carpeta en scripts con el nombre del subproyecto.")
            
    # global path_datain	  
    # global path_dataout  
    # global path_scripts  
    # global path_figures  
    # global path_maps	  
    # global path_tables	  
    # global path_programas


    path_datain	   = path_user + r'\data\data_in'
    path_dataout   = path_user + r'\data\data_out'
    path_scripts   = path_user + fr'\scripts\{subproyecto}'
    path_figures   = path_user + fr'\outputs\figures\{subproyecto}'
    path_maps	   = path_user + fr'\outputs\maps\{subproyecto}'
    path_tables	   = path_user + fr'\outputs\tables\{subproyecto}'
    path_programas = path_user + r'"C:\Users\Administrador\Documents\MECON\0. Varios\scripts\Programas"'


    try:
        from sfi import Macro
        Macro.setGlobal('path_user', path_user)
        Macro.setGlobal('path_datain', path_datain)
        Macro.setGlobal('path_dataout', path_dataout)
        Macro.setGlobal('path_scripts', path_scripts)
        Macro.setGlobal('path_figures', path_figures)
        Macro.setGlobal('path_maps', path_maps)
        Macro.setGlobal('path_tables', path_tables)
        Macro.setGlobal('path_programas', path_programas)

    except:
        return (
            path_user,
            path_datain,	  
            path_dataout,  
            path_scripts, 
            path_figures,  
            path_maps,	  
            path_tables,	  
            path_programas
        )
    
if __name__ == "__main__":
    plantilla(sys.argv[1], sys.argv[2])
