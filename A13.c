#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char   *data;
    size_t  length;
    size_t  capacity;
} StringBuffer;

StringBuffer *sb_init(size_t initial_capacity) {
    StringBuffer *sb = malloc(sizeof(StringBuffer));
    if (!sb) return NULL;
    sb->data = malloc(initial_capacity);
    if (!sb->data) {
        free(sb);
        return NULL;
    }
    sb->data[0] = '\0';
    sb->length   = 0;
    sb->capacity = initial_capacity;
    return sb;
}

int sb_append(StringBuffer *sb, const char *str) {
    size_t slen = strlen(str);
    while (sb->length + slen + 1 > sb->capacity) {
        size_t  new_cap = sb->capacity * 2;
        char   *tmp     = realloc(sb->data, new_cap);
        if (!tmp) return -1;
        sb->data     = tmp;
        sb->capacity = new_cap;
    }
    memcpy(sb->data + sb->length, str, slen + 1);
    sb->length += slen;
    return 0;
}

void sb_free(StringBuffer *sb) {
    if (!sb) return;
    free(sb->data);
    free(sb);
}

int main(void) {
    StringBuffer *sb = sb_init(8);
    if (!sb) {
        fprintf(stderr, "sb_init failed\n");
        return 1;
    }

    printf("Initial   -> length: %zu, capacity: %zu\n", sb->length, sb->capacity);

    sb_append(sb, "Hello");
    printf("After 1st -> length: %zu, capacity: %zu, data: \"%s\"\n", sb->length, sb->capacity, sb->data);

    sb_append(sb, ", world");
    printf("After 2nd -> length: %zu, capacity: %zu, data: \"%s\"\n", sb->length, sb->capacity, sb->data);

    sb_append(sb, "! Dynamic buffers grow automatically.");
    printf("After 3rd -> length: %zu, capacity: %zu, data: \"%s\"\n", sb->length, sb->capacity, sb->data);

    sb_free(sb);
    printf("Buffer freed.\n");

    return 0;
}