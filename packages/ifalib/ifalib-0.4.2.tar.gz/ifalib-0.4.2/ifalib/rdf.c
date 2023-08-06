#ifdef  __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <stdlib.h>

int get_nearests(double x1, double x2, double cell, double rcut);
int get_distances(double * r1, double * r2, double cell, double rcut);
int rdf(int nbins, double rcut, double * g_r, int Npart1, int Npart2, int Nsteps, double * Rpart1, double * Rpart2, double cell);

#ifdef  __cplusplus
}
#endif

// #define MAX_X_LIST 3
// #define MAX_L_LIST MAX_X_LIST*MAX_X_LIST*MAX_X_LIST

int MAX_X_LIST, MAX_L_LIST;
double* x_list; //[MAX_X_LIST*3]; // 3x3
int x_list_id, x_list_0;
double* l_list; //[MAX_X_LIST*MAX_X_LIST*MAX_X_LIST]; // 3x3x3
double l_list_buf=0;
int l_list_id;
double dx, dx0;
int count,k;

int get_nearests(double x1, double x2, double cell, double rcut){
    // Return ABS(axis distances)
    dx = fabs(x2-x1);

    count = dx / cell;
    dx = dx - count * cell;
    if (fabs(dx-cell) < fabs(dx)){
        dx = dx-cell;
    }
    x_list_0=x_list_id;
    while (dx < rcut){
        if (x_list_id-x_list_0 >= MAX_X_LIST){
            printf ("dx: %f | ", dx);
            printf ("max_x_list: %d | ", MAX_X_LIST);
            printf("exit -1 (dx < rcut)\n");
            exit(-1);
        }
        x_list[x_list_id]=fabs(dx);
        x_list_id++;
        dx += cell;
    }   

    dx = x_list[x_list_0]-cell;
    while (dx > -rcut){
        if (x_list_id-x_list_0 >= MAX_X_LIST){
            printf ("dx: %f | ", dx);
            printf ("max_x_list: %d | ", MAX_X_LIST);
            printf("exit -1 (dx > -rcut)\n");
            exit(-1);
        }
        x_list[x_list_id]=fabs(dx);
        x_list_id++;
        dx -= cell;
    }
    while(x_list_id-x_list_0 < MAX_X_LIST){
        x_list[x_list_id]=-1;
        x_list_id++;
    }
    return 0;
}

int get_distances(double * r1, double * r2, double cell, double rcut){
    for (int i=0; i<3; i++){
        x_list_id=i*MAX_X_LIST;
        get_nearests(r1[i], r2[i], cell, rcut);
    }
    l_list_id=0;
    for (int i=0; i<MAX_X_LIST; i++)
        if (x_list[i]>=0)
            for (int j=0; j<MAX_X_LIST; j++)
                if (x_list[j+MAX_X_LIST]>=0)
                    for (int k=0; k<MAX_X_LIST; k++)
                        if (x_list[k+2*MAX_X_LIST]>=0){
                            l_list_buf = sqrt(pow(x_list[i],2) + pow(x_list[j+MAX_X_LIST],2) + pow(x_list[k+2*MAX_X_LIST],2));
                            if (l_list_buf>0 && l_list_buf < rcut){
                                l_list[l_list_id]=l_list_buf;
                                l_list_id++;
                            }
                        }
    while(l_list_id < MAX_L_LIST){
        l_list[l_list_id]=-1;
        l_list_id++;
    }
    return 0;
}

int rdf(int nbins, double rcut, double * g_r, int Npart1, int Npart2, int Nsteps, double * Rpart1, double * Rpart2, double cell){
    // TODO  max_x_list should be automatic acoording Cell size and rcut
    MAX_X_LIST = (int)2*rcut/cell+2;

    MAX_L_LIST = MAX_X_LIST * MAX_X_LIST * MAX_X_LIST;
    x_list = (double *) malloc (sizeof(double)*MAX_X_LIST*3);
    l_list = (double *) malloc (sizeof(double)*MAX_L_LIST);
    double rho = Npart2/(cell*cell*cell);
    int* counts = (int *) malloc (sizeof(int)*nbins);
    for (int i=0; i<nbins; i++){
        counts[i] = 0;
    }
    double dbins=rcut/nbins;
    for (int step=0; step < Nsteps; step++)
        for (int i=0; i < Npart1; i++)
            for (int j=0; j<Npart2; j++){
                get_distances(&Rpart1[3*Npart1*step+i*3], &Rpart2[3*Npart2*step+j*3],cell, rcut);

                for (int k=0; k<MAX_L_LIST; k++)
                    if (l_list[k] > 0 && l_list[k] < rcut ){
                        counts[(int)(l_list[k]/dbins)]++;
                    }
            }
    
    
    for (int i=0; i<nbins; i++){
        g_r[i] = ( counts[i]/(4*3.14*(pow(dbins*(i+0.5),2)*dbins)) / Npart1/Nsteps) / rho;
    }

    free(x_list);
    free(l_list);
    free(counts);
    
    return 0;
}