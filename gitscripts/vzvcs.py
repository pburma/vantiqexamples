import git
import os 
import subprocess
import shutil, errno
import datetime

g = git.cmd.Git(os. getcwd())
project = "VZMain"

def pull():
    print("\nPulls changes from the current folder if *.git is initialized.")
    msg = g.pull()
    print(msg)

def vantiqexport():
    #Full namespace meta and data export
    print("Run full metadata and data export from Vantiq CLI")
    p1 = subprocess.Popen(["D:/vantiq/vantiq-1.31.17/bin/vantiq.bat", "-s", "internal_vz_cloud_admin", "export", "-d", "D:/vantiq/repos/vz_cloud_admin"])
    p1.wait()

    print("Complete full metadata export, starting data export")
    p2 = subprocess.Popen(["D:/vantiq/vantiq-1.31.17/bin/vantiq.bat", "-s", "internal_vz_cloud_admin", "export", "data", "-d", "D:/vantiq/repos/vz_cloud_admin"])
    p2.wait()
    print("Complete data export, job finished")

    #Project only data and metadata export
    print("Run metadata and data export from Vantiq CLI for project")   
    p3 = subprocess.Popen(["D:/vantiq/vantiq-1.31.17/bin/vantiq.bat", "-s", "internal_vz_cloud_admin", "export", "project", project, "-d", "D:/vantiq/repos/vz_git/VerizonSOW/VZMain"])
    p3.wait()

    print("Complete project export, starting projectdata export")
    p4 = subprocess.Popen(["D:/vantiq/vantiq-1.31.17/bin/vantiq.bat", "-s", "internal_vz_cloud_admin", "export", "projectdata", project, "-d", "D:/vantiq/repos/vz_git/VerizonSOW/VZMain"])
    p4.wait()
    print("Complete projectdata export, job finished")    

def commit():
    print("Perform git add and then commit")
    g.add("*")
    #message = input("\nType in your commit message: ")
    #commit_message = f'{message}'
    today = datetime.datetime.now()
    commit_message = "Daily backup and sync" + today.strftime('%m-%d-%Y')
    g.commit("-m", commit_message)

def push():
    print("Perform git push to origin using master branch")
    g.push()

def copy():
    print("Copy missing deployment folders from full backup to project backup")
    try:
        shutil.copytree("D:/vantiq/repos/vz_cloud_admin/deployconfigs", "D:/vantiq/repos/vz_git/VerizonSOW/VZMain/deployconfigs", dirs_exist_ok=True)
        shutil.copytree("D:/vantiq/repos/vz_cloud_admin/environments", "D:/vantiq/repos/vz_git/VerizonSOW/VZMain/environments", dirs_exist_ok=True)
        shutil.copytree("D:/vantiq/repos/vz_cloud_admin/documents", "D:/vantiq/repos/vz_git/VerizonSOW/VZMain/documents", dirs_exist_ok=True)
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy("D:/vantiq/repos/vz_cloud_admin/deployconfigs", "D:/vantiq/repos/vz_git/VerizonSOW/VZMain/deployconfigs", dirs_exist_ok=True)
            shutil.copy("D:/vantiq/repos/vz_cloud_admin/environments", "D:/vantiq/repos/vz_git/VerizonSOW/VZMain/environments", dirs_exist_ok=True)
            shutil.copy("D:/vantiq/repos/vz_cloud_admin/documents", "D:/vantiq/repos/vz_git/VerizonSOW/VZMain/documents", dirs_exist_ok=True)
        else: raise    

def fullsync():
    print("Perform full sync, project export, git push, git pull") 
    pull()
    vantiqexport()
    copy()
    commit()
    push()    

def main():
    choices = 'fullsync, pull, vantiqexport, copy, push, commit'
    print("Commands to use: " + choices)

    choose_command = input("Type in the command you want to use: ")
    choose_command = choose_command.lower()

    if choose_command == "pull":
        pull()
    
    elif choose_command == "vantiqexport":
        vantiqexport()
    
    elif choose_command == "commit":
        commit()

    elif choose_command == "push":
        push()        

    elif choose_command == "fullsync":
        fullsync()

    elif choose_command == "copy":
        copy()        

    else:
        print("\nNot a valid command!")
        print("\nUse " + choices)

main()
