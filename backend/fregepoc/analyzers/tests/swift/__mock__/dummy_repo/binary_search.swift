func binarySearch<T: Comparable>(a: [T], key: T, range: Range<Int>) -> Int? {
  if range.startIndex >= range.endIndex {
        return nil
  } else {
        let midIndex = range.startIndex + (range.endIndex - range.startIndex) / 2

        if a[midIndex] > key {
          return binarySearch(a: a, key: key, range: range.startIndex ..< midIndex)
        } else if a[midIndex] < key {
          return binarySearch(a: a, key: key, range: midIndex + 1 ..< range.endIndex)
        } else {
          return midIndex
        }
  }
}

// Example
let numbers = [0, 4, 9, 13, 19, 23, 40, 54, 60, 64, 77, 90, 101, 123]

print(binarySearch(a: numbers, key: 101, range: 0 ..< numbers.count)) // output: 12
