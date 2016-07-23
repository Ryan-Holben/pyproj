"""

    Savely is short for "SAVE safeLY"

    Lets you safely build a collection of files and folders.  It keeps track of everything written to disk, and automatically deletes everything we created if an error is encountered.

    Contains classes "Path" and "Savely".

"""

import os, sys
from subprocess import call
from shutil import rmtree
# from traceback import print_exc
import atexit
from pprint import pprint

class Path(object):
    """A simple class for building and representing file paths."""
    def __init__(self, *args):
        self.encodePath(*args)

    def encodePath(self, *args):
        """Take in a path, clean it, and save the result."""
        if args == None:
            self.parts = []
            return None
        else:
            self.parts = [x.strip("/") for x in args]

    def __str__(self):
        """Glue strings together into a nice path string."""
        return "/".join(self.parts)

    def subpaths(self):
        """Returns a list of all subpaths.  For example, if we have encoded "a/b/c", this returns ["a", "a/b", "a/b/c"]"""
        fullpath = self.__str__()
        splits = filter(lambda i: fullpath[i]=="/", range(len(fullpath)))
        return [fullpath[:i] for i in splits] + [fullpath]

    def onlyFolders(self):
        """If the Path() represents a file (e.g. "a/b/c/file.txt") return a Path() instance with the file removed."""
        return Path(*(folder for folder in self.parts[:-1]))


class Savely(object):
    """Class for safe creation of files and folders.  Features include recursively adding folders as necessary, and keeping track of everything written to disk so that we may delete our files/folders (but not preexisting files/folders) if an error is encountered."""
    def __init__(self):
        self.files = []
        self.folders = []
        self.fulldelete = []
        atexit.register(self.__exit_callback)
        self.error = 1          # Default behavior upon exit is to assume an error and clean up files.

    def __exit_callback(self):
        try:
            # print "======Exiting========"
            # print "\nWe added these folders:"
            # pprint(self.folders)
            # print "\nWe added these folders:"
            # pprint(self.files)
            if self.error == 0:
                # print "Exiting normally."
                pass
            else:
                print ""
                print "Exiting with error:", self.error
                print "Deleting all files and folders that we can."
                self.files.sort(key=len, reverse=True)
                self.folders.sort(key=len, reverse=True)
                for path in self.files:
                    try:
                        os.remove(path)
                    except Exception as e:
                        print e
                        # pass
                for path in self.folders:
                    try:
                        os.rmdir(path)
                    except Exception as e:
                        print e
                        # pass
                for path in self.fulldelete:
                    try:
                        rmtree(path)
                    except Exception as e:
                        pass
                    try:
                        os.remove(path)
                    except Exception as e:
                        pass

        except Exception as e:
            print "Fatal exception during exit callback:", e

    def exit(self, error):
        """This should be called to exit, rather than the Python-included function exit().  If Python's exit() is called, we will assume an error HAS occurred, and delete our files and folders."""
        self.error = error
        exit(error)

    def addFullDelete(self, path):
        """Ugly little bit of design: add a path that you want to fully delete.  This is useful for cleaning up files & folders created by code we call, but cannot fully control."""
        self.fulldelete.append(str(path))

    def __pathExists(self, path):
        """Check if the given path already exists."""
        return os.access(str(path), os.F_OK)

    def addFolder(self, path):
        """Make an empty folder from a Path() class instance."""
        try:
            # Move up from the root through the end of the path, adding folders as needed.
            for subpath in path.subpaths():
                if not self.__pathExists(subpath):
                    os.mkdir(subpath)
                    if subpath not in self.folders:
                        self.folders.append(subpath)
                    print "Added folder:\t" + subpath

        except Exception as e:
            print "addFolder exception!"
            self.exit(e)

    def addFile(self, path, contents = ""):
        """Make a file from a Path() class instance, and optionally write some binary data to that file."""
        try:
            # To be SUPER careful, we panic and quit if the file already exists (we'll take this as a sign that a project already exists, and we'd like to avoid writing over anything.)
            if self.__pathExists(path):
                self.exit("File already exists: " + str(path))
            # Add folders if necessary
            self.addFolder( path.onlyFolders() )

            # Then add the file
            with open(str(path), "wb") as newfile:
                newfile.write(contents)

            # Then add the file
            self.files.append(str(path))
            print "  Added file:\t" + str(path)

        except Exception as e:
            print "addFile exception!"
            self.exit(e)
