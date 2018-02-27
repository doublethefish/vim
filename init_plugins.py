#!/usr/bin/env python3
import os
import subprocess
import shutil
import sys

# forces the sub dir to be deleted if we've
# uninstalled the module
DEL = True

USE_SSH = True
PLUGIN_MODULES = [
    ('github.com/msanders/snipmate.vim.git',      'bundle/snipmate.git'),
    (DEL, 'github.com/msanders/snipmate.vim.git',      'bundle/snipmate'),
    ('github.com/tpope/vim-surround.git',         'bundle/surround.git'),
    (DEL, 'github.com/tpope/vim-surround.git',         'bundle/surround'),
    ('github.com/tpope/vim-git.git',              'bundle/git.git'),
    (DEL, 'github.com/tpope/vim-git.git',              'bundle/git'),
    (DEL, 'github.com/ervandew/supertab.git',          'bundle/supertab.git'), # pile of crap
    (DEL, 'github.com/ervandew/supertab.git',          'bundle/supertab'),
    ('github.com/fholgado/minibufexpl.vim.git',   'bundle/minibufexpl.git'),
    (DEL, 'github.com/fholgado/minibufexpl.vim.git',   'bundle/minibufexpl'),
    # to install Command-T on mac ensure you've got the ruby-dev stuff installed
    # sudo xcode-select --install
    ('github.com/wincent/Command-T.git',          'bundle/command-t.git'),
    (DEL, 'github.com/wincent/Command-T.git',     'bundle/command-t'),
    ('github.com/mileszs/ack.vim.git',            'bundle/ack.git'),
    (DEL, 'github.com/mileszs/ack.vim.git',       'bundle/ack'),
    ('github.com/sjl/gundo.vim.git',              'bundle/gundo.git'),
    (DEL, 'github.com/sjl/gundo.vim.git',         'bundle/gundo'),
    ('github.com/reinh/vim-makegreen.git',        'bundle/makegreen.git'),
    (DEL, 'github.com/reinh/vim-makegreen.git',   'bundle/makegreen'),
    # conflicts with command-t
    (DEL, 'github.com/vim-scripts/TaskList.vim.git',   'bundle/tasklist'),
    ('github.com/vim-scripts/The-NERD-tree.git',  'bundle/nerdtree.git'),
    (DEL, 'github.com/vim-scripts/The-NERD-tree.git',  'bundle/nerdtree'),
    ('github.com/plasticboy/vim-markdown.git',    'bundle/vim-markdown.git'),
    ('github.com/keith/swift.vim.git',            'bundle/swift_vim.git'),
    (DEL, 'github.com/keith/swift.vim.git',       'bundle/swift_vim'),
    (DEL, 'github.com/keith/swift.vim.git',       'bundle/swift.vim'),
    ('github.com/mhinz/vim-signify.git',          'bundle/vim-signify.git'),
    (DEL, 'github.com/mhinz/vim-signify.git',     'bundle/vim-signify'),
    ('github.com:artoj/qmake-syntax-vim.git', 'bundle/qmake-syntax-vim.git'),
    ]

PYTHON_PLUGINS = [
    (DEL, 'github.com/python-rope/ropevim.git',           'bundle/ropevim'),
    (DEL, 'github.com/mitechie/pyflakes-pathogen.git',    'bundle/pyflakes'),
    (DEL, 'github.com/fs111/pydoc.vim.git',               'bundle/pydoc'),
    (DEL, 'github.com/vim-scripts/pep8.git',              'bundle/pep8'),
    ('github.com/alfredodeza/pytest.vim.git',             'bundle/py.test.git'),
    ('github.com:python-mode/python-mode.git', 'bundle/python-mode.git'),
    ]
PLUGIN_MODULES.extend(PYTHON_PLUGINS)


def synchronous_sub_proc_run(cmd_list, error_msg="", cwd=None):
    proc_run_info = subprocess.run(cmd_list, cwd=cwd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
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
    cmd = ['git', 'submodule', 'add', '--force', MODULE_URL, INSTALL_LOCATION]
    synchronous_sub_proc_run(cmd)


def uninstallModule(MODULE_URL, INSTALL_LOCATION):
    if not os.path.exists(INSTALL_LOCATION):
        return False
    print("Uninstalling: '%s' (will require commit)" % INSTALL_LOCATION)
    ssh = get_correct_prefix(MODULE_URL, USE_SSH=True)
    https = get_correct_prefix(MODULE_URL, USE_SSH=False)
    for module_url in (ssh, https):
        cmd = ['git', 'submodule', 'deinit', '--force', INSTALL_LOCATION]
        try:
            synchronous_sub_proc_run(cmd)
        except RuntimeError:
            # may have already been installed
            pass
        cmd = ['git', 'rm', 'deinit', INSTALL_LOCATION]
        try:
            synchronous_sub_proc_run(cmd)
        except RuntimeError:
            # may have already been installed
            pass
    INSTALL_LOCATION = os.path.abspath(INSTALL_LOCATION)
    try:
        shutil.rmtree(INSTALL_LOCATION)
    except FileNotFoundError:
        # assume already uninstalled
        pass
    cmd = ['git', 'add', INSTALL_LOCATION]
    try:
        synchronous_sub_proc_run(cmd)
    except RuntimeError:
        pass
    assert(not os.path.exists(INSTALL_LOCATION))
    return True


uninstalled_a_plug_in = False
for PLUGIN_INFO in PLUGIN_MODULES:
    install = True
    if len(PLUGIN_INFO) == 3:
        assert(PLUGIN_INFO[0] == DEL)
        PLUGIN_INFO = PLUGIN_INFO[1:]
        install = False
    URL = PLUGIN_INFO[0]
    INSTALL_LOCATION = PLUGIN_INFO[1]
    if install:
        installModule(URL, INSTALL_LOCATION)
    else:
        uninstalled = uninstallModule(URL, INSTALL_LOCATION)
        uninstalled_a_plug_in = uninstalled_a_plug_in or uninstalled

cmd = ['git', 'add', INSTALL_LOCATION]
synchronous_sub_proc_run(cmd)

if uninstalled_a_plug_in:
    print("You need to commit the deletion of the modules before continuing")
    print("Run this command again once done")
    sys.exit(0)

post_setup_init_cmds = (
    ['git', 'submodule', 'init'],
    ['git', 'submodule', 'update'],
    ['git', 'submodule', 'foreach', 'git', 'submodule', 'init'],
    ['git', 'submodule', 'foreach', 'git', 'submodule', 'update'],
)
for cmd in post_setup_init_cmds:
    synchronous_sub_proc_run(cmd)
print("DONE")
