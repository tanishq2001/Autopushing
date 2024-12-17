# -*- coding: utf-8 -*-
"""
Created on Mon May 20 13:23:41 2024

@author: tanishq.agarwal
"""

# Note this script is only work if the repo is already cloned in desired mounted File Share
# Note this script is only work if PAT token is provided currently workable till 19 May 2025

import os  
import shutil  
# os.environ["GIT_PYTHON_REFRESH"] = "quiet"
# import git
from git import Repo
# from PipelineTrigger import *
from Handler.config_automation import ado_pat 
from Handler.Utils import Utils
from Handler.Logger import *
from constants import *

def initialize_git_repo(repo_path, jobid, logger):  
    """Initialize a Git repository if it does not exist."""  
    Utils.log("Checking if the Git repository is initialized.", jobid=jobid, level=logging.INFO, write_logs=True, logger=logger)  
    if not os.path.isdir(os.path.join(repo_path, '.git')):  
        Utils.log("Initializing a new Git repository.", jobid=jobid, level=logging.INFO, write_logs=True, logger=logger)  
        try:  
            repo = Repo.init(repo_path)  
            Utils.log("Git repository successfully initialized.", jobid=jobid, level=logging.INFO, write_logs=True, logger=logger)  
        except Exception as e:  
            Utils.log(f"An error occurred while initializing Git repository: {e}", jobid=jobid, level=logging.ERROR, write_logs=True, logger=logger)  
            print(f"An error occurred while initializing Git repository: {e}")  
            raise Exception(e)  
    else:  
        Utils.log("Git repository already initialized.", jobid=jobid, level=logging.INFO, write_logs=True, logger=logger)  
        repo = Repo(repo_path)  
    return repo  
