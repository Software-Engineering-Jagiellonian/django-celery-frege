object InsertionSort {

  def sort(xs: List[Int]): List[Int] = {

    if (xs.isEmpty) Nil
    else insert(xs.head, sort(xs.tail))
  }

  def insert(x: Int, xs: List[Int]): List[Int] = {

    if (xs.isEmpty || x <= xs.head) x :: xs
    else xs.head :: insert(x, xs.tail)
  }

  def main(args: Array[String]): Unit = {

    val l1 = List()
    println(sort(l1))

    val l2 = List(5, 3, 0, 0, 0, -2, -5, 9)
    println(sort(l2))

    val l3 = List(44, 12241, 241, 3, 0, -2,
      -5, 3, 32, -2142, 4, 241, 3, 9, 241,
      214, 22421 , 2, 321, 2, -2, -2414, -141,
      2412, -242, 24145, -44, 0)
    println(sort(l3))

    val lists = List[List[Int]](l1, l2, l3)
    lists.foreach(sort)
  }
}
