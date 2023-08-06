'''
# cdktf-multi-stack-tfe

Setting up Terraform Cloud / Terraform Enterprise workspaces can be tiring when dealing with CDK for Terraform applications spanning multiple stacks and therefore workspaces. This library aims to automate this.

## Usage

You need to create the initial workspace yourself, in this case `my-app-base`.

```python
import * as cdktf from "cdktf";
import Construct from "constructs";
import { BaseStack, Stack } from "cdktf-multi-stack-tfe";

// We need to have an already created "base" TFE workspace as a basis.
// It will store the TFE workspace configuration and state for all stacks.
// As it creates all TFE workspaces, it's required to be created first (and as a result will scaffold out all the required workspaces).
class MyAppBaseStack extends BaseStack {
  // The name is set to my-app-base
  constructor(scope: Construct) {
    // This will configure the remote backend to use my-company/my-app-base as a workspace
    // my-company is the Terraform organization
    // my-app is the prefix to use for all workspaces
    super(scope, "my-company", "my-app", {
      hostname: "app.terraform.io", // can be set to configure a different Terraform Cloud hostname, e.g. for privately hosted Terraform Enterprise
      token: "my-token", // can be set to configure a token to use
    });

    // You can do additional things in this stack as well
  }
}

class VpcStack extends Stack {
  public vpcId: string

  // This stack will depend on the base stack and it
  // will use the my-company/my-app-$stackName workspace as a backend
  constructor(scope: Construct, stackName: string) {
    super(scope, stackName);

    // Setup an VPC, etc.

    this.vpcId = ....
  }
}

class WebStack extends Stack {
  constructor(scope: Construct, stackName: string, vpcId: string) {
    super(scope, stackName);

    // Setup yourwebapp using the vpcId
  }
}

const app = new cdktf.App();
new MyAppBaseStack(app); // the stack name is "base"

// This cross-stack reference will lead to permissions being set up so that
// the staging-web workspace can access the staging-vpc workspace.
const vpc = new VpcStack(app, "staging-vpc"); // the stack name is "staging-vpc"
new Web(app, "staging-web", vpc.vpcId); // the stack name is "staging-web"

const prodVpc = new VpcStack(app, "production-vpc");
new Web(app, "production-web", prodVpc.vpcId);

app.synth();
```

## Warning

There are some potentially harmful side effects you could run into, so please always carefully read the diff before applying it.

### Renaming stacks

This is not supported by the library, if you rename an already existing stack the workspace hosting it will be destroyed and a new one with the new name will be created. This means all references to the infrastructure provisioned in the old stack will be lost, making it impossible to destroy the infrastructure through terraform. In this case we recommend destroying the stack, renaming it and then re-creating it.
There are some ways around this issue, but the library currently does not support them.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import cdktf
import cdktf_cdktf_provider_tfe
import constructs


class BaseStack(
    cdktf.TerraformStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-multi-stack-tfe.BaseStack",
):
    def __init__(
        self,
        scope: constructs.Construct,
        organization_name: builtins.str,
        prefix: builtins.str,
        *,
        hostname: typing.Optional[builtins.str] = None,
        ssl_skip_verify: typing.Optional[builtins.bool] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param organization_name: -
        :param prefix: -
        :param hostname: 
        :param ssl_skip_verify: 
        :param token: 
        '''
        options = BaseStackOptions(
            hostname=hostname, ssl_skip_verify=ssl_skip_verify, token=token
        )

        jsii.create(self.__class__, self, [scope, organization_name, prefix, options])

    @jsii.member(jsii_name="baseStackOf") # type: ignore[misc]
    @builtins.classmethod
    def base_stack_of(cls, construct: constructs.IConstruct) -> "BaseStack":
        '''
        :param construct: -
        '''
        return typing.cast("BaseStack", jsii.sinvoke(cls, "baseStackOf", [construct]))

    @jsii.member(jsii_name="isBaseStack") # type: ignore[misc]
    @builtins.classmethod
    def is_base_stack(cls, x: typing.Any) -> builtins.bool:
        '''
        :param x: -
        '''
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isBaseStack", [x]))

    @jsii.member(jsii_name="bootstrapWorkspace")
    def bootstrap_workspace(
        self,
        stack_name: builtins.str,
    ) -> cdktf_cdktf_provider_tfe.Workspace:
        '''
        :param stack_name: -
        '''
        return typing.cast(cdktf_cdktf_provider_tfe.Workspace, jsii.invoke(self, "bootstrapWorkspace", [stack_name]))

    @jsii.member(jsii_name="getRemoteBackendOptions")
    def get_remote_backend_options(
        self,
        stack_name: builtins.str,
    ) -> "RemoteBackendOptions":
        '''
        :param stack_name: -
        '''
        return typing.cast("RemoteBackendOptions", jsii.invoke(self, "getRemoteBackendOptions", [stack_name]))

    @jsii.member(jsii_name="getWorkspaceName")
    def get_workspace_name(self, stack_name: builtins.str) -> builtins.str:
        '''If you want to have more control over the workspace name, you can override this method.

        :param stack_name: -
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "getWorkspaceName", [stack_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> cdktf_cdktf_provider_tfe.DataTfeOrganization:
        return typing.cast(cdktf_cdktf_provider_tfe.DataTfeOrganization, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: cdktf_cdktf_provider_tfe.DataTfeOrganization) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tfeProvider")
    def tfe_provider(self) -> cdktf_cdktf_provider_tfe.TfeProvider:
        return typing.cast(cdktf_cdktf_provider_tfe.TfeProvider, jsii.get(self, "tfeProvider"))

    @tfe_provider.setter
    def tfe_provider(self, value: cdktf_cdktf_provider_tfe.TfeProvider) -> None:
        jsii.set(self, "tfeProvider", value)


@jsii.data_type(
    jsii_type="cdktf-multi-stack-tfe.BaseStackOptions",
    jsii_struct_bases=[],
    name_mapping={
        "hostname": "hostname",
        "ssl_skip_verify": "sslSkipVerify",
        "token": "token",
    },
)
class BaseStackOptions:
    def __init__(
        self,
        *,
        hostname: typing.Optional[builtins.str] = None,
        ssl_skip_verify: typing.Optional[builtins.bool] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: 
        :param ssl_skip_verify: 
        :param token: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if hostname is not None:
            self._values["hostname"] = hostname
        if ssl_skip_verify is not None:
            self._values["ssl_skip_verify"] = ssl_skip_verify
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_skip_verify(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("ssl_skip_verify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseStackOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-multi-stack-tfe.RemoteBackendOptions",
    jsii_struct_bases=[],
    name_mapping={
        "organization": "organization",
        "workspaces": "workspaces",
        "hostname": "hostname",
        "token": "token",
    },
)
class RemoteBackendOptions:
    def __init__(
        self,
        *,
        organization: builtins.str,
        workspaces: "RemoteBackendOptionsWorkspace",
        hostname: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param organization: 
        :param workspaces: 
        :param hostname: 
        :param token: 
        '''
        if isinstance(workspaces, dict):
            workspaces = RemoteBackendOptionsWorkspace(**workspaces)
        self._values: typing.Dict[str, typing.Any] = {
            "organization": organization,
            "workspaces": workspaces,
        }
        if hostname is not None:
            self._values["hostname"] = hostname
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def organization(self) -> builtins.str:
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspaces(self) -> "RemoteBackendOptionsWorkspace":
        result = self._values.get("workspaces")
        assert result is not None, "Required property 'workspaces' is missing"
        return typing.cast("RemoteBackendOptionsWorkspace", result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoteBackendOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-multi-stack-tfe.RemoteBackendOptionsWorkspace",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class RemoteBackendOptionsWorkspace:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoteBackendOptionsWorkspace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Stack(
    cdktf.TerraformStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-multi-stack-tfe.Stack",
):
    def __init__(self, scope: constructs.Construct, stack_name: builtins.str) -> None:
        '''
        :param scope: -
        :param stack_name: -
        '''
        jsii.create(self.__class__, self, [scope, stack_name])

    @jsii.member(jsii_name="isMultiStackStack") # type: ignore[misc]
    @builtins.classmethod
    def is_multi_stack_stack(cls, x: typing.Any) -> builtins.bool:
        '''
        :param x: -
        '''
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isMultiStackStack", [x]))

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, dependency: cdktf.TerraformStack) -> None:
        '''
        :param dependency: -
        '''
        return typing.cast(None, jsii.invoke(self, "addDependency", [dependency]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspace")
    def workspace(self) -> cdktf_cdktf_provider_tfe.Workspace:
        return typing.cast(cdktf_cdktf_provider_tfe.Workspace, jsii.get(self, "workspace"))

    @workspace.setter
    def workspace(self, value: cdktf_cdktf_provider_tfe.Workspace) -> None:
        jsii.set(self, "workspace", value)


__all__ = [
    "BaseStack",
    "BaseStackOptions",
    "RemoteBackendOptions",
    "RemoteBackendOptionsWorkspace",
    "Stack",
]

publication.publish()
