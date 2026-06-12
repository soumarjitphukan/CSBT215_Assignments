#include <stdio.h>
#include <time.h>

void linear_time(int n) {
    volatile int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += i;
    }
}

void quadratic_time(int n) {
    volatile int count = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            count++;
        }
    }
}

void logarithmic_time(int n) {
    volatile int count = 0;
    for (int i = 1; i < n; i *= 2) {
        count++;
    }
}

int main() {
    int choice, n;
    clock_t start, end;
    double time_taken;

    while (1) {
        printf("\nTime Complexity Analysis\n");
        printf("1. Linear Time O(n)\n");
        printf("2. Quadratic Time O(n^2)\n");
        printf("3. Logarithmic Time O(log n)\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        if (choice == 4) {
            printf("Exiting...\n");
            break;
        }

        printf("Enter input size n: ");
        scanf("%d", &n);

        start = clock();

        switch (choice) {
            case 1:
                linear_time(n);
                break;
            case 2:
                quadratic_time(n);
                break;
            case 3:
                logarithmic_time(n);
                break;
            default:
                printf("Invalid choice\n");
                continue;
        }

        end = clock();
        time_taken = (double)(end - start) / CLOCKS_PER_SEC;

        printf("Time taken: %f seconds\n", time_taken);
    }

    return 0;
}

