#! /usr/bin/env python
import os
from os.path import expanduser
from easysparkcli.subcommands.auxiliar.exceptions import ArgumentValueError
from pathlib import PurePath
import shutil
import glob

#subcommand create -- configure minikube run options
def set_minikube_cpus(cmd, value):
    cmd.extend(['--cpus',str(value)])

def set_minikube_memory(cmd,value):
    cmd.extend(['--memory',str(value)])

def set_minikube_provider(cmd,value):
    cmd.extend(['--driver',value.lower()])

#subcommand submit -- write properties file
def set_master(f, value):
    f.write(f"spark.master".ljust(67) + f"{value}\n")

def deploy_mode(f,value):
    f.write("spark.submit.deployMode".ljust(67) + f"{value}\n")

def set_app_name(file,value):
    file.write("spark.app.name".ljust(67) + f"{value}\n")

def set_container_image(file,value):
    file.write("spark.kubernetes.container.image".ljust(67) + f"{value}\n")

def mount_sharedpaths_into_pods(file):

    file.write("spark.kubernetes.driver.volumes.hostPath.localhost.mount.path".ljust(67) + "/tmp/sharedpath\n")
    file.write("spark.kubernetes.driver.volumes.hostPath.localhost.mount.subpath".ljust(67) + "jars\n")
    file.write("spark.kubernetes.driver.volumes.hostPath.localhost.mount.subpath".ljust(67) + "libs\n")
    file.write("spark.kubernetes.driver.volumes.hostPath.localhost.mount.subpath".ljust(67) + "historylogs\n")
    file.write("spark.kubernetes.driver.volumes.hostPath.localhost.readOnly".ljust(67) + "False\n")
    file.write("spark.kubernetes.driver.volumes.hostPath.localhost.options.path".ljust(67) + "/localsharedfolder\n")
    file.write("spark.kubernetes.driver.volumes.hostPath.localhost.options.type".ljust(67) + "DirectoryOrCreate\n")

    file.write("spark.kubernetes.executor.volumes.hostPath.localhost.mount.path".ljust(67) + "/tmp/sharedpath\n")
    file.write("spark.kubernetes.executor.volumes.hostPath.localhost.mount.subpath".ljust(67) + "jars\n")
    file.write("spark.kubernetes.executor.volumes.hostPath.localhost.mount.subpath".ljust(67) + "libs\n")
    file.write("spark.kubernetes.executor.volumes.hostPath.localhost.mount.subpath".ljust(67) + "historylogs\n")
    file.write("spark.kubernetes.executor.volumes.hostPath.localhost.readOnly".ljust(67) + "False\n")
    file.write("spark.kubernetes.executor.volumes.hostPath.localhost.options.path".ljust(67) + "/localsharedfolder\n")
    file.write("spark.kubernetes.executor.volumes.hostPath.localhost.options.type".ljust(67) + "DirectoryOrCreate\n")

def set_spark_logging(file,cluster_type):
    file.write("spark.eventLog.enabled".ljust(67) + "True\n")
    if cluster_type == 'k8s':
        file.write("spark.eventLog.dir".ljust(67) + "/tmp/sharedpath/historylogs\n")
    elif cluster_type == 'standalone':
        file.write("spark.eventLog.dir".ljust(67) + "/vagrant/historylogs\n")
        file.write("spark.standalone.submit.waitAppCompletion".ljust(67) + "True\n")

def set_executor_memory(file,value):
    file.write("spark.executor.memory".ljust(67) + f"{value}\n")

def set_executor_cores(file,value):
    file.write(f"spark.executor.cores".ljust(67) + f"{value}\n")

def set_driver_memory(file,value):
    file.write(f"spark.driver.memory".ljust(67) + f"{value}\n")

def set_driver_cores(file,value):
    file.write(f"spark.driver.cores".ljust(67) + f"{value}\n")

def set_jars_classpath(file,clustertype,jars_names_list):
    length=len(jars_names_list)
    if length > 0:
        i=0
        added_jars=""
        if clustertype == "standalone":
            sharedpath= "/vagrant/jars/"
        elif clustertype=="k8s":
            sharedpath="/tmp/sharedpath/jars/"
        while i<length:
            if ( i == (length -1)):
                added_jars+= sharedpath + jars_names_list[i]+ "\n"
            else:
                added_jars+= sharedpath + jars_names_list[i] + ":"
            i +=1
        file.write(f"spark.driver.extraClassPath".ljust(67) + added_jars)
        file.write(f"spark.executor.extraClassPath".ljust(67) + added_jars)

