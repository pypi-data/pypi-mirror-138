"""
Utility functions.

Author: Matt Hall, agilescientific.com
Licence: Apache 2.0

Copyright 2022 Agile Scientific

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import numpy as np


def is_numeric(a):
    """
    Decide if a sequence is numeric.

    Args:
        a (array): A sequence.

    Returns:
        bool: True if a is numeric.

    Example:
        >>> is_numeric([1, 2, 3])
        True
        >>> is_numeric(['a', 'b', 'c'])
        False
    """
    a = np.asarray(a)
    return np.issubdtype(a.dtype, np.number)


def generate_data(counts):
    """
    Generate data from a list of counts.

    Args:
        counts (array): A sequence of class counts.

    Returns:
        array: A sequence of classes matching the counts.

    Example:
        >>> generate_data([3, 5])
        [0, 0, 0, 1, 1, 1, 1, 1]
    """
    data = [c * [i] for i, c in enumerate(counts)]
    return [item for sublist in data for item in sublist]


def sorted_unique(a):
    """
    Unique items in appearance order.

    `np.unique` is sorted, `set()` is unordered, `pd.unique()` is fast, but we
    don't have to rely on it. This does the job, and is not too slow.

    Args:
        a (array): A sequence.

    Returns:
        array: The unique items, in order of first appearance.

    Example:
        >>> sorted_unique([3, 0, 0, 1, 3, 2, 3])
        array([3, 0, 1, 2])
    """
    a = np.asarray(a)
    _, idx = np.unique(a, return_index=True)
    return a[np.sort(idx)]
