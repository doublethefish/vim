call pathogen#runtime_append_all_bundles()
filetype on
filetype off
syntax on
filetype plugin indent on
call pathogen#helptags()

colorscheme slate "darkblue "Darkcarvedwood_cust
" Dark
set ruler
set cindent
set tabstop=2
set softtabstop=2
set shiftwidth=2
set sw=2
set noexpandtab
"set nowrap ignorecase showmatch
set ignorecase smartcase
set nowrap showmatch
"set ai
set guioptions+=a          " mark -> copy
set wildmenu
set bs=2
set vb
set incsearch
set hlsearch
set guifont=Andale\ Mono\ 11
"set guifont=gohufont-14
set nu
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
au! BufNewFile,BufRead *.as setlocal ft=javascript

""""""""""""""""""""""""""""
" show tabs
set list
set listchars=tab:→\ 

""""""""""""""""""""""
" Py-mode config
let g:pymode_folding = 0
let g:pymode_indent = 0
""""""""""""""""""""""""""""

