vim.filetype.add {
  extension = {
    yml = 'yaml.ansible'
  },
  filename = {
    ['.pre-commit-config.yaml'] ='yaml'
  }
}

vim.api.nvim_create_autocmd("VimEnter", {
  command = "silent! <cmd>poetry shell<cr>"
})
