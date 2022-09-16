#ifndef CYGORITHMS_KMP_H
#define CYGORITHMS_KMP_H

#ifndef DLL_EXPORT
#define DLL_EXPORT __declspec(dllexport)
#endif

#ifdef __cplusplus
extern "C" {
#endif

#include <stddef.h>

DLL_EXPORT int* build_kmp_table(const char *query, size_t len);
DLL_EXPORT int* do_match(int *positions, const char *text, size_t text_len, const char *query, size_t query_len, int *kmp_table);
DLL_EXPORT void kmp_free(int *positions, int *kmp_table);

#ifdef __cplusplus
}
#endif

#endif // CYGORITHMS_KMP_H