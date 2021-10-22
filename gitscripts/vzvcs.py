import git
import os 
import subprocess

g = git.cmd.Git(os. getcwd())

def pull():
    print("\nPulls changes from the current folder if *.git is initialized.")
    msg = g.pull()
    print(msg)

def vantiqexport():
    print("Run metadata and data export from Vantiq CLI for project")
    p1 = subprocess.Popen(["D:/vantiq/vantiq-1.31.17/bin/vantiq.bat", "-s", "internal_vz_cloud_admin", "export", "project", "VZMain", "-d", "D:/vantiq/repos/vz_cloud_admin"])
    p1.wait()
    print("Complete project export, starting projectdata export")
    p2 = subprocess.Popen(["D:/vantiq/vantiq-1.31.17/bin/vantiq.bat", "-s", "internal_vz_cloud_admin", "export", "projectdata", "VZMain", "-d", "D:/vantiq/repos/vz_cloud_admin"])
    p2.wait()
    print("Complete data export, job finished")
    print("Run full metadata and data export from Vantiq CLI")
    p3 = subprocess.Popen(["D:/vantiq/vantiq-1.31.17/bin/vantiq.bat", "-s", "internal_vz_cloud_admin", "export", "project", "VZMain", "-d", "D:/vantiq/repos/vz_git/VerizonSOW/VZMain"])
    p3.wait()
    print("Complete full metadata export, starting data export")
    p4 = subprocess.Popen(["D:/vantiq/vantiq-1.31.17/bin/vantiq.bat", "-s", "internal_vz_cloud_admin", "export", "projectdata", "VZMain", "-d", "D:/vantiq/repos/vz_git/VerizonSOW/VZMain"])
    p4.wait()
    print("Complete data export, job finished")    

def fullsync():
    print("Perform full sync, project export, git push, git pull") 

def commit():
    print("Perform git add and then commit")
    g.add("*")
    message = input("\nType in your commit message: ")
    commit_message = f'{message}'
    g.commit("-m", commit_message)

def push():
    print("Perform git push to origin using master branch")
    g.push()

def main():
    choices = 'pull, vantiqexport'
    print("Commands to use: " + choices)

    choose_command = input("Type in the command you want to use: ")
    choose_command = choose_command.lower()

    if choose_command == "pull":
        pull()
    
    elif choose_command == "vantiqexport":
        vantiqexport()
    
    elif choose_command == "commit":
        commit()

    elif choose_command == "fullsync":
        fullsync()

    else:
        print("\nNot a valid command!")
        print("\nUse " + choices)

main()