#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

typedef struct {
    bool is_negative;
    size_t len;
    uint32_t *data;
} BigInt32;

int count_zeroes_from_right(const uint32_t *num, size_t len);
BigInt32 multiply_bigint(const BigInt32 *t, const BigInt32 *s);
void print_bigint(const char *name, const BigInt32 *num);
void free_bigint(BigInt32 *num);

int main(void) {
    // Example 1: (-0x123456789ABCDEF0_00000000) * (0xFEDCBA9876543210)
    uint32_t t1_data[] = { 0x12345678, 0x9ABCDEF0, 0x00000000 };
    uint32_t s1_data[] = { 0xFEDCBA98, 0x76543210 };
    BigInt32 t1 = { .is_negative = true,  .len = 3, .data = t1_data };
    BigInt32 s1 = { .is_negative = false, .len = 2, .data = s1_data };

    printf("Test Case 1\n");
    print_bigint("t1", &t1);
    print_bigint("s1", &s1);
    BigInt32 res1 = multiply_bigint(&t1, &s1);
    print_bigint("res1", &res1);
    free_bigint(&res1);

    // Example 2: 8 words * 8 words -> 16 words 
    uint32_t t2_data[] = {
        0xFFFFFFFF, 0xEEEEEEEE, 0xDDDDDDDD, 0xCCCCCCCC,
        0xBBBBBBBB, 0xAAAAAAAA, 0x99999999, 0x00000000
    };
    uint32_t s2_data[] = {
        0x12345678, 0x87654321, 0xABCDEF01, 0x10FEDCBA,
        0x00112233, 0x44556677, 0x8899AABB, 0xCCDDEEFF
    };
    BigInt32 t2 = { .is_negative = true, .len = 8, .data = t2_data };
    BigInt32 s2 = { .is_negative = true, .len = 8, .data = s2_data };

    printf("\nTest Case 2 (256-bit x 256-bit)\n");
    print_bigint("t2", &t2);
    print_bigint("s2", &s2);
    BigInt32 res2 = multiply_bigint(&t2, &s2);
    print_bigint("res2", &res2);
    free_bigint(&res2);

    // Example 3: 16 words * 16 words -> 32 words 
    uint32_t t3_data[16] = {
        0xDEADBEEF, 0xCAFEBABE, 0x87654321, 0x12345678,
        0x0000FFFF, 0xFFFF0000, 0x10101010, 0x01010101,
        0xFFFFFFFF, 0xFFFFFFFF, 0x12340000, 0x00005678,
        0xABCDEF00, 0x00FEDCBA, 0x00000000, 0x00000000
    };
    uint32_t s3_data[16] = {
        0x11111111, 0x22222222, 0x33333333, 0x44444444,
        0x55555555, 0x66666666, 0x77777777, 0x88888888,
        0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
        0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0x00000000
    };
    BigInt32 t3 = { .is_negative = false, .len = 16, .data = t3_data };
    BigInt32 s3 = { .is_negative = true,  .len = 16, .data = s3_data };

    printf("\nTest Case 3 (512-bit x 512-bit)\n");
    print_bigint("t3", &t3);
    print_bigint("s3", &s3);
    BigInt32 res3 = multiply_bigint(&t3, &s3);
    print_bigint("res3", &res3);
    free_bigint(&res3);

    return 0;
}

int count_zeroes_from_right(const uint32_t *num, size_t len) {
    int idx = (int)len - 1;
    while (idx >= 0 && num[idx] == 0) {
        idx--;
    }
    return (int)len - 1 - idx;
}

BigInt32 multiply_bigint(const BigInt32 *t, const BigInt32 *s) {
    size_t res_len = t->len + s->len;
    uint32_t *result_data = (uint32_t *)calloc(res_len, sizeof(uint32_t));

    int t_zeroes = count_zeroes_from_right(t->data, t->len);
    int s_zeroes = count_zeroes_from_right(s->data, s->len);

    int t_start_from = (int)t->len - t_zeroes - 1;
    int s_start_from = (int)s->len - s_zeroes - 1;

    for (int i = t_start_from; i >= 0; i--) {
        for (int j = s_start_from; j >= 0; j--) {
            uint64_t prod = (uint64_t)t->data[i] * s->data[j];

            int pos_from_right = (t_start_from - i) + (s_start_from - j) + t_zeroes + s_zeroes;
            int res_idx = (int)res_len - 1 - pos_from_right;

            uint64_t sum = (uint64_t)result_data[res_idx] + prod;
            result_data[res_idx] = (uint32_t)(sum & 0xFFFFFFFFULL);
            uint64_t carry = sum >> 32;

            int idx = res_idx - 1;
            while (carry > 0 && idx >= 0) {
                uint64_t c_sum = (uint64_t)result_data[idx] + carry;
                result_data[idx] = (uint32_t)(c_sum & 0xFFFFFFFFULL);
                carry = c_sum >> 32;
                idx--;
            }
        }
    }

    bool is_zero = true;
    for (size_t i = 0; i < res_len; i++) {
        if (result_data[i] != 0) {
            is_zero = false;
            break;
        }
    }

    BigInt32 res = {
        .is_negative = is_zero ? false : (t->is_negative ^ s->is_negative),
        .len = res_len,
        .data = result_data
    };

    return res;
}

void print_bigint(const char *name, const BigInt32 *num) {
    printf("%s: %s0x", name, num->is_negative ? "-" : "+");
    
    size_t start = 0;
    while (start < num->len - 1 && num->data[start] == 0) {
        start++;
    }

    printf("%X", num->data[start]);
    for (size_t i = start + 1; i < num->len; i++) {
        printf("%08X", num->data[i]);
    }

    printf("  [Words: ");
    for (size_t i = 0; i < num->len; i++) {
        printf("%08X%s", num->data[i], (i == num->len - 1) ? "" : " ");
    }
    printf("]\n");
}

void free_bigint(BigInt32 *num) {
    if (num->data) {
        free(num->data);
        num->data = NULL;
    }
}
