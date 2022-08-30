import warnings
warnings.filterwarnings('ignore')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


import time
import subprocess




class gitCommands():
    '''
    Collection of git command
    ----------

    Returns
    -------

    '''
    def __init__(self, repo_dir = None,repo_name = None,git_email= None, git_username = None, git_token = None, commit_message = None, file_name = None):
        self.repo_dir = repo_dir
        self.repo_name = repo_name
        self.email = git_email
        self.username = git_username
        self.token = git_token
        self.commit_message  = commit_message
        self.file_name  = file_name

#         self.final_set,self.labels = self.build_data()
    def gitSetup(self):
        repoDir= os.getcwd() # your git repository , windows your need to use double backslash for right directory.
        path, Repo = os.path.split(os.getcwd()) # repo name
        cmd = 'git config --global user.email '+ self.email

        pipe = subprocess.Popen(cmd, shell=True, cwd=self.repo_dir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
        (out, error) = pipe.communicate()
        print (out,error)

        cmd = 'git config --global user.name '+ self.username
        pipe = subprocess.Popen(cmd, shell=True, cwd=self.repo_dir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
        (out, error) = pipe.communicate()
        print (out,error)
        return 
        
    def gitAdd(self):
        cmd = 'git add ' + self.file_name
        pipe = subprocess.Popen(cmd, shell=True, cwd=self.repo_dir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
        (out, error) = pipe.communicate()
        print (out,error)
        pipe.wait()
        return 

    def gitCommit(self):
        cmd = 'git commit -am "%s"'%self.commit_message
        pipe = subprocess.Popen(cmd, shell=True, cwd=self.repo_dir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
        (out, error) = pipe.communicate()
        print (out,error)
        pipe.wait()
        return 
    def gitPush(self):
        #
        self.gitSetup()
        self.gitPull()
        self.gitAdd()
        self.gitCommit()
        cmd = 'git push https://'+self.token+'@github.com/'+self.username+'/'+self.repo_name+'.git'

        pipe = subprocess.Popen(cmd, shell=True, cwd=self.repo_dir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
        print("passed!")
        (out, error) = pipe.communicate()
        print("passed!")
        print (out, error)
        pipe.wait()
        return 
    def gitPull(self):
        # cmd = 'git push '
        self.gitSetup()
        cmd = 'git pull '

        pipe = subprocess.Popen(cmd, shell=True, cwd=self.repo_dir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
        (out, error) = pipe.communicate()
        print (out, error)
        pipe.wait()
        return 
    