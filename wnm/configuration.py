from traitlets.config import Config
from traitlets.config.loader import FileConfigLoader, JSONFileConfigLoader, ConfigFileNotFound
import yaml 
import os


from .utilities import write_wnm_documentation, write_rst_documentation, write_sphinx_config, write_root_index, install_logo

class YAMLFileConfigLoader(FileConfigLoader):
    """A YAML file loader for config                                                  
                                                                                      
    Can also act as a context manager that rewrite the configuration file to disk on exit.                                                                                 

    Example::                                                                         
        with YAMLFileConfigLoader('myapp.yaml','/home/jupyter/configurations/') as c:
            c.MyNewConfigurable.new_value = 'Updated'                                 
    """
    def load_config(self):
        """Load the config from a file and return it as a Config object."""
        self.clear()
        try:
            self._find_file()
        except IOError as e:
            raise ConfigFileNotFound(str(e))
        dct = self._read_file_as_dict()
        self.config = self._convert_to_config(dct)
        return self.config

    def _read_file_as_dict(self):
        with open(self.full_filename) as f:
            return yaml.load(f)

    def _convert_to_config(self, dictionary):
        c = Config(dictionary)

        ## Hand-made sub-config handle since the standard one doesn't work here. 
        for key, value in c.items():
            if isinstance(value, dict) and not isinstance(value, Config):
                setattr(c, key, Config(value))
        return c

    def __enter__(self):
        self.load_config()
        return self.config

    def __exit__(self, exc_type, exc_value, traceback):
        """                                                                           
        Exit the context manager but do not handle any errors.                        
                                                                                      
        In case of any error, we do not want to write the potentially broken          
        configuration to disk.                                                        
        """
        with open(self.full_filename, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)



_DEFAULT_CONFIG = {
    "manager": {
        "data_path": "~/.local/wnm/sources",
        "build_path": "~/.local/wnm/build",
        "name": "Working Notes Manager",
        "editor": "env"},
    "sphinx": {
        "theme": "sphinx_rd_theme",
        "logo": "~/.local/wnm/logo.png"
    }
}

class WNMConfigLoader(YAMLFileConfigLoader):
    def __init__(self, fpath=None, fname="config.yaml"):
        if fpath == None:
            fpath = self._locate_config(fname)
            
        YAMLFileConfigLoader.__init__(self, fname, fpath)
            
    def _locate_config(self, fname):
        home_dir = os.getenv("HOME")
        wnm_local = os.path.join(home_dir, ".local", "wnm" )
        if os.path.exists( wnm_local ):
            conf_file = os.path.join( wnm_local, fname )
            if os.path.exists( conf_file ):
                return wnm_local
        else:
            self._create_default( fname )
            return wnm_local

    def _create_default(self, fname ):
        print("Create a default config file")
        home_dir = os.getenv("HOME")
        wnm_local = os.path.join(home_dir, ".local", "wnm" )
        os.makedirs( wnm_local )
        conf_file = os.path.join( wnm_local, fname )

        with open(conf_file, "w") as f:
            yaml.dump( _DEFAULT_CONFIG, f, default_flow_style=False)


_DEFAULT_CONFIG = {
    "version": 0.1,
    "manager": {
        "notes": {
            "notebook":{
                "name": "Working Notes Manager",
                "data": os.path.expandvars("$HOME/.local/wnm/sources"),
                "build": os.path.expandvars("$HOME/.local/wnm/build"),
            }
        },
        "editor": "internal"
    },
    "sphinx": {
        "theme": "sphinx_rtd_theme",
        "logo": os.path.expandvars("$HOME/.local/wnm/logo.png"),
        "static": os.path.expandvars("$HOME/.local/wnm/sources/_static")
    },
    "shortcut": {
        "pdf": "Ctrl+p",
        "zoomin": "Ctrl+z",
        "zoomout": "Ctrl+u",
        "edit": "Ctrl+e",
        "create": "Ctrl+n",
        "delete": "Ctrl+d",
        "compile": "Ctrl+x"
    }
}


def get_default_conf_path():
    home_dir = os.getenv("HOME")
    wnm_local = os.path.join(home_dir, ".local", "wnm", "config.yaml")
    return wnm_local

def fill_configuration( conf, before="" ):
    for key, value in conf.items():
        if isinstance( value, Config):
            fill_configuration( value, before=before+" "+key)
        else:
            inp = input("{} {} [default: {}] : ".format(before, key, value))
            if inp == "":
                continue
            else:
                conf[key] = inp


def conf_recursive( conf ):
    for key, value in conf.items():
        if isinstance(value, dict) and not isinstance(value, Config):
            setattr(conf, key, Config(value))
            conf_recursive( conf[key] )
    

def create_environment(cpath, cfile):
    header = """Welcome to Working Notes Manager 
Please configure as you want the following parameters"""
    print( header )
    
    conf = Config(_DEFAULT_CONFIG)
    conf_recursive( conf )

    #fill_configuration( conf )

    ## Create the ~/.local/wnm/config.yaml
    home_dir = os.getenv("HOME")
    try:
        os.makedirs( cpath )
    except:
        print("The ~/.local/wnm directory already exists")
        print("The content of the previous one will be overwrite")
        inp = input(" Are you sure you want to overwrite it [yes/no]" )
        if inp != "yes":
            sys.exit(0)

    conf_file = os.path.join( cpath, cfile )
    with open(conf_file, "w") as f:
        yaml.dump( conf, f, default_flow_style=False)

    ## Create the notes sources directory as specified in the config.yml
    src_dir = conf.manager.notes.notebook.data
    if os.path.exists( src_dir ):
        print('The data directory specified already exists')
    else:
        os.mkdir( src_dir )

    ## Create the static dir 
    static_dir = os.path.join( conf.manager.notes.notebook.data, "_static" )
    if not os.path.exists( static_dir ):
        os.mkdir( static_dir )

    install_logo( static_dir )


    index_rst = os.path.join( conf.manager.notes.notebook.data, "index.rst" )
    if not os.path.exists( index_rst):
        with open(index_rst, "w") as f:
            write_root_index( f, conf) 

    else:
        return False

    ## Install in the source directory the help for RST file and WMN usage 
    os.mkdir( os.path.join( conf.manager.notes.notebook.data, "category_help" ) )
    
    with open( os.path.join(conf.manager.notes.notebook.data, "category_help", "Notice.rst" ), "w") as f:
        write_wnm_documentation( f )

    with open( os.path.join(conf.manager.notes.notebook.data, "category_help", "reStructuredText.rst" ), "w") as f:
        write_rst_documentation( f )


    ## Create the ~/.local/wnm/config.py need for the sphinx-build command
    sphinx_config = os.path.join( conf.manager.notes.notebook.data, "conf.py" )
    with open( sphinx_config, "w") as f:
        write_sphinx_config( f, conf)

    return True
    
        
if __name__ == "__main__":                                             
    create_environment(None, None)
