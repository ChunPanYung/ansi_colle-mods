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
[string]$stdout = $null
if ((-not $state) -or ($state -eq 'present')) {
    # $stdout = winget install --id $id --exact --silent
    $module.Result.stdout = winget install --id $id --exact --silent
} else {
    $stdout = winget uninstall --id $id --exact --silent
}

# Remove empty lines
# $stdout = $stdout | Out-String

$module.Result.rc = $LASTEXITCODE
if ($module.Result.rc -eq -1978335212) {
    $module.Result.stderr = $stdout
    $module.FailJson("Failed to found package.")
}

$module.ExitJson()
