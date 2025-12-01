#!powershell

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ansible.windows.plugins.module_utils.Process

Set-StrictMode -Version Latest

$spec = @{
    options = @{
        id = @{ type = "str"; required = $true }
        scope = @{ type = "str"; default = "user" ; choices = "user", "machine" }
        state = @{ type = "str"; default = "present" ; choices = "absent", "present" }
    }
    supports_check_mode = $false
}

[Ansible.Basic.AnsibleModule]$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

# Setup default value
$module.Result.changed = $false
$module.Result.failed = $false
$id = $module.Params.id
$scope = $module.Params.scope

# Execute winget command to install packages
[object[]]$output = $null
if ($module.Params.state -eq 'present') {
    $output = winget install --id $id --scope $scope `
        --exact --silent --accept-source-agreements --accept-source-agreements
} else {
    $output = winget uninstall --id $id --scope $scope `
        --exact --silent --accept-source-agreements --accept-source-agreements
}
$module.Result.rc = $LASTEXITCODE

switch ($module.Result.rc) {
    0 { # Successfully installed/removed
        $module.Result.changed = $true
        break
    }
    -1978335189 { # Package is already installed
        break
    }
    -1978335212 {
        if ($module.Params.state -ne 'absent') {
            $module.FailJson("No package found matching input criteria.")
        }
        break
    }
    Default {
        $module.Result.output = $output
    }
}

$module.ExitJson()