# Pulls the latest changes from the remote Git repository to avoid conflicts.  
def pull_changes(repo, jobid, logger):  
    try:  
        Utils.log(f"Pulling start", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
        origin = repo.remote(name='origin')  
        origin.pull()  
        Utils.log(f"Pull successful", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
        print("Pull successful.")  
    except Exception as e:  
        Utils.log(f"An error occurred while pulling changes: {e}", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
        print(f"An error occurred while pulling changes: {e}")
        raise Exception(e)

# Stages changes by removing an old folder matching source_type and adding new files to the Git repository.  
def stage_changes(repo, repo_path, subfolder_in_repo, source_type, folder_to_push,jobid, logger):  
    """Stage the deletion of the old folder matching source_type and add new files to the repository."""  
    Utils.log(f"Stage the deletion of the old folder matching source_type and add new files to the repository.", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
       
    try: 
        folder_to_push_path = f"/mnt/semanticstructured/{folder_to_push}"  
        folder_to_delete = f"BackupTo{source_type}{DeltaMovement.remove_folder}" # uncomment for only removing particular data type 
        structured_path = os.path.join(repo_path, subfolder_in_repo)  
        # Find and remove the old folder that starts with source_type  
        for item in os.listdir(structured_path):  
            if item.startswith(folder_to_delete) and os.path.isdir(os.path.join(structured_path, item)):  
                old_folder_path = os.path.join(structured_path, item)  
                repo.git.rm('-r', '-f', os.path.relpath(old_folder_path, repo.working_tree_dir))
                Utils.log(f"The existing folder '{old_folder_path}' has been removed from the repository.", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
                print(f"The existing folder '{old_folder_path}' has been removed from the repository.")  
  
      
  
        destination_path = os.path.join(structured_path, f"{folder_to_push}")  
        # if not os.path.exists(destination_path):
        #     os.mkdir(destination_path)
        # Copy the new folder to the repository  
        shutil.copytree(folder_to_push_path, destination_path)  
        Utils.log(f"The folder '{destination_path}' has been copied to the repository.", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
        print(f"The folder '{destination_path}' has been copied to the repository.")  
  
        # Stage the new folder for addition  
        repo.index.add([os.path.relpath(destination_path, repo.working_tree_dir)])  
        for root, dirs, files in os.walk(destination_path):  
            for file in files:  
                file_path = os.path.relpath(os.path.join(root, file), repo.working_tree_dir)  
                print(file_path)  
                repo.index.add([file_path])  
        Utils.log("Stagging Complete", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
    except Exception as e:  
        Utils.log(f"An error occurred during staging changes: {e}", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
        print(f"An error occurred during staging changes: {e}")
        raise Exception(e)


# Commits the staged changes with a specific message to the Git repository.  
def commit_changes(repo, subfolder_in_repo, folder_to_push, jobid, logger):  
    """Commit the staged changes to the repository."""  
    Utils.log("Commit the staged changes to the repository.", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
    try:  
        commit_message = f"Replace contents of '{subfolder_in_repo}/{folder_to_push}'"  
        repo.index.commit(commit_message)  
        Utils.log("Changes have been committed.", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
        print("Changes have been committed.")  
    except Exception as e:  
        Utils.log(f"An error occurred during commit: {e}", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
        print(f"An error occurred during commit: {e}")  
        raise Exception(e)

# Pushes the committed changes to the remote Git repository.  
def push_changes(repo, jobid, logger):  
    Utils.log("Push the committed changes to the remote repository.", jobid=jobid, level=logging.INFO, write_logs=True, logger=logger)  
    """Push the committed changes to the remote repository."""  
    try:  
        origin = repo.remote(name='origin')  
        origin.push()  
        Utils.log("Push successful.", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
        print("Push successful.")  
    except Exception as e:  
        Utils.log(f"An error occurred while pushing changes: {e}", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
        print(f"An error occurred while pushing changes: {e}") 
        raise Exception(e)   

# Disables the post-commit hook in a Git repository if it exists. 
def disable_post_commit_hook(repo_path, jobid, logger):  
    """Disable the post-commit hook if it exists.""" 
    Utils.log("Disable the post-commit hook if it exists.", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
    try:  
        post_commit_hook_path = os.path.join(repo_path, '.git', 'hooks', 'post-commit')  
        post_commit_hook_disabled_path = post_commit_hook_path + '.disabled'  
        
        if os.path.exists(post_commit_hook_disabled_path):  
            os.remove(post_commit_hook_disabled_path)  
            Utils.log("Existing disabled post-commit hook removed.", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
            print("Existing disabled post-commit hook removed.")  
          
        if os.path.exists(post_commit_hook_path):  
            os.rename(post_commit_hook_path, post_commit_hook_disabled_path)  
            Utils.log("The post-commit hook has been temporarily disabled.", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
            print("The post-commit hook has been temporarily disabled.")  
    except Exception as e:
        Utils.log(f"An error occurred while disabling post-commit hook: {e}", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
        print(f"An error occurred while disabling post-commit hook: {e}")  


# Creates a script for non-interactive authentication using ASKPASS in Git.  
def create_askpass_script(repo_path, ado_pat, jobid, logger):  
    """Create an ASKPASS script for non-interactive authentication."""  
    Utils.log("Create an ASKPASS script for non-interactive authentication.", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
    askpass_script_path = os.path.join(repo_path, 'git-askpass-helper.sh')  
    try:  
        with open(askpass_script_path, 'w') as script:  
            script.write("#!/bin/sh\n")  
            script.write(f"echo {ado_pat}\n")  
        os.chmod(askpass_script_path, 0o700)  
        return askpass_script_path  
    except Exception as e:  
        Utils.log(f"An error occurred while creating ASKPASS script: {e}", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
        print(f"An error occurred while creating ASKPASS script: {e}")  
        raise Exception(e)

# Main function that orchestrates the Git operations for updating the repository.
def main(repository_name, folder_to_push, ado_pat, source_type, jobid, logger):
    Utils.log(f"Main function to execute the Git operations", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
      
    """Main function to execute the Git operations."""  
    
    repo_folder_path = "/mnt/semanticstructured/File_movement/automation/"  
    repo_path = os.path.join(repo_folder_path, repository_name)  
    subfolder_in_repo = 'Structured'  
   
    try:  
        repo = Repo(repo_path) 
        repo = initialize_git_repo(repo_path, jobid, logger)  
        Utils.log(f"working1", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
    
        repo.git.lfs('install')  
        Utils.log(f"working2", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
    
        repo.git.lfs('track', '*.pkl')  
        Utils.log(f"working3", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
    
        repo.index.add(['.gitattributes'])  
        
        Utils.log(f"working4", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)
    
        askpass_script_path = create_askpass_script(repo_path, ado_pat, jobid, logger)  
        os.environ['GIT_ASKPASS'] = askpass_script_path  
        os.environ['GIT_TERMINAL_PROMPT'] = '0'  

        # pull_changes(repo, jobid, logger)  
        stage_changes(repo, repo_path, subfolder_in_repo, source_type, folder_to_push, jobid, logger)
        commit_changes(repo, subfolder_in_repo, folder_to_push, jobid, logger)  
        disable_post_commit_hook(repo_path, jobid, logger)
        push_changes(repo, jobid, logger)  
          
        # os.remove(askpass_script_path)  
        # del os.environ['GIT_ASKPASS']  
        # del os.environ['GIT_TERMINAL_PROMPT'] 
        return True 
          
    except Exception as e:
        Utils.log(f"An error occurred: {e}", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)  
        print(f"An error occurred: {e}") 
        return False 
    

def delta_pipeline(repository_name, folder_to_push, source_type, build_def_id, branch_name, release_def_id, collection_name_for_whole, stage_build_def_id, jobid, logger):
    main(repository_name, folder_to_push, ado_pat, source_type,  jobid, logger)
    
        # Utils.log(f"trigger_pipeline_called", jobid=jobid, level = logging.INFO, write_logs = True, logger=logger)  
        # try:
        #     if not trigger_pipeline(build_def_id, branch_name, release_def_id,source_type, collection_name_for_whole, folder_to_push, jobid, logger):
        #         sendNotification(f"Delta Movement to devtest successfully completed for {source_type}", emailBodyForFinish(source_type, jobid, FolderName= read_pickle_path))
        #         try:
        #             stage_build_trigger(stage_build_def_id, branch_name, jobid, logger) # After this test, put it below trigger pipeline
        #         except:
        #             Utils.log(f"Error in stage build", jobid=jobid, level = logging.ERROR, write_logs = True, logger=logger)  
        #     else:
        #         sendNotification(f"Delta Movement to devtest failed completed for {source_type}", emailBodyForError(source_type, jobid, logMessage={"error": f"Error in Devtest Build/Load/Release for {source_type}"}))
        # except:
        #     Utils.log(f"Error in devtest build", jobid=jobid, level = logging.ERROR, write_logs = True, logger=logger)  
        # # Utils.log(f"Try catch block working fine", jobid=jobid, level = logging.ERROR, write_logs = True, logger=logger)  
        
