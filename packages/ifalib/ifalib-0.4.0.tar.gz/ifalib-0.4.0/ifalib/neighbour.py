#!/usr/bin/python
"""! @brief Radial Distribution Analysis"""
##
# @mainpage Neighbour analysis
#
# @section Neighbour Neighbour
# Neighbour (Composition) analysis for MD coordinates
#
# @file neighbour.py
#
# @section todo_neighbour TODO
# - None.

import os, glob
import ctypes

def neighbour(coord, types, cell, rcut, step_to_compare=1, maxunique=4, l_of_p=False): 
    '''! Neighbour analysis of system
    @param coord XYZ coordinates of particles, format coord[Nstep][Nparticles][Dimension]
    @param types Type of every particle
    @param cell Size of cubic cell
    @param rcut Max radius of RDF
    @param step_to_compare Number of steps to compare: dist[step] < rcut && dist[step+step_to_compare] < rcut
    @param maxunique maximum number molecules type to find (default: 4)
    @param l_of_p Flag (on/off) list_of_particles in return (default: False)
    @return [{
            'composition': {'H': 2, 'e':1},
            'label': 'H2 e1',
            'count': [Nmol[step] for step in range(Nstep)]
            }, ...], (l_of_p==on) {'
            'label': [label] = id,
            'particle_attach': [[id for idp in range(Npart)] for step in range(Nstep)]
            }, ...]
    }
    '''
    # Load Library
    basedir = os.path.abspath(os.path.dirname(__file__))
    libpath = os.path.join(basedir, 'libneighbour*.so')
    libpath = glob.glob(libpath)[0]
    neighbour_ctypes = ctypes.CDLL(libpath)

    # Объявляем структуру в Python аналогичную в C структуре MolInfo
    class MolInfo(ctypes.Structure):
        _fields_ = [('exist', ctypes.c_int),
                    ('typesCount', ctypes.POINTER(ctypes.c_int)),
                    ('quantityByStep', ctypes.POINTER(ctypes.c_int))]

    # Объявляем структуру в Python аналогичную в C структуре MolsInfo
    class MolsInfo(ctypes.Structure):
        _fields_ = [('Maxtypes', ctypes.c_int),
                    ('Maxsteps', ctypes.c_int),
                    ('Maxunique', ctypes.c_int),
                    ('step', ctypes.c_int),
                    ('particleAttachemnt', ctypes.POINTER(ctypes.c_int)),
                    ('molInfo', ctypes.POINTER(MolInfo))]

    class SystemState(ctypes.Structure):
        _fields_ = [('Npart', ctypes.c_int),
                    ('Nsteps', ctypes.c_int),
                    ('maxtypes', ctypes.c_int),
                    ('steptocompare', ctypes.c_int),
                    ('types', ctypes.POINTER(ctypes.c_int)),
                    ('cell', ctypes.c_double),
                    ('r', ctypes.POINTER(ctypes.c_double))]

    # Указываем, что функция возвращает MolsInfo *
    neighbour_ctypes.neighbour.restype = ctypes.POINTER(MolsInfo)
    # Указываем, что функция принимает аргумент void *
    neighbour_ctypes.neighbour.argtypes = [SystemState, ctypes.c_double, ctypes.c_int]

    
    Nsteps = len(coord)
    Npart = len(coord[0])
    # print (Npart)
    Rpart=[]
    for step in range(Nsteps):
        for idp in range(Npart):
            for dim in range(3):
                Rpart.append(coord[step][idp][dim])
    Rpart_c_double=(ctypes.c_double * (Nsteps*Npart*3)) (*Rpart)
    unique_flag = 0
    Types_label = {}
    types_for_c = []
    for idp in range(Npart):
        if not types[idp] in Types_label:
            Types_label[types[idp]] = unique_flag
            unique_flag+= 1
        types_for_c.append(Types_label[types[idp]])
    maxtypes = unique_flag

    Types_c_int=(ctypes.c_int * (Npart)) (*types_for_c)

    # Создаем структуру
    sysState = SystemState(Npart, Nsteps, maxtypes, step_to_compare, Types_c_int, cell, Rpart_c_double)

    # maxunique+1 because we want to add other")
    molsInfo_p = neighbour_ctypes.neighbour(sysState,rcut, maxunique+1)
    molsInfo = molsInfo_p.contents #ctypes.byref(molsInfo_p)
  
    list_of_molecules = {}
    list_of_particles = {
        'label': {},
        'particle_attach': [[0 for idp in range(Npart)] for step in range(molsInfo.Maxsteps) ] # [step][idp]  
    }
    for i in range(molsInfo.Maxunique):
        # print ("molInfo[{:d}]: ".format(i), molsInfo.molInfo[i].exist)
        if (molsInfo.molInfo[i].exist == 0): break
        label = ""
        composition = {}
        number_of_particles = 0
        for key in Types_label:
            n = molsInfo.molInfo[i].typesCount[Types_label[key]]
            if ( n > 0):
                composition[key] = n
                label += str(key) + str(n) + " "
            number_of_particles+= n

        # remove last space
        if len(label)>0:
            label = label[:-1]
        count_of_molecules = []
        count_of_particles = []
        for step in range(molsInfo.Maxsteps):
            count_of_particles.append(molsInfo.molInfo[i].quantityByStep[step])
        
        if (i == molsInfo.Maxunique-1):
            label = "unknown"
            composition = []

        list_of_molecules[label] = {
            'composition': composition,
            'count_of_particles': count_of_particles
        }
        list_of_particles['label'][label]=i
    
    # Create list of particle attachments
    for step in range(molsInfo.Maxsteps):
        for idp in range(Npart):
            list_of_particles['particle_attach'][step][idp]=molsInfo.particleAttachemnt[step*Npart + idp]


    # Free memory
    neighbour_ctypes.freeMolsInfo.argtypes = [ctypes.c_void_p]
    neighbour_ctypes.freeMolsInfo(molsInfo_p)

    del Rpart, Rpart_c_double, types_for_c, Types_c_int
    
    if l_of_p:
        return list_of_molecules, list_of_particles
    else:
        return list_of_molecules