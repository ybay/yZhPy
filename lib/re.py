#
#加密实验室(Secret Labs)的正则表达式引擎
#文件名：re.py
#汉译@ybay 2019.3.1
#
# re —— SRE 匹配引擎的兼容接口
#
#版权(c) 1998-2001由加密实验室AB(Secret Labs AB)发行。保留所有权利。
#
#这个版本的SRE库可以在CNRI库 Python 1.6 许可证下重新分发
#（CNRI，Corporation for National Research Initiatives） 。
#如有任何其他用途，请联系加密实验室AB(info@pythonware.com)。
#
#这款引擎的有些部分是与 CNRI 合作开发的。
#惠普为 1.6 集成以及其他兼容性工作提供了资金。
#

"""支持正则表达式( RE )。

本模块提供类似于那些在Perl中所见的正则表达式匹配操作。它既支持8位字符
也支持Unicode字符串；能处理的字符和字符串可以包含空字节和超出美国ASCII
范围之外的字符。

正则表达式可以包含特殊字符和原义字符。大多数原义字符，如“A”、“a”或“0”，
都是最简单的正则表达式；它们只是匹配自己而已。你可以将其关联到那些原义字符，
如最近的匹配字符串“last”。

特殊字符:
    "."      匹配除换行符以外的任何字符。
    "^"      匹配字符串的开头。
    "$"      匹配字符串的结尾或刚好在的换行符之前字符串的末尾。
    "*"      匹配前述RE的0次或更多次(贪婪)重复。贪婪意味着它会匹配尽可能多的重复。
    "+"      匹配前述RE的1次或多次(贪婪)重复。
    "?"      匹配前述RE的0或1(贪婪)。
    *?,+?,?? 前面三个特殊字符的非贪婪格式。
    {m,n}    匹配前述RE的 m 到 n 次重复。
    {m,n}?   上面的非贪婪格式。
    "\\"     转义特殊字符或者标记特殊序列信息。
    []       指示一组字符。
             “^”作为第一个字符出现表示是一互补集。
    "|"      A|B, 创建一个与A或B匹配的RE。
    (...)    匹配括号内的RE。
             内容可以在所附的字符串中检索或匹配。
    (?aiLmsux) 为RE设置A、I、L、M、S、U或X标志(见下文)。
    (?:...)  常规括号的非分组格式。
    (?P<name>...) 可以通过名称访问的成组匹配的子字符串。
    (?P=name) 匹配前面命名过的成组匹配的文本。
    (?#...)  评论；忽略。
    (?=...)  如果...匹配下一个但不摄取该字符串，则匹配。
    (?!...)  如果...不匹配后续的，则匹配。
    (?<=...) 如果由...预设的(必须是固定长度)，则匹配。
    (?<!...) 如果前面没有...(必须是固定长度)，则匹配。
    (?(id/name)yes|no) 如果id/名称的组匹配过则匹配“是”模式，否则(可选)匹配“否”模式。

特殊序列由“\\”和下列表中的一个字符组成。如果原义字符不在列表中，则
将导致RE匹配第二个字符。
    \number  相同数字的内容则匹配。
    \A       仅在字符串的首位匹配。
    \Z       仅在字符串的末端匹配。
    \b       仅匹配在单词的开头或结尾的空字符串。
    \B       不匹配在单词的开头或结尾的空字符串。
    \d       Matches any decimal digit; equivalent to the set [0-9] in
             bytes patterns or string patterns with the ASCII flag.
             In string patterns without the ASCII flag, it will match the whole
             range of Unicode digits.
			 匹配任何十进制数字；相当于带有ASCII标志的字节模式或字符串模式的集合[ 0 - 9 ]。
             在没有ASCII标志的字符串模式中，它将匹配整个字符串Unicode数字的范围。
    \D       匹配任何非数字字符；相当于[·^\d。
    \s       匹配任何空白字符；相当于带有ASCII标志的字节模式或字符串模式中的[\t\n\r\f\v]。
             在没有ASCII标志的字符串模式中，它将匹配整个Unicode空白字符范围。
    \S       匹配任何非空白字符；相当于[·^\s]。
    \w       匹配任何字母数字字符；相当于带有ASCII标志的字节模式或字符串模式中的[a-zA-Z0-9_。
             在没有ASCII标志的字符串模式中，它将匹配Unicode字母数字字符的范围(字母加数字加下划线)。
             使用 LOCAL，它将匹配当前区域设置中定义为字母的集合[ 0 - 9 _ ]加上字符。
    \W       匹配\W的补码。
    \\       匹配反斜杠字符。

本模块功能输出如下:
    match     将正则表达式模式与字符串的开头匹配。
    fullmatch 将正则表达式模式与所有字符串匹配。
    search    按规定格式搜索字符串。
    sub       把字符串中找到的格式内容做替换。
    subn      与sub相同，但返回替换的次数。
    split     根据格式的出现分割字符串。
    findall   在字符串中查找规定格式的所有匹配项。
    finditer  返回一个迭代器，为每个匹配产生一个匹配(Match)对象。
    compile   将格式编译成格式(Pattern)对象。
    purge     清除正则表达式缓存。
    escape    反斜杠字符串中的所有非字母数字。

本模块中的一些函数中作为可选参数的标识符:
    A  ASCII       对于字符串模式，使用 \w, \W, \b, \B, \d, \D
                   匹配相应的ASCII字符类别(而不是整个Unicode类别，后者是默认的)。
                   对于字节模式，此标志是唯一可用特征，无需指定。
    I  IGNORECASE  执行不区分大小写的匹配。
    L  LOCALE      使用 \w, \W, \b, \B, 这取决于当前的地域性设置。
    M  MULTILINE   “^”匹配行的开头(换行符之后)和字符串。
                   “$”匹配行尾(换行符之前)以及字符串的结尾。
    S  DOTALL      "."匹配任何字符，包括换行符。
    X  VERBOSE     忽略空白和注释，让RE结果看起来更漂亮。
    U  UNICODE     仅出于兼容性考虑。字符串格式被忽略(这是默认值)，字节模式被禁止。

此模块还定义了异常“错误”(error)。

"""

