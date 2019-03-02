#核心代码
#文件名：core.py (Python-3.7.2)
#汉译@ybay 2019.3.1
#‘远程设备.内核’(distutils.core)，Distutils可以用来在Python环境中构建和安装额外的模块。

"""distutils.core

使用 Distutils 需要导入的唯一模块；提供“设置”(setup)功能(将从设置脚本中调用)。
也间接提供 Distribution 与 Command类，尽管它们实际上是在 distutils.dist 
和 distants.cmd中所定义的。
"""

import os
import sys

from distutils.debug import DEBUG
from distutils.errors import *

# 主要是导入这些脚本，这样安装脚本就可以“从‘远程设备.内核’(distutils.core)导入”它们。
from distutils.dist import Distribution
from distutils.cmd import Command
from distutils.config import PyPIRCCommand
from distutils.extension import Extension

#这是在用户运行安装脚本时生成的不带参数的帮助消息。
#使用各种帮助选项生成更有用的帮助: 全局帮助、列表命令和按命令帮助。
USAGE = """\
用法: %(script)s [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
  或: %(script)s --help [cmd1 cmd2 ...]
  或: %(script)s --help-commands
  或: %(script)s cmd --help
"""

def gen_usage (script_name):
    script = os.path.basename(script_name)
    return USAGE % vars()


# 从“run_setup ( )”中控制“setup ( )”行为的一些渐进做法。
_setup_stop_after = None
_setup_distribution = None

# setup ( )函数的合法关键字参数
setup_keywords = ('distclass', 'script_name', 'script_args', 'options',
                  'name', 'version', 'author', 'author_email',
                  'maintainer', 'maintainer_email', 'url', 'license',
                  'description', 'long_description', 'keywords',
                  'platforms', 'classifiers', 'download_url',
                  'requires', 'provides', 'obsoletes',
                  )

# 扩展构造函数的合法关键字参数
extension_keywords = ('name', 'sources', 'include_dirs',
                      'define_macros', 'undef_macros',
                      'library_dirs', 'libraries', 'runtime_library_dirs',
                      'extra_objects', 'extra_compile_args', 'extra_link_args',
                      'swig_opts', 'export_symbols', 'depends', 'language')

