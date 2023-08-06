#!/usr/bin/env python3

"""
** Avoid display conflicts between threads. **
----------------------------------------------

This allows to replace the 'print' method native to python. All formatting must be done before.
"""

import math
import os
import re
import threading
import time

from context_verbose.memory import get_lifo, get_id
from context_verbose.tree import Tree


EXPERIMENTAL = False


def cut(string, size):
    r"""
    ** Allows to cut the text without breaking the special characters. **

    Parameters
    ----------
    string : str
        The text to be cut, which can contain text formatting characters.

    Returns
    -------
    sections : list
        Each element of the list is a portion of the
        text cut in order to ensure correct formatting.

    Examples
    --------
    >>> from context_verbose.color import format_text
    >>> from context_verbose.thread_safe import cut
    >>> format_text('test_string')
    'test_string'
    >>> cut(_, 7)
    ['test_st', 'ring']
    >>> format_text('test_string', color='blue')
    '\x1b[22m\x1b[34mtest_string\x1b[0m'
    >>> cut(_, 7)
    ['\x1b[22m\x1b[34mtest_st\x1b[0m', '\x1b[22m\x1b[34mring\x1b[0m']
    >>> format_text('test_string', color='blue') + format_text('test_string', blink=True)
    '\x1b[22m\x1b[34mtest_string\x1b[0m\x1b[5mtest_string\x1b[0m'
    >>> cut(_, 11)
    ['\x1b[22m\x1b[34mtest_string\x1b[0m', '\x1b[22m\x1b[34m\x1b[0m\x1b[5mtest_string\x1b[0m']
    >>>
    """
    assert isinstance(string, str)
    assert isinstance(size, int)
    assert size > 0

    sections = []
    specials = list(re.finditer(r'\x1b\[\S+?m', string))

    # cutting in packages of the right size
    clean_string = string
    for special_str in {m.group() for m in specials}:
        clean_string = clean_string.replace(special_str, '')
    while clean_string:
        sections.append(clean_string[:size])
        clean_string = clean_string[size:]

    # repositioning of special chains
    dec = 0
    positions = {}
    for special in specials:
        start, end = special.span()
        positions[start-dec] = positions.get(start-dec, '') + special.group()
        dec += end - start

    # added markup
    current_markers = ''
    loc_dec = 0
    for dec, section in enumerate(sections.copy()):
        section = current_markers + section
        loc_dec = len(current_markers)
        for i in range(size):
            if i + dec*size in positions:
                special = positions[i + dec*size]
                section = section[:i+loc_dec] + special + section[i+loc_dec:]
                if special == '\x1b[0m':
                    current_markers = ''
                else:
                    current_markers += special
                loc_dec += len(special)
        if current_markers:
            section += '\x1b[0m'
        sections[dec] = section

    # incomplete chain management
    if not string.endswith('\x1b[0m') and sections[-1].endswith('\x1b[0m'):
        sections[-1] = sections[-1][:-4]
    return sections


def get_terminal_size():
    """
    ** Recover the dimensions of the terminal. **

    Returns
    -------
    columns : int
        The number of columns in the terminal.
    lines : int
        The number of lines present in the terminal.

    Examples
    --------
    >>> import tempfile
    >>> import sys
    >>> from context_verbose.thread_safe import get_terminal_size
    >>> size = get_terminal_size()
    >>> size # doctest: +SKIP
    (100, 30)
    >>> stdout = sys.stdout
    >>> with tempfile.TemporaryFile('w', encoding='utf-8') as file:
    ...     sys.stdout = file
    ...     size = get_terminal_size()
    ...
    >>> sys.stdout = stdout
    >>> size
    (100, inf)
    >>>
    """
    try:
        size = os.get_terminal_size()
    except OSError:
        return get_lifo().columns, math.inf
    else:
        return size.columns, size.lines


def print_safe(text, *, end='\n'):
    """
    ** Replacement of 'print'. **

    Constrained to display in a particular area to avoid mixing between threads.

    Parameters
    ----------
    text : str
        The string to display
    end : str, optional
        Transfer directly to the native ``print`` function.
    """
    assert isinstance(text, str)

    if EXPERIMENTAL:
        Pipe().add_line(text)

    else:
        columns, _ = get_terminal_size()
        if len(text) <= columns or columns <= 5:
            print(text, end=end)
        else:
            print('\n'.join(cut(text, columns)), end=end)


def _reset_memory():
    """
    ** Removes all traces of memory. **
    """
    for name in list(globals()).copy():
        if name.startswith('_pipe_'):
            del globals()[name]


