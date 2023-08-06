
def findFilesDirectory(root,pattern):
    '''
    inspired by the following entry:
    https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files
    
    USAGE: data=findFilesDirectory('e:\data','*.csv')
    '''
    import os
    from fnmatch import fnmatch

    #root = 'c:/data'
    #pattern = "*.xlsx"
    out1=[]
    out2=[]
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                out1=os.path.join(path, name)
                out2.append(out1)
                #print(os.path.join(path, name))
    return out2


def findUniqueList(param1):
    ''' it returns the unique subset of the list
	USAGE: findUniqueList([1,3,3,4,5,5,6])
	'''
    used=set()
    
    
    if len(param1) < 2:
        print("this is not a list")
    else:
        unique_list = [x for x in param1 if x not in used and (used.add(x) or True)]
        return unique_list
    

def extractData(data, textSearched):
    ''' 
    USAGE: extractData(['orange','apple','apple1','banana'],'apple') 
    '''
    
    index_page=[]
    
    for i in range(0,len(data),1):
        if textSearched in data[i]:
            index_page.append(data[i].strip())
    return index_page



def isMatch(name1,name2):
    ''' it returns if two names are related. 
    USAGE: isMatch('Apple juice','apple Juice')
    if result is 0-> two names are identical
    if result is more than 0 but less than 15deg, the names have similarity
    if the result is more than 30deg, the names have no similarity
    '''
    import math
    from collections import Counter

    def build_vector(iterable1, iterable2):
        counter1 = Counter(iterable1)
        counter2 = Counter(iterable2)
        all_items = set(counter1.keys()).union(set(counter2.keys()))
        vector1 = [counter1[k] for k in all_items]
        vector2 = [counter2[k] for k in all_items]
        return vector1, vector2

    def cosim(v1, v2):
        dot_product = sum(n1 * n2 for n1, n2 in zip(v1, v2) )
        magnitude1 = math.sqrt(sum(n ** 2 for n in v1))
        magnitude2 = math.sqrt(sum(n ** 2 for n in v2))
        return dot_product / (magnitude1 * magnitude2)
    
    l1 = name1.lower().split()
    l2 = name2.lower().split()

#l1 = "A cover".lower().split()
#l2 = "a cover".lower().split()


    v1, v2 = build_vector(l1, l2)
    result=round(math.degrees(math.acos(cosim(v1, v2))),5)
    
    return result