
import os
import shutil
import inspect

import urllib.request

def download(matpower_version='7.1', destination=None, force=False, rename=True):
    if destination is None:
        matpower_dir = os.path.dirname(os.path.abspath(inspect.getfile(download)))
        print(f"MATPOWER will be downloaded in {matpower_dir}.")
        print("Use downloader.delete_default_download() to remove MATPOWER (pip uninstall will not remove it).")
    else:
        matpower_dir = destination

    file_name = os.path.join(matpower_dir, "matpower.zip")
    
    if os.path.exists(file_name):
        print("matpower.zip already exist in destionation.")
        if force is True:
            print("Force is True, delete old zip file.")
            shutil.rmtree(file_name)
        else:
            print("Force is False, cancel download. Set force=True to force download.")
            return
    
    matpower_url = "https://github.com/MATPOWER/matpower/archive/refs/tags/" + matpower_version + ".zip"

    print("Downloading MATPOWER...")
    print(matpower_url)
    urllib.request.urlretrieve(matpower_url, file_name) # source, dest

    shutil.unpack_archive(file_name, matpower_dir, 'zip')
    
    os.remove(file_name) # remove zipfile
    
    default_matpower_dir = os.path.join(matpower_dir,'matpower-' + matpower_version)
    if rename:
        renamed_name = os.path.join(matpower_dir,'matpower')
        if os.path.exists(renamed_name):
            print("Matpower folder already exist in path")
            if force is True:
                print("Force is True, delete old folder.")
                shutil.rmtree(renamed_name)
            else:
                print("Force is False, cancel rename. Set force=True to force rename.")
                return

        os.rename(default_matpower_dir, renamed_name)
        print(f"matpower saved on {renamed_name}")
    else:
        print(f"matpower saved on {default_matpower_dir}")

def delete_default_download(matpower_dir=None):
    if matpower_dir is None:
        matpower_dir_ = os.path.dirname(os.path.abspath(inspect.getfile(download)))
        matpower_dir = os.path.join(matpower_dir_, 'matpower')
    shutil.rmtree(matpower_dir)