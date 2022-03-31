import java.lang.reflect.Array;
import java.util.*;
import java.util.function.Predicate;

interface Pair<K, V>{
    K getKey();
    V getValue();
}
class OrderedPair<K extends Comparable<? super K>, V> implements Pair<K, V>, Comparable<OrderedPair<K, V>>{
    private K key;
    private V value;

    OrderedPair(K key, V value){
        this.key = key;
        this.value = value;
    }
    @Override
    public K getKey() {
        return key;
    }

    @Override
    public V getValue() {
        return value;
    }

    @Override
    public int compareTo(OrderedPair<K, V> o) {
       return this.key.compareTo(o.getKey());
    }
    public String toString(){
        return "[ "+ key.toString()+", "+value.toString()+" ]";
    }
}
public class BinaryTree {
    public static void main(String[] args) {
        BinarySearchTree<Integer> bst = new BinarySearchTree<>();
        for (int i = 0; i < 25; i++) {
            bst.add(i);
        }
        bst.print();
        System.out.println(bst.contains(13));
        ArrayList<Integer> ar = new ArrayList<>();
        ar.add(46);
        ar.add(66);
        ar.add(153);
        System.out.println(bst.containsAll(ar));
        System.out.println(bst.addAll(ar));
        for (Object e : bst) {
            System.out.print(e + " ");
        }
        System.out.println();
        Object[] arr = bst.toArray();
        for(Object o: arr){
            System.out.print(o+" ");
        }
        System.out.println();
        Number[] array = new Number[5];
        array = bst.toArray(array);
        for(Object o: array){
            System.out.print(o+" ");
        }
        System.out.println();
        OrderedPair<Integer, String> pair1 = new OrderedPair<>(3,"abs");
        OrderedPair<Integer, String> pair2 = new OrderedPair<>(1,"cde");
        OrderedPair<Integer, String> pair3 = new OrderedPair<>(2,"dfg");
        System.out.println(pair1+" "+pair2+" "+pair3);
        System.out.println(pair1.compareTo(pair3));
    }
}
class BinaryIterator<E extends Comparable<? super E>>  implements Iterator<E> {
    private Stack<Node<E>> stack = new Stack<>();

    BinaryIterator(Node<E> node) {
        Node<E> current = node;
        while (current!= null) {
            stack.push(current);
            current = current.left;
        }
    }

    @Override
    public boolean hasNext() {
        return !stack.empty();
    }

    @Override
    public E next() {
        Node<E> current = stack.peek();
        Node<E> res = current;
        current = current.right;
        stack.pop();
        while (current != null) {
            stack.push(current);
            current = current.left;
        }
       return res.data;
    }
}

    class Node<E extends Comparable<? super E>> {
        Node<E> right;
        Node<E> left;
        Node<E> up;
        E data;

        Node() {
            right = left = null;
        }

        Node(Node<E> up, Node<E> left, Node<E> right, E data) {
            this.right = right;
            this.left = left;
            this.up = up;
            this.data = data;
        }
    }

    class BinarySearchTree<E extends Comparable<? super E>> implements Collection<E> {
        private int size;
        private boolean contains;
        private Node<E> root;

        {
            contains = false;
            root = null;
            size = 0;
        }

        void print() {
            Predicate<Node<E>> display = (v) -> {
                if (v != null) System.out.print(v.data + " ");
                return (v == null);
            };
            in_order(root, display);
        }

        private void in_order(Node<E> v, Predicate<Node<E>> f) {
            if (v != null) {
                in_order(v.left, f);
                f.test(v);
                in_order(v.right, f);
            }
        }

        @Override
        public int size() {
            return size;
        }

        @Override
        public boolean isEmpty() {
            return size == 0;
        }

        @Override
        public boolean contains(Object o) {
            Predicate<Node<E>> equals = (v) -> {
                if (o.equals(v.data)) {
                    contains = true;
                }
                return o.equals(v.data);
            };
            in_order(root, equals);
            boolean res = contains;
            contains = false;
            return res;
        }

        @Override
        public Iterator<E> iterator() {
            return new BinaryIterator<E>(root);
        }

        @Override
        public Object[] toArray() {
            ArrayList<Object> arr = new ArrayList<>();
            Iterator<E> it = iterator();
            while(it.hasNext()){
                arr.add(it.next());
            }
            return arr.toArray();
        }

        @Override
        public <T> T[] toArray(T[] a) {
          T[] array =  (T[]) Array.newInstance(a.getClass().getComponentType(), size);
          Iterator<E> it = iterator();
          int i = 0;
          while(it.hasNext()){
              array[i] = (T) it.next();
              i++;
          }
          return array;
        }

        @Override
        public boolean add(E e) {
            Node<E> p = root;
            if (p == null) {
                root = new Node<E>(null, null, null, e);
                size++;
            } else {
                while (true) {
                    if (e.compareTo(p.data) < 0) {
                        if (p.left == null) {
                            p.left = new Node<E>(p, null, null, e);
                            size++;
                            break;
                        } else {
                            p = p.left;
                        }
                    } else if (e.compareTo(p.data) > 0) {
                        if (p.right == null) {
                            p.right = new Node<E>(p, null, null, e);
                            size++;
                            break;
                        } else {
                            p = p.right;
                        }
                    } else if (e.compareTo(p.data) == 0) {
                        return false;
                    }
                }
            }
            return true;
        }


        @Override
        public boolean remove(Object o) throws UnsupportedOperationException{
            throw new UnsupportedOperationException();
        }

        @Override
        public boolean containsAll(Collection<?> c) {
            boolean res = true;
            for (Object o : c) {
                if (!contains(o)) {
                    res = false;
                    break;
                }
            }
            return res;
        }

        @Override
        public boolean addAll(Collection<? extends E> c) {
            int old_size = size;
            c.forEach(this::add);
            return old_size != size;
        }

        @Override
        public boolean removeAll(Collection<?> c) throws UnsupportedOperationException {
            throw new UnsupportedOperationException();
        }

        @Override
        public boolean retainAll(Collection<?> c) throws UnsupportedOperationException {
            throw new UnsupportedOperationException();

        }

        @Override
        public void clear() throws UnsupportedOperationException{
            throw new UnsupportedOperationException();
        }
    }