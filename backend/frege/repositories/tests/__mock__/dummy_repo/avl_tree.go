package main

import (
	"fmt"
	"strings"
)

type AvlTree struct {
	value string
	left  *AvlTree
	right *AvlTree
}

func (tree *AvlTree) String() string { return tree.str(1) }

func (tree *AvlTree) str(n int) string {
	if tree == nil {
		return "<nil>"
	}
	return fmt.Sprintf("%q\n%s%v,%v\n%s", tree.value, strings.Repeat("\t", n), tree.left.str(n+1), tree.right.str(n+1), strings.Repeat("\t", n-1))
}

func rotateLeftToRoot(ptree **AvlTree) {
	tree := *ptree
	if tree == nil {
		return
	}
	prevLeft := tree.left
	if prevLeft != nil {
		tree.left = prevLeft.right
		prevLeft.right = tree
		tree = prevLeft
	}
	*ptree = tree
}

func main() {
	tree := &AvlTree{
		value: "t",
		left: &AvlTree{
			value: "L",
			left: &AvlTree{
				value: "LL",
			},
			right: &AvlTree{
				value: "LR",
			},
		},
		right: &AvlTree{
			value: "R",
		},
	}
	fmt.Println(tree)
	rotateLeftToRoot(&tree)
	fmt.Println(tree)
}
