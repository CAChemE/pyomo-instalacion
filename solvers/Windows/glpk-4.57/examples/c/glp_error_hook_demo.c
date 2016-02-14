/***********************************************************************
*  This code is part of WinGLPK
*
*  Copyright (C) 2010 Heinrich Schuchardt (xypron.glpk@gmx.de)
*
*  WinGLPK is free software: you can redistribute it and/or modify it
*  under the terms of the GNU General Public License as published by
*  the Free Software Foundation, either version 3 of the License, or
*  (at your option) any later version.
*
*  GLPK is distributed in the hope that it will be useful, but WITHOUT
*  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
*  or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
*  License for more details.
*
*  You should have received a copy of the GNU General Public License
*  along with GLPK. If not, see <http://www.gnu.org/licenses/>.
***********************************************************************/

/*
 * This example file demonstrates how to safely treat errors when
 * calling the glpk library.
 *
 * It creates a problem and alternativly adds 1 or -1 columns.
 * Trying to add -1 columns will cause an error to occur.
 */

#include <stdio.h>
#include <stdlib.h>
#include <setjmp.h>
#include "glpk.h"

void errorHook(void *in);
void buildModel(int forceError);

#define INFO struct sinfo

struct sinfo {
    char    *text;
    jmp_buf *env;
};

/*
 * This is the main function.
 */
int main(int argc, char** argv) {
    int i;
    printf("GLPK version: %s\n", glp_version());
    for (i = 1; i < 5; i++) {
        printf ("\nIteration %d", i);
        if (i & 1) {
            printf(", error expected to occur.\n");
        } else {
            printf(", success expected.\n");
        }
        if (runOptimizer(i)) {
            printf("An error has occured.\n");
        } else {
            printf("Successful execution.\n");
        }
    }
    return (EXIT_SUCCESS);
}

/**
 * This function secures calls to glpk with an error hook.
 * @param forceError force error if bit 0 = 1
 * @return ok code: 1 failure, 2 out of memory
 */
int runOptimizer(int forceError) {
    int ret = 0;
    INFO *info;
    info = (INFO*) malloc(sizeof(INFO));
    if (info == NULL) {
        return 2;
    }
    info->env = (jmp_buf *) malloc(sizeof(jmp_buf));
    if (info->env == NULL) {
        free(info);
        return 2;
    }
    info->text = "This information was passed to the hook function.";
    if (setjmp(*(info->env))) {
        printf("Post treatment of error.\n");
        ret = 1;
    } else {
        glp_error_hook(errorHook, info);
        buildModel(forceError);
    }
    glp_error_hook(NULL, NULL);
    free(info->env);
    free(info);
    return ret;
}

/**
 * Build a model with one column
 * @param forceError force error if bit 0 = 1
 */
void buildModel(int forceError) {
    glp_prob *lp;
    /* create problem */
    lp = glp_create_prob();
    if (forceError & 1) {
        /* add -1 column
         * this will cause an error.
         */
        glp_add_cols(lp, -1);
    } else {
        /* add 1 column */
        glp_add_cols(lp, 1);
    }
    /* delete problem */
    glp_delete_prob(lp);
}

/**
 * This hook function will be called if an error occured when
 * calling the glpk library
 */
void errorHook(void *in) {
    INFO *info;
    info = (INFO *) in;
    printf("%s\n",info->text);
    /* free glpk memory */
    glp_free_env();
    /* safely return */
    longjmp(info->env, 1);
}
