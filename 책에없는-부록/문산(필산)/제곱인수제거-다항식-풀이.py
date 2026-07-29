import sympy as sp


def horner_eval(poly_expr, var, val):
    """Evaluate a polynomial at var=val using Horner's method."""
    poly = sp.Poly(poly_expr, var)
    result = 0

    for coefficient in poly.all_coeffs():
        result = result * val + coefficient

    return result


def square_free_part(poly_expr, var):
    """Return gcd(P, P') and the square-free part P / gcd(P, P')."""
    poly = sp.Poly(poly_expr, var)
    gcd_poly = sp.gcd(poly, poly.diff())
    reduced_poly = poly.exquo(gcd_poly)

    return gcd_poly.as_expr(), reduced_poly.as_expr()


def square_free_factors(poly_expr, var):
    """Return square-free factors together with their exact multiplicities."""
    poly = sp.Poly(poly_expr, var)
    content, factors = sp.sqf_list(poly)

    return content, [
        (factor.as_expr(), multiplicity)
        for factor, multiplicity in factors
    ]


def real_root_intervals(poly_expr, var, interval_epsilon=sp.Rational(1, 10**12)):
    """Return rational isolating intervals for all distinct real roots."""
    poly = sp.Poly(poly_expr, var)

    return [
        interval
        for interval, _multiplicity in sp.intervals(
            poly,
            eps=interval_epsilon,
        )
    ]


def initial_value(interval):
    """Return the midpoint of an isolating interval as a floating-point value."""
    left, right = interval

    if left == right:
        return float(left)

    return float((left + right) / 2)


def newton_root_horner(
    poly_expr,
    var,
    initial,
    step_tolerance=1e-12,
    residual_tolerance=1e-12,
    derivative_tolerance=1e-14,
    max_iterations=100,
    cancel_quadratic_error=True,
):
    """Find a simple root using Horner evaluation and Chebyshev correction.

    The ordinary Newton correction is f/f'. When enabled, the additional term

        f'' / (2f') * (f/f')**2

    cancels the leading quadratic error term and gives local cubic convergence
    for a simple root.
    """
    first_derivative = sp.diff(poly_expr, var)
    second_derivative = sp.diff(first_derivative, var)

    current = float(initial)

    for iteration in range(1, max_iterations + 1):
        function_value = float(horner_eval(poly_expr, var, current))
        derivative_value = float(
            horner_eval(first_derivative, var, current)
        )

        if abs(derivative_value) <= derivative_tolerance:
            raise ZeroDivisionError(
                f"Derivative is too close to zero at iteration {iteration}: "
                f"x={current!r}, f'(x)={derivative_value!r}"
            )

        newton_correction = function_value / derivative_value
        chebyshev_correction = 0.0

        if cancel_quadratic_error:
            second_derivative_value = float(
                horner_eval(second_derivative, var, current)
            )
            chebyshev_correction = (
                0.5
                * second_derivative_value
                / derivative_value
                * newton_correction**2
            )

        next_value = (
            current
            - newton_correction
            - chebyshev_correction
        )

        residual = abs(
            float(horner_eval(poly_expr, var, next_value))
        )
        absolute_step = abs(next_value - current)
        relative_step_limit = (
            step_tolerance * max(1.0, abs(next_value))
        )

        if (
            absolute_step <= relative_step_limit
            and residual <= residual_tolerance
        ):
            return next_value, iteration, residual

        current = next_value

    raise RuntimeError(
        f"Root iteration did not converge within {max_iterations} iterations."
    )


def find_real_roots_with_multiplicity(
    poly_expr,
    var,
    interval_epsilon=sp.Rational(1, 10**12),
    step_tolerance=1e-12,
    residual_tolerance=1e-12,
    derivative_tolerance=1e-14,
    max_iterations=100,
    cancel_quadratic_error=True,
):
    """Find all real roots and recover exact multiplicities algebraically.

    Each square-free factor is processed independently. Every root of a factor
    inherits that factor's multiplicity in the original polynomial.
    """
    _content, factors = square_free_factors(poly_expr, var)
    roots = []

    for factor_expr, multiplicity in factors:
        intervals = real_root_intervals(
            factor_expr,
            var,
            interval_epsilon=interval_epsilon,
        )

        for interval in intervals:
            start = initial_value(interval)

            root, iterations, residual = newton_root_horner(
                factor_expr,
                var,
                start,
                step_tolerance=step_tolerance,
                residual_tolerance=residual_tolerance,
                derivative_tolerance=derivative_tolerance,
                max_iterations=max_iterations,
                cancel_quadratic_error=cancel_quadratic_error,
            )

            roots.append(
                {
                    "root": root,
                    "multiplicity": multiplicity,
                    "factor": factor_expr,
                    "interval": interval,
                    "initial": start,
                    "iterations": iterations,
                    "factor_residual": residual,
                }
            )

    roots.sort(key=lambda item: item["root"])
    return roots


x = sp.Symbol("x")

P = sp.expand(
    (x - 2) ** 3
    * (x + 1) ** 2
    * (x - 5)
)

print(f"Original polynomial P(x) [degree {sp.degree(P, x)}]:")
print(P)

G, Q = square_free_part(P, x)

print("\n1. Repeated-factor gcd G(x) = gcd(P, P'):")
print(sp.expand(G))

print("\n2. Square-free part Q(x) = P / G:")
print(sp.expand(Q))

content, factors = square_free_factors(P, x)

print("\n3. Exact square-free factorization:")
print(f"Content: {content}")

for factor_expr, multiplicity in factors:
    print(
        f"Factor: {sp.expand(factor_expr)}, "
        f"multiplicity: {multiplicity}"
    )

found_roots = find_real_roots_with_multiplicity(
    P,
    x,
    cancel_quadratic_error=True,
)

print("\n4. Real-root isolation and Chebyshev iteration:")

for result in found_roots:
    root = result["root"]
    multiplicity = result["multiplicity"]
    interval = result["interval"]
    initial = result["initial"]
    iterations = result["iterations"]
    factor_residual = result["factor_residual"]

    original_residual = abs(float(horner_eval(P, x, root)))

    print(
        f"Interval {interval}, "
        f"initial {initial:.12g} "
        f"-> root {root:.12g}, "
        f"multiplicity {multiplicity}, "
        f"iterations {iterations}, "
        f"factor residual {factor_residual:.3e}, "
        f"P residual {original_residual:.3e}"
    )

root_multiplicity_pairs = [
    (result["root"], result["multiplicity"])
    for result in found_roots
]

print("\n5. Restored roots as (root, multiplicity):")
print(root_multiplicity_pairs)

print("\n6. SymPy exact reference:")
print(sp.roots(P, x))
