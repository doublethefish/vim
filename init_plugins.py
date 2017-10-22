#!/usr/bin/env python3
import subprocess
from multiprocessing import Process
USE_SSH = True
PLUGIN_MODULES = [
        ('github.com/msanders/snipmate.vim.git',            'bundle/snipmate'),
        ('github.com/tpope/vim-surround.git',               'bundle/surround'),
        ('github.com/tpope/vim-git.git',                    'bundle/git'),
        ('github.com/ervandew/supertab.git',                'bundle/supertab'),
        ('github.com/fholgado/minibufexpl.vim.git',         'bundle/minibufexpl'),
        ('github.com/wincent/Command-T.git',                'bundle/command-t'),
        ('github.com/mitechie/pyflakes-pathogen.git',       'bundle/pyflakes'),
        ('github.com/mileszs/ack.vim.git',                  'bundle/ack'),
        ('github.com/sjl/gundo.vim.git',                    'bundle/gundo'),
        ('github.com/fs111/pydoc.vim.git',                  'bundle/pydoc'),
        ('github.com/vim-scripts/pep8.git',                 'bundle/pep8'),
        ('github.com/alfredodeza/pytest.vim.git',           'bundle/py.test'),
        ('github.com/reinh/vim-makegreen.git',              'bundle/makegreen'),
        ('github.com/vim-scripts/TaskList.vim.git',         'bundle/tasklist'),
        ('github.com/vim-scripts/The-NERD-tree.git',        'bundle/nerdtree'),
        ('github.com/python-rope/ropevim.git',              'bundle/ropevim'),
        ('github.com/plasticboy/vim-markdown.git',          'bundle/vim-markdown.git'),
        ('github.com/keith/swift.vim.git',                  'bundle/swift_vim'),
        ]


def synchronous_sub_proc_run( cmd_list, error_msg="", cwd=None):
    proc_run_info = subprocess.run(cmd_list, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret_code = proc_run_info.returncode
    if ret_code != 0 :
        if b"already exists in the index" in proc_run_info.stderr:
            return
        print(proc_run_info.stdout)
        print(proc_run_info.stderr)
        raise RuntimeError("%s Exit code was %d"%(cmd_list, ret_code))


def installModule(MODULE_URL, INSTALL_LOCATION):
    if USE_SSH:
        prefix = "git@"
        MODULE_URL = MODULE_URL.replace("github.com/", "github.com:")
    else:
        prefix = "https://"
    print(MODULE_URL)
    MODULE_URL = prefix + MODULE_URL
    cmd = ['git', 'submodule', 'add', MODULE_URL, INSTALL_LOCATION]
    synchronous_sub_proc_run(cmd)


for PLUGIN_INFO in PLUGIN_MODULES:
  URL              = PLUGIN_INFO[0]
  INSTALL_LOCATION = PLUGIN_INFO[1]
  installModule(URL, INSTALL_LOCATION)

post_setup_init_cmds = (
    ['git', 'submodule', 'init'],
    ['git', 'submodule', 'update'],
    ['git', 'submodule', 'foreach', 'git', 'submodule', 'init'],
    ['git', 'submodule', 'foreach', 'git', 'submodule', 'update'],
)
for cmd in post_setup_init_cmds:
    synchronous_sub_proc_run(cmd)
print("DONE")
