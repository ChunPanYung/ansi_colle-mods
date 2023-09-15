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
if ((-not $state) -or ($state -eq 'present')) {
    $output = winget install --id $id --exact --silent
} else {
    $output = winget uninstall --id $id --exact --silent
}

$module.Result.rc = $LASTEXITCODE

if ($module.Params.debug) {
    $module.Result.output = $output
}

if ($output -match "Package") {
    $module.Result.stdout = "Package already installed."
}

if ($module.Result.rc -eq -1978335212) {
    $module.Result.stderr = $stdout
    $module.FailJson("Failed to found package.")
} elseif ($module.Result.rc -eq -1978335189) {
    $module.Result.stdout = "Package already installed."
} elseif ($module.Result.rc -eq 0){
    $module.Result.stdout = ""
}

$module.ExitJson()
