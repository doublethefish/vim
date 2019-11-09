#!/usr/bin/env python3
import datetime
import os
import subprocess
import shutil


def backup_plugins_dir(bundle_path):
    time_stamp = str(datetime.datetime.utcnow())
    time_stamp = time_stamp.translate(str.maketrans(" -:.", "_" * 4))
    try:
        shutil.move(bundle_path, "%s-%s-bak" % (bundle_path, time_stamp))
    except FileNotFoundError:
        pass


bundle_path = os.path.abspath("%s/.vim/bundle" % os.environ.get("HOME", "."))
backup_plugins_dir(bundle_path)

# Make the install dir for plgins
os.makedirs(bundle_path, exist_ok=True)

USE_SSH = True
PLUGIN_MODULES = [
    (
        "github.com/w0rp/ale.git",
        "bundle/ale.git",
        "Asynchronous Lint Engine",
        ":help ale_python",
    ),
    (
        "github.com/garbas/snipmate.vim.git",
        "bundle/snipmate.git",
        "Extra snippet on <tab>",
        ":help snipMate",
    ),
    (
        "github.com/tpope/vim-surround.git",
        "bundle/surround.git",
        "Change surrounding chars",
        "cs'<p>, :help surround",
    ),
    ("github.com/tpope/vim-fugitive", "bundle/fuGITive.git", "Git wrapper", "help: G"),
    (
        "github.com/mileszs/ack.vim.git",
        "bundle/ack.git",
        "Ack search tool",
        r":Ack [options] {pattern} [{directories}], :h Ack",
    ),
    ("github.com/sjl/gundo.vim.git", "bundle/gundo.git", "Visualize Undo Tree", "????"),
    (
        "github.com/reinh/vim-makegreen.git",
        "bundle/makegreen.git",
        "Show test-run status",
        ":MakeGreen %",
    ),
    # conflicts with command-t
    # ('github.com/vim-scripts/The-NERD-tree.git',  'bundle/nerdtree.git'),
    (
        "github.com/plasticboy/vim-markdown.git",
        "bundle/vim-markdown.git",
        "Highlighting for .md",
        ":h vim-markdown",
    ),
    (
        "github.com/keith/swift.vim.git",
        "bundle/swift_vim.git",
        "Syntax and indent files for Swift",
        "no help",
    ),
    (
        "github.com/mhinz/vim-signify.git",
        "bundle/vim-signify.git",
        "Shows diff in the gutter",
        ":h signify",
    ),
    (
        "github.com/artoj/qmake-syntax-vim.git",
        "bundle/qmake-syntax-vim.git",
        "Syntax etc for qmake files",
        "no help",
    ),
    (
        "github.com/tpope/vim-abolish.git",
        "bundle/abolish.git",
        "Subvert, coercion (crs, cru), Abbreviation",
        "h: crs, h:abbrviations, :Subvert, really nice",
    ),
    (
        "github.com/vimoutliner/vimoutliner.git",
        "bundle/vimoutliner.git",
        "Quick note taking and outlineing of tasks/information",
        "h: vo, use ',,', <leader>cb, <leader>cp, <leader>s, <leader>S",
    ),
]

PYTHON_PLUGINS = [
    (
        "github.com/alfredodeza/pytest.vim.git",
        "bundle/py.test.git",
        "Py.test wrapper",
        ":h test",
    ),
    (
        "github.com/python-mode/python-mode.git",
        "bundle/python-mode.git",
        "",
        ":help pymode, '<C-c>rm',  '<leader>r' -> runs the current python script, '<leader>b' adds a breakpoints",
    ),
]
PLUGIN_MODULES.extend(PYTHON_PLUGINS)


def synchronous_sub_proc_run(cmd_list, error_msg="", cwd=None):
    proc_run_info = subprocess.run(
        cmd_list, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    ret_code = proc_run_info.returncode
    if ret_code != 0:
        if b"already exists in the index" in proc_run_info.stderr:
            return
        print(proc_run_info.stdout)
        print(proc_run_info.stderr)
        raise RuntimeError("%s Exit code was %d" % (" ".join(cmd_list), ret_code))


def get_correct_prefix(MODULE_URL, USE_SSH=USE_SSH):
    if USE_SSH:
        prefix = "git@"
        MODULE_URL = MODULE_URL.replace("github.com/", "github.com:")
    else:
        prefix = "https://"
    print(MODULE_URL)
    MODULE_URL = prefix + MODULE_URL
    return MODULE_URL


def installModule(MODULE_URL, INSTALL_LOCATION):
    MODULE_URL = get_correct_prefix(MODULE_URL)
    cmd = ["git", "submodule", "add", "--force", MODULE_URL, INSTALL_LOCATION]
    synchronous_sub_proc_run(cmd)


for PLUGIN_INFO in PLUGIN_MODULES:
    URL = PLUGIN_INFO[0]
    INSTALL_LOCATION = PLUGIN_INFO[1]
    summary = PLUGIN_INFO[2]
    print(summary)
    installModule(URL, INSTALL_LOCATION)

cmd = ["git", "add", INSTALL_LOCATION]
synchronous_sub_proc_run(cmd)

post_setup_init_cmds = (
    ["git", "submodule", "init"],
    ["git", "submodule", "update", "--init", "--recursive"],
    ["git", "submodule", "foreach", "git", "submodule", "init"],
    ["git", "submodule", "foreach", "git", "submodule", "update"],
)
for cmd in post_setup_init_cmds:
    synchronous_sub_proc_run(cmd)
print("DONE")