def setup (**attrs):
    """Distutils的网关:以高度灵活和用户驱动的方式，完成安装脚本需要做的一切。
	简而言之:创建分发实例；查找和解析配置文件；解析命令行；运行在那里找到的
	每个Distutils命令，通过提供给“setup ( )”(作为关键字参数)、配置文件和命令
	行的选项进行自定义。

    Distribution 实例可能是通过“distclass”关键字参数提供给“setup”的类的实例；、
	如果没有提供这样的类，那么Distribution类(在dist.py中)被实例化。
    “setup”(除了“cmdclass”)的所有其他参数都用于设置 Distribution 实例的属性。
    如果提供了“cmdclass”参数，则该参数是将命令名映射到命令类的字典。命令行上
	遇到的每个命令都将被转换成一个命令类，然后被实例化；在“cmdclass”中找到的
	任何类都被用来代替默认值，默认值是(对于命令“foo_bar”)模块
	“distutils.command.foo_bar”中的类“foo_bar”。命令类必须提供一个
	“user_options”属性，该属性是“distutils.fancy _ getopt”的选项说明符列表。
	当前命令和下一个命令之间的任何命令行选项都用于设置当前命令对象的属性。

    当整个命令行被成功解析后，依次在每个命令对象上调用“run()”方法。这个方法
	将完全由Distribution对象(由于其构造函数，每个命令对象都有引用)和成为每个
	命令对象属性的命令特定选项驱动。
    """

    global _setup_stop_after, _setup_distribution

    #确定分发类-呼叫方提供的或我们的分发(见下文)。
    klass = attrs.get('distclass')
    if klass:
        del attrs['distclass']
    else:
        klass = Distribution

    if 'script_name' not in attrs:
        attrs['script_name'] = os.path.basename(sys.argv[0])
    if 'script_args'  not in attrs:
        attrs['script_args'] = sys.argv[1:]

    # 使用剩余的参数(即：除了distclass之外的所有东西)来初始化它
    try:
        _setup_distribution = dist = klass(attrs)
    except DistutilsSetupError as msg:
        if 'name' not in attrs:
            raise SystemExit("设置命令出错: %s" % msg)
        else:
            raise SystemExit("错误在 %s 设置命令: %s" % \
                  (attrs['name'], msg))

    if _setup_stop_after == "init":
        return dist

    # 查找并解析配置文件:它们将覆盖设置脚本中的选项，但会被命令行覆盖。
    dist.parse_config_files()

    if DEBUG:
        print("选项(解析配置文件后) :")
        dist.dump_option_dicts()

    if _setup_stop_after == "config":
        return dist

    # 解析命令行并覆盖配置文件；任何命令行错误是最终用户的错误，因此将
	# 其转换为SystemExit以抑制追溯。
    try:
        ok = dist.parse_command_line()
    except DistutilsArgError as msg:
        raise SystemExit(gen_usage(dist.script_name) + "\n错误: %s" % msg)

    if DEBUG:
        print("选项(解析命令行后):")
        dist.dump_option_dicts()

    if _setup_stop_after == "commandline":
        return dist

    # 最后，运行命令行中找到的所有命令。
    if ok:
        try:
            dist.run_commands()
        except KeyboardInterrupt:
            raise SystemExit("interrupted")
        except OSError as exc:
            if DEBUG:
                sys.stderr.write("错误: %s\n" % (exc,))
                raise
            else:
                raise SystemExit("错误: %s" % (exc,))

        except (DistutilsError,
                CCompilerError) as msg:
            if DEBUG:
                raise
            else:
                raise SystemExit("错误: " + str(msg))

    return dist

# setup ()


def run_setup (script_name, script_args=None, stop_after="run"):
    """在稍微受控制的环境中运行安装脚本，并返回驱动事物的Distribution实例。
	如果您需要查找分发元数据(作为关键字 args 从“脚本”传递到“setup ( )”)，
	或者配置文件或命令行的内容，这很有用。

	“script_name”是一个将使用“exec ()”读取和运行的文件；在通话期间，
	sys.argv[0]”将替换为“script”。“script_args”是字符串列表；如果提供，
	“sys.argv[1:]”将在呼叫期间被“script_args”替换。

    'stop_after告诉“setup( )”何时停止处理；可能值:
      init
        创建分发实例并使用关键字参数填充“setup( )”后停止
      config
        解析配置文件后停止(及其存储在分发实例中)
      commandline
        解析命令行(“sys.argv[1:]”或“script_args”)后停止(并将数据存储在分发中)
      run [default]
        运行完所有命令后停止(就像以通常的方式调用“setup( )”一样)

    返回Distribution实例，该实例提供用于驱动Distutils的所有信息。
    """
    if stop_after not in ('init', 'config', 'commandline', 'run'):
        raise ValueError("'stop_after'的值无效: %r" % (stop_after,))

    global _setup_stop_after, _setup_distribution
    _setup_stop_after = stop_after

    save_argv = sys.argv.copy()
    g = {'__file__': script_name}
    try:
        try:
            sys.argv[0] = script_name
            if script_args is not None:
                sys.argv[1:] = script_args
            with open(script_name, 'rb') as f:
                exec(f.read(), g)
        finally:
            sys.argv = save_argv
            _setup_stop_after = None
    except SystemExit:
        # 嗯，如果用非零代码退出，我们应该做些什么吗
        # (即：错误)？
        pass

    if _setup_distribution is None:
        raise RuntimeError(("从未调用'distutils.core.setup()' -- "
               "也许 '%s' 不是远程安装脚本?") % \
              script_name)

    # 我想知道安装脚本的命名空间-- g and l --是否是
    # 来电者有兴趣吗？
    # 打印"_setup_distribution:", _setup_distribution
    return _setup_distribution

# run_setup ()
