#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

#define BUFFER_SIZE     8
#define NUM_PRODUCERS   3
#define NUM_CONSUMERS   3
#define ITEMS_PER_PRODUCER 5

typedef struct {
    int data[BUFFER_SIZE];
    int head;
    int tail;
    int count;
} RingBuffer;

typedef struct {
    RingBuffer  *buffer;
    sem_t       *sem_empty;
    sem_t       *sem_full;
    pthread_mutex_t *mutex;
    pthread_cond_t  *cond_not_empty;
    pthread_cond_t  *cond_not_full;
    int          id;
    int          items_to_produce;
} ThreadArgs;

static pthread_mutex_t stats_mutex = PTHREAD_MUTEX_INITIALIZER;
static int total_produced = 0;
static int total_consumed = 0;

static void timestamp(char *buf, size_t len) {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    long ms = ts.tv_nsec / 1000000;
    snprintf(buf, len, "%03ld", ms);
}

static void print_buffer_state(RingBuffer *buf) {
    printf("  [Buffer: ");
    for (int i = 0; i < BUFFER_SIZE; i++) {
        int idx = (buf->head + i) % BUFFER_SIZE;
        if (i < buf->count)
            printf("%3d", buf->data[idx]);
        else
            printf("  _");
    }
    printf(" ] (count=%d)\n", buf->count);
}

static void *producer(void *arg) {
    ThreadArgs *args = (ThreadArgs *)arg;

    for (int i = 0; i < args->items_to_produce; i++) {
        int item = (args->id * 100) + i + 1;
        usleep((rand() % 200 + 100) * 1000);

        sem_wait(args->sem_empty);
        pthread_mutex_lock(args->mutex);

        while (args->buffer->count == BUFFER_SIZE)
            pthread_cond_wait(args->cond_not_full, args->mutex);

        args->buffer->data[args->buffer->tail] = item;
        args->buffer->tail = (args->buffer->tail + 1) % BUFFER_SIZE;
        args->buffer->count++;

        char ts[16];
        timestamp(ts, sizeof(ts));
        printf("[+%s ms] PRODUCER-%d  produced item %3d  | count after: %d\n",
               ts, args->id, item, args->buffer->count);
        print_buffer_state(args->buffer);

        pthread_mutex_lock(&stats_mutex);
        total_produced++;
        pthread_mutex_unlock(&stats_mutex);

        pthread_cond_signal(args->cond_not_empty);
        pthread_mutex_unlock(args->mutex);
        sem_post(args->sem_full);
    }

    char ts[16];
    timestamp(ts, sizeof(ts));
    printf("[+%s ms] PRODUCER-%d  finished all %d items\n",
           ts, args->id, args->items_to_produce);
    return NULL;
}

static void *consumer(void *arg) {
    ThreadArgs *args = (ThreadArgs *)arg;
    int expected = NUM_PRODUCERS * args->items_to_produce;

    while (1) {
        pthread_mutex_lock(&stats_mutex);
        int done = (total_consumed >= expected);
        pthread_mutex_unlock(&stats_mutex);
        if (done) break;

        int rc = sem_trywait(args->sem_full);
        if (rc != 0) {
            usleep(50000);
            continue;
        }

        pthread_mutex_lock(args->mutex);

        while (args->buffer->count == 0) {
            pthread_mutex_lock(&stats_mutex);
            int all_done = (total_consumed >= expected);
            pthread_mutex_unlock(&stats_mutex);
            if (all_done) {
                pthread_mutex_unlock(args->mutex);
                sem_post(args->sem_full);
                return NULL;
            }
            pthread_cond_wait(args->cond_not_empty, args->mutex);
        }

        int item = args->buffer->data[args->buffer->head];
        args->buffer->head = (args->buffer->head + 1) % BUFFER_SIZE;
        args->buffer->count--;

        char ts[16];
        timestamp(ts, sizeof(ts));
        printf("[+%s ms] CONSUMER-%d  consumed item %3d  | count after: %d\n",
               ts, args->id, item, args->buffer->count);
        print_buffer_state(args->buffer);

        pthread_mutex_lock(&stats_mutex);
        total_consumed++;
        int cur = total_consumed;
        pthread_mutex_unlock(&stats_mutex);

        pthread_cond_signal(args->cond_not_full);
        pthread_mutex_unlock(args->mutex);
        sem_post(args->sem_empty);

        if (cur >= expected) break;

        usleep((rand() % 300 + 150) * 1000);
    }

    char ts[16];
    timestamp(ts, sizeof(ts));
    printf("[+%s ms] CONSUMER-%d  exiting\n", ts, args->id);
    return NULL;
}

