from collections.abc import Mapping
from typing import Union

ValueType = Union[Mapping[str, bool], bool, None]
SubCategoryDict = Mapping[str, ValueType]
SubCategoryType = Union[SubCategoryDict, bool, None]
CategoryType = Union[Mapping[str, SubCategoryType], Mapping[str, ValueType], bool, None]
PolicyType = Mapping[str, CategoryType]
