""" Strategy Pattern – Sorting Service

    Problem:

    Create a sorting utility that can apply different algorithms (Bubble, Merge, Quick) to an integer list.

    - The client picks or changes the algorithm at runtime.
    - The chosen strategy sorts the list in place.
    - If no strategy is set, the context raises an error.

    Real‐World Analogy:

    Like choosing between walking, driving or cycling based on distance and traffic, you select the best sorting method for your data.

             +-------------------------+
             | «interface»             |
             | SortingStrategy         |
             |-------------------------|
             | + sort(array: List[int])|
             +-------------------------+
                       ^
                       |
    +------------------+------------------+------------------+
    |                  |                  |                  |
+----------------+ +--------------------+ +--------------------+
| BubbleSort     | | MergeSortStrategy  | | QuickSortStrategy  |
| Strategy       | |--------------------| |--------------------|
|----------------| | + sort(...)        | | + sort(...)        |
| + sort(...)    | | - _merge_sort(...) | | - _quick_sort(...) |
+----------------+ |                    | | - _partition(...)  |
                   |                    | | - _swap(...)       |
                   +--------------------+ +--------------------+


               +---------------------------+
               | SortingContext            |
               |---------------------------|
               | - _sorting_strategy       |
               |---------------------------|
               | + __init__(strategy)      |
               | + set_sorting_strategy()  |
               | + sort(array: List[int]) |
               +---------------------------+
                             |
                             | uses
                             ↓
                      SortingStrategy

"""



from abc import ABC, abstractmethod
from typing import Optional, List


from enum import Enum



class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, array: List[int]) -> None:
        pass

class SortingContext(ABC):
    # with a strategy to sort
    def __init__(self, strategy: SortingStrategy = None):
        if not isinstance(strategy, SortingStrategy):
            raise ValueError("A valid SortingStrategy is required")
        self._sorting_strategy: Optional[SortingStrategy] = strategy

    def set_sorting_strategy(self, strategy: SortingStrategy) -> None:
        if not isinstance(strategy, SortingStrategy):
            raise ValueError("A valid SortingStrategy is required")
        self._sorting_strategy = strategy
    
    def sort(self, array: List[int]) -> None:
        if not self._sorting_strategy:
            raise RuntimeError("No sorting strategy set")
        self._sorting_strategy.sort(array)


class BubbleSortStrategy(SortingStrategy):

    def sort(self, array: List[int]) -> None:
        print("Implementing Bubble Sort strategy")
        
        # outter loop to itterate over the list n times
        for n in reversed(range(len(array))):
            #Initialize swapped to track if any swaps occur
            swapped: bool = False

            # Inner loop to compare adjacent elements
            for i in range(n):
                if array[i] > array[i + 1]:

                    # Swap elements if they are in wrong order
                    array[i], array[i + 1] = array[i + 1], array[i]

                    # Mark swapped
                    swapped = True

            # if no swap appears then list is already sorted
            if not swapped:
                break

class MergeSortStrategy(SortingStrategy):
    def sort(self, array: List[int]) -> None:
        print("Implementing Merge Sort strategy")
        self._merge_sort(array)

    def _merge_sort(self, array: List[int]) -> None:
        n: int = len(array)
        if n > 1:
            mid = n // 2
            left = array[:mid]
            right = array[mid:]

            # Recursively call on each half
            self._merge_sort(left)
            self._merge_sort(right)

            # Iterattor for traversing two halfs
            i = 0
            j = 0

            # Iterator for main list
            k = 0

            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    array[k] = left[i]
                    i += 1
                else:
                    array[k] = right[j]
                    j += 1

                k += 1

            # for all the remaining valeus
            while i < len(left):
                array[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                array[k] = right[j]
                j += 1
                k += 1

class QuickSortStrategy(SortingStrategy):
    def sort(self, array: List[int]) -> None:
        print("Implementing Quick Sort strategy")
        n: int = len(array)
        self._quick_sort(array, 0, n-1)

    def _quick_sort(self, array: List[int], low: int, high: int) -> None:
        
        
        if low < high:
            pi = self._partition(array, low, high)
            self._quick_sort(array, low, pi - 1)
            self._quick_sort(array, pi + 1, high)

    def _swap(self, array: List[int], i: int, j: int) -> None:
        array[i], array[j] = array[j], array[i]

    def _partition(self, array: List[int], low: int, high: int) -> int:
        # choosing a pivot
        pivot: int = array[high]

        i = low - 1

        for j in range(low, high):
            if array[j] < pivot:
                i += 1
                self._swap(array, i, j)

        self._swap(array, i + 1, high)

        return i + 1
    
class Strategy(Enum):
    BUBBLE = BubbleSortStrategy()
    MERGE = MergeSortStrategy()
    QUICK = QuickSortStrategy()

class BubbleSortContext(SortingContext):
    def __init__(self):
        super().__init__(Strategy.BUBBLE.value)
    
class MergeSortContext(SortingContext):
    def __init__(self):
        super().__init__(Strategy.MERGE.value)

class QuickSortContext(SortingContext):
    def __init__(self):
        super().__init__(Strategy.QUICK.value)

def print_divider(title: str) -> None:
    print("\n" + "=" * 40)
    print(f"  {title}")
    print("=" * 40 + "\n")




# -------- Demo --------
if __name__ == "__main__":
    print_divider("Creating Sorting context with BubbleSort Strategy")
    # sorting_context: SortingContext = SortingContext(Strategy.BUBBLE.value)
    sorting_context: SortingContext = BubbleSortContext()
    array1: List[int] = [5, 2, 9, 1, 5]
    print("Array 1 :", array1)
    sorting_context.sort(array1)
    print("After sorting with Bubble Sort Strategy")
    print("Bubble Sort array 1 :", array1)

    print_divider("Creating Sorting context with MergeSort Strategy")
    # sorting_context: SortingContext = SortingContext(Strategy.MERGE.value)
    sorting_context: SortingContext = MergeSortContext()
    array2: List[int] = [8, 3, 7, 4, 2]
    print("Array 2 :", array2)
    sorting_context.sort(array2)
    print("After sorting with Merge Sort Strategy")
    print("Merge Sort array 2 :", array2)

    print_divider("Creating Sorting context with QuickSort Strategy")
    # sorting_context: SortingContext = SortingContext(Strategy.QUICK.value)
    sorting_context: SortingContext = QuickSortContext()
    array3: List[int] = [8, 3, 7, 4, 2]
    print("Array 3 :", array3)
    sorting_context.sort(array3)
    print("After sorting with Quick Sort Strategy")
    print("Quick Sort array 3 :", array3)