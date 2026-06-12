#include <stdio.h>
#include <pthread.h>

#define NUM_THREADS 8
#define INCREMENTS  1000000
#define EXPECTED    (NUM_THREADS * INCREMENTS)

long long counter = 0;

void *increment(void *arg) {
    for (int i = 0; i < INCREMENTS; i++)
        counter++;
    return NULL;
}

int main(void) {
    pthread_t threads[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++)
        pthread_create(&threads[i], NULL, increment, NULL);

    for (int i = 0; i < NUM_THREADS; i++)
        pthread_join(threads[i], NULL);

    printf("Expected : %d\n", EXPECTED);
    printf("Got      : %lld\n", counter);
    printf("Lost     : %lld\n", (long long)EXPECTED - counter);

    return 0;
}