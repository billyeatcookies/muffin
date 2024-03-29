import io
import tkinter as tk
import tokenize

PY_KEYWORDS = [
    'import', 'if', 'else', 'elif', 'for', 'while', 
    'try', 'except', 'as', 'any','is', 'not', 'with'
]

PY_DEFS = [
    'def', 'class', 'int', 'float', 'char', 'str',
    'True', 'False', 'None', 'object', 'bool',
]

PY_BUILTINS = [
    "abs","all","any","ascii","bytearray","callable",
    "classmethod","complex","delattr","dir","divmod",
    "enumerate","exec","filter","format","frozenset",
    "globals","hasattr","help","hex","id","input", "eval",
    "isinstance","issubclass","len","list","locals",
    "max","memoryview","next","open","ord","pow","print",
    "property","repr","reversed","setattr","sorted",
    "staticmethod","sum","super","tuple","type","vars","zip"
]

CPP_KEYWORDS = [
    'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor', 'bool', 'break',
    'case', 'catch', 'char', 'char16_t', 'char32_t', 'class', 'compl', 'concept', 'const',
    'constexpr', 'const_cast', 'continue', 'decltype', 'default', 'delete', 'do', 'double',
    'dynamic_cast', 'else', 'enum', 'explicit', 'export', 'extern', 'false', 'float', 'for',
    'friend', 'goto', 'if', 'inline', 'int', 'long', 'mutable', 'namespace', 'new', 'noexcept',
    'not', 'not_eq', 'nullptr', 'operator', 'or', 'or_eq', 'private', 'protected', 'public',
    'register', 'reinterpret_cast', 'requires', 'return', 'short', 'signed', 'sizeof', 'static',
    'static_assert', 'static_cast', 'struct', 'switch', 'template', 'this', 'thread_local', 'throw',
    'true', 'try', 'typedef', 'typeid', 'typename', 'union', 'unsigned', 'using', 'virtual', 'void',
    'volatile', 'wchar_t', 'while', 'xor', 'xor_eq'
]

CPP_DEFS = [
    'class', 'enum', 'namespace', 'struct', 'typedef', 'union'
]

CPP_BUILTINS = [
    'abort', 'abs', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'exp', 'fabs', 'floor',
    'fmod', 'log', 'log10', 'max', 'min', 'pow', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tolower',
    'toupper', 'setprecision', 'fixed', 'setw', 'setfill', 'endl', 'cin', 'cout'
]

class Text(tk.Text):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.pack_propagate()
        self.config(relief=tk.FLAT, wrap=tk.WORD)
        self.path = None

        self.tag_configure("keyword", foreground="#989898")
        self.tag_configure("def", foreground="#636363")
        self.tag_configure("builtin", foreground="#949494")
        self.tag_configure("string", foreground="#4E4E4E")
        self.tag_configure("comment", foreground="#C9C9C9")
        self.tag_configure("TODO", background="#515151", foreground="#C9C9C9")

        self.configure(font=("FixedSys", 16))

        self.focus_set()
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
    
    def _proxy(self, *args):
        if args[0] == 'get' and (args[1] == tk.SEL_FIRST and args[2] == tk.SEL_LAST) and not self.tag_ranges(tk.SEL): 
            return
        if args[0] == 'delete' and (args[1] == tk.SEL_FIRST and args[2] == tk.SEL_LAST) and not self.tag_ranges(tk.SEL): 
            return

        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")
            
        return result

    def write(self, text):
        self.insert('1.0', text)
    
    def clear(self):
        self.delete('1.0', tk.END)

    def readfile(self, path):
        self.path = path
        self.clear()
        with open(path, 'r', encoding='UTF-8') as fp:
            self.write(fp.read())

    def highlight(self, *_):
        if not self.path: 
            return
        
        io_text = io.StringIO(self.get("1.0", "end"))
        if self.path.endswith('.py'):
            for token_type, token, start, end, _ in tokenize.generate_tokens(io_text.readline):
                s = f"{start[0]}.{start[1]}"
                e = f"{end[0]}.{end[1]}"
                if token in PY_KEYWORDS:
                    self.tag_add("keyword", s, e)
                elif token in PY_DEFS:
                    self.tag_add("def", s, e)
                elif token in PY_BUILTINS:
                    self.tag_add("builtin", s, e)
                elif token_type == tokenize.STRING:
                    self.tag_add("string", s, e)
                elif token_type == tokenize.COMMENT:
                    self.tag_add("comment", s, e)
                elif token == "TODO":
                    self.tag_add("TODO", s, e)
        elif self.path.endswith('.c') or self.path.endswith('.cpp') or self.path.endswith('.h'):
            for token_type, token, start, end, _ in tokenize.generate_tokens(io_text.readline):
                s = f"{start[0]}.{start[1]}"
                e = f"{end[0]}.{end[1]}"
                if token in CPP_KEYWORDS:
                    self.tag_add("keyword", s, e)
                elif token in CPP_DEFS:
                    self.tag_add("def", s, e)
                elif token in CPP_BUILTINS:
                    self.tag_add("builtin", s, e)
                elif token_type == tokenize.STRING:
                    self.tag_add("string", s, e)
                elif token_type == tokenize.COMMENT:
                    self.tag_add("comment", s, e)
                elif token == "TODO":
                    self.tag_add("TODO", s, e)