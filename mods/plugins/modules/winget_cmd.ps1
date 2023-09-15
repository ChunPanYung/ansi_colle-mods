#!powershell

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ansible.windows.plugins.module_utils.Process

Set-StrictMode -Version "Latest"

$spec = @{
    options = @{
        id = @{ type = "str"; required = $true }
        state = @{ type = "str"; choices = "absent", "present" }
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
[string[]]$output = $null
if ((-not $state) -or ($state -eq 'present')) {
    $output = winget install --id $id --exact --silent
    # $module.Result.output = winget install --id $id --exact --silent
} else {
    $output = winget uninstall --id $id --exact --silent
}

# Filter string array -- must contains at least one letter.
$module.Result.output = $output | Select-String -Pattern '[A-Za-z]+'

$module.Result.rc = $LASTEXITCODE
if ($module.Result.rc -eq -1978335212) {
    $module.Result.stderr = $stdout
    $module.FailJson("Failed to found package.")
}



$module.ExitJson()
