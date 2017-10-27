" This next set of lines and weirdess is to make sure pathogen and all plugins
" work
call pathogen#runtime_append_all_bundles()
filetype on                    " read the docs on this one!
filetype off
syntax on                      " enable syntax hhighlighting
filetype plugin indent on
call pathogen#helptags()

colorscheme slate "darkblue "Darkcarvedwood_cust
" Dark
set ruler                      " Show the line and column number of the cursor position
set cindent                    " Enables automatic C program indenting
set tabstop=2                  " Number of spaces that a <Tab> in the file counts for
set softtabstop=2              " Number of spaces that a <Tab> counts for while performing editing operations, like inserting a <Tab> or using <BS>.
set shiftwidth=2               " Number of spaces to use for each step of (auto)indent
set noexpandtab                " Use tabs not spaces
set ignorecase                 " Ignore case in search patterns
set smartcase                  " Override the 'ignorecase' option if the search pattern contains upper case characters
set nowrap                     " Don't wrap at the end of the window buffer
"set showmatch                  " When a bracket is inserted, briefly jump to the matching one.
set autoindent                 " Copy indent from current line when starting a new line
set guioptions+=a              " highlighting text copies that text to the clip board
set wildmenu                   " possible matches are shown just above the command line
set backspace=indent,eol,start " allow backspace to work over elements named
set novisualbell               " Don't use visual bell - stop the flashing
set incsearch                  " show matches as you type
set hlsearch                   " highlight all matches after typing
set guifont=Andale\ Mono\ 12   " a list of fonts which will be used for the GUI version of Vim
"set guifont=gohufont-14
set number                     " precede each line with its line number
set spell spelllang=en_gb      " enable spell-checking

"-------------------
" This will look in the current directory for "tags", and work up the 
" tree towards root until one is found. 
" IOW, you can be anywhere in your source tree instead of just the 
" root of it.
set tags=tags;/

"taglist setup
let Tlist_Ctags_Cmd = 'd:/UnixUtils/ctags'
:nnoremap <silent> <F3> :Tlist<CR>
let Tlist_WinWidth = 50


hi Visual gui=bold guibg=Black guifg=White
map <F7> :wall<CR>:make<CR>
map <F8> :wall<CR>:make debug<CR>
map <C-p> "0p
map <C-P> "0P
map <C-Left> :tabp<CR>
map <C-Right> :tabn<CR>
map :W :w
map :Q :q

" function that toggles between editing the source and header file for a file pair
" bound to alt-tab by default
function EAlt()
	let curext=expand("%:e")
	let base=expand("%:r")
	let altfile=""
	let ffile=""
	if (curext=="h")
		" try looking for a .c or .cpp file
		if (filereadable(base.".c"))
			let altfile = base.".c"
		elseif (filereadable(base.".cpp"))
			let altfile = base.".cpp"
		else
			" special case, if in the engine include dir then look for a c file in the non include dir
			let altfile = substitute(base,"include/engine","Source","")
			echo altfile
			if (filereadable(altfile.".c"))
				let altfile = altfile.".c"
			elseif (filereadable(altfile.".cpp"))
				let altfile = altfile.".cpp"
			else
				let altfile = ""
				let ffile = expand("%:t:r").".cpp"
			endif
		endif
	elseif (curext=="cpp"|| curext=="c")
		if (filereadable(base.".h"))
			let altfile = base.".h"
		else
			let ffile = expand("%:t:r").".h"
		endif
	endif
	if (altfile!="")
		exe ":edit " altfile
	elseif (ffile!="")
		exe ":find " ffile
	else
		echo "No alt file found"
	endif
endfunction
" mapping M-I should be alt-tab, but it doesn't seem to work. Mapping C-I (cntl-tab) seems to make both control and alt tab work??
map <M-`>      :call EAlt()<CR>

" this is dynamic tags taken from jimB -- slowing down too much ??
"let g:ctags_path='/usr/bin/ctags'
"let g:ctags_args='-I __declspec+ --c-types=f'
"let g:ctags_statusline=1
"let g:ctags_title = 1
"let generate_tags=1
"source $HOME/vim/ctags.vim

"-------------------
" fix up the tag function to show the full list instead of the first match
map <C-]> :tjump <C-R>=expand("<cword>")<CR><CR>

" fix all uses of ta->tj as the new ta is fixed and want it to call tj instead
cabbrev ta tj 

"enable matchit plugin
source $VIMRUNTIME/macros/matchit.vim

""""""""""""""""""""""""""""
" vimoutliner stuff
filetype plugin indent on
runtime! ftdetect/*.vim
syntax on
au! BufRead,BufNewFile *.otl            setfiletype vo_base
""""""""""""""""""""""""""""

"-------------------
" Syntax mapping for :
" Actionscript files
au! BufNewFile,BufRead *.as setlocal ft=javascript
" shader files
au! BufNewFile,BufRead *.shader setlocal ft=c
" SConscripts with .py extensions
au! BufNewFile,BufRead SConscript setlocal ft=python

""""""""""""""""""""""""""""
" show tabs
set list
set listchars=tab:→\ 

""""""""""""""""""""""
" Py-mode config
let g:pymode_folding = 0
let g:pymode_indent = 0
let g:pymode_python = 'python3'
""""""""""""""""""""""""""""

""""""""""""""""""""""
" signify - git-gutter replacement config
" get more frequent updates
let g:signify_realtime=1
""""""""""""""""""""""""""""
