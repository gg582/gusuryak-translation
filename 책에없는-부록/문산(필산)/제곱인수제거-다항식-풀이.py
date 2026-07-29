import sympy as sp

def horner_eval(poly_expr, var, val):
    """
    호너법(Horner's Method)을 이용해 특정 x = val에서의 함숫값을 O(n)으로 계산합니다.
    """
    # SymPy 다항식 객체 변환 및 계수 추출 (고차항부터 저차항 순)
    poly = sp.Poly(poly_expr, var)
    coeffs = poly.all_coeffs()
    
    result = 0
    for coeff in coeffs:
        result = result * val + coeff
        
    return result

def reduce_polynomial_roots(poly_expr, var):
    """
    유클리드 호제법을 이용해 다항식의 중복 해를 다듬고,
    해의 유실 없이 차수가 낮아진 다항식 Q(x)와 중근 다항식 G(x)를 반환합니다.
    """
    # 1. 도함수 P'(x) 계산
    poly_diff = sp.diff(poly_expr, var)
    
    # 2. 유클리드 호제법을 통한 최대공약수 G(x) = gcd(P(x), P'(x)) 계산
    gcd_poly = sp.gcd(poly_expr, poly_diff)
    
    # 3. 해의 유실 없는 차수 축소 다항식 Q(x) = P(x) / G(x) 계산
    reduced_poly = sp.simplify(poly_expr / gcd_poly)
    
    return gcd_poly, reduced_poly

# --------------------------------------------------
# 사용 예시
# --------------------------------------------------
x = sp.Symbol('x')

# 예시 다항식: P(x) = (x - 2)^3 * (x + 1)^2 * (x - 5)
P = (x - 2)**3 * (x + 1)**2 * (x - 5)
P_expanded = sp.expand(P)

print(f"원래 다항식 P(x) [6차]: {P_expanded}")

# 1. Square-Free Reduction 적용 (차수 축소)
G, Q = reduce_polynomial_roots(P_expanded, x)

print(f"\n1. 유클리드 호제법 결과 G(x) = gcd(P, P') [3차]: {sp.expand(G)}")
print(f"2. 해를 잃지 않는 차수 축소 다항식 Q(x) = P / G [3차]: {sp.expand(Q)}")

# 2. 축소된 다항식 Q(x)에 호너법 적용 (함숫값 계산)
eval_point = 3.0
q_val_horner = horner_eval(Q, x, eval_point)
q_val_direct = Q.subs(x, eval_point)

print(f"\n[호너법 검증]")
print(f"x = {eval_point} 일 때 축소 다항식 Q({eval_point}) 함숫값 (호너법): {q_val_horner}")
print(f"x = {eval_point} 일 때 축소 다항식 Q({eval_point}) 함숫값 (직접대입): {q_val_direct}")

# 3. 최종 해 목록
original_roots = sp.solve(P_expanded, x)
reduced_roots = sp.solve(Q, x)

print(f"\n원래 식 P(x)=0 의 해 목록: {original_roots}")
print(f"축소 식 Q(x)=0 의 해 목록: {reduced_roots}")