int main(void) {
    srand((unsigned)time(NULL));

    printf("...\n");
    printf("  Producer-Consumer with Semaphores + Cond Vars\n");
    printf("  Producers: %d  |  Consumers: %d  |  Buffer: %d\n",
           NUM_PRODUCERS, NUM_CONSUMERS, BUFFER_SIZE);
    printf("  Items per producer: %d  |  Total items: %d\n",
           ITEMS_PER_PRODUCER, NUM_PRODUCERS * ITEMS_PER_PRODUCER);
    printf("...\n\n");

    RingBuffer buffer = { .head = 0, .tail = 0, .count = 0 };

    sem_t sem_empty, sem_full;
    sem_init(&sem_empty, 0, BUFFER_SIZE);
    sem_init(&sem_full,  0, 0);

    pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
    pthread_cond_t  cond_not_empty = PTHREAD_COND_INITIALIZER;
    pthread_cond_t  cond_not_full  = PTHREAD_COND_INITIALIZER;

    pthread_t prod_threads[NUM_PRODUCERS];
    pthread_t cons_threads[NUM_CONSUMERS];
    ThreadArgs prod_args[NUM_PRODUCERS];
    ThreadArgs cons_args[NUM_CONSUMERS];

    for (int i = 0; i < NUM_PRODUCERS; i++) {
        prod_args[i] = (ThreadArgs){
            .buffer          = &buffer,
            .sem_empty       = &sem_empty,
            .sem_full        = &sem_full,
            .mutex           = &mutex,
            .cond_not_empty  = &cond_not_empty,
            .cond_not_full   = &cond_not_full,
            .id              = i + 1,
            .items_to_produce= ITEMS_PER_PRODUCER
        };
        pthread_create(&prod_threads[i], NULL, producer, &prod_args[i]);
    }

    for (int i = 0; i < NUM_CONSUMERS; i++) {
        cons_args[i] = (ThreadArgs){
            .buffer          = &buffer,
            .sem_empty       = &sem_empty,
            .sem_full        = &sem_full,
            .mutex           = &mutex,
            .cond_not_empty  = &cond_not_empty,
            .cond_not_full   = &cond_not_full,
            .id              = i + 1,
            .items_to_produce= ITEMS_PER_PRODUCER
        };
        pthread_create(&cons_threads[i], NULL, consumer, &cons_args[i]);
    }

    for (int i = 0; i < NUM_PRODUCERS; i++)
        pthread_join(prod_threads[i], NULL);

    pthread_mutex_lock(prod_args[0].mutex);
    pthread_cond_broadcast(&cond_not_empty);
    pthread_mutex_unlock(prod_args[0].mutex);

    for (int i = 0; i < NUM_CONSUMERS; i++)
        pthread_join(cons_threads[i], NULL);

    printf("\n...\n");
    printf("  Summary\n");
    printf("  Total produced : %d\n", total_produced);
    printf("  Total consumed : %d\n", total_consumed);
    printf("  Items in buffer: %d (should be 0)\n", buffer.count);
    printf("  Result         : %s\n",
           (total_produced == total_consumed && buffer.count == 0)
           ? "PASS — no data loss, no deadlock"
           : "FAIL — synchronization error detected");
    printf("...\n");

    sem_destroy(&sem_empty);
    sem_destroy(&sem_full);
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond_not_empty);
    pthread_cond_destroy(&cond_not_full);
    pthread_mutex_destroy(&stats_mutex);

    return 0;
}