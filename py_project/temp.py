# Student Examination Portal
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
path1='Student.csv'
if os.path.isfile(path1):
    pass
else:
    fob1=open('Student.csv','a',newline='')
    wob1=csv.writer(fob1)
    wob1.writerow(['Student ID','Name','Class Roll No.','Batch ID'])
    fob1.close()


path2='Course.csv'
if os.path.isfile(path2):
    pass
else:
    fob2=open('Course.csv','a',newline='')
    wob2=csv.writer(fob2)
    wob2.writerow(['Course ID','Course Name','Marks Obtained'])
    fob2.close()


path3='Batch.csv'
if os.path.isfile(path3):
    pass
else:
    fob3=open('Batch.csv','a',newline='')
    wob3=csv.writer(fob3)
    wob3.writerow(['Batch ID','Batch Name','Department Name','List of Courses','List of Students'])
    fob3.close()


path4='Department.csv'
if os.path.isfile(path4):
    pass
else:
    fob4=open('Department.csv','a',newline='')
    wob4=csv.writer(fob4)
    wob4.writerow(['Department ID','Department Name','List of batches'])
    fob4.close()
        

def help1(l3d4,l3d3):
    fob1=open('Course.csv','r')
    rob1=csv.reader(fob1)
    int1=0
    l3d7=[]
    for m in range(len(l3d4)):
        for row in rob1:
            for k in range(len(l3d3)):
                if row[0]==l3d3[k]:
                    str2=row[2]
                    str3=''
                    a1d=l3d4[m]
                    lst1=list(str2.partition(a1d))
                    # print(lst1)
                    for l in range(len(lst1[2])):
                        if l==0:
                            pass
                        else:
                            if lst1[2][l].isdigit():
                                str3+=lst1[2][l]
                            else:
                                break
                    int1+=int(str3)
            l3d7.append(int1/len(l3d3))
            int1=0
    fob1.close()
    return (l3d7)



def help2(str2,stuid):
    str3=''
    lst1=list(str2.partition(stuid))
    print(lst1)
    for l in range(len(lst1[2])):
        if l==0:
            pass
        else:
            if lst1[2][l].isdigit():
                str3+=lst1[2][l]
            else:
                break
    return(int(str3))



