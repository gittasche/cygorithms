#ifndef CYGORITHMS_CTYPES_KMP_H
#define CYGORITHMS_CTYPES_KMP_H

#ifdef __cplusplus
#define EXTERN_C extern "C"
#include <cstddef>
#else
#define EXTERN_C
#include <stddef.h>
#endif // __cplusplus

#if defined(_MSC_VER) || defined(_WIN32)
#define DLL_EXPORT EXTERN_C __declspec(dllexport)
#else
#define DLL_EXPORT EXTERN_C __attribute__ ((visibility ("default")))
#endif // defined(_MSC_VER) || defined(_WIN32)

DLL_EXPORT int* build_kmp_table(const char *query, size_t len);
DLL_EXPORT int* do_match(int *positions, const char *text, size_t text_len, const char *query, size_t query_len, int *kmp_table);
DLL_EXPORT void kmp_free(int *positions, int *kmp_table);

#endif // CYGORITHMS_CTYPES_KMP_H