import enum
import sre_compile
import sre_parse
import functools
try:
    import _locale
except ImportError:
    _locale = None


# 全局符号
__all__ = [
    "match", "fullmatch", "search", "sub", "subn", "split",
    "findall", "finditer", "compile", "purge", "template", "escape",
    "error", "Pattern", "Match", "A", "I", "L", "M", "S", "X", "U",
    "ASCII", "IGNORECASE", "LOCALE", "MULTILINE", "DOTALL", "VERBOSE",
    "UNICODE",
]

__version__ = "2.2.1"

class RegexFlag(enum.IntFlag):
    ASCII = sre_compile.SRE_FLAG_ASCII # 假设属于 ascii “语言环境”（locale）
    IGNORECASE = sre_compile.SRE_FLAG_IGNORECASE # 忽略大小写
    LOCALE = sre_compile.SRE_FLAG_LOCALE # 假设当前为8位语言环境
    UNICODE = sre_compile.SRE_FLAG_UNICODE # 假设属于 unicode “语言环境”（locale）
    MULTILINE = sre_compile.SRE_FLAG_MULTILINE # 锚定到新行探寻
    DOTALL = sre_compile.SRE_FLAG_DOTALL # 做点匹配换新行
    VERBOSE = sre_compile.SRE_FLAG_VERBOSE # 忽略空白和注释
    A = ASCII
    I = IGNORECASE
    L = LOCALE
    U = UNICODE
    M = MULTILINE
    S = DOTALL
    X = VERBOSE
    # sre扩展(实验性的，不要依赖这些)
    TEMPLATE = sre_compile.SRE_FLAG_TEMPLATE # 禁止回溯
    T = TEMPLATE
    DEBUG = sre_compile.SRE_FLAG_DEBUG # 编译后的转储格式
globals().update(RegexFlag.__members__)

# sre 除外
error = sre_compile.error

# --------------------------------------------------------------------
# 全局接口

def match(pattern, string, flags=0):
    """尝试在字符串开头应用模式，返回Match对象；或者如果没有找到匹配项，则返回None。"""
    return _compile(pattern, flags).match(string)

def fullmatch(pattern, string, flags=0):
    """尝试将模式应用于所有字符串，返回Match对象；如果找不到匹配项，则返回None。"""
    return _compile(pattern, flags).fullmatch(string)

def search(pattern, string, flags=0):
    """扫描字符串，查找与模式匹配的内容，返回match对象；如果没有找到匹配内容，则返回None。"""
    return _compile(pattern, flags).search(string)

def sub(pattern, repl, string, count=0, flags=0):
    """返回通过用替换 repl 替换字符串中模式的最左边不重叠的部分而获得的字符串。
	repl 可以是字符串或可调用的；如果是字符串，则会处理其中的反斜杠转义。如果
	它是可调用的，它将传递Match对象，并且必须返回要使用的替换字符串。"""
    return _compile(pattern, flags).sub(repl, string, count)

def subn(pattern, repl, string, count=0, flags=0):
    """返回包含( new_string，number )的二元组。 
	new_tring 是通过用替换复制子替换源字符串中模式最左边的非重叠出现而获得的字符串。
	number是进行的替换的数量。repl 可以是字符串或可调用的；如果是字符串，则会处理其中的反斜杠转义。
    如果它是可调用的，它将传递 Match 对象，并且必须返回要使用的替换字符串。"""
    return _compile(pattern, flags).subn(repl, string, count)