def student():
    while True:
        print('a.Create a new student')
        print('b.Update student details')
        print('c.Remove a student from the database')
        print('d.Generate report card')
        print('e.Exit')
        ch1=input('Enter your choice:')
        if ch1 in ('a','A'):
            while True:
                l1a1,l1a2,l1a3,l1a4,l1a5=[],[],[],[],[]
                a1=input('Enter Student ID:')
                fob1=open('Student.csv','r')
                rob1=csv.reader(fob1)
                for row in rob1:
                    l1a1.append(row[0])
                fob1.close()
                while True:
                    if a1 in l1a1:
                        print('This student already exists')
                        print('Enter again')
                        a1=input('Enter Student ID:')
                    else:
                        break
                b1=input('Enter name of the Student:')
                c1=input('Enter class roll number:')
                d1=input('Enter Batch ID:')
                fob1=open('Batch.csv','r')
                rob1=csv.reader(fob1)
                for row in rob1:
                    l1a2.append(row)
                fob1.close()
                for i in range(len(l1a2)):
                    l1a3.append(l1a2[i][0])
                while True:
                    if d1 not in l1a3:
                        print('This batch doesn`t exists')
                        print('Note:A student can only be enrolled in an existing batch!')
                        print('Enter again')
                        d1=input('Enter Batch ID:')
                    else:
                        break
                fob1=open('Student.csv','a',newline='')
                wob1=csv.writer(fob1)
                wob1.writerow([a1,b1,c1,d1])
                fob1.close()
                for j in range(len(l1a2)):
                    if l1a2[j][0]==d1:
                        l1a4.append(l1a2[j][3])
                        var1=l1a2[j][4]
                        var1=var1+':'+a1
                        num1=j-1
                        df1=pd.read_csv('Batch.csv')
                        df1.loc[num1,'List of Students']=var1
                        df1.to_csv("Batch.csv", index=False)
                fob1=open('Course.csv','r')
                rob1=csv.reader(fob1)
                for row in rob1:
                    l1a5.append(row)
                fob1.close()
                for k in range(len(l1a5)):
                    for l in range(len(l1a4)):
                        if l1a5[k][0]==l1a4[l]:
                            var2=l1a5[k][2]
                            print('The marks in the course',l1a5[k][0])
                            ask1=int(input('is:'))
                            var2=var2+'-'+a1+':'+str(ask1)
                            df2=pd.read_csv('Course.csv')
                            num2=k-1
                            df2.loc[num2,'Marks Obtained']=var2
                            df2.to_csv('Course.csv',index=False)
                sch1=input('Enter more records?(y/n):')
                if sch1 in ('n','N'):
                    break
        elif ch1 in('b','B'):
            while True:
                l1b1,l1b2=[],[]
                ask1b1=input('Enter the Student ID of the student whose details you want to update:')
                fob1=open('Student.csv','r')
                rob1=csv.reader(fob1)
                for row in rob1:
                    l1b1.append(row)
                fob1.close()
                for i in range(len(l1b1)):
                    l1b2.append(l1b1[i][0])
                while True:
                    if ask1b1 not in l1b2:
                        print('This student doesn`t exist')
                        print('Enter again')
                        ask1b1=input('Enter Student ID:')
                    else:
                        break
                for j in range(len(l1b1)):
                    if l1b1[j][0]==ask1b1:
                        num1=j-1
                        break
                b1b=input('Enter name of the Student:')
                c1b=input('Enter class roll number:')
                df=pd.read_csv('Student.csv')
                df.loc[num1,'Name']=b1b
                df.loc[num1,'Class Roll No.']=c1b
                df.to_csv("Student.csv", index=False)
                sch2=input('Update more records?(y/n)')
                if sch2 in ('n','N'):
                    break
        elif ch1 in ('c','C'):
            while True:
                l1c1,l1c2,l1c3=[],[],[]
                ll=[]
                ask1c1=input('Enter the Student ID of the student whose details you want to delete:')
                fob1=open('Student.csv','r')
                rob1=csv.reader(fob1)
                for row in rob1:
                    if row[0]==ask1c1:
                        str1=row[3]
                        break
                fob1.close()
                fob1=open('Student.csv','r')
                rob1=csv.reader(fob1)
                for row in rob1:
                    ll.append(row)
                fob1.close()
                for a in range(len(ll)):
                    if ll[a][0]==ask1c1:
                        del ll[a]
                fob1=open('Student.csv','w',newline='')
                wob1=csv.writer(fob1)
                wob1.writerows(ll)
                fob1.close()
                fob1=open('Batch.csv','r')
                rob1=csv.reader(fob1)
                for row in rob1:
                    l1c1.append(row)
                fob1.close()
                for i in range(len(l1c1)):
                    if l1c1[i][0]==str1:
                        l1c2.append(l1c1[i][3])
                        str2=l1c1[i][4]
                        lst1=list(str2.partition(':'+ask1c1))
                        if lst1[1]=='':
                            for j in range(len(lst1[0])):
                                if lst1[0][j]==':':
                                    str3=lst1[0][j+1:]
                                    break
                                elif ':' not in lst1[0]:
                                    str3=lst1[0]
                                    break
                        else:
                            str3=lst1[0]+lst1[2]
                        df=pd.read_csv('Batch.csv')
                        df.loc[i-1,'List of Students']=str3
                fob1=open('Course.csv','r')
                rob1=csv.reader(fob1)
                for row in rob1:
                    l1c3.append(row)
                fob1.close()
                for k in range(len(l1c3)):
                    for l in range(len(l1c2)):
                        if l1c3[k][0]==l1c2[l]:
                            str4=l1c3[k][2]
                            lst2=list(str4.partition(ask1c1))
                            if lst2[2][0]==':' and lst2[2][1:].isdigit():
                                str5=lst2[0][:-1]
                            else:
                                for m in range(len(lst2[2])):
                                    if lst2[2][m]=='-':
                                        str5=lst2[0]+lst2[2][m+1:]
                                        break
                            df=pd.read_csv('Course.csv')
                            df.loc[k-1,'Marks Obtained']=str5
                sch3=input('Delete more records?(y/n)')
                if sch3 in ('n','N'):
                    break
        elif ch1 in('d','D'):
            while True:
                l1d1,l1d2,l1d3=[],[],[]
                print('Enter Student ID of the student whose report is to be generated:')
                a1d=input('Student ID:')
                fob1=open('Student.csv','r')
                rob1=csv.reader(fob1)
                for row in rob1:
                    l1d1.append(row)
                    
                fob1.close()
                for i in range(len(l1d1)):
                    l1d2.append(l1d1[i][0])
                while True:
                    if a1d in l1d2:
                        break
                    else:
                        print('This student doesn`t exist')
                        print('Enter again')
                        a1d=input('Student ID:')
                for j in range(len(l1d1)):
                    if l1d1[j][0]==a1d:
                        str1=l1d1[j][3]
                        name=l1d1[j][1]
                        roll=l1d1[j][2]
                        break
                fob1=open('Batch.csv','r')
                rob1=csv.reader(fob1)
                for row in rob1:
                    if row[0]==str1:
                        l1d3.append(row[3])
                fob1.close()
                fob1=open('Course.csv','r')
                rob1=csv.reader(fob1)
                int1=0
                for row in rob1:
                    for k in range(len(l1d3)):
                        if row[0]==l1d3[k]:
                            str2=row[2]
                            str3=''
                            lst1=list(str2.partition(a1d))
                            # print(lst1)
                            for l in range(len(lst1[2])):
                                if l==0:
                                    pass
                                else:
                                    if lst1[2][l].isdigit():
                                        str3+=lst1[2][l]
                                    else:
                                        break
                            int1+=int(str3)
                fob1.close()
                num=int1/len(l1d3)
                stat='PASS'
                if num>=90:
                    grade='A'
                elif num>=80 and num<90:
                    grade='B'
                elif num>=70 and num<80:
                    grade='C'
                elif num>=60 and num<70:
                    grade='D'
                elif num>=40 and num<60:
                    grade='E'
                elif num<40:
                    grade='F'
                    stat='FAIL'
                with open('result.txt','w+') as res:
                    l1d4=['Student ID: '+a1d+'\n','Student Name:'+name+'\n','Student Roll No.:'+str(roll)+'\n','Batch ID:'+str1+'\n','Percentage:'+str(num)+'%\n','Overall Grade:'+grade+'\n','Passing Status:'+stat]
                    res.write('REPORT CARD\n')
                    res.writelines(l1d4)
                res=open('result.txt','r')
                print(res.read())
                res.close()
                sch6=input('Generate more report cards?(y/n):')
                if sch6 in ('n','N'):
                    break
        elif ch1 in('e','E'):
            break
        else:
            print('INVALID INPUT!!')
            print('Enter again')


def course():
    while True:
        print('a.Create a new course')
        print('b.View performance of all students in the course')
        print('c.Show course statistics')
        print('d.Exit')
        ch2=input('Enter your choice:')
        if ch2 in ('a','A'):
            while True:
                l2a1,l2a2,l2a3,l2a4,l2a5,l2a6=[],[],[],[],[],[]
                a2=input('Enter Course ID:')
                fob2=open('Course.csv','r')
                rob2=csv.reader(fob2)
                for row in rob2:
                    l2a5.append(row)
                fob2.close()
                for k in range(len(l2a5)):
                    l2a1.append(l2a5[k][0])
                while True:
                    if a2 in l2a1:
                        break
                    else:
                        print('This course already exists.')
                        print('Enter again')
                        a2=input('Enter Course ID:')
                b2=input('Enter Course Name:')
                c2=input('Enter the Batch ID under which this course will run:')
                fob2=open('Batch.csv','r')
                rob2=csv.reader(fob2)
                for row in rob2:
                    l2a2.append(row)
                fob2.close()
                for i in range(len(l2a2)):
                    l2a3.append(l2a2[i][0])
                while True:
                    if c2 in l2a3:
                        break
                    else:
                        print('This batch doesn`t exist')
                        print('Note:A new course can only be added to an existing batch')
                        print('Enter again')
                        c2=input('Enter Batch ID:')
                for j in range(len(l2a2)):
                    if l2a2[j][0]==c2:
                        l2a4.append(l2a2[j][3])
                for l in range(len(l2a5)):
                    for m in range(len(l2a4)):
                        if l2a5[l][0]==l2a4[m]:
                            str1=l2a5[l][2]
                            str1+='-'
                            lst1=[]
                            var=''
                            for n in range(len(str1)):
                                if str1[n]==':':
                                    lst1.append(var)
                                    var=''
                                    continue
                                if str1[n]=='-':
                                    var=''
                                    continue
                                var+=str1[n]
                                l2a6.extend(lst1)
                l2a6=list(set(l2a6))
                str2,str3='',''
                for o in range(len(l2a6)):
                    print('Enter marks of student with ID:',l2a6[o])
                    d2=input('Enter marks:')
                    str2=str2+l2a6[o]+':'+d2+'-'
                    str3=str3+l2a6[o]+':'
                str2=str2.rstrip('-')
                str3=str3.rstrip(':')
                for p in range(len(l2a2)):
                    if l2a2[p][0]==c2:
                        baname=l2a2[p][1]
                        deptname=l2a2[p][2]
                        break
                with open ('Course.csv','a',newline='') as fob1, open ('Batch.csv','a',newline='') as fob2:
                    wob1=csv.writer(fob1)
                    wob2=csv.writer(fob2)
                    wob1.writerow([a2,b2,str2])
                    wob2.writerow([c2,baname,deptname,a2,str3])
                sch2=input('Enter more Courses?(y/n):')
                if sch2 in ('n','N'):
                    break
        elif ch2 in('b','B'):
            while True:
                a2=input('Enter course ID:')
                with open('Course.csv','r') as fob1, open('Student.csv','r') as fob2 :
                    rob1=csv.reader(fob1)
                    rob2=csv.reader(fob2)
                    for row1 in rob1:
                        if row1[0]==a2:
                            str1=row1[2]
                            break
                    lst1,lst2=[],[]
                    var=''
                    for n in range(len(str1)):
                        if str1[n]==':':
                            lst1.append(var)
                            var=''
                            continue
                        if str1[n]=='-':
                            lst2.append(var)
                            var=''
                            continue
                        var+=str1[n]
                    for row2 in rob2:
                        for i in range(len(lst1)):
                            if row2[0]==lst1[i]:
                                print('Student ID:',lst1[i])
                                print('Student Name:',row2[1])
                                print('Class roll no.:',row2[2])
                                print('Marks obtained:',lst2[i])
                                print()
                                break
                sch3=input('Check more results?(y/n)')
                if sch3 in ('n','N'):
                    break
        # elif ch2 in ('c','C'):
            
            
                                    
                                                                                                            
def batch():
    while True:
        print('a.Create a new batch')
        print('b.View list of all students in a batch')
        print('c.View list of all courses taught in the batch')
        print('d.View complete performance of all students in a batch')
        print('e.Pie chart of percentage of all students')
        print('f.EXIT')
        ch3=input('Enter your choice:')
        if ch3 in ('a','A'):
            while True:
                l3a1,l3a2,l3a3=[],[],[]
                a3=input('Enter Batch ID:')
                fob3=open('Batch.csv','r')
                rob3=csv.reader(fob3)
                for row in rob3:
                    l3a1.append(row[0])
                fob3.close()
                while True:
                    if a3 in l3a1:
                        print('This batch already exists')
                        print('Enter again')
                        a3=input('Enter Batch ID:')
                    else:
                        break
                b3=input('Enter Batch Name:')
                c3=input('Enter Department Name:')
                fob3=open('Department.csv','r')
                rob3=csv.reader(fob3)
                for row in rob3:
                    l3a2.append(row)
                fob3.close()
                for i in range(len(l3a2)):
                    l3a3.append(l3a2[i][1])
                while True:
                    if c3 in l3a3:
                        break
                    else:
                        print('This department doesn`t exist')
                        print('Note:A batch can be created only under an existing department.')
                        c3=input('Enter Batch ID:')
                fob3=open('Batch.csv','a')
                wob3=csv.writer(fob3)
                wob3.writerow([a3,b3,c3,'',''])
                fob3.close()
                for j in range(len(l3a2)):
                    if l3a2[j][1]==c3:
                        str1=l3a2[j][2]
                        str1=str1+':'+a3
                        df=pd.read_csv('Department.csv')
                        df.loc[j-1,'List of batches']=str1
                        df.to_csv("Department.csv", index=False)
                        break
                sch3=input('Enter more records?(y/n):')
                if sch3 in ('n','N'):
                    break
        elif ch3 in('b','B'):
            while True:
                a3=input('Enter the required batch ID:')
                fob3=open('Student.csv','r')
                rob3=csv.reader(fob3)
                for row in rob3:
                    if row[3]==a3:
                        print('Student ID:',row[0])
                        print('Student Name:',row[1])
                        print()
                fob3.close()
                sch3=input('Check more batches?(y/n):')
                if sch3 in ('n','N'):
                    break
        elif ch3 in('c','C'):
            while True:
                a3=input('Enter the required batch ID:')
                fob3=open('Batch.csv','r')
                rob3=csv.reader(fob3)
                print('The courses in this batch are:')
                for row in rob3:
                    if row[0]==a3:
                        print(row[3])
                sch3=input('Check more batches?(y/n):')
                if sch3 in ('n','N'):
                    break
        elif ch3 in ('d','D'):
            while True:
                l3d1,l3d2,l3d3,l3d4,l3d5,l3d6,l3d7=[],[],[],[],[],[],[]
                a3=input('Enter the batch ID whose performance is to be viewed:')
                fob3=open('Batch.csv','r')
                rob3=csv.reader(fob3)
                for row in rob3:
                    l3d1.append(row)
                fob3.close()
                for i in range(len(l3d1)):
                    l3d2.append(l3d1[i][0])
                while True:
                    if a3 in l3d2:
                        break
                    else:
                        print('This batch doesn`t exist')
                        print('Enter again')
                        a3=input('Enter Batch ID:')
                for j in range(len(l3d1)):
                    if l3d1[i][0]==a3:
                        l3d3.append(l3d1[i][3])
                with open('Student.csv','r') as fob3:
                    rob3=csv.reader(fob3)
                    for row in rob3:
                        if row[3]==a3:
                            l3d4.append(row[0])
                            l3d5.append(row[1])
                            l3d6.append(row[2])
                l3d7=help1(l3d4,l3d3)
                for n in range(len(l3d4)):
                    print('Student ID:',l3d4[n])
                    print('Student Name:',l3d5[n])
                    print('Class roll no.:',l3d6[n])
                    print('Percentage:',l3d7[n])
                sch3=input('View any more results?(y/n)')
                if sch3 in('n','N'):
                    break
        elif ch3 in ('e','E'):
            pass
        


def dept():
    while True:
        print('a.Create a new Department')
        print('b.View all batches in a deartment')
        print('c.View average performance of all batches in a departmment')
        print('d.Show department statistics')
        print('e.EXIT')
        ch4=input('Enter your choice:')
        if ch4 in('a','A'):
            while True:
                l4a1=[]
                a4=input('Enter Department ID:')
                fob4=open('Department.csv','r')
                rob4=csv.reader(fob4)
                for row in rob4:
                    l4a1.append(row[0])
                fob4.close()
                while True:
                    if a4 in l4a1:
                        print('This Department already exists')
                        print('Enter again')
                        a4=input('Enter Department ID:')
                    else:
                        break
                b4=input('Enter Department name:')
                fob4=open('Department.csv','a',newline='')
                wob4=csv.writer(fob4)
                wob4.writerow([a4,b4,''])
                fob4.close()
                sch4=input('Enter more records(y/n):')
                if sch4 in('n','N'):
                    break
        elif ch4 in('b''B'):
            a4=input('Enter the department ID:')
            fob4=open('Department.csv','r')
            rob4=csv.reader(fob4)
            str2=''
            for row in rob4:
                if row[0]==a4:
                    str1=row[2]
                    break
            fob4.close()
            print('The batches in this department are:')
            for i in str1:
                if i==':':
                    print(str2)
                    str2=''
                    continue
                str2+=i
        elif ch4 in ('c','C'):
            while True:
                l4b1,l4b2,l4b3,l4b4,l4b5,l4b6,l4b7=[],[],[],[],[],[],[]
                a4=input('Enter Department ID:')
                fob4=open('Department.csv','r')
                rob4=csv.reader(fob4)
                for row in rob4:
                    l4b1.append(row)
                fob4.close()
                for i in range(len(l4b1)):
                    l4b2.append(l4b1[i][0])
                while True:
                    if a4 not in l4b2:
                        print('This Department doesn`t exist')
                        print('Enter again')
                        a4=input('Enter Department ID:')
                    else:
                        break
                for j in range(len(l4b1)):
                    if l4b1[j][0]==a4:
                        str1=l4b1[j][2]
                        break
                str2=''
                for k in str1:
                    if k==':':
                        l4b3.append(str2)
                        str2=''
                        continue
                    str2+=k
                fob4=open('Batch.csv','r')
                rob4=csv.reader(fob4)
                for l in range(len(l4b3)):
                    for row in rob4:
                        if l4b3[l]==row[0]:
                            
                            l4b4.append(row[3])
                    l4b5.append(l4b4)
                    l4b4=[]
                fob4.close()
                fob4=open('Student.csv','r')
                rob4=csv.reader(fob4)
                for m in range(l4b3):
                    for row in rob4:
                        if l4b3[m]==row[3]:
                            l4b6.append(row[0])
                    l4b7.append(l4b6)
                    l4b6=[]
                fob4.close()
                print('Following are the batches in the Department-',a4)
                for n in range(len(l4b3)):
                    var=help1(l4b7[n],l4b5[n])
                    percentage=sum(var)/len(var)
                    print('Batch ID:',l4b3[n])
                    print('Average percentage:',percentage)
                    print()
                sch4=input('Enter any other Department?(y/n)')
                if sch4 in ('n','N'):
                    break
        elif ch4 in ('d','D'):
            pass
        elif ch4 in ('e','E'):
            break
        else:
            print('Invalid Input')
            print('Enter again')

            
def exam():
    while True:
        print('a.View performance of all students in the examination')
        print('b.Show examination statistics:Scatter Plot of all marks obtained')
        print('c.Exit')
        ch5=input('Enter your choice:')
        if ch5 in ('a','A'):
            l5a1=[]
            with open('Student.csv','r') as fob1, open('Course.csv','r') as fob2:
                rob1=csv.reader(fob1)
                rob2=csv.reader(fob2)
                for row1 in rob1:
                    if row1[0]!='Student ID':
                        for row2 in rob2:
                            if row1[0] in row2[2]:
                                print(type(row2[2]))
                                int1=help2(row2[2],row1[0])
                                l5a1.append(int1)
                        print('Student ID:',row1[0])
                        print('Overall Percentage:',sum(l5a1)/len(l5a1))
                        l5a1=[]
                    
        elif ch5 in ('b','B'):
            l5b1,l5b2,l5b3=[],[],[]
            str1=''
            fob5=open('Course.csv','r')
            rob5=csv.reader(fob5)
            for row in rob5:
                if row[2]!='Marks Obtained':
                    l5b1.append(row[0])
                    str2=row[2]
                    str2=str2+'-'
                    for i in range(len(str2)):
                        if str2[i]==':':
                            str1=''
                            continue
                        if str2[i]=='-':
                            l5b2.append(int(str1))
                            str1=''
                            continue
                        str1=str1+str2[i]
                    l5b3.append(l5b2)
                    l5b2=[]
                
            fob5.close()
            colors=['black','gray','silver','aqua','rosybrown','firebrick','red','darksalmon','sienna','sandybrown','bisque' ,'tan','snow','brown','r','lightgray','W','lightcoral','maroon','mistyrose' ,'coral','seashell','peachpuff','darkorange','navajowhite','orange' ,'darkgoldenrod','lemonchiffon', 'Ivory','olive' ,'yellowgreen','lawngreen','lightgreen','dimgray','darkgray','lightgrey','white','indianred','darkred','salmon','orangered','chocolate', 'peru','burlywood','blanchedalmond','wheat' ,'goldenrod','khaki' ,'beige','moccasin' ,'floralwhite','gold' ,'darkkhaki']
            colors=colors[:len(l5b1)]
            for j in range(len(l5b1)):
                num1=sum(l5b3[j])/len(l5b3[j])
                plt.scatter(num1,l5b1[j],c=colors[j])
            plt.show()
        elif ch5 in ('c','C'):
            break
        else:
            print('Invalid Input')
            print('Enter again')
        
        
while True:
    print('1.Student Details')
    print('2.Course Details')
    print('3.Batch Details')
    print('4.Department Details')
    print('5.Examination Details')
    print('6.END')
    ch=int(input('Enter your choice:'))
    if ch==1:
        student()
    elif ch==2:
        course()
    elif ch==3:
        batch()
    elif ch==4:
        dept()
    elif ch==5:
        exam()
    elif ch==6:
        break
    else:
        print('INVALID INPUT!!')
        print('Enter again')