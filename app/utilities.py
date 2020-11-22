from random import shuffle

def has_fixed_points(perm):
    ''' Checks whether argument perm (permutation, which is expected to 
        be list of unique indices, which order represents permutation)
        has fixed points in it. '''

    for i, e in enumerate(perm):
        if i == e:
            return True
    
    return False


def permutation_without_fixed_points(n):
    ''' This function return permutation of lenght *n*
        without fixed points. '''

    l = [ i for i in range(n) ]

    shuffle(l)
    while has_fixed_points(l):
        shuffle(l)

    return l