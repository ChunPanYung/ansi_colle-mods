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
if ((-not $State) -or ($State -eq 'present')) {
    $output = winget install --id $module.Params.id --extract
} else {
    $output = winget uninstall --id $module.Params.id --extract
}

$module.Result.output = Invoke-Winget -Module $module -Id $id -State $state
$module.ExitJson()
