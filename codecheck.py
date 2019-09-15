import os
import xlsxwriter
import subprocess
import signal

class RunTimeError(Exception):
    pass


def runfile(cmd,tc,time,ansout):

    try:
        #print(cmd)
        infi = open(tc,'r')
        outf = open(ansout, 'w')
       
        rx=subprocess.call(cmd,stdin=infi,stdout=outf,stderr=subprocess.PIPE, shell=True,timeout=time)

        infi.close()
        outf.close()

        if rx==-1 :
            raise RunTimeError

        return 1,1

    except subprocess.TimeoutExpired:
        print("TLE")
        return -1,-1

    except RunTimeError:
        print("Runtime Error")
        return -2,-2


def compiling(cmd):
    cfile=subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cfile.communicate()
    print("Compiling "+cmd)
    return cfile.stdout,cfile.stderr



projectPath=os.getcwd()

#path 설정
Anspath=projectPath+'/AnsFile'
Ansexec=Anspath+'/Ansexec'
Ansout=Anspath+'/Ansout'

TCpath=projectPath+'/TC'

Codepath=projectPath+'/Codes'
CodeExpath=Codepath+'/CodeEx'
Codeout=Codepath+'/Codeout'

Ansfile=""
Alist=list()

stulist=list()

workbook = xlsxwriter.Workbook('cell.xlsx')
worksheet = workbook.add_worksheet()
row,col=(0,0)

for i in range(1,21):
    worksheet.write(0,i,'TC_'+str(i))

row=0
col=0

#Compiling
#Ans Compile(must only one file) and run
for (path,dir,files) in os.walk(Anspath):
    for filename in files:
        ext= os.path.splitext(filename)[-1]
        onlyfn = os.path.splitext(filename)[-2]
        if ext=='.cpp':
            Ansfile=Ansexec+'/'+onlyfn
            command = "g++ -std=gnu++14 -o "+Ansfile+' '+Anspath+'/'+filename
            compiling(command)
            print("cmd : "+command)

            command = Ansexec+'/./'+onlyfn

            for (tpath,tdir,tfiles) in os.walk(TCpath):
                for tcname in tfiles:
                    tcext=os.path.splitext(tcname)
                    if tcext[-1] == '.txt':
                        Ansoutfile=Ansout + '/'+tcext[-2]+'out.txt'
                        Alist.append(Ansoutfile)
                        Aouts, Aerr = runfile(command,TCpath+'/'+tcname,5,Ansoutfile)

#Checked Code Compile

for (path,dir, files) in os.walk(Codepath):
    files.sort()
    for filename in files:
        ext = os.path.splitext(filename)
        if ext[-1]=='.cpp':
            saveExe=CodeExpath+'/'+ext[-2]
            command= "g++ -std=gnu++14 -o "+saveExe+' '+Codepath+'/'+filename
            stulist.append(ext[-2])
            compiling(command)
            print(filename+" Compile complete")

            newfolder=Codeout + '/'+ext[-2]

            worksheet.write(row,0,ext[-2])
            row+=1
            col=0

            if not os.path.isdir(newfolder):
                os.mkdir(newfolder)

            command=CodeExpath+'/./'+ext[-2]

            for (tpath,tdir,tfiles) in os.walk(TCpath):
                tfiles.sort()
                for tcname in tfiles:
                    col+=1
                    tcext=os.path.splitext(tcname)
                    if tcext[-1] == '.txt':
                        outfile=Codeout + '/'+ext[-2]+'/'+tcext[-2]+'out.txt'
                        outs,err = runfile(command,TCpath+'/'+tcname,2,outfile)

                        if outs==-1 and err==-1 :
                            worksheet.write(row,col,'TLE')
                            continue

                        if outs==-2 and err == -2:
                            worksheet.write(row,col,'RTE')
                            continue

                        Ansfiledir=Ansout+'/'+tcext[-2]+'out.txt'
                        fa=open(Ansfiledir,'r')
                        anslist=fa.read().split()
                        fa.close()

                        fc=open(outfile,'r')
                        codelist=fc.read().split()
                        fc.close()

                        if len(anslist) != len(codelist) :
                            worksheet.write(row,col,'too many')
                            continue
                        
                        right=True
                        for i in range(0,len(anslist)):
                            if anslist[i] != codelist[i]:
                                right=False
                                break
                        
                        if right :
                            worksheet.write(row,col,'O')
                        else :
                            worksheet.write(row,col,'X')

workbook.close()

