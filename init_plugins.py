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
    ("github.com/w0rp/ale.git", "bundle/ale.git"),
    ("github.com/garbas/snipmate.vim.git", "bundle/snipmate.git"),
    ("github.com/tpope/vim-surround.git", "bundle/surround.git"),
    ("github.com/tpope/vim-git.git", "bundle/git.git"),
    # to install Command-T on mac ensure you've got the ruby-dev stuff installed
    # sudo xcode-select --install
    ("github.com/wincent/Command-T.git", "bundle/command-t.git"),
    ("github.com/mileszs/ack.vim.git", "bundle/ack.git"),
    ("github.com/sjl/gundo.vim.git", "bundle/gundo.git"),
    ("github.com/reinh/vim-makegreen.git", "bundle/makegreen.git"),
    # conflicts with command-t
    ("github.com/vim-scripts/The-NERD-tree.git", "bundle/nerdtree.git"),
    ("github.com/plasticboy/vim-markdown.git", "bundle/vim-markdown.git"),
    ("github.com/keith/swift.vim.git", "bundle/swift_vim.git"),
    ("github.com/mhinz/vim-signify.git", "bundle/vim-signify.git"),
    ("github.com:artoj/qmake-syntax-vim.git", "bundle/qmake-syntax-vim.git"),
]

PYTHON_PLUGINS = [
    ("github.com/alfredodeza/pytest.vim.git", "bundle/py.test.git"),
    ("github.com:python-mode/python-mode.git", "bundle/python-mode.git"),
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
