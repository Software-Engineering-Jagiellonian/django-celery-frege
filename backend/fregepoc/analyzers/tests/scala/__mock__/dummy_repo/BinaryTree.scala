object BinaryTree {

  def main(args: Array[String]): Unit = {

    val tree = new NonEmptyTree(3, new EmptyTree, new EmptyTree)
    println(s"Tree with one node: $tree")

    val nodes = List(8, 3, 15, 9)
    var treeWithNodes = new NonEmptyTree(5, new EmptyTree, new EmptyTree) includes 4
    nodes.foreach(node => {
      treeWithNodes = treeWithNodes union (treeWithNodes includes node)
    })

    println(s"Tree with nodes: $treeWithNodes")
    val n = 15
    val w = treeWithNodes.contains(n) match
      case true => "is"
      case false => "is not"

    println(s"Node $n $w in tree $treeWithNodes")
  }
}

trait BinaryTree {

  def contains(x: Int): Boolean

  def includes(x: Int): BinaryTree

  def union(other: BinaryTree): BinaryTree
}

class EmptyTree extends BinaryTree {

  def contains(x: Int): Boolean = false

  def includes(x: Int): BinaryTree = new NonEmptyTree(x, new EmptyTree, new EmptyTree)

  def union(other: BinaryTree): BinaryTree = other

  override def toString = "."
}

class NonEmptyTree(element: Int, leftBranch: BinaryTree, rightBranch: BinaryTree) extends BinaryTree {
    
  def contains(x: Int): Boolean = {

    if (x < element) leftBranch contains x
    else if (x > element) rightBranch contains x
    else true
  }

  def includes(x: Int): BinaryTree = {

    if (x < element) new NonEmptyTree(element, leftBranch includes x, rightBranch)
    else if (x > element) new NonEmptyTree(element, leftBranch, rightBranch includes x)
    else this
  }

  def union(other: BinaryTree): BinaryTree = {

    ((leftBranch union rightBranch) union other) includes element
  }

  override def toString: String = "{" + leftBranch + element + rightBranch + "}"
}
