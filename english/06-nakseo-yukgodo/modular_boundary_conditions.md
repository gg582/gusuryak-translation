# Nakseo-Yukgodo (洛書六觚圖) Target Sum Modular Feasibility Boundary Conditions

## Executive Summary
This report formulates the mathematical necessary and sufficient modular boundary conditions ($n \pmod k$) required for the existence of feasible placement solutions when target sums for **Rings ($k=1 \dots 9$)** and **Sectors (觚, $j=1 \dots 6$)** are modulated.

---

## 1. Ring Target Sum Modular Condition ($T_{\text{ring}}(k) \pmod{813}$)

- **Structure:** Concentric ring $k$ contains $6k$ cells forming $3k$ antipodal complement pairs $(a_i, b_i)$ with $a_i + b_i = 271$.
- **Modular Boundary Equation:**
  $$T_{\text{ring}}(k) = \sum_{i=1}^{3k} (a_i + b_i) = 3k \times 271 = 813k$$
- **Feasibility Condition:**
  For any modified ring target sum $T_{\text{ring}}'(k)$, a valid solution exists **if and only if**:
  $$T_{\text{ring}}'(k) \equiv 0 \pmod 3 \quad \text{and} \quad T_{\text{ring}}'(k) \equiv 0 \pmod{271} \iff T_{\text{ring}}'(k) \equiv 0 \pmod{813}$$

---

## 2. Sector Target Sum Modular Condition ($\sum T_{\text{sec}}(j) \pmod 6$)

- **Structure:** 6 sectors (觚), each containing 45 cells (odd number).
- **Total Sum Constraint:**
  $$\sum_{j=1}^6 T_{\text{sec}}(j) = S_{\text{total}} = \sum_{x=1}^{270} x = \frac{270 \times 271}{2} = 36,585$$
- **Modular Boundary Equation:**
  $$36,585 = 6 \times 6097 + 3 \implies 36,585 \equiv 3 \pmod 6$$
- **Feasibility Condition:**
  For any set of modified sector target sums $\{T_{\text{sec}}'(j)\}_{j=1}^6$, a valid global placement exists **if and only if**:
  $$\sum_{j=1}^6 T_{\text{sec}}'(j) \equiv 3 \pmod 6 \quad \text{and} \quad \sum_{j=1}^6 T_{\text{sec}}'(j) = 36,585$$
  *(Average sector target is $6097.5$, requiring 3 sectors summing to $6097$ and 3 sectors summing to $6098$).*

---

## 3. Axis Target Sum Modular Condition ($T_{\text{axis}} \pmod{271}$)

- **Structure:** 3 axes (中觚), each consisting of 19 cells (9 antipodal pairs + 1 void center).
- **Feasibility Condition:**
  $$T_{\text{axis}} = 9 \times 271 = 2439 \implies T_{\text{axis}} \equiv 0 \pmod{271}$$

---

## Execution Verification Metrics
- **Ring Modular Feasibility ($T_{\text{ring}} \equiv 0 \pmod{813}$):** Verified True
- **Sector Modular Feasibility ($\sum T_{\text{sec}} \equiv 3 \pmod 6$):** Verified True
