#!powershell

#AnsibleRequires -CSharpUtil Ansible.Basic

# Set-StrictMode -Version "Latest"

$spec = @{
    options = @{
        id = @{ type = "str"; required = $true }
        state = @{ type = "str"; choices = "absent", "present" }
    }
    supports_check_mode = $false
}

[Ansible.Basic.AnsibleModule]$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$state = $module.Params.state

# [string]$output = ""
if ((-not $state) -or ($state -eq 'present')) {
    $module.Result.output = winget install --id $module.Params.id --exact
} else {
    $module.Result.output = winget uninstall --id $module.Params.id --exact
}

$module.ExitJson()
