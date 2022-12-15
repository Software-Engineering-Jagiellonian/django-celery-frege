class BST {
    value: number;
    left?: BST;
    right?: BST;

    constructor(value: number) {
        this.value = value;
    }

    find(key: number): BST | string {
        if (key === this.value) return this;

        if (key < this.value && this.left !== undefined) return this.left.find(key);

        if (key > this.value && this.right !== undefined) return this.right.find(key);

        return `value ${key} not found`;
    }

    add(key: number): BST | string {
        if (key < this.value) {
            if (this.left === undefined) {
                this.left = new BST(key);
                return this.left;
            }
            else {
                return this.left.add(key);
            }
        }
        else if (key > this.value) {
            if (this.right === undefined) {
                this.right = new BST(key);
                return this.right;
            }
            else {
                return this.right.add(key);
            }
        }

        return `key ${key} already exists in this tree`;
    }

    getPreorder(): string {
        let result: string = this.value.toString();

        if (this.left !== undefined) {
            result += ` ${this.left.getPreorder()}`
        }

        if (this.right !== undefined) {
            result += ` ${this.right.getPreorder()}`
        }

        return result
    }
}
