import sympy as sp


def horner_eval(poly_expr, var, val):
    """호너법으로 다항식 ``poly_expr``의 ``var=val`` 값을 계산한다."""
    result = 0
    for coeff in sp.Poly(poly_expr, var).all_coeffs():
        result = result * val + coeff
    return result


def square_free_part(poly_expr, var):
    """G = gcd(P, P') 및 중복도를 제거한 Q = P/G를 반환한다."""
    p = sp.Poly(poly_expr, var)
    g = sp.gcd(p, p.diff())
    q = p.exquo(g)
    return g.as_expr(), q.as_expr()


def real_root_intervals(poly_expr, var):
    """Q의 서로 다른 실근을 포함하는 유리수 구간(또는 정확한 근)을 구한다."""
    # Q는 square-free이므로 각 항목의 중복도는 언제나 1이다.
    return [interval for interval, _ in sp.polys.polytools.intervals(
        sp.Poly(poly_expr, var), eps=sp.Rational(1, 10**12)
    )]


def initial_value(interval):
    """분리 구간의 중점(정확한 근이면 그 근)을 뉴턴법 초기값으로 사용한다."""
    left, right = interval
    return float(left if left == right else (left + right) / 2)


def newton_root_horner(
    q_expr,
    var,
    initial,
    tolerance=1e-12,
    max_iterations=100,
    cancel_quadratic_error=True,
):
    """호너법 기반 뉴턴법에 2차 오차항 소거 보정을 적용해 근을 구한다.

    ``f/f'``는 통상의 뉴턴 보정량이다. ``f''/(2f') * (f/f')**2``를
    추가로 빼면 테일러 전개의 선도 2차 오차항이 소거되어, 단순근에서는
    3차 수렴하는 Chebyshev(수정 뉴턴) 보정이 된다.
    """
    dq_expr = sp.diff(q_expr, var)
    d2q_expr = sp.diff(dq_expr, var)
    current = float(initial)

    for _ in range(max_iterations):
        # 모든 다항식 평가는 반복 내부에서 호너법으로 수행한다.
        fx = float(horner_eval(q_expr, var, current))
        dfx = float(horner_eval(dq_expr, var, current))
        if abs(dfx) < tolerance:
            raise ZeroDivisionError("뉴턴법 도함숫값이 0에 너무 가깝습니다.")

        newton_correction = fx / dfx
        error_correction = 0.0
        if cancel_quadratic_error:
            d2fx = float(horner_eval(d2q_expr, var, current))
            # 선도 2차 오차항: (Q'' / (2 Q')) * (Q / Q')^2
            error_correction = 0.5 * d2fx / dfx * newton_correction**2

        next_value = current - newton_correction - error_correction
        residual = float(horner_eval(q_expr, var, next_value))
        step_error = abs(next_value - current)
        if step_error < tolerance and abs(residual) < tolerance:
            return next_value
        current = next_value

    raise RuntimeError("뉴턴법이 지정한 반복 횟수 안에 수렴하지 않았습니다.")


def root_multiplicity(poly_expr, var, root, tolerance=1e-7):
    """P, P', ...를 검사하여 수치 근 ``root``의 원래 중복도를 복원한다."""
    derivative = poly_expr
    multiplicity = 0
    while derivative != 0:
        if abs(complex(derivative.subs(var, root))) > tolerance:
            break
        multiplicity += 1
        derivative = sp.diff(derivative, var)
    return multiplicity


# --------------------------------------------------
# 근 찾기 파이프라인 예시
# --------------------------------------------------
x = sp.Symbol("x")
P = sp.expand((x - 2)**3 * (x + 1)**2 * (x - 5))

print(f"원래 다항식 P(x) [6차]: {P}")

# P -> gcd(P, P') -> square-free part Q
G, Q = square_free_part(P, x)
print(f"\n1. G(x) = gcd(P, P') [3차]: {sp.expand(G)}")
print(f"2. Square-free part Q(x) = P / G [3차]: {sp.expand(Q)}")

# Q의 근 구간 분리 -> 초기값 -> (호너법 및 2차 오차항 소거를 포함한) 뉴턴 반복
intervals = real_root_intervals(Q, x)
print("\n3. Q의 실근 분리 구간과 수정 뉴턴법 결과 (2차 오차항 소거)")
found_roots = []
for interval in intervals:
    start = initial_value(interval)
    root = newton_root_horner(Q, x, start)
    multiplicity = root_multiplicity(P, x, root)
    found_roots.append((root, multiplicity))
    print(
        f"   구간 {interval}, 초기값 {start:.12g}"
        f" -> 근 {root:.12g}, P에서의 중복도 {multiplicity}"
    )

print("\n4. 근 복원 결과 (근, 중복도):")
print(found_roots)
