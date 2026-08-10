#include <stdio.h>

int count_zeroes_from_right(const int *num, size_t len);
static void print_res(const char *tag, const int *t, size_t t_len, const int *res, size_t res_len, const int *s, size_t s_len);

int main(void) {
    int t[] = { 3, 0, 0 };
    size_t t_len = sizeof(t) / sizeof(t[0]);

    int s[] = { 1, 6 };
    size_t s_len = sizeof(s) / sizeof(s[0]);

    constexpr int RES_LEN = 4;
    int result[RES_LEN] = { 0 };

    int t_zeroes = count_zeroes_from_right(t, t_len);
    int s_zeroes = count_zeroes_from_right(s, s_len);

    int t_start_from = (int)t_len - t_zeroes - 1;
    int s_start_from = (int)s_len - s_zeroes - 1;

    print_res("Initial State", t, t_len, result, RES_LEN, s, s_len);
    printf("\nIndex multiplication and accumulation\n");

    for (auto i = t_start_from; i >= 0; i--) {
        for (auto j = s_start_from; j >= 0; j--) {
            int prod = t[i] * s[j];

            int pos_from_right = (t_start_from - i) + (s_start_from - j) + t_zeroes + s_zeroes;
            int res_idx = (RES_LEN - 1) - pos_from_right;

            int sum = result[res_idx] + prod;
            int digit = sum % 10;
            int carry = sum / 10;

            result[res_idx] = digit;

            int idx = res_idx - 1;
            int temp_carry = carry;
            while (temp_carry > 0 && idx >= 0) {
                int c_sum = result[idx] + temp_carry;
                result[idx] = c_sum % 10;
                temp_carry = c_sum / 10;
                idx--;
            }

            if (carry > 0) {
                printf("t[%d](%d) * s[%d](%d) = %2d  -> accumulates into %d->result[%d] %d->result[%d]\n",
                       i, t[i], j, s[j], prod, carry, res_idx - 1, digit, res_idx);
            } else {
                printf("t[%d](%d) * s[%d](%d) = %2d  -> accumulates into result[%d]\n",
                       i, t[i], j, s[j], prod, res_idx);
            }

            print_res("current result", t, t_len, result, RES_LEN, s, s_len);
        }
    }

    printf("\ncarry\n");
    for (auto idx = RES_LEN - 1; idx > 0; idx--) {
        if (result[idx] >= 10) {
            int carry = result[idx] / 10;
            result[idx - 1] += carry;
            result[idx] %= 10;

            printf("result[%d] carry applied (+%d -> result[%d])\n", idx, carry, idx - 1);
            print_res("  current result", t, t_len, result, RES_LEN, s, s_len);
        }
    }

    int start_print = 0;
    while (start_print < RES_LEN - 1 && result[start_print] == 0) {
        start_print++;
    }

    printf("\nfinal output: ");
    for (int i = start_print; i < RES_LEN; i++) {
        printf("%d", result[i]);
    }
    printf("\n");

    return 0;
}

int count_zeroes_from_right(const int *num, size_t len) {
    int idx = (int)len - 1;
    while (idx >= 0 && num[idx] == 0) {
        idx--;
    }
    return (int)len - 1 - idx;
}

static void print_res(const char *tag, const int *t, size_t t_len, const int *res, size_t res_len, const int *s, size_t s_len) {
    (void)tag;
    printf("[   ");
    for (size_t i = 0; i < t_len; i++) {
        printf("%d ", t[i]);
    }
    puts("]: t");

    printf("[ ");
    for (size_t i = 0; i < res_len; i++) {
        printf("%d ", res[i]);
    }
    puts("]: result");

    printf("[     ");
    for (size_t i = 0; i < s_len; i++) {
        printf("%d ", s[i]);
    }
    printf("]: s\n");
}