def copy_dir_jars(value,file,clustertype):
    dir = PurePath(value)
    if os.path.isdir(dir):
        defaultShared = expanduser("~") #Obtemos path directorio home donde creamos a carpeta a compartir
        defaultJarDir = PurePath(defaultShared) / ".easySparkTool/jars"
        jars_names_list=[]
        with os.scandir(dir) as dirElements:
            for obj in dirElements:
                filename,extension = os.path.splitext(obj)
                if obj.is_file() and extension == ".jar":
                    jars_names_list.append(obj.name)
                    destinationFile = defaultJarDir / obj.name
                    shutil.copy(obj,destinationFile)
                else:
                    print(f"Ignoring object {obj.name} from the specified folder, only files with .jar extension will be used ...\n")
        set_jars_classpath(file,clustertype,jars_names_list)

def copy_specific_jars(value,file,clustertype):
    filesList = value.split(',')
    defaultShared = expanduser("~") #Obtemos path directorio home donde creamos a carpeta a compartir
    defaultJarDir = PurePath(defaultShared) / ".easySparkTool/jars"
    jars_names_list=[]
    for stringjarfile in filesList:
        jarfile = PurePath(stringjarfile)
        if os.path.isfile(jarfile) and jarfile.suffix == ".jar":
            copiedJarPath = defaultJarDir / jarfile.name
            shutil.copy(jarfile,copiedJarPath)
            jars_names_list.append(jarfile.name)
        else:
            print(f"File {jarfile} specified at jars option is not a jar file, ignoring...")
    set_jars_classpath(file,clustertype,jars_names_list)

def copy_dir_libs(value, file,clustertype):
    dir = PurePath(value)
    copiedFiles = 0
    if os.path.isdir(dir):
        defaultShared = expanduser("~") #Obtemos path directorio home donde creamos a carpeta a compartir
        defaultJarDir = PurePath(defaultShared) / ".easySparkTool/libs"
        with os.scandir(dir) as dirElements:
            for obj in dirElements:
                if obj.is_file():
                    destinationFile = defaultJarDir / obj.name
                    shutil.copy(obj,destinationFile)
                    copiedFiles+=1
                else:
                    print(f"Ignoring object {obj.name} from the specified folder, only the files from the first level of the directory will be used ...\n")
    if copiedFiles > 0:
        if clustertype == "standalone":
            file.write("spark.driver.extraLibraryPath".ljust(67) + "/vagrant/libs\n")
            file.write(f"spark.executor.extraLibraryPath".ljust(67) + "/vagrant/libs\n")
        elif clustertype == "k8s":
            file.write("spark.driver.extraLibraryPath".ljust(67) + "/tmp/sharedpath/libs\n")
            file.write(f"spark.executor.extraLibraryPath".ljust(67) + "/tmp/sharedpath/libs\n")

def set_executor_instances(file,value):
    file.write(f"spark.executor.instances       {value}\n")

def set_supervise_value(file,value):
    file.write("spark.driver.supervise".ljust(67) + f"{value}\n")

def copy_historyfile(strDestinationPath):
    defaultShared = expanduser("~") #Obtemos path directorio home donde creamos a carpeta a compartir
    defaultHistoryLogDir = PurePath(defaultShared) / ".easySparkTool/historylogs/*"
    try:
        listOfFiles = glob.glob(str(defaultHistoryLogDir))     
        latestFile=PurePath(max(listOfFiles, key=os.path.getmtime))
        destinationPath = PurePath(strDestinationPath)
        copiedHistoryFilePath = destinationPath / latestFile.name
        shutil.copy(latestFile,copiedHistoryFilePath)
    except:
        print('An error ocurred generating history file at the specified directory path '+ f"{strDestinationPath}")
#def set_extrafiles(file,value):
#    file.write(f"spark.files       {value}\n")

#def set_files_upload_path(file,value):
#    file.write(f"spark.kubernetes.file.upload.path       {value}")


