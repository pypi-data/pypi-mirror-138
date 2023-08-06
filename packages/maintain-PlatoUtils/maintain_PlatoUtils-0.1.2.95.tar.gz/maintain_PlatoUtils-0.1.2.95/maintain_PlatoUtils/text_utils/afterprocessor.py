
def getEntityFromTags(mySentList,myTagList):
    '''
    从tagList中获取sentList中的实体
    '''
    entityList=[]
    tmpEntity=""
    if len(mySentList)==len(myTagList):
        for tagI,_ in enumerate(myTagList):
            if myTagList[tagI]=="B":
                tmpEntity=mySentList[tagI]
            elif myTagList[tagI]=="I":
                tmpEntity+=mySentList[tagI]
            else:
                if len(tmpEntity)>0:
                    entityList.append(tmpEntity)
                tmpEntity=""
    return entityList