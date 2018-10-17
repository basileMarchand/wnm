import os
import sphinx.cmd.build as sphinx
import subprocess as sub

from .configuration import WNMConfigLoader, get_default_conf_path, create_environment

class NotesManager:
    def __init__(self, conf_file=None):
        if conf_file == None:
            self._conf_path = get_default_conf_path()
        else:
            self._conf_path = conf_file

        self._config = None
        self._nb_name = "notebook"
        
    def get_config(self):
        return self._config

    def get_build_dir(self):
        return os.path.join( self._config.manager.notes[self._nb_name].build, "html")

    def set_current_notebook(self, name ):
        self._nb_name = name

    def config_exists(self):
        return  os.path.exists( self._conf_path )

    def load_config(self):
        cpath, cfile = os.path.split( self._conf_path )
        loader = WNMConfigLoader(fpath=cpath, fname=cfile)
        self._config = loader.load_config()
        
    def initialize_config(self):
        cpath, cfile = os.path.split( self._conf_path )        
        ret = create_environment(cpath, cfile)
        return ret

    def listCategory(self):
        list_dirs = os.listdir( self._config.manager.notes[self._nb_name].data )
        list_category = [ f[len("category_"):] for f in list_dirs if f[:len("category_")] == "category_" ]
        list_category.remove("help")   ## To avoid new notes in the help category
        return list_category

    def listNotes(self):
        _data = {}
        list_category = self.listCategory()
        for cate in list_category:
            _data[cate] = []
            list_file = os.listdir( os.path.join( self._config.manager.notes[self._nb_name].data, "category_"+cate ))
            for f in list_file:
                if f != "index.rst" and f[-3:] == "rst":
                    _data[cate].append( f )
        return _data

    def createCategory(self, category_name ):
        list_category = self.listCategory()
        if category_name in list_category:
            raise Exception()
        else:
            os.mkdir( os.path.join( self._config.manager.notes[self._nb_name].data, "category_" + category_name ) )

        with open( os.path.join( self._config.manager.notes[self._nb_name].data, "category_" + category_name  , "index.rst"), "w") as f:
            f.write(".. _{}-index:".format( category_name ))
            f.write("\n\n")
            f.write("".join(["="]*len(category_name)))
            f.write("\n")
            f.write(category_name + "\n")
            f.write("".join(["="]*len(category_name)))
            f.write("\n\n\n")
            f.write(".. toctree::\n")
            f.write("    :maxdepth: 1\n")
            f.write("\n")
            f.write("\n")
                    
        ## write the link in the root index.rst
        fid = open(os.path.join( self._config.manager.notes[self._nb_name].data, "index.rst"), "r")
        content = fid.read().split("\n")
        fid.close()

        with open(os.path.join( self._config.manager.notes[self._nb_name].data, "index.rst"), "w") as f:
            _inserted = False
            i = 0
            while i < len(content):
                line = content[i]
                f.write( line )
                f.write("\n")
                i+= 1
                if ":maxdepth:" in line:
                    f.write("\n")
                    f.write("   {} <{}/index>".format(category_name, "category_"+category_name))


    def createNote(self, category, name ):
        note_path = os.path.join( self._config.manager.notes[self._nb_name].data, "category_"+category, name + ".rst" )
        
        with open( note_path, "w") as f:
            f.write( name + "\n")
            f.write( "".join( ["="]*len(name)))
            f.write("\n")

        ## Add the link in the corrisponding index
        index_path = os.path.join( self._config.manager.notes[self._nb_name].data, "category_"+category, "index.rst" )
        fid = open( index_path, "r")
        content = fid.read().split("\n")
        fid.close()
        
        with open( index_path, "w" ) as f:
            _inserted = False
            for line in content:
                if ".rst" in line and not _inserted: ## I add the new link before other one
                    f.write("    {}\n".format( name + ".rst" ))
                    _inserted = True

                f.write(line)
                f.write("\n")

            if not _inserted:
                f.write("    {}\n".format( name + ".rst" ))


    def editNote(self, category, name ):

        if category is None:
            fpath = os.path.join(self._config.manager.notes[self._nb_name].data, name + ".rst")
        else:
            fpath = os.path.join(self._config.manager.notes[self._nb_name].data, "category_" + category, name + ".rst")

        if self._config.manager.editor == "env":
            editor = os.getenv("EDITOR")
            sub.call(editor + " " + fpath, shell=True)
        elif self._config.manager.editor == "internal":
            pass
            ## Do a minimal qt base text editor

        else: ## Define directly the command to use for example emacs or geany
            editor = self._config.manager.editor
            sub.call(editor + " " + fpath, shell=True)
            

    def compileHtml(self):
        sphinx_args = "-b html -d {0}/doctrees {1} {0}/html".format( self._config.manager.notes[self._nb_name].build, self._config.manager.notes[self._nb_name].data)
        print(sphinx_args )
        sphinx.main( sphinx_args.split() )



    
