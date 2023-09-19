#}!powershell

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ansible.windows.plugins.module_utils.Process

Set-StrictMode -Version "Latest"

$spec = @{
    options = @{
        id = @{ type = "str"; required = $true }
        state = @{ type = "str"; choices = "absent", "present" }
        debug = @{ type = "bool" }
    }
    supports_check_mode = $false
}

[Ansible.Basic.AnsibleModule]$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

# Setup default value
$module.Result.changed = $false
$module.Result.failed = $false
$state = $module.Params.state
$id = $module.Params.id

# Execute winget command to install packages
[object[]]$output = $null
if ((-not $state) -or ($state -eq 'present')) {
    $output = winget install --id $id --exact --silent
} else {
    $output = winget uninstall --id $id --exact --silent
}

$module.Result.rc = $LASTEXITCODE

# if ($module.Params.debug) {
#     $module.Result.output = $output
# }

switch -Regex ($output) {
    'Package already installed' {
        $module.Result.stdout = "Package already installed."
        break
    }
    'No package found' {
        $module.FailJson("Failed to found package.")
        break
    }
    'Successfully installed' {}
    'Successfully uninstalled' {
        $module.Result.changed = $true
        break
    }
    Default {
        $module.Result.output = $output
    }
}

$module.ExitJson()
