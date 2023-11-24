import numpy as np



def update_9(M):
    """
    Update M using the 8 nearest neighbors on the grid
    """
    M1 = M.copy()
    for idx, row in enumerate(M1):
        for jdx, v in enumerate(row):
            S = None
            if (idx == 0):
                S = M[:, :2]
            elif (idx == n-1):
                S = M[:, -2:]
            else:
                S = M[:, idx-1:idx+2]

            if (jdx == 0):
                S = S[:2]
            elif jdx == n-1:
                S = S[-2:]
            else:
                S = S[jdx-1:jdx+2]

            M1[idx, jdx] = np.mean(S)
    
    return M1


def update_4(M):
    """
    Update M using the 4 nearest neighbors on the grid
    :param M: square matrix
    """
    M1 = M.copy()
    n = len(M1)
    for idx, row in enumerate(M1):
        for jdx, v in enumerate(row):
            lst = [v]
            
            if (idx != 0):
                lst.append(M[idx-1, jdx])
            if (idx != n-1):
                lst.append(M[idx+1, jdx])
            if (jdx != 0):
                lst.append(M[idx, jdx-1])
            if (jdx != n-1):
                lst.append(M[idx, jdx+1])
            
            M1[idx, jdx] = np.mean(lst)
    
    return M1

def update_4_circular(M):
    """
    Update M using the 8 nearest neighbors on the grid
    + continuity betwween left and right border.
    
    :param M: square matrix
    """

    M1 = M.copy()
    n = len(M1)
    for idx, row in enumerate(M1):
        for jdx, v in enumerate(row):
            lst = [v]
            
            if (idx != 0):
                lst.append(M[idx-1, jdx])
            else:
                lst.append(M[n-1, jdx])
            
            if (idx != n-1):
                lst.append(M[idx+1, jdx])
            else:
                lst.append(M[0, jdx])
                
            if (jdx != 0):
                lst.append(M[idx, jdx-1])
            else:
                lst.append(M[idx, n-1])
                
            if (jdx != n-1):
                lst.append(M[idx, jdx+1])
            else:
                lst.append(M[idx, 0])
                
            M1[idx, jdx] = np.mean(lst)
    
    return M1