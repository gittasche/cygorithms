#include <stddef.h>
#include <stdlib.h>

#include "cygorithms_ctypes/kmp.h"


int* build_kmp_table(const char *query, size_t len)
{
    int pos = 1, cnd = 0;
    int *kmp_table;
    if ((kmp_table = (int*)malloc((len + 1) * sizeof(int))) == NULL)
        exit(1);

    kmp_table[0] = -1;

    while (pos < len)
    {
        if (query[pos] == query[cnd])
            kmp_table[pos] = kmp_table[cnd];
        else
        {
            kmp_table[pos] = cnd;
            while (cnd >= 0 && (query[pos] != query[cnd]))
                cnd = kmp_table[cnd];
        }
        pos++;
        cnd++;
    }
    kmp_table[pos] = cnd;

    return kmp_table;
}


int* do_match(int *num_positions, const char *text, size_t text_len, const char *query, size_t query_len, int *kmp_table)
{
    int j = 0, k = 0;
    int *positions, *safe_buffer;
    if ((positions = (int*)malloc(0)) == NULL)
        exit(1);

    while (j < text_len)
    {
        if (query[k] == text[j])
        {
            j++;
            k++;
            if (k == query_len)
            {
                safe_buffer = positions;
                if ((positions = realloc(positions, (*num_positions + 1) * sizeof(int))) == NULL)
                {
                    free(safe_buffer);
                    exit(1);
                }
                positions[*num_positions] = j - k;
                (*num_positions)++;
                k = kmp_table[k];
            }
        }
        else
        {
            k = kmp_table[k];
            if (k < 0)
            {
                j++;
                k++;
            }
        }
    }

    return positions;
}

void kmp_free(int *positions, int *kmp_table)
{
    free(positions);
    free(kmp_table);
}
