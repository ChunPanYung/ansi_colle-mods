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

$state = $module.Params.state
$id = $module.Params.id

if ((-not $state) -or ($state -eq 'present')) {
    $module.Result.output = winget install --id $id --exact
} else {
    $module.Result.output = winget uninstall --id $id --exact
}

# Idempotency

$module.ExitJson()
