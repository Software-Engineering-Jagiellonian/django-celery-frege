class Node {
  var visited = false
  var connections: [Connection] = []
}

class Connection {
  public let to: Node
  public let weight: Int

  public init(to node: Node, weight: Int) {
    assert(weight >= 0, "Weight has to be a non negative value.")
    self.to = node
    self.weight = weight
  }
}

class Path {
  public let cumulativeWeight: Int
  public let node: Node
  public let previousPath: Path?

  init(to node: Node, via connection: Connection? = nil, previousPath path: Path? = nil) {
    if
      let previousPath = path,
      let viaConnection = connection {
      self.cumulativeWeight = viaConnection.weight + previousPath.cumulativeWeight
    } else {
      self.cumulativeWeight = 0
    }

    self.node = node
    self.previousPath = path
  }
}

extension Path {
  var array: [Node] {
    var array: [Node] = [self.node]

    var iterativePath = self
    while let path = iterativePath.previousPath {
      array.append(path.node)

      iterativePath = path
    }

    return array
  }
}

func shortestPath(source: Node, destination: Node) -> Path? {
  var frontier: [Path] = [] {
    didSet { frontier.sort { return $0.cumulativeWeight < $1.cumulativeWeight } }
  }

  frontier.append(Path(to: source))

  while !frontier.isEmpty {
    let cheapestPathInFrontier = frontier.removeFirst()
    guard !cheapestPathInFrontier.node.visited else { continue }

    if cheapestPathInFrontier.node === destination {
      return cheapestPathInFrontier
    }

    cheapestPathInFrontier.node.visited = true

    for connection in cheapestPathInFrontier.node.connections where !connection.to.visited {
      frontier.append(Path(to: connection.to, via: connection, previousPath: cheapestPathInFrontier))
    }
  }
  return nil
}

// Example
class MyNode: Node {
  let name: String

  init(name: String) {
    self.name = name
    super.init()
  }
}

let nodeA = MyNode(name: "1")
let nodeB = MyNode(name: "2")
let nodeC = MyNode(name: "3")
let nodeD = MyNode(name: "4")
let nodeE = MyNode(name: "5")

nodeA.connections.append(Connection(to: nodeB, weight: 1))
nodeB.connections.append(Connection(to: nodeC, weight: 3))
nodeC.connections.append(Connection(to: nodeD, weight: 1))
nodeB.connections.append(Connection(to: nodeE, weight: 1))
nodeE.connections.append(Connection(to: nodeC, weight: 1))

let sourceNode = nodeA
let destinationNode = nodeD

var path = shortestPath(source: sourceNode, destination: destinationNode)

if let succession: [String] = path?.array.reversed().flatMap({ $0 as? MyNode}).map({$0.name}) {
  print("Shortest path: \(succession)")
} else {
  print("No path has been found between: \(sourceNode.name) & \(destinationNode.name)")
}