
" http://jeffkreeftmeijer.com/2012/relative-line-numbers-in-vim-for-super-fast-movement/
set number
set relativenumber
map <leader>1 :set norelativenumber<CR>:set number<CR>
map <leader>2 :set relativenumber<CR>:set number<CR>
map <leader>3 :set norelativenumber<CR>:set nonumber<CR>

au FocusLost   * :set norelativenumber
au FocusGained * :set relativenumber

au WinLeave    * :set norelativenumber
au WinEnter    * :set relativenumber

autocmd InsertEnter * :set norelativenumber
autocmd InsertLeave * :set relativenumber

