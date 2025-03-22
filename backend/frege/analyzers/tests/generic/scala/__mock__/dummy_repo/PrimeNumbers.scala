object PrimeNumbers {

  def primeStream(stream: LazyList[Int] = LazyList.from(3, 2)): LazyList[Int] = {

    stream.head #:: primeStream(stream.tail.filter(_ % stream.head != 0))
  }

  def main(args: Array[String]): Unit = {

    println(primeStream().take(5).toList)
  }
}
