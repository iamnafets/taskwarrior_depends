" Vim syntax file
" Language:	taskoutline data
" Maintainer:	Stefan Mai <stefan.mai@iamnafets.com>
" Updated: Mon Aug  1 16:20:45 PDT 2011
"
" For version 5.x: Clear all syntax items.
" For version 6.x: Quit when a syntax file was already loaded.
if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

syn match taskoutlineActiveTask '^\s*[0-9]\+\* .*$' contains=taskoutlineId
syn match taskoutlineOldTask '^\s*[0-9]\+: .*$' contains=taskoutlineId
syn match taskoutlineDoneTask '^\s*[0-9]\+[xX] .*$' contains=taskoutlineId
syn match taskoutlineNewActiveTask '^\s*[^0-9]*\*.*$'
syn match taskoutlineId '^\s*[0-9]\+[:*xX]' contained

" The default methods for highlighting.  Can be overridden later.
hi def link taskoutlineActiveTask	Special
hi def link taskoutlineDoneTask	Comment
hi def link taskoutlineId Type
hi def link taskoutlineOldTask Statement
hi def link taskoutlineNewTask Statement
hi def link taskoutlineNewActiveTask Constant

let b:current_syntax = "taskoutline"

" vim:noexpandtab
