# more\_bisect

A binary search extension of Python `bisect` module that enables flexible comparisons.
Includes these functions:

- `first_pos_eq`: find the first index of value equal to `x`
- `last_pos_eq`: find the last index of value equal to `x`
- `last_pos_lt`: find the last index of value less than `x`
- `last_pos_le`: find the last index of value less than or equal to `x`
- `first_pos_gt`: find the first index of value greater than `x`
- `first_pos_ge`: find the first index of value greater than or equal to `x`
- `bisect_left`: the same as `bisect.bisect_left`
- `bisect_right`: the same as `bisect.bisect_right`
- `last_closest_to`: find the last index of value closest to `x`
- `first_closest_to`: find the first index of value closest to `x`

All functions are of the same signature:

    (x, a=None, lo=None, hi=None, key=None)

- `x`: the value based on which to search
- `a`: the array to search for; if provided `None`, `key` will be used to form an array (see below)
- `lo`, `hi`: bound the range (left inclusive, right exclusive) of array to search
- `key`: if `a` is not `None`, `a[i]` will be mapped to `key(a[i])` on each index `i`;
  if `a` is `None`, `a[i]` will be mapped to `key(i)` on each index `i`.
  This way, when `a` is `None`, not all elements of the *fake* array need to be given before binary search 


## Installation

	pip install more_bisect

View the package at [PyPI](https://pypi.org/project/more-bisect/0.1.0/).


## Examples

1. Invoke `first_pos_eq` with an array:

```python
import more_bisect
more_bisect.first_pos_eq(3, [2, 3, 3, 4, 4, 4])
```

2. Invoke `last_closest_to` with a function (the code snippet can be a solution to [LeetCode 887 Super Egg Drop](https://leetcode.com/problems/super-egg-drop/):

```python
import more_bisect
class Solution:
    def superEggDrop(self, k: int, n: int) -> int:
        memo = {}

        def recur(k, n):
            if (k, n) not in memo:
                if n == 0:
                    ans = 0
                elif k == 1:
                    ans = n
                else:
                    i = more_bisect.last_closest_to(
                            0, lo=1, hi=n + 1,
                            key=lambda x: recur(k - 1, x - 1) - recur(k, n - x))
                    ans = 1 + max(recur(k - 1, i - 1), recur(k, n - i))
                memo[k, n] = ans
            return memo[k, n]
        
        return recur(k, n)
```
