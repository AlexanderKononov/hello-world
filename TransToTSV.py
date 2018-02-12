import sys

def relayRaceSerch(ch, pos, cna_data, start):
    current=start
    #print(cna_data[current])
    while ch!=cna_data[current][0]:
        if current>=len(cna_data)-1:
            return [-1, current]
        current+=1
    while pos>=cna_data[current][1]:
        if pos<=cna_data[current][2]:
            return [current, current]
        if current>=len(cna_data)-1:
            return [-1, current]
        if cna_data[current][0]!=ch:
            return [-1, current]
        current+=1
    return [-1, current]

class Sep_cell:
	def __init__(self, targ_cell, sep):
		self.targ_cell=targ_cell
		self.sep=sep

#Arguments prossesing
arg=sys.argv
snv_col=[]
cna_col=[]
print(arg)
if len(arg)<5:
    wey_input_SNV=arg[1]
    wey_input_CNA=arg[2]
    print('Let\'s default run...' )
    arg.append('-d')
if '-h' in arg:
    print("help:\n usage: python TransToTSV.py [-h] -snv_f <SNV_data.csv> [column numbers from SNV_data] -cna_f <CNA_data> [column numbers from CNA_data] -d\n\n -d To start by default for HERCULES project data")
if '-d' in arg:
    snv_col=[0,1,36]
    cna_col=[2,3,4,8,9]

else:
    file_1=arg.index('-snv_f')
    file_2=arg.index('-cna_f')
    wey_input_SNV=arg[file_1+1]
    wey_input_CNA=arg[file_2+1]
    '''
    if file_1<file_2:
        coin=file_1+2
        while coin!=file_2:
            if arg[coin]=='sep':
                coin+=3
                snv_col.append(Sep_cell(arg[coin-1], arg[coin-2]))
                continue
            snv_col.append(arg[coin])
            coin+=1
        coin+=2
        while coin<len(arg):
            if arg[coin]=='sep':
                coin+=3
                cna_col.append(Sep_cell(arg[coin-1], arg[coin-2]))
                continue
            cna_col.append(arg[coin])
            coin+=1
    else:
        coin=file_2+2
        while coin!=file_1:
            if arg[coin]=='sep':
                coin+=3
                cna_col.append(Sep_cell(arg[coin-1], arg[coin-2]))
                continue
            cna_col.append(arg[coin])
            coin+=1
        coin+=2
        while coin<len(arg):
            if arg[coin]=='sep':
                coin+=3
                snv_col.append(Sep_cell(arg[coin-1], arg[coin-2]))
                continue
            snv_col.append(arg[coin])
            coin+=1
	'''

#Take the SNV data
SNV_data=[]
SNV_file_read=open(wey_input_SNV, 'r')
first_line=True
for line in SNV_file_read:
    line.strip()
    if first_line:
        first_line=False
        continue
    if line=='':
        break
    pros_line=line.split('\t')
    mut=[]
    for i in snv_col:
    	if i==36:
    		cell=pros_line[i].strip('"').split(',')
    		for j in cell:
    			mut.append(j)
    		continue
    	mut.append(pros_line[i].strip('"'))
    Na=False
    for check in mut:
        if check=='NA':
            Na=True
    if Na:
        continue
    SNV_data.append(mut)
SNV_file_read.close()    
print('------ SNV has been downloaded -----')

#Take the CNA data
CNA_file_read=open(wey_input_CNA, 'r')    
first_line=True
bibliography_dict={}
CNA_dict={}
CNA_data=[]
for line in CNA_file_read:
    line.strip()
    if first_line:
        first_line=False
        continue
    if line=='':
        break
    pline=line.split('\t')
    alt=[]
    for i in cna_col:
        alt.append(pline[i].strip('"'))
    CNA_data.append(alt)
CNA_file_read.close()
print('------ CNA has been downloaded -----')

#CNA and SNV sorting
for i in SNV_data:
    i[0]=i[0].strip('chr').strip('ch').strip('Chr').strip('Ch').replace('X','23').replace('M','25')
    i[0]=int(i[0])
    i[1]=int(i[1])   
SNV_data.sort(key=lambda x: [x[0],x[1]])

for i in CNA_data:
    i[0]=i[0].strip('chr').strip('ch').strip('Chr').strip('Ch').replace('X','23').replace('M','25')
    i[0]=int(i[0])
    i[1]=int(i[1])
    i[2]=int(i[2])    
CNA_data.sort(key=lambda x: [x[0],x[1],x[2]])
'''
#Rename for uniforming
n_snv=0
n_cna=0
while n_snv<=len(SNV_data):
    curr_snv=SNV_data[n_snv][0]
    curr_cna=CNA_data[n_cna][0]
    if CNA_data[n_cna][0].find(SNV_data[n_snv][0])>=0:
        while SNV_data[n_snv][0]==curr_snv:
            n_snv+=1
            if n_snv==len(SNV_data):
                break
        while CNA_data[n_cna][0]==curr_cna:
            CNA_data[n_cna][0]=curr_snv
            n_cna+=1
            if n_cna==len(CNA_data):
                n_cna=0
                n_snv+=1
                break
    elif SNV_data[n_snv][0].find(CNA_data[n_cna][0])>=0:
        while CNA_data[n_cna][0]==curr_cna:
            n_cna+=1
            if n_cna==len(CNA_data):
                n_cna=0
                n_snv+=1
                break
        while SNV_data[n_snv][0]==curr_snv:
            SNV_data[n_snv][0]=curr_cna
            n_snv+=1
            if n_snv==len(SNV_data):
                break
    else:
        while CNA_data[n_cna][0]==curr_cna:
            n_cna+=1
            if n_cna==len(CNA_data):
                n_cna=0
                n_snv+=1
                break
'''
#Tied up CNA and SNV
data=[]
step=[0, 0]
for i in SNV_data:
    data_line=[]
    data_line.append(i[0])
    data_line.append(i[1])
    data_line.append(i[2])
    data_line.append(int(i[3]))
    data_line.append(2)
    step=relayRaceSerch(i[0],i[1],CNA_data,step[1])
    if step[0]==-1:
        data_line.append(0)
        data_line.append(2)        
    else:
        data_line.append(CNA_data[step[0]][4])
        data_line.append(CNA_data[step[0]][3])
    data.append(data_line) 


#wey_out=wey_input_SNV.replace('csv', 'tsv')
wey_out=wey_input_SNV+'CNA.tsv'
file_write=open(wey_out, 'w')
file_write.write('mutation_id\tref_counts\tvar_counts\tnormal_cn\tminor_cn\tmajor_cn\n')
'''
print(data[0])
print(CNA_data[0])
print(data[1])
print(CNA_data[1])
'''
for i in data:
    file_write.write(str(i[0])+':'+str(i[1])+'\t'+str(i[2])+'\t'+str(i[3])+'\t'+str(i[4])+'\t'+str(i[5])+'\t'+str(i[6])+'\n')
        
file_write.close()
print('----- Completed -----')