class Pipe(threading.Thread):
    """
    ** Allows you to communicate with other execution threads. **

    * If this object is instantiated from the main thread of the main process:
        * It just keeps the display tree up to date and prints the new changes.
    * If it is instantiated in a thread of the main process:
        * It transmits messages to the main process.
        * He responds to callers who ask him if he is alive.
    * If it is instantiated in the main thread of a secondary process:
        * Failed : not implemented
    * If it is instantiated in a secondary thread of a secondary process:
        * Failed : not implemented
    """

    def __new__(cls):
        """
        ** Guarantees the uniqueness of an instance of this class. **

        Examples
        --------
        >>> import threading
        >>> from context_verbose.thread_safe import Pipe
        >>> def compare(pointer):
        ...     pointer[0] = Pipe()
        ...     pointer[1] = Pipe()
        ...
        >>> pointer1 = [None, None]
        >>> compare(pointer1)
        >>> p1, p2 = pointer1
        >>> p1 is p2
        True
        >>> pointer2 = [None, None]
        >>> t = threading.Thread(target=compare, args=(pointer2,))
        >>> t.start()
        >>> t.join()
        >>> p3, p4 = pointer2
        >>> p1 is p3
        False
        >>> p3 is p4
        True
        >>>
        """
        self_id = get_id()
        proc_name = self_id['proc_name']
        thread_name = self_id['thread_name']
        father_proc = self_id['father_proc']
        self_name = f'_pipe_{proc_name}_{thread_name}'
        if self_name not in globals():
            self = super(Pipe, cls).__new__(cls)
            self._init(proc_name, thread_name, father_proc)
            if thread_name == 'MainThread':
                self.start()
            globals()[self_name] = self
        return globals()[self_name]

    def _init(self, proc_name, thread_name, father_proc):
        """
        ** Unique initiator. **
        """
        threading.Thread.__init__(self)
        self.daemon = True

        self.proc_name = proc_name
        self.thread_name = thread_name
        self.father_proc = father_proc

        self.lines = []
        self.stop = False
        if proc_name == 'MainProcess' and thread_name == 'MainThread':
            self.tree = Tree()
        else:
            self.tree = None
        self.lock = threading.Lock()

    def add_line(self, message):
        """
        ** Add to the queue, the future message to display. **

        Parameters
        ----------
        message : str
            The new line to display in this thread.
        """
        assert isinstance(message, str)

        if self.thread_name != 'MainThread':
            with self.lock:
                self.lines.extend(message.split('\n'))
            self._put_to_main_thread()
        elif self.proc_name == 'MainProcess':
            self.conn(message.split('\n'), proc_name='MainProcess', thread_name='MainThread')
        else:
            raise NotImplementedError(
                'the transfer of information between processes is not yet coded'
            )

    def conn(self, lines, proc_name, thread_name):
        """
        ** Retrieves new information from a child feed. **

        Parameters
        ----------
        lines : list
            The list of lines to display in the child feed.
        proc_name : str
            The name of the child process.
        thread_name : str
            The name of the child thread.

        Examples
        --------
        >>> from context_verbose.thread_safe import Pipe, _reset_memory
        >>> _reset_memory()
        >>> p = Pipe()
        >>> print(p.tree)
        Tree with 0 nodes and 0 edges
        >>> p.conn(['message'], proc_name='MainProcess', thread_name='MainThread')
        message
        >>> print(p.tree)
        Tree with 1 nodes and 0 edges
        >>>
        """
        if self.thread_name != 'MainThread':
            raise RuntimeError('only main threads can collect data from other threads')
        if self.proc_name == 'MainProcess':
            self.tree.add_content(lines, proc_name=proc_name, thread_name=thread_name)
            with self.lock:
                self.tree.display()
        else:
            raise NotImplementedError(
                'the transfer of information to the process above is not coded'
            )

    def _put_to_main_thread(self):
        """
        ** Transmits information to the main thread. **
        """
        try:
            father = globals()[f'_pipe_{self.proc_name}_MainThread']
        except KeyError as err:
            raise ImportError(
                "you have to import 'context_verbose' in the main thread "
                "before importing it in the secondary threads"
            ) from err
        else:
            with self.lock:
                father.conn(self.lines, proc_name=self.proc_name, thread_name=self.thread_name)
                self.lines = []

    def _display_from_tree(self):
        """
        ** Displays the information contained in the tree. **
        """
        if self.proc_name != 'MainProcess' or self.thread_name != 'MainThread':
            raise RuntimeError('only the main thread of the main process can display')
        with self.lock:
            self.tree.display()

    def run(self):
        """
        ** Transmits or collects the display tree. **

        Examples
        --------
        >>> import threading
        >>> from context_verbose.thread_safe import Pipe, _reset_memory
        >>> _reset_memory()
        >>> Pipe()
        <Pipe(MainProcess, MainThread)>
        >>>
        >>> def test():
        ...     Pipe().add_line('sentence in the main thread')
        ...     threading.Thread(target=(lambda: Pipe().add_line('text in a subthread'))).start()
        ...     threading.Thread(target=(lambda: Pipe().add_line('text in a subthread'))).start()
        ...
        >>> test() # doctest: +SKIP
        sentence in the main thread
        sentence in the main thread
        ********** ('MainProcess', 'Thread-20') **********
        text in a subthread
        **************************************************
        sentence in the main thread
        ********** ('MainProcess', 'Thread-20') **********
        text in a subthread
        **************************************************
        ********** ('MainProcess', 'Thread-23') **********
        text in a subthread
        **************************************************
        >>>
        """
        while not self.stop:
            if self.thread_name != 'MainThread':
                self._put_to_main_thread()
            elif self.proc_name == 'MainProcess':
                self._display_from_tree()
            else:
                raise NotImplementedError(
                    'the transfer of information between processes is not yet coded'
                )
            time.sleep(0.1)

    def __del__(self):
        """
        ** Disappears and tries to remove the traces. **
        """
        self.stop = True
        self_name = f'_pipe_{self.proc_name}_{self.thread_name}'
        if self_name in globals():
            del globals()[self_name]

    def __repr__(self):
        """
        ** Offers a better representation. **
        """
        return f'<Pipe({self.proc_name}, {self.thread_name})>'


if EXPERIMENTAL:
    Pipe()
