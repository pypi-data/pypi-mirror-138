#ifdef  __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <stdlib.h>

struct MolInfo
{
    // Structure of just one cluster
    int exist; // if 1 that exist
    int* typesCount; // len() = Maxtypes // Number of types in molecule
    int* quantityByStep; // len() = Mxsteps // number of such molecule for every step
};

struct MolsInfo {
    // Structure of different unique clusters
    int Maxtypes; // Number of types
    int Maxsteps;  // Number of steps
    int Maxunique; // Number of unique molecules allowed
    int step; // Current step
    int* particleAttachemnt; // Size [Npart*Nstep=molinfo_id
    struct MolInfo* molInfo; // len() = Maxunique // massive of MolInfo
};



struct  SystemState
{
    /* data */
    int Npart;
    int Nsteps;
    int maxtypes;
    int* types;
    double cell;
    double* r; // r[Nstep*Npart*3 + Npart*3 + dimenstion] = r[Npart][dimension]
};

// int get_nearests(double x1, double x2, double cell);
// int get_distances(double * r1, double * r2, double cell);
struct MolsInfo* neighbour(struct SystemState sysState, double rcut, int maxunique);
void freeMolsInfo(struct MolsInfo *molsInfo);

#ifdef  __cplusplus
}
#endif

// #define MAX_X_LIST 3
// #define MAX_L_LIST MAX_X_LIST*MAX_X_LIST*MAX_X_LIST


// double x_list[MAX_X_LIST*3]; // 3x3
// int x_list_id, x_list_0;
// double l_list[MAX_X_LIST*MAX_X_LIST*MAX_X_LIST]; // 3x3x3
// double l_list_buf=0;
int l_list_id;
double dx, dr, dx_buf;
int count,k;
struct MolsInfo* molsInfo;

double get_nearest(double x1, double x2, double cell){
    // Return ABS(axis distances)

    dx = fabs(x2-x1);

    count = dx / cell;
    dx = dx - count * cell;
    if (fabs(dx-cell) < fabs(dx)){
        dx = dx-cell;
    }

    // printf ("get nearest: x1: %f, x2: %f, dx: %f\n", x1, x2, dx);
    return dx;
}

double get_distance(double* r1, double* r2, double cell){
    dr = 0;
    for (int i=0; i<3; i++){
        dx_buf = get_nearest(r1[i], r2[i], cell);
        dr += dx_buf*dx_buf;
    }

    // printf ("get dist: r1: %f, r2: %f, dr: %f\n", r1[0], r2[0], dr);
    return sqrt(dr);
}

int update_mol_info(int* typesCount, int k_size){
    // find in mols_info
    // printf("ksize = %d\n", k_size);
    int find_flag = 0;
    int compare_flag=0;
    int i = 0;
    for (i = 0; i < molsInfo->Maxunique-1; i++){
        if (molsInfo->molInfo[i].exist == 0){
            break;
        }
        compare_flag = 0;
        for (int j = 0; j < molsInfo->Maxtypes; j++){
            if (typesCount[j] != molsInfo->molInfo[i].typesCount[j]){
                compare_flag ++;
                break;
            }
        }
        // printf ( "typesCount[0]: %d %d %d %d\n", typesCount[0], molsInfo->molInfo[i].typesCount[0], molsInfo->molInfo[i].typesCount[1], compare_flag);
        if (compare_flag == 0 ){
            // Found!
            find_flag = 1;
            break;
        }
    }
    // printf("i=%d, maxunique=%d, find_flag, %d\n", i, molsInfo->Maxunique, find_flag);
    if (find_flag == 1){
        // Found!
        molsInfo->molInfo[i].quantityByStep[molsInfo->step] +=k_size;
        free(typesCount);
    } else {
        // printf ( "Create new unique, typesCount[0]: %d\n", typesCount[0]);
        // Not found. 
        // Check if there not enough space in Maxunique we put all into last element of massive
        if (molsInfo->molInfo[i].exist == 0){
            molsInfo->molInfo[i].exist = 1; 
            molsInfo->molInfo[i].typesCount = typesCount;
        }else{
            free(typesCount);
        }
        molsInfo->molInfo[i].quantityByStep[molsInfo->step] +=k_size;
    }
    return i;
}

