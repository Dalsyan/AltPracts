import numpy as np



def levenshtein_matriz(x, y, threshold=None):
    # esta versión no utiliza threshold, se pone porque se puede
    # invocar con él, en cuyo caso se ignora
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
            )

    return D[lenX, lenY]

def get_damerau_intermediate_matriz(x, y, threshold=None):
    # completar versión Damerau-Levenstein intermedia con matriz
    lenX, lenY = len(x), len(y)
    ruleNum = 0
    rule2Num = 0
    rule3Num = 0
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            if(i > 1 and j > 1 and (x[i - 2] == y[j - 1]) and (x[i - 1] == y[j - 2])):
                ruleNum = D[i - 2][j - 2] + 1
            else:
                ruleNum = D[i - 1][j] + 10 #it never is the minimum

            if(i > 2 and j > 1 and (x[i - 3] == y[j - 1]) and (x[i - 1] == y[j - 2])):
                rule2Num = D[i - 3][j - 2] + 2
            else:
                rule2Num =  D[i - 1][j] + 10 #it never is the minimum

            if(i > 1 and j > 2 and (x[i - 1] == y[j - 3]) and (x[i - 2] == y[j - 1])):
                rule3Num = D[i - 2][j - 3] + 2
            else:
                rule3Num =  D[i - 1][j] + 10 #it never is the minimum

            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
                ruleNum,
                rule2Num,
                rule3Num,
            )
    #print(D)
    return D

def get_damerau_restricted_matriz(x, y, threshold=None):
    # completar versión Damerau-Levenstein restringida con matriz
    lenX, lenY = len(x), len(y)
    ruleNum = 0
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            if(i > 1 and j > 1 and (x[i - 2] == y[j - 1]) and (x[i - 1] == y[j - 2])):
                ruleNum = D[i - 2][j - 2] + 1
            else:
                ruleNum = D[i - 1][j] + 10 #it never is the minimum
            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
                ruleNum,
            )

    return D

def getMatrixLevenstein(x, y, threshold=None):
    # esta versión no utiliza threshold, se pone porque se puede
    # invocar con él, en cuyo caso se ignora
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
            )

    return D
#print(levenshtein_matriz("ejemplo","campos",None))
def levenshtein_edicion(x, y, threshold=None):
    D = getMatrixLevenstein(x, y, None)
    dist = 0
    lenX = len(x)
    lenY = len(y)
    curr =(lenX,lenY)
    nex = (lenX,lenY)
    camino = []
    iterations = 0
    #print("Curr = " + str(curr[0]) + " , " + str(curr[1]))
    while(curr[0] != 0 or curr[1] != 0):

        if(curr[0] == 0):
            nex = [curr[0],curr[1] - 1]
            camino.append(('',y[curr[1]-1]))
            dist = dist+1
        elif(curr[1] == 0):
            nex = [curr[0] - 1,curr[1]]
            camino.append((x[curr[0]-1],''))
            dist = dist+1
        else:
            valCurr = D[curr[0],curr[1]]
            if(valCurr - D[curr[0] - 1,curr[1]] == 1):
                nex = (curr[0] - 1,curr[1])
                camino.append((x[curr[0]-1],''))
                dist = dist+1
            elif(valCurr - D[curr[0],curr[1] - 1] == 1):
                nex = (curr[0],curr[1] - 1)
                camino.append(('',y[curr[1]-1]))
                dist = dist+1
            else:
                nex = (curr[0] - 1,curr[1] - 1)
                camino.append((x[curr[0]-1],y[curr[1]-1]))
                if(x[curr[0]-1] != y[curr[1]-1]): dist = dist+1
        curr = nex
        iterations = iterations+1
        #print(camino)
        #dar la vuelta a la lista
    camino.reverse()
    return dist,camino
#print(levenshtein_edicion("zapato","patos",None))

def levenshtein_reduccion(x, y, threshold=None):
    lenX, lenY = len(x), len(y)
    vPrev = np.zeros(lenX + 1,dtype=np.int)
    vCurr = np.zeros(lenX + 1,dtype=np.int)
    for i in range(1, lenX + 1):
        vPrev[i] = vPrev[i - 1] + 1
    #print(vPrev)
    for j in range(1, lenY + 1):
        vCurr[0] = vPrev[0] + 1
        for i in range(1, lenX + 1):
            vCurr[i] = min(
                vPrev[i] + 1,
                vCurr[i - 1] + 1,
                vPrev[i - 1] + (x[i - 1] != y[j - 1]),
            )
        #print("PREVIOUS")
        #print(vPrev)
        #print("CURRENT")
        #print(vCurr)
        vPrev,vCurr = vCurr,vPrev

    return vPrev[lenX] # COMPLETAR Y REEMPLAZAR ESTA PARTE
#print(levenshtein_reduccion("ejemplo","campos",None))

def levenshtein(x, y, threshold):
    lenX, lenY = len(x), len(y)
    vPrev = np.zeros(lenX + 1,dtype=np.int)
    vCurr = np.zeros(lenX + 1,dtype=np.int)

    for i in range(1, lenX + 1):
        vPrev[i] = vPrev[i - 1] + 1
    #print(vPrev)
    for j in range(1, lenY + 1):
        vCurr[0] = vPrev[0] + 1
        allAbove = True
        if(vCurr[0] < threshold): allAbove = False
        elif(vCurr[0] == threshold and lenX - i == lenY - j): allAbove = False
        for i in range(1, lenX + 1):
            vCurr[i] = min(
                vPrev[i] + 1,
                vCurr[i - 1] + 1,
                vPrev[i - 1] + (x[i - 1] != y[j - 1]),
            )
            if(vCurr[i] < threshold): allAbove = False
            elif(vCurr[i] == threshold and lenX - i == lenY - j): allAbove = False
        #print(vCurr)
        if(allAbove): return threshold+1
        #print("PREVIOUS")
        #print(vPrev)
        #print("CURRENT")

        vPrev,vCurr = vCurr,vPrev
    return vPrev[lenX] # COMPLETAR Y REEMPLAZAR ESTA PARTE
#print(levenshtein("ejemplo","campos",6))


def levenshtein_cota_optimista(x, y, threshold):
    return 0 # COMPLETAR Y REEMPLAZAR ESTA PARTE

def damerau_restricted_matriz(x, y, threshold=None):
    # completar versión Damerau-Levenstein restringida con matriz
    lenX, lenY = len(x), len(y)
    ruleNum = 0
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            if(i > 1 and j > 1 and (x[i - 2] == y[j - 1]) and (x[i - 1] == y[j - 2])):
                ruleNum = D[i - 2][j - 2] + 1
            else:
                ruleNum = D[i - 1][j] + 10 #it never is the minimum
            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
                ruleNum,
            )
    #print(D)
    return D[lenX, lenY]
#print(damerau_restricted_matriz("algortimac","algoritmica",50))


def damerau_restricted_edicion(x, y, threshold=None):
    D = get_damerau_restricted_matriz(x, y, None)
    dist = 0
    lenX = len(x)
    lenY = len(y)
    curr = (lenX,lenY)
    nex = (lenX,lenY)
    camino = []
    iterations = 0
    valCurr = 0
    #print("Curr = " + str(curr[0]) + " , " + str(curr[1]))
    while(curr[0] != 0 or curr[1] != 0):

        if(curr[0] == 0):
            nex = [curr[0],curr[1] - 1]
            camino.append(('',y[curr[1]-1]))
            dist = dist+1
        elif(curr[1] == 0):
            nex = [curr[0] - 1,curr[1]]
            camino.append((x[curr[0]-1],''))
            dist = dist+1
        else:
            valCurr = D[curr[0],curr[1]]
            if(curr[0] > 1 and curr[1] > 1 and (x[curr[0] - 2] == y[curr[1] - 1]) and (x[curr[0] - 1] == y[curr[1] - 2])):
                nex = (curr[0] - 2,curr[1] - 2)
                camino.append(( x[curr[0]-2]+x[curr[0]-1] , y[curr[1]-2]+y[curr[1]-1]))
                dist = dist+1
            elif(valCurr - D[curr[0] - 1,curr[1]] == 1):
                nex = (curr[0] - 1,curr[1])
                camino.append((x[curr[0]-1],''))
                dist = dist+1
            elif(valCurr - D[curr[0],curr[1] - 1] == 1):
                nex = (curr[0],curr[1] - 1)
                camino.append(('',y[curr[1]-1]))
                dist = dist+1
            else:
                nex = (curr[0] - 1,curr[1] - 1)
                camino.append((x[curr[0]-1],y[curr[1]-1]))
                if(x[curr[0]-1] != y[curr[1]-1]): dist = dist+1
        curr = nex
        iterations = iterations+1
        #print(camino)
        #dar la vuelta a la lista
    camino.reverse()
    return dist,camino # COMPLETAR Y REEMPLAZAR ESTA PARTE

def damerau_restricted(x, y, threshold=None):
    # versión con reducción coste espacial y parada por threshold
    lenX, lenY = len(x), len(y)
    vPrev = np.zeros(lenX + 1,dtype=np.int)
    vCurr = np.zeros(lenX + 1,dtype=np.int)
    vPrev2 = np.zeros(lenX + 1,dtype=np.int)
    ruleNum = 0;
    for i in range(1, lenX + 1):
        vPrev[i] = vPrev[i - 1] + 1
    #print(vPrev)
    for j in range(1, lenY + 1):
        vCurr[0] = vPrev[0] + 1
        allAbove = True
        if(vCurr[0] < threshold): allAbove = False
        elif(vCurr[0] == threshold and lenX - i == lenY - j): allAbove = False
        for i in range(1, lenX + 1):
            if(i > 1 and j > 1 and (x[i - 2] == y[j - 1]) and (x[i - 1] == y[j - 2])):
                ruleNum = vPrev2[i - 2] + 1
            else:
                ruleNum =  vPrev[i] + 10 #it never is the minimum
            vCurr[i] = min(
                vPrev[i] + 1,
                vCurr[i - 1] + 1,
                vPrev[i - 1] + (x[i - 1] != y[j - 1]),
                ruleNum,
            )
            if(vCurr[i] < threshold): allAbove = False
            elif(vCurr[i] == threshold and lenX - i == lenY - j): allAbove = False
        #print(vCurr)
        if(allAbove): return threshold+1
        #print("PREVIOUS")
        #print(vPrev)
        #print("CURRENT")

        vPrev,vPrev2,vCurr = vCurr,vPrev,vPrev2
    return vPrev[lenX] # COMPLETAR Y REEMPLAZAR ESTA PARTE

def damerau_intermediate_matriz(x, y, threshold=None):
    # completar versión Damerau-Levenstein intermedia con matriz
    lenX, lenY = len(x), len(y)
    ruleNum = 0
    rule2Num = 0
    rule3Num = 0
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            if(i > 1 and j > 1 and (x[i - 2] == y[j - 1]) and (x[i - 1] == y[j - 2])):
                ruleNum = D[i - 2][j - 2] + 1
            else:
                ruleNum = D[i - 1][j] + 10 #it never is the minimum

            if(i > 2 and j > 1 and (x[i - 3] == y[j - 1]) and (x[i - 1] == y[j - 2])):
                rule2Num = D[i - 3][j - 2] + 2
            else:
                rule2Num =  D[i - 1][j] + 10 #it never is the minimum

            if(i > 1 and j > 2 and (x[i - 1] == y[j - 3]) and (x[i - 2] == y[j - 1])):
                rule3Num = D[i - 2][j - 3] + 2
            else:
                rule3Num =  D[i - 1][j] + 10 #it never is the minimum

            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
                ruleNum,
                rule2Num,
                rule3Num,
            )
    #print(D)
    return D[lenX, lenY]

def damerau_intermediate_edicion(x, y, threshold=None):
    D = get_damerau_intermediate_matriz(x, y, None)
    dist = 0
    lenX = len(x)
    lenY = len(y)
    curr = (lenX,lenY)
    nex = (lenX,lenY)
    camino = []
    iterations = 0
    valCurr = 0
    #print("Curr = " + str(curr[0]) + " , " + str(curr[1]))
    while(curr[0] != 0 or curr[1] != 0):

        if(curr[0] == 0):
            nex = [curr[0],curr[1] - 1]
            camino.append(('',y[curr[1]-1]))
            dist = dist+1
        elif(curr[1] == 0):
            nex = [curr[0] - 1,curr[1]]
            camino.append((x[curr[0]-1],''))
            dist = dist+1
        else:
            valCurr = D[curr[0],curr[1]]
            if(curr[0] > 1 and curr[1] > 1 and (x[curr[0] - 2] == y[curr[1] - 1]) and (x[curr[0] - 1] == y[curr[1] - 2])):
                nex = (curr[0] - 2,curr[1] - 2)
                camino.append(( x[curr[0]-2]+x[curr[0]-1] , y[curr[1]-2]+y[curr[1]-1]))
                dist = dist+1
            elif(curr[0] > 2 and curr[1] > 2 and (x[curr[0] - 3] == y[curr[1] - 1]) and (x[curr[0] - 1] == y[curr[1] - 2])):
                nex = (curr[0] - 3,curr[1] - 2)
                camino.append(( x[curr[0]-3]+x[curr[0]-2]+x[curr[0]-1] , y[curr[1]-2]+y[curr[1]-1]))
                dist = dist+2
            elif(curr[0] > 1 and curr[1] > 1 and (x[curr[0] - 1] == y[curr[1] - 3]) and (x[curr[0] - 2] == y[curr[1] - 1])):
                nex = (curr[0] - 2,curr[1] - 3)
                camino.append(( x[curr[0]-2]+x[curr[0]-1] , y[curr[1]-3]+y[curr[1]-2]+y[curr[1]-1]))
                dist = dist+2
            elif(valCurr - D[curr[0] - 1,curr[1]] == 1):
                nex = (curr[0] - 1,curr[1])
                camino.append((x[curr[0]-1],''))
                dist = dist+1
            elif(valCurr - D[curr[0],curr[1] - 1] == 1):
                nex = (curr[0],curr[1] - 1)
                camino.append(('',y[curr[1]-1]))
                dist = dist+1
            else:
                nex = (curr[0] - 1,curr[1] - 1)
                camino.append((x[curr[0]-1],y[curr[1]-1]))
                if(x[curr[0]-1] != y[curr[1]-1]): dist = dist+1
        curr = nex
        iterations = iterations+1
        #print(camino)
        #dar la vuelta a la lista
    camino.reverse()
    return dist,camino # COMPLETAR Y REEMPLAZAR ESTA PARTE

def damerau_intermediate(x, y, threshold=None):
    # versión con reducción coste espacial y parada por threshold
    lenX, lenY = len(x), len(y)
    vPrev = np.zeros(lenX + 1,dtype=np.int)
    vCurr = np.zeros(lenX + 1,dtype=np.int)
    vPrev2 = np.zeros(lenX + 1,dtype=np.int)
    vPrev3 = np.zeros(lenX + 1,dtype=np.int)
    ruleNum = 0
    rule2Num = 0
    rule3Num = 0
    for i in range(1, lenX + 1):
        vPrev[i] = vPrev[i - 1] + 1
    #print(vPrev)
    for j in range(1, lenY + 1):
        vCurr[0] = vPrev[0] + 1
        allAbove = True
        if(vCurr[0] < threshold): allAbove = False
        elif(vCurr[0] == threshold and lenX - i == lenY - j): allAbove = False
        for i in range(1, lenX + 1):
            if(i > 1 and j > 1 and (x[i - 2] == y[j - 1]) and (x[i - 1] == y[j - 2])):
                ruleNum = vPrev2[i - 2] + 1
            else:
                ruleNum =  vPrev[i] + 10 #it never is the minimum

            if(i > 2 and j > 1 and (x[i - 3] == y[j - 1]) and (x[i - 1] == y[j - 2])):
                rule2Num = vPrev2[i - 3] + 2
            else:
                rule2Num =  vPrev[i] + 10 #it never is the minimum

            if(i > 1 and j > 2 and (x[i - 1] == y[j - 3]) and (x[i - 2] == y[j - 1])):
                rule3Num = vPrev3[i - 2] + 2
            else:
                rule3Num =  vPrev[i] + 10 #it never is the minimum

            vCurr[i] = min(
                vPrev[i] + 1,
                vCurr[i - 1] + 1,
                vPrev[i - 1] + (x[i - 1] != y[j - 1]),
                ruleNum,
                rule2Num,
                rule3Num,
            )
            if(vCurr[i] < threshold): allAbove = False
            elif(vCurr[i] == threshold and lenX - i == lenY - j): allAbove = False
        #print(vCurr)
        if(allAbove): return threshold+1
        #print("PREVIOUS")
        #print(vPrev)
        #print("CURRENT")

        vPrev,vPrev2,vPrev3,vCurr = vCurr,vPrev,vPrev2,vPrev3
    return vPrev[lenX] # COMPLETAR Y REEMPLAZAR ESTA PARTE
#print(damerau_intermediate("algoritmo","algortximo",50))

opcionesSpell = {
    'levenshtein_m': levenshtein_matriz,
    'levenshtein_r': levenshtein_reduccion,
    'levenshtein':   levenshtein,
    'levenshtein_o': levenshtein_cota_optimista,
    'damerau_rm':    damerau_restricted_matriz,
    'damerau_r':     damerau_restricted,
    'damerau_im':    damerau_intermediate_matriz,
    'damerau_i':     damerau_intermediate
}

opcionesEdicion = {
    'levenshtein': levenshtein_edicion,
    'damerau_r':   damerau_restricted_edicion,
    'damerau_i':   damerau_intermediate_edicion
}
