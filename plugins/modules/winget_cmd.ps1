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

switch ($module.Result.rc) {
    -1978335189 {
        $module.Result.stdout = "Package is already installed."
        break
    }
    -1978335212 {
        if ($state -eq 'absent') {
            $module.Result.stdout = "No installed package found matching input criteria."
        } else {
            $module.FailJson("No package found matching input criteria.")
        }
        break
    }
    0 { # Sucessfully installed/removed
        $module.Result.changed = $true
        break
    }
    Default {
        $module.Result.output = $output
    }
}

$module.ExitJson()
