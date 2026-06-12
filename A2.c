#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>

long get_memory_usage() {
    struct rusage r_usage;
    getrusage(RUSAGE_SELF, &r_usage);
    return r_usage.ru_maxrss;
}

void constant_space(int n) {
    long before = get_memory_usage();
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += i;
    }
    long after = get_memory_usage();
    long diff = after - before;
    unsigned long calculated = 0;
    printf("Constant space for n=%d: %ld KB (calculated: %lu KB)\n", n, diff, calculated);
}

void linear_space(int n) {
    long before = get_memory_usage();
    int *arr = (int *)malloc(n * sizeof(int));
    if (!arr) {
        printf("Allocation failed for linear space with n=%d\n", n);
        return;
    }
    for (int i = 0; i < n; i++) {
        arr[i] = i;
    }
    long after = get_memory_usage();
    long diff = after - before;
    unsigned long calculated = (n * sizeof(int)) / 1024;
    printf("Linear space for n=%d: %ld KB (calculated: %lu KB)\n", n, diff, calculated);
    free(arr);
}

void quadratic_space(int n) {
    long before = get_memory_usage();
    int **matrix = (int **)malloc(n * sizeof(int *));
    if (!matrix) {
        printf("Allocation failed for quadratic space with n=%d\n", n);
        return;
    }
    for (int i = 0; i < n; i++) {
        matrix[i] = (int *)malloc(n * sizeof(int));
        if (!matrix[i]) {
            printf("Allocation failed for quadratic space with n=%d\n", n);
            return;
        }
        for (int j = 0; j < n; j++) {
            matrix[i][j] = i * j;
        }
    }
    long after = get_memory_usage();
    long diff = after - before;
    unsigned long calculated = (n * sizeof(int *) + n * n * sizeof(int)) / 1024;
    printf("Quadratic space for n=%d: %ld KB (calculated: %lu KB)\n", n, diff, calculated);
    for (int i = 0; i < n; i++) {
        free(matrix[i]);
    }
    free(matrix);
}

int main() {
    int sizes[] = {10, 100, 1000, 10000};
    int num_sizes = sizeof(sizes) / sizeof(sizes[0]);
    
    for (int i = 0; i < num_sizes; i++) {
        int n = sizes[i];
        printf("\nTesting with n = %d\n", n);
        constant_space(n);
        linear_space(n);
        if (n <= 1000) {
            quadratic_space(n);
        } else {
            printf("Skipping quadratic space for n=%d to avoid high memory consumption\n", n);
        }
    }
    
    return 0;
}