void get_neighboard_list(struct SystemState sysState, int step, double rcut){
    /*!
    \brief Update data in molInfo with data from step
    We prefer unrecursive way. We go through Npart list, 
    and numerate particles by k_flag to understand which one bounded.
    */
    // Get number of particles in system
    int Npart = sysState.Npart;
    // printf ("run get neighbour\n");
    // Split
    int belongList[Npart];
    for (int i = 0; i < Npart; i++){
        belongList[i] = 0;
    }
    int kflag=0, kflag_old=0;
    double dist1=0, dist2=0;;
    for (int i = 0 ; i < Npart; i++){
        // DEBUG
        // printf(" i = %d \n", i);
        if (belongList[i] == 0) {
            // if particles not bounded
            kflag++;
            belongList[i] = kflag;
        }
        for (int j = i+1; j < Npart; j++){
            // check distance to this particle
            dist1 = get_distance(&sysState.r[step*Npart*3 + i*3], &sysState.r[step*Npart*3 + j*3], sysState.cell);
            dist2 = get_distance(&sysState.r[(step+1)*Npart*3 + i*3], &sysState.r[(step+1)*Npart*3 + j*3], sysState.cell);
            // printf ("dist1: %f dist2: %f\n", dist1, dist2);
            // printf ("x1: %f x2: %f\n", sysState[0].r[i*3], sysState[0].r[j*3]);
            if (dist1 < rcut && dist2 < rcut){
                // Realy connect during this dStep
                if ( belongList[j] == 0){
                    // It's not connected yet to anyone
                    belongList[j] = belongList[i];
                } else {
                    if (belongList[i] != belongList[j]){
                    // It's already in cluster (maybe just one particle) we connect to this cluster
                        // printf ("more then two in cluster %d (for %d) Kflag %d Kflag_old %d\n", j, i, belongList[j], belongList[i]);
                        kflag_old = belongList[i];
                        for (int l = 0; l < Npart; l++){
                            if (belongList[l] == kflag_old){
                                belongList[l] = belongList[j];
                                // printf ("add to %d \n", l);
                            }
                        }
                        kflag--;
                    }
                }
            }
        }
    }
    // Here we sort info from belongList and sysState->types 
    // to update MolInfo list with unique_count members
    int n_part = 0;
    int k_belong_molinfo_id[kflag+1];
    for (int k = 1; k <= kflag; k++){
        int *typesCount = (int *) malloc (sizeof(int)*molsInfo->Maxtypes);
        for (int i = 0; i < molsInfo->Maxtypes; i++){
            typesCount[i] = 0;
        }
        int k_size = 0;
        for (int i = 0; i < Npart; i++){
            if (belongList[i] == k){
                k_size ++ ;
                typesCount[sysState.types[i]] ++;
            }
        }
        if (k_size > 0){
            k_belong_molinfo_id[k] = update_mol_info(typesCount, k_size);    
        } else {
            free(typesCount);
        }
        n_part += k_size;
    }
    // printf ("n_part: %d \n", n_part);
    for (int i = 0; i < Npart; i++){
        int bl = belongList[i];
        if (bl > kflag || bl < 1 ){
            printf("Something wrong %d\n", bl);
        }
    }
    for (int i = 0; i < Npart; i++){
        molsInfo->particleAttachemnt[molsInfo->step*Npart+i] = k_belong_molinfo_id[belongList[i]];    
    } 
    

}

struct MolsInfo* neighbour(struct SystemState sysState, double rcut, int maxunique){
    /*! \brief Function return Step dependent list of particle culsters from X,Y,Z coords of particles
    1) For every step in Nsteps, we get sysState[step] and sysState[step+1]. 
    2) Look, which particles stay together (distance less then rcut) in both steps. (bound pair)
    3) Combine bouned pairs into clusters. 
    4) Analyse compositions of such clusters to create list of unique combination
    5) Return count of such unique combination as dependense of time (molInfo)

    ! MolsInfo should be inititalisated in Python mode

    @return Count of different combination
    */
    // Initialisation of molsInfo
    // printf ( "Nparticles: %d\n", sysState.Npart);
    // printf ( "Cell: %f\n", sysState.cell);
    // printf ( "Rcut: %f\n", rcut);
    molsInfo = (struct MolsInfo *) malloc (sizeof(struct MolsInfo));
    molsInfo->Maxtypes = sysState.maxtypes;
    molsInfo->Maxsteps = sysState.Nsteps-1;
    molsInfo->Maxunique = maxunique;
    molsInfo->step=0;
    molsInfo->molInfo = (struct MolInfo *) malloc (sizeof(struct MolInfo)*maxunique);
    molsInfo->particleAttachemnt = ( int *) malloc (sizeof(int)*(sysState.Nsteps-1)*sysState.Npart);
    for (int i = 0; i < maxunique; i++){
        molsInfo->molInfo[i].exist=0;
        molsInfo->molInfo[i].quantityByStep = (int *) malloc (sizeof(int)*(sysState.Nsteps-1));
        for (int j = 0; j < sysState.Nsteps-1; j++){
            molsInfo->molInfo[i].quantityByStep[j] = 0;
        }   
    }
    // return *molsInfo; // TODO
    // printf ("Debug after initial: exist: %d\n", molsInfo->molInfo[0].exist);
    // printf ("here %d\n", sysState.Nsteps);
    for (int step=0; step<sysState.Nsteps-1; step++){
        get_neighboard_list(sysState, step, rcut);
        molsInfo->step++;
    }
    // printf ("Debug at the end: exist: %d\n", molsInfo->molInfo[0].exist);
    return molsInfo;
}


void freeMolsInfo(struct MolsInfo *molsInfo){
    
    for (int i = 0; i < molsInfo->Maxunique; i++){
        free(molsInfo->molInfo[i].quantityByStep);
        if (molsInfo->molInfo[i].exist == 1){
            free(molsInfo->molInfo[i].typesCount);
        }
    }
    free(molsInfo->particleAttachemnt);
    free(molsInfo->molInfo);
    free(molsInfo);
}