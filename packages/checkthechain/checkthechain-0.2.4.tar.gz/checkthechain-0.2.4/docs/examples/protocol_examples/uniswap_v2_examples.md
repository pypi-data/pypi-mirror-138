
# Uniswap V2 Examples

can import using

```python
from uniswap_v2 import uniswap_v2_utils
```

## Get Pool Mints, Burns, and Swaps

```python
pool = '0x94b0a3d511b6ecdb17ebf877278ab030acb0a878'

swaps = await uniswap_v2_utils.async_get_pool_swaps(pool)
mints = await uniswap_v2_utils.async_get_pool_mints(pool)
burns = await uniswap_v2_utils.async_get_pool_burns(pool)
```

