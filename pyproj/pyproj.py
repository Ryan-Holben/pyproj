"""

    This script builds a standard Python project folder for use, and creates a git repository as well.

"""
import sys, os
from savely import Savely, Path
from subprocess import call
import strings

proj_name = "project_name"

def shellCall(command):
    """Runs a shell command (and shows the user what that command was.)"""
    print "shell>", command
    # Parse the command.  Note that command.split() will split up arguments contained in parentheses, so we can't use that.
    paren, i, args = False, 0, []
    command += " "
    for j in range(len(command)):
        if command[j] == " " and paren == False:
            args.append(command[i:j].strip("\""))
            i = j+1
        elif command[j] == "\"":
            paren = not paren
    return call(args)

def main():
    # We only accept calls of the form "python pyproj.py [project_name]"
    if len(sys.argv) != 2:
        print "Usage: python pyproj.py \"project_name\"\n"
        exit(1)

    # Initialize our class that handles safe file/folder saving and cleanup.
    save = Savely()

    # Sanitize the project name.
    proj_name = "_".join(sys.argv[1].split())
    print "\nBuilding project:", proj_name + "\n"

    # Add folders first
    save.addFolder( Path(proj_name) )
    save.addFolder( Path(proj_name, proj_name) )
    save.addFolder( Path(proj_name, "docs") )
    save.addFolder( Path(proj_name, "examples") )
    save.addFolder( Path(proj_name, "tests") )

    # Add files second
    if sys.platform == "darwin":
        save.addFile( Path(proj_name, ".gitignore"), strings.gitignore_mac )
    elif sys.platform == "win32":
        save.addFile( Path(proj_name, ".gitignore"), strings.gitignore_win )
    elif sys.platform.startswith("linux"):
        save.addFile( Path(proj_name, ".gitignore"), strings.gitignore_linux )
    else:
        save.addFile( Path(proj_name, ".gitignore") )

    save.addFile( Path(proj_name, "main.py"), strings.main_py.format(proj_name) )
    save.addFile( Path(proj_name, "LICENSE"), strings.LICENSE )
    save.addFile( Path(proj_name, "readme.md"), strings.readme_md.format(proj_name.title()) )
    save.addFile( Path(proj_name, "requirements.txt"), strings.requirements_txt )
    save.addFile( Path(proj_name, proj_name, "__init__.py"), strings.src_init_py )
    save.addFile( Path(proj_name, "tests", "__init__.py"), strings.tests_init_py )
    save.addFile( Path(proj_name, "examples", "example1.py"), strings.examples_example_py.format(proj_name) )

    # Format of shell command for making system links: "ln -s /path/to/original/ /path/to/link"
    # if sys.platform == "darwin":
    #     shellCall("ln -s {} {}".format( Path(proj_name, proj_name), Path(proj_name, "examples", proj_name)) )

    # In case git fails, we sandblast the .git folder.
    save.addFullDelete( Path(proj_name, ".git") )

    # Lastly, run some git commands
    os.chdir(proj_name)
    shellCall("git init")
    shellCall("git add .")
    shellCall("git commit -m \"First commit\"")

    print "\nProject successfully created!\n"

    print "If you would like to connect your project to an empty GitHub repository, type the following:"
    print "\tcd {}".format(proj_name)
    print "\tgit remote add origin [GitHub URL]"
    print "\tgit push -u origin master\n"
    save.exit(0)

print ""
main()
