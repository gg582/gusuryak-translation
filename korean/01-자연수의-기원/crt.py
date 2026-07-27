def crt(r_list, m_list):
    # 1. 전체 곱 M
    M = 1
    for m in m_list:
        M *= m

    # 2. 연기수 (M_i = M / m_i)
    M_list = [M // m for m in m_list]

    # 3. 대연구일술: 필산 나눗셈 축약법으로 승수(z) 도출
    z_list = []
    for M_i, m in zip(M_list, m_list):
        # M_i를 m으로 나눈 나머지를 나눗셈 시작값으로 사용
        a = M_i % m
        b = m
        x0, x1 = 1, 0

        # 나머지가 0이 될 때까지 나눗셈 몫(q)을 구하며 축약
        while b > 0:
            q = a // b
            a, b = b, a % b
            x0, x1 = x1, x0 - q * x1

        # 승수(z) 확정
        z = x0 % m
        z_list.append(z)

    # 4. 각 항의 곱을 누적 후 전체 곱 M으로 감산
    X = sum(r * M_i * z for r, M_i, z in zip(r_list, M_list, z_list))

    return X % M


if __name__ == "__main__":
    assert crt([2, 3, 2], [3, 5, 7]) == 23
    print("대연술의 결과가 23이 맞습니다.")
