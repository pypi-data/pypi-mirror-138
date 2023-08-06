#!/usr/bin/env python3

"""
** Representation of messages as a tree. **
-------------------------------------------

Each branch corresponds to a thread or a process.
This makes it possible to represent the display
of each thread and process in the most easily exploitable way.
"""

import logging
import re

import networkx


def get_length(text):
    r"""
    ** Returns the length of the displayed text. **

    Parameters
    ----------
    text : str
        Single-line text that can contain formatting characters.

    Returns
    -------
    length : int
        The size of the text.

    Examples
    --------
    >>> from context_verbose.tree import get_length
    >>> from context_verbose.color import format_text
    >>> get_length('hello')
    5
    >>> get_length('\thello')
    9
    >>> format_text('hello', color='red')
    '\x1b[22m\x1b[31mhello\x1b[0m'
    >>> get_length(_)
    5
    >>> get_length('')
    0
    >>>
    """
    assert isinstance(text, str)
    assert '\n' not in text

    length = len(text)
    length -= sum((len(c) for c in re.findall(r'\x1b\[\S+?m', text)), start=0)
    length += 3*len(re.findall(r'\t', text))

    return length


class Branch:
    """
    ** Corresponds to the display thread of a thread or a process. **
    """
    def __init__(self, proc_name='MainProcess', thread_name='MainThread'):
        """
        Parameters
        ----------
        proc_name : str
            The name of the process associated with this branch.
        thread_name : str
            The name of the thread associated with this process.
        """
        self.proc_thread = (proc_name, thread_name)
        self.lines = []
        self.childs = []

    def add_text(self, text):
        """
        ** Adds a message line on the current branch. **

        Parameters
        ----------
        text : str
            The new text line to be displayed follows the existing lines in this display thread.
        """
        assert isinstance(text, str)
        assert '\n' not in text

        self.lines.append(text)

    def add_lines(self, lines):
        """
        ** Adds several display lines linked to this branch. **

        Parameters
        ----------
        lines : list
            The different lines to add.
        """
        assert isinstance(lines, list)

        for text in lines:
            self.add_text(text)

    def get_max_length(self):
        """
        ** Returns the length of the longest line. **

        Returns
        -------
        length : int
            The number of characters (printable + spaces + tabs) in the longest line.

        Examples
        --------
        >>> from context_verbose.tree import Branch
        >>> branch = Branch()
        >>> branch.get_max_length()
        0
        >>> branch.add_text('hello')
        >>> branch.get_max_length()
        5
        >>> branch.add_text('welcome')
        >>> branch.get_max_length()
        7
        >>> branch.add_text('yo')
        >>> branch.get_max_length()
        7
        >>>
        """
        return max(
            (get_length(l) for l in self.lines),
            default=0,
        )

    def __eq__(self, other):
        """
        ** Return True if the 2 branches are the same. **

        Parameters
        ----------
        other : object
            The element of comparison.

        Examples
        --------
        >>> from context_verbose.tree import Branch
        >>> b1 = Branch('p1', 't1')
        >>> b2 = Branch('p1', 't1')
        >>> b3 = Branch('p1', 't2')
        >>> b1 == b1
        True
        >>> b1 == b2
        True
        >>> b1 == b3
        False
        >>>
        """
        if not isinstance(other, Branch):
            return NotImplemented
        return self.proc_thread == other.proc_thread

    def __gt__(self, other):
        """
        ** Compare the depth of the branches. **

        Parameters
        ----------
        other : object
            The element of comparison.

        Examples
        --------
        >>> from context_verbose.tree import Branch
        >>> Branch('p1', 't1') > Branch('p1', 't1')
        False
        >>> Branch('p1', 't1') > Branch('p2', 't1')
        False
        >>> Branch('p2', 't1') > Branch('p1', 't1')
        True
        >>> Branch('p1', 't1') > Branch('p1', 't2')
        False
        >>> Branch('p1', 't2') > Branch('p1', 't1')
        True
        >>>
        """
        if not isinstance(other, Branch):
            return NotImplemented
        if self.proc_thread[0] == other.proc_thread[0]:
            return self.proc_thread[1] > other.proc_thread[1]
        return self.proc_thread[0] > other.proc_thread[0]

    def __hash__(self):
        """
        ** Allows to build hash tables. **

        Examples
        --------
        >>> from context_verbose.tree import Branch
        >>> b1 = Branch('p1', 't1')
        >>> b2 = Branch('p1', 't1')
        >>> b3 = Branch('p1', 't2')
        >>> sorted({b1, b2, b3})
        [Branch(p1, t1), Branch(p1, t2)]
        >>>
        """
        return hash(self.proc_thread)

    def __repr__(self):
        """
        ** Offers a slightly better representation. **

        Examples
        --------
        >>> from context_verbose.tree import Branch
        >>> Branch()
        Branch(MainProcess, MainThread)
        >>>
        """
        proc, thread = self.proc_thread
        return f'Branch({proc}, {thread})'


class Tree(networkx.DiGraph):
    """
    ** This is the complete graph that represents the whole display. **

    Examples
    --------
    >>> from context_verbose.tree import Tree
    >>> tree = Tree()
    >>> print(tree)
    Tree with 0 nodes and 0 edges
    >>>
    """
    def __init__(self):
        networkx.DiGraph.__init__(self)
        self.new = False

    def add_content(self, lines, proc_name, thread_name, father_proc=None):
        """
        ** Add the corresponding text in the right branch. **

        Parameters
        ----------
        lines : list
            The display lines to be added to the corresponding branch.
        proc_name : str
            The name of the process associated with this branch.
        thread_name : str
            The name of the thread associated with this process.
        father_proc : str or None
            If it is provided, it corresponds to the name of the parent process.


        Examples
        --------
        >>> from context_verbose.tree import Tree
        >>> tree = Tree()
        >>> print(tree)
        Tree with 0 nodes and 0 edges
        >>> tree.add_content(['a'], proc_name='MainProcess', thread_name='Thread-1')
        >>> print(tree)
        Tree with 2 nodes and 1 edges
        >>> tree.add_content(['b'], proc_name='MainProcess', thread_name='Thread-2')
        >>> print(tree)
        Tree with 3 nodes and 2 edges
        >>>
        """
        node = (proc_name, thread_name)

        # create new node and edge
        if not self.has_node(node):
            self.add_node(node, data=Branch(proc_name=proc_name, thread_name=thread_name))
            if thread_name != 'MainThread':
                father = (proc_name, 'MainThread')
            elif proc_name != 'MainProcess':
                if father_proc is None:
                    logging.warning(
                        f"the process '{proc_name}' is not attached to any fatther process"
                    )
                father = (father_proc, 'MainThread')
            else:
                father = None
            if father is not None:
                self.add_content([], proc_name=father[0], thread_name=father[1])
                self.add_edge(father, node)

        # update content
        self.nodes[node]['data'].add_lines(lines)
        if lines:
            self.new = True

    def display(self):
        """
        ** Displays the contents of the tree. **
        """
        if self.new:
            self.new = False

            if self.nodes[('MainProcess', 'MainThread')]['data'].lines:
                print('\n'.join(self.nodes[('MainProcess', 'MainThread')]['data'].lines))
                self.nodes[('MainProcess', 'MainThread')]['data'].lines = []

            for node in self.nodes:
                if node != ('MainProcess', 'MainThread'):
                    if self.nodes[node]['data'].lines:
                        header = f'********** {node} **********'
                        print(header)
                        print('\n'.join(self.nodes[node]['data'].lines))
                        self.nodes[node]['data'].lines = []
                        print('*'*len(header))
