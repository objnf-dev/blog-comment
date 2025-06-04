---
type: post
title: Algorithms and Data Structures – Generalized Lists
date: 2023-09-22 0:00
updated: 2025-06-02 0:00
categories: 开发与代码
tags:
  - 算法
  - 广义表
---

## Brief Introduction

A generalized list is an extension of a linear list. While a linear list requires all elements to be of the same type, a generalized list has no such restriction. It's important to note that both generalized lists and linear lists are generally considered to have finite lengths, but the depth of a generalized list can be infinite (i.e., a recursive list).

A generalized list is a type of data structure. Common operations on generalized lists include:

- Creation
- Create from string form
- Destroy
- Copy
- Get head
- Get tail
- Check if empty
- Get length
- Get depth
- Insert at head
- Delete from head
- Traverse

Generalized lists are the fundamental data structure in Lisp. Examples of each basic operation are provided in Common Lisp and C++ in the following sections.

<!-- more -->

## Annotations

### Length

Refers to the number of elements in a generalized list. Examples are as follows:

> Example 1

```
(a, b)
```

The table contains two elements: the atomic term `a` and the atomic term `b`. Therefore, the length of the table is 2.

> Example 2

```
(a, (b, c))
```

The table contains two elements: the atomic item `a` and the generalized list `(b, c)`. Therefore, the length of the table is 2.

### Depth

Refers to the nesting level of sublists within a generalized list. Examples are as follows:

> Example 1

```
(a, b)
```

This list contains no sublists, so its depth is 1.

> Example 2

```
(a, (b, c))
```

This list contains a nested sublist without further nesting, so its depth is 2.

> Example 3

```
((a, b), (c, d))
```

This table contains two non-nested subtables, so the depth of the table is 2.

> Example 4

```
(a, (b, (c, d)))
```

This table contains 1 nested subtable, which in turn contains 1 non-nested subtable, making the table's depth 3.

It can be understood as the number of bracket layers in the string representation of a generalized list.

### Sublist

A generalized list nested within another generalized list is called a sublist of that generalized list. For example:

```
(a, (b, c))
```

`(b, c)` is referred to as a sublist of `(a, (b, c))`.

### Atomic Item

An element that cannot be further divided as a generalized list. For example:

```
(1, (a, b))
```

In the above list, `1` is not a generalized list and cannot be further divided within the context of generalized lists, thus it is an atomic item.

In the above table, `(a, b)` is a generalized list that can be split into `(a)` and `(b)`, thus it is not an atomic item.

### String Form (Written Form)

A serialization method for generalized lists. That is, writing a generalized list as a string composed of parentheses, atomic values, (commas), etc. For example:

```
(1 2 (A B))
```

and

```
(1, 2, (A, B))
```

are common forms of generalized list notation.

## Implementation in Lisp

Using the SBCL Lisp environment.

### Creation

The `cons` function can be used to create lists. For example, to create a list containing only the number 1 (with the head being the atomic integer 1 and the tail being empty):

```
(cons 1 nil)
```

Or:

```
(list 1)
```

You can also create a list based on an existing head and tail:

```
(cons 1 '(2 5))
```

Symbols can also be used.

```
(cons 'a '(b 2))
```

Set variable X as the list `(1 A B)` to serve as the following example:

```
(let ((x (cons 1 '(a b)))) (prin1 x))
```

Output:

```
(1 A B)
```

### Copy

Can be understood as passing variables by value.

```
(let ((x (cons 1 '(a b))))
     (let ((y x))
          (prin1 y)))
```

Output:

```
(1 A B)
```

### Get the Head of a List

Use the `car` function.

```
(let ((x (cons 1 '(a b)))) (car x))
```

Output:

```
1
```

The output is an atomic item.

### Taking the Tail of a List

Use the `cdr` function.

```
(let ((x (cons 1 '(a b)))) (cdr x))
```

Output:

```
(A B)
```

The output is a generalized list.

### Finding the Length

Use the `length` function.

> Example 1

Given the generalized list `(1 A B)`, find its length.

```
(length '(1 A B))
```

The result is 3.

> Example 2

Given the generalized list `(1 (A B))`, find its length.

```
(length '(1 (A B)))
```

The result is 2.

### Checking if empty

A generalized list is considered empty when its length is 0.

```
(if (= (length '()) 1) t nil)
```

The result is `NIL`.

### Inserting from the Head

Repeatedly applying the `cons` function allows inserting data into a generalized list from the head.

```
(let ((x (cons 1 '(A B))))
     (setf x (cons 3 (cons 2 x)))
     (prin1 x))
```

Output:

```
(3 2 1 A B)
```

### Remove from head

Repeatedly applying the `cdr` function allows for removing data from the head of the list.

```
(let ((x (cons 1 '(a b))))
     (setf x (cdr (cdr x)))
     (prin1 x))
```

Output:

```
(B)
```

### Get Depth

Basic approach: Recursive.

- Define the function `list-depth`, accepting the variable `list` as a parameter
- Check if `list` is a generalized list; if not, directly return 0
- If `list` is a generalized list, then:
  - For each element in this generalized list, call `list-depth`, using `mapcar` to implement this operation. The return values form another generalized list.
  - Take the maximum value of this generalized list.
  - (Assign initial value, optional)
  - Increment the existing maximum depth value by 1.

```text
(defun list-depth (list)
    (if (listp list)
        (+ 1 (reduce #'max (mapcar #'list-depth list)
            :initial-value 0))
        0)
)
```

Call:

```
(list-depth '(1 (2 3)))
```

Output:

```
2
```

## C++ Implementation

Due to the characteristics of generalized lists, it is difficult to store them using a sequential structure. Therefore, generalized lists are mostly built on a linked storage structure.

Discussing generalized lists containing only two possible types of nodes:

- Atomic item nodes of type int
- A generalized list node composed of int type; in this case, the node is equivalent to a pointer to the head node of a sublist.

Therefore, the "list structure" and "node structure" can be designed. The "list structure" stores the pointer to the head node of the list and the length of the list. When the list is empty, its head node pointer is `nullptr`. The "node structure" stores the actual data. The specific storage structure is as follows:

```c++
#define ElementType int

typedef struct Node
{
    bool type;
    Node *next;
    union
    {
        ElementType atom;
        Node *nodePointer;
    }
    data;
};

typedef struct List
{
    int length;
    Node *head;
};
```

Here, `Node.type` indicates the type of the node: when it is `false`, it represents an atomic item node, and when it is `true`, it represents a sublist node.

### Creation

Place all nodes in the heap.

```c++
List::List(): length(0), head(nullptr)
{

}

List demo = new List();
```

### Destroy

```c++
List::~List()
{
    delete *head;
}
```

### Check if empty

Use the `length` in the `List` struct.

```c++
bool List::CheckEmpty()
{
    if (this->length == 0) {
        return true;
    }
    return false;
}
```

### Get length

Same as above.

```c++
demo.length;
```

[TODO]