# Precision Limitations

The Earth Mover's Distance implementation in PyEMD uses the Pele & Werman algorithm, which employs integer arithmetic internally for efficiency and numerical stability. This design choice introduces small precision errors in certain cases.

## How It Works

The C++ implementation normalizes inputs before computation:

1. **Normalization factors** are computed:
   - `PQnormFactor = 1000000 / max(sum(P), sum(Q))`
   - `CnormFactor = 1000000 / max(C)`

2. **Values are converted to integers** via rounding:
   - `iC[i][j] = floor(C[i][j] * CnormFactor + 0.5)`
   - `iP[i] = floor(P[i] * PQnormFactor + 0.5)`

3. **EMD is computed** using integer min-cost flow algorithm

4. **Result is unnormalized**:
   - `dist = int_dist / PQnormFactor / CnormFactor`

## Precision Impact

The rounding step can introduce small errors, typically less than 1%.

### Example

Given:
```python
distance_matrix = np.array([
    [2.236,  8795.2, 3.162],
    [8796.5, 0.0,    8792.1],
    [0.0,    8796.5, 5.0]
])
arr1 = np.array([0.5, 0.5, 0.0])
arr2 = np.array([0.0, 0.5, 0.5])
```

The EMD computation involves:
- `maxC = 8796.5`, so `CnormFactor = 113.68`
- `C[0][2] = 3.162` normalizes to `floor(3.162 * 113.68 + 0.5) = 359`
- True normalized value would be `359.47`

This rounding error propagates:
- **Returned EMD**: `1.5790`
- **Expected (flow × distance)**: `1.5811`
- **Error**: ~0.13%

## Factors Affecting Precision

1. **Distance values spanning many orders of magnitude** - Large `maxC` values reduce `CnormFactor`, causing more rounding in smaller distances

2. **Flow-distance correspondence** - The returned EMD may not exactly equal `sum(flow * distance_matrix)`

## Workarounds

To compute EMD directly from the flow matrix:
```python
emd_value, flow = emd_with_flow(P, Q, C)
exact_emd = np.sum(np.multiply(flow, C))
```

To reduce rounding error, normalize the distance matrix to avoid values spanning many orders of magnitude.

## References

- Pele, O. and Werman, M. (2009). "Fast and Robust Earth Mover's Distances." *ICCV 2009*.
- [GitHub Issue #32](https://github.com/wmayner/pyemd/issues/32) - Original report of this behavior