def split(pattern, string, maxsplit=0, flags=0):
    """按照模式的出现分割源字符串，返回包含结果子字符串的列表。如果在模式中使用捕获括号，
	则模式中所有组的文本也将作为结果列表的一部分返回。如果maxsplit非零，最多会发生 maxsplit 拆分，
	字符串的剩余部分将作为列表的最后一个元素返回。"""
    return _compile(pattern, flags).split(string, maxsplit)

def findall(pattern, string, flags=0):
    """返回字符串中所有不重叠匹配项的列表。
    如果模式中存在一个或多个捕获组，则返回组列表；如果模式有多个组，这将是元组列表。
    结果中包含空匹配项。"""
    return _compile(pattern, flags).findall(string)

def finditer(pattern, string, flags=0):
    """返回字符串中所有非重叠匹配项的迭代器。对于每个匹配，迭代器返回一个match对象。
    结果中包含空匹配项。"""
    return _compile(pattern, flags).finditer(string)

def compile(pattern, flags=0):
    "编译正则表达式格式，返回一个 pattern 对象。"
    return _compile(pattern, flags)

def purge():
    "清除正则表达式缓存"
    _cache.clear()
    _compile_repl.cache_clear()

def template(pattern, flags=0):
    "编译模板格式，返回 Pattern 对象"
    return _compile(pattern, flags|T)

# SPECIAL_CHARS
# 闭括号 ')', '}' 与 ']'
# '-' (字符集中的一个范围)
# '&', '~', (扩展字符集操作)
# '#' 在冗余模式下的(注释)和空白(忽略)
_special_chars_map = {i: '\\' + chr(i) for i in b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f'}

def escape(pattern):
    """
    转义字符串中的特殊字符。
    """
    if isinstance(pattern, str):
        return pattern.translate(_special_chars_map)
    else:
        pattern = str(pattern, 'latin1')
        return pattern.translate(_special_chars_map).encode('latin1')

Pattern = type(sre_compile.compile('', 0))
Match = type(sre_compile.compile('', 0).match(''))

# --------------------------------------------------------------------
# 内部构件

_cache = {}  # 特定!

_MAXCACHE = 512
def _compile(pattern, flags):
    # 内部:编译模式
    if isinstance(flags, RegexFlag):
        flags = flags.value
    try:
        return _cache[type(pattern), pattern, flags]
    except KeyError:
        pass
    if isinstance(pattern, Pattern):
        if flags:
            raise ValueError(
                "无法使用编译模式处理标志参数")
        return pattern
    if not sre_compile.isstring(pattern):
        raise TypeError("第一个参数必须是字符串或编译模式")
    p = sre_compile.compile(pattern, flags)
    if not (flags & DEBUG):
        if len(_cache) >= _MAXCACHE:
            # 删除最旧的项目
            try:
                del _cache[next(iter(_cache))]
            except (StopIteration, RuntimeError, KeyError):
                pass
        _cache[type(pattern), pattern, flags] = p
    return p

@functools.lru_cache(_MAXCACHE)
def _compile_repl(repl, pattern):
    # 内部:编译替换模式
    return sre_parse.parse_template(repl, pattern)

def _expand(pattern, match, template):
    # 内部:匹配。展开实现钩联
    template = sre_parse.parse_template(template, pattern)
    return sre_parse.expand_template(template, match)

def _subx(pattern, template):
    # 内部: Pattern.sub/subn 实施助手
    template = _compile_repl(template, pattern)
    if not template[0] and len(template[1]) == 1:
        # 文字替换
        return template[1][0]
    def filter(match, template=template):
        return sre_parse.expand_template(template, match)
    return filter

# 登记自己的所爱

import copyreg

def _pickle(p):
    return _compile, (p.pattern, p.flags)

copyreg.pickle(Pattern, _pickle, _compile)

# --------------------------------------------------------------------
# 实验材料(详见python-dev讨论)

class Scanner:
    def __init__(self, lexicon, flags=0):
        from sre_constants import BRANCH, SUBPATTERN
        if isinstance(flags, RegexFlag):
            flags = flags.value
        self.lexicon = lexicon
        # 将短语组合成复合模式
        p = []
        s = sre_parse.Pattern()
        s.flags = flags
        for phrase, action in lexicon:
            gid = s.opengroup()
            p.append(sre_parse.SubPattern(s, [
                (SUBPATTERN, (gid, 0, 0, sre_parse.parse(phrase, flags))),
                ]))
            s.closegroup(gid, p[-1])
        p = sre_parse.SubPattern(s, [(BRANCH, (None, p))])
        self.scanner = sre_compile.compile(p)
    def scan(self, string):
        result = []
        append = result.append
        match = self.scanner.scanner(string).match
        i = 0
        while True:
            m = match()
            if not m:
                break
            j = m.end()
            if i == j:
                break
            action = self.lexicon[m.lastindex-1][1]
            if callable(action):
                self.match = m
                action = action(self, m.group())
            if action is not None:
                append(action)
            i = j
        return result, string[i:]
