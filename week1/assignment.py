sno = ['S001', 'S002', 'S003', 'S004']
name = ['Adina Park', 'Leyton Marsh', 'Duncan Boyle', 'Saim Richards']
marks = [85, 98, 89, 92]

plist=[]
for i in range(len(sno)):
    plist.append({sno[i]:{name[i]:marks[i]}})
print(plist)

pass