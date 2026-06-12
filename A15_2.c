#include <stdio.h>
#include <pthread.h>

#define NUM_THREADS 8
#define INCREMENTS  1000000
#define EXPECTED    (NUM_THREADS * INCREMENTS)

long long counter = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *increment(void *arg) {
    for (int i = 0; i < INCREMENTS; i++) {
        pthread_mutex_lock(&lock);
        counter++;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main(void) {
    pthread_t threads[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++)
        pthread_create(&threads[i], NULL, increment, NULL);

    for (int i = 0; i < NUM_THREADS; i++)
        pthread_join(threads[i], NULL);

    pthread_mutex_destroy(&lock);

    printf("Expected : %d\n", EXPECTED);
    printf("Got      : %lld\n", counter);
    printf("Correct  : %s\n", counter == EXPECTED ? "YES" : "NO");

    return 0;
}