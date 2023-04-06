"""
Definition of views.
"""
import pandas as pd
from datetime import datetime
from django.shortcuts import render
import numpy as np
import json
from django.http import HttpRequest,JsonResponse
from skimage.feature import greycomatrix


def home(request):
    """Renders the home page."""
    if request.method == "POST":
        navig=request.POST['button']
        if navig == 'button1':
            return JsonResponse({'FirstMatrix':convertTOjson(np.random.randint(0,6,(6,6)))})
        elif navig=='button2':
            distance=request.POST.get('distance')
            angle=request.POST.get('angle')
            IA=request.POST.get('inputarray')
            return JsonResponse({'SecondMatrix':convertTOjson(greycomatrix(clearmatrix(IA), [distance], [angle], levels=6))})
        elif navig=='buttonSearch':
            btnid=str(request.POST.get('clicked_id'))
            innputarray=request.POST.get('inputarray')
            distance=request.POST.get('distance')
            angle=request.POST.get('angle')
            clecnmat=clearmatrix(innputarray)
            indexid=list(btnid)
            list1=int(indexid[0])
            list2=int(indexid[1])
            positionitions = []
            for i in range(len(clecnmat)):
                for j in range(len(clecnmat[i])):
                    if clecnmat[i][j] == list1:
                        positionitions.append((i, j))

            arraydistance=np.array(positionitions)
            matlength=0;
            duplicate=[]
            if (len(arraydistance))>0:
                r=arraydistance[:,0]
                matlength=(len(r))
            for i in range(matlength):
                first=arraydistance[i][0]
                position=arraydistance[i][1]
                distance=int(distance)
                if(int(angle)==0):
                    if((position+distance)<6 and (clecnmat[first][position+distance]==list2)):
                        duplicate.append((first,position)) 
                        print("pair found")
                elif(int(angle)==90):
                    if((first+distance)<6 and (clecnmat[first+distance][position]==list2)):
                        duplicate.append((first,position)) 
                        print("pair found")
                elif(int(angle)==45):
                    if((position+distance)<6 and (clecnmat[first-distance][position+distance]==list2)):
                        duplicate.append((first,position)) 
                        print("pair found")
                elif(int(angle)==135):
                    if((position+distance)<6 and (clecnmat[first-distance][position-distance]==list2)):
                        duplicate.append((first,position)) 
                        print("pair found")
            finalResults=np.array(duplicate)
            finalResults=json.dumps(finalResults.tolist())
            return JsonResponse({'Result_Pair':finalResults})
    
    return render(
        request,
        'app/index.html')



def clearmatrix(inputarray):
    array=json.loads(inputarray)
    if len(array)==0:
        array=np.random.randint(0,1,(6,6))

    stringfilter=''.join((filter(lambda x:x not in ['[',']',',','"','\\'],str(array))))      
    result=np.array(stringfilter.split()).reshape(-1,6)
    return np.array(result).astype(np.int)



def convertTOjson(mat):
    convert=mat.tolist()
    result=json.dumps(convert)
    return result
