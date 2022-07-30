import pysam as py
import sys
bf = py.AlignmentFile(sys.argv[1], 'rb')
result = py.AlignmentFile(sys.argv[2], "wb", template=bf)
chrom = sys.argv[3]
df=py.IndexedReads(bf, multiple_iterators=True)
df.build()
tmp_dict={}
pos_list=[]

def CB(read):
    for i in read.tags:
        if i[0]=="CB" or i[0]=="CR":
            cb=i[1][0:20]
    return cb
def UB(read):
#    ub=""
    for i in read.tags:
        if i[0]=="UR" or i[0]=="UB":
            ub=i[1]
    return ub

def duplicate(dictA):
    dictp = {}
    list1=[]
    klist = list(dictA.keys())
    for i in range(len(klist)):
        j=1
        while i+j <= (len(klist)-1):
            if dictA[klist[i]][1]==dictA[klist[i+j]][1]:
                if dictA[klist[i]][2] < dictA[klist[i + j]][2]:
                    dictp[klist[i]] = [dictA[klist[i]][0],dictA[klist[i]][1],dictA[klist[i]][2]]
                    # print(dictA[klist[i]][0],klist[i])
                else:
                    dictp[klist[i + j]] = [dictA[klist[i + j]][0],dictA[klist[i + j]][1],dictA[klist[i + j]][2]]
            j+=1
    return dictp

def qual(read):
    total=0
    for i in read.query_qualities:
        total+=i
    return total
l = bf.count(chrom)-1
bf = py.AlignmentFile(sys.argv[1], 'rb')
for index,r in enumerate(bf.fetch(chrom)):
    r.set_tag("PG","MarkDuplicates")
    name = r.query_name
#First read
    if len(pos_list) == 0 and index != l:
        pos_list.append(r.reference_start)
#        sequence=r.query_sequence+CB(r)+UB(r)
        sequence=CB(r)+UB(r)
        qualtity=qual(r)
        tmp_dict.setdefault(name,[]).append(r.reference_start)
        tmp_dict.setdefault(name,[]).append(sequence)
        tmp_dict.setdefault(name,[]).append(int(qualtity))
#only one read
    elif len(pos_list) == 0 and index == l:
        result.write(r)
#non first read and non only one reads
    else:
        pastpos=pos_list[len(pos_list)-1]
        if r.reference_start == pastpos and index != l:
            pos_list.append(r.reference_start)
#            sequence=r.query_sequence+CB(r)+UB(r)
            sequence=CB(r)+UB(r)
            qualtity=qual(r)
            tmp_dict.setdefault(name,[]).append(r.reference_start)
            tmp_dict.setdefault(name,[]).append(sequence)
            tmp_dict.setdefault(name,[]).append(int(qualtity))
        elif r.reference_start == pastpos and index == l:
            pos_list.append(r.reference_start)
            #            sequence=r.query_sequence+CB(r)+UB(r)
            sequence = CB(r) + UB(r)
            qualtity = qual(r)
            tmp_dict.setdefault(name, []).append(r.reference_start)
            tmp_dict.setdefault(name, []).append(sequence)
            tmp_dict.setdefault(name, []).append(int(qualtity))
            dictdup = duplicate(tmp_dict)
            for ak in tmp_dict:
                if ak not in dictdup.keys():
                    sr = a = df.find(ak)
                    for uniread in sr:
                        uniread.set_tag("PG", "MarkDuplicates")
                        result.write(uniread)
                else:
                    sr = a = df.find(ak)
                    for dupread in sr:
                        dupread.flag = dupread.flag + 1024
                        dupread.set_tag("PG", "MarkDuplicates")
                        result.write(dupread)
        elif r.reference_start > pastpos and index != l:
            dictdup=duplicate(tmp_dict)
            for ak in tmp_dict:
                if ak not in dictdup.keys():
                    sr=a=df.find(ak)
                    for uniread in sr:
                        uniread.set_tag("PG", "MarkDuplicates")
                        result.write(uniread)
                else:
                    sr=a=df.find(ak)
                    for dupread in sr:
                        dupread.flag=dupread.flag+1024
                        dupread.set_tag("PG", "MarkDuplicates")
                        result.write(dupread)
            pos_list=[]
            tmp_dict={}
            pos_list.append(r.reference_start)
#            sequence=r.query_sequence+CB(r)+UB(r)
            sequence=CB(r)+UB(r)
            qualtity=qual(r)
            tmp_dict.setdefault(name,[]).append(r.reference_start)
            tmp_dict.setdefault(name,[]).append(sequence)
            tmp_dict.setdefault(name,[]).append(int(qualtity))
        elif r.reference_start > pastpos and index == l:
            dictdup = duplicate(tmp_dict)
            for ak in tmp_dict:
                if ak not in dictdup.keys():
                    sr = a = df.find(ak)
                    for uniread in sr:
                        uniread.set_tag("PG", "MarkDuplicates")
                        result.write(uniread)
                else:
                    sr = a = df.find(ak)
                    for dupread in sr:
                        dupread.flag = dupread.flag + 1024
                        dupread.set_tag("PG", "MarkDuplicates")
                        result.write(dupread)
            result.write(r)
            
result.close()
bf.close()
#df.close()
