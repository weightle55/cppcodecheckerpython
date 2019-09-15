import os

projectPath=os.getcwd()
print(projectPath)

#path 설정
Anspath=projectPath+'/AnsFile'
Ansexec=Anspath+'/Ansexec'
Ansout=Anspath+'/Ansout'

TCpath=projectPath+'/TC'

Codepath=projectPath+'/Codes'
CodeExpath=Codepath+'/CodeEx'
Codeout=Codepath+'/Codeout'

if not os.path.isdir(Anspath):
    os.mkdir(Anspath)

if not os.path.isdir(Ansexec):
    os.mkdir(Ansexec)

if not os.path.isdir(Ansout):
    os.mkdir(Ansout)

if not os.path.isdir(TCpath):
    os.mkdir(TCpath)

if not os.path.isdir(Codepath):
    os.mkdir(Codepath)

if not os.path.isdir(CodeExpath):
    os.mkdir(CodeExpath)

if not os.path.isdir(Codeout):
    os.mkdir(Codeout)

