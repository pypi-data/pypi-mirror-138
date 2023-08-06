'''
# aws-cdk-microservice

aws-cdk-microservice construct library is an open-source extension of the AWS Cloud Development Kit (AWS CDK) to deploy configurable microservice infra and its individual components in less than 50 lines of code and human readable configuration which can be managed by pull requests!

## A typical microservice architecture on AWS looks like:

![Architecture diagram](static/microservice.png)

Using cdk a microservice can be deployed using the following sample code snippet:

```python
import { Stack, StackProps } from '@aws-cdk/core';
import { Construct } from 'constructs';
import { MicroService } from '@smallcase/aws-cdk-microservice';
import { App } from '@aws-cdk/core';

export class UnknownAPIStackDev extends Stack {
 constructor(scope: Construct, id: string, props?: StackProps) {
   super(scope, id, props);
   new MicroService(stack, 'UnknownAPI', {
     appName: 'UnknownAPI',
     env: 'development',
     asgMaxSize: '1',
     asgMinSize: '1',
     diskSize: 20,
     instanceLabels: [
       {
         key: 'NODE-VERSION',
         propagateAtLaunch: true,
         value: '12',
       },
       {
         key: 'TYPE',
         propagateAtLaunch: true,
         value: 'application',
       },
     ],
     instanceType: 't3.micro',
     vpc: 'vpc-1234567',
     port: 8000,
     protocol: 'HTTP',
     healthCheckPath: '/health',
     subnets: ['subnet-987654321', 'subnet-12345678'],
     tcpRules: [
       {
         sourceSG: 'sg-12345678',
         description: 'ssh rule',
         port: 22,
       },
     ],
     host: 'abc-test-123.smallcase.com',
     lbArn: 'arn:aws:elasticloadbalancing:ap-south-1:12345678910:loadbalancer/app/API-DEV-External',
     sslEnabled: false,
     sshKey: 'master-dev',
     createCodedeployApplication: true,
     role: {
       type: 'new',
     },
   });
 }
}

new UnknownAPIStackDev(app, 'UnknownAPIStackDev', {
 env: { account: '12345678910', region: 'ap-south-1' },
});

app.synth()
```

Please refer [here](/API.md) to check how to use individual resource constructs.

Install using NPM:

```
npm install @smallcase/aws-cdk-microservice
```

Using yarn

```
yarn add @smallcase/aws-cdk-microservice
```

Configuration helper
| **Property**                 | **Type**                                  | **Default** | **Description**                                                                                                                                                                                                                                                 |
|------------------------------|-------------------------------------------|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| appName                      | string                                    |             | Name of the application to be deployed                                                                                                                                                                                                                          |
| applicationType?              | string                                    | new         | Type of application, new or existing, if existing, codedeploy will skip it's application creation and create a deployment group in existing application.                                                                                                        |
| asgMaxSize?                  | number                                    | 2           | Max ASG scale size                                                                                                                                                                                                                                              |
| asgMinSize?                  | number                                    | 1           | Min ASG scale size                                                                                                                                                                                                                                              |
| env?                         | string                                    | development | Application environment name                                                                                                                                                                                                                                    |
| instanceLabels?              | CfnAutoScalingGroup.TagPropertyProperty[] | []          | Tags to apply to the stack                                                                                                                                                                                                                                      |
| healthCheckPath?             | string                                    | /health     | Health check path for target group                                                                                                                                                                                                                              |
| port?                        | number                                    | undefined   | Port on which application is running. If not passed, target group will not be created                                                                                                                                                                           |
| protocol?                    | string (HTTP/HTTPS/GRPC)                  | HTTP        | Service protocol                                                                                                                                                                                                                                                |
| diskSize?                    | number                                    | 8GB         | Size of root volume for launch template                                                                                                                                                                                                                         |
| vpc                          | string                                    |             | VPC in which application infra is to be deployed                                                                                                                                                                                                                |
| role?                        | string                                    |             | Role ARN which is to be used with launch template                                                                                                                                                                                                               |
| tcpRules                     | IngressRule[]                             | []          | TCP Rules which are to be applied to the security group                                                                                                                                                                                                         |
| subnets                      | string[]                                  |             | Subnets in which subnets are to be deployed                                                                                                                                                                                                                     |
| sslEnabled?                  | boolean                                   | false       | Whether to use HTTPS ALB listener, or HTTP ALB listener                                                                                                                                                                                                         |
| host?                        | string                                    |             | DNS name, for example abc.xyz.com. Won't be created if TG is not created,                                                                                                                                                                                       |
| lbArn?                       | string                                    |             | Load balancer arn for application load balancing                                                                                                                                                                                                                |
| sshKey                       | string                                    |             | The ssh key pair name which is to be used                                                                                                                                                                                                                       |
| diskType?                    | string (GP2/GP3/IO1/IO2)                  | GP3         | Type of disk to be used                                                                                                                                                                                                                                         |
| createCodedeployApplication? | boolean                                   | false       | Whether to create a codedeploy application and a deployment group for current ENV passed, if applicationType is new, this will not create an application but will create a new deployment group in the same application name, will throw an error if not found. |
| deploymentPolicies?          | string[]                                  | []          | Deployment group policies which are to be passed, there are major policies already attached which will allow usage of S3 and triggering codedeploy agents on instances.                                                                                         |

Bootstrap the environment

```
cdk bootstrap
```

Check the changed which are to be deployed

```
~ -> cdk diff
Stack my-stack-dev
...
IAM Policy Changes
┌───┬──────────────────────────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────────────┐
│   │ Resource                                                                     │ Managed Policy ARN                                                 │
├───┼──────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ + │ ${UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-ASG-stackRole} │ arn:aws:iam::aws:policy/service-role/AmazonEC2SpotFleetTaggingRole │
│ + │ ${UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-ASG-stackRole} │ arn:aws:iam::aws:policy/ReadOnlyAccess                             │
│ + │ ${UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-ASG-stackRole} │ arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM           │
│ + │ ${UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-ASG-stackRole} │ arn:aws:iam::aws:policy/AmazonEC2FullAccess                        │
└───┴──────────────────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────┘
Security Group Changes
┌───┬─────────────────────────────────────────────────────────────────────────────────────┬─────┬────────────┬─────────────────┐
│   │ Group                                                                               │ Dir │ Protocol   │ Peer            │
├───┼─────────────────────────────────────────────────────────────────────────────────────┼─────┼────────────┼─────────────────┤
│ + │ ${UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-ASG-stack-sg.GroupId} │ In  │ TCP 22     │ sg-12346578     │
│ + │ ${UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-ASG-stack-sg.GroupId} │ Out │ Everything │ Everyone (IPv4) │
└───┴─────────────────────────────────────────────────────────────────────────────────────┴─────┴────────────┴─────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)

Resources
[+] AWS::EC2::SecurityGroup UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-ASG-stack-sg UnknownAPIdevelopmentUnknownAPIasdevelopmentUnknownAPIASGstacksg858F9DBC
[+] AWS::EC2::SecurityGroupIngress UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-ASG-stack-sg/from mystackdevUnknownAPIdevelopmentUnknownAPIassgf9c56492221D098D02:22 UnknownAPIdevelopmentUnknownAPIasdevelopmentUnknownAPIASGstacksgfrommystackdevUnknownAPIdevelopmentUnknownAPIassgf9c56492221D098D0222498F0E3E
[+] AWS::IAM::Role UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-ASG-stackRole UnknownAPIdevelopmentUnknownAPIasdevelopmentUnknownAPIASGstackRole3CEFE0B7
[+] AWS::IAM::Policy UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-ASG-stackRole/DefaultPolicy UnknownAPIdevelopmentUnknownAPIasdevelopmentUnknownAPIASGstackRoleDefaultPolicy8F61E954
[+] AWS::IAM::InstanceProfile UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-LT/Profile UnknownAPIdevelopmentUnknownAPIasdevelopmentUnknownAPILTProfileC84DF85A
[+] AWS::EC2::LaunchTemplate UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-LT UnknownAPIdevelopmentUnknownAPIasdevelopmentUnknownAPILT3B54AB26
[+] AWS::ElasticLoadBalancingV2::TargetGroup UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-TG UnknownAPIdevelopmentUnknownAPIasdevelopmentUnknownAPITG141FD907
[+] AWS::AutoScaling::AutoScalingGroup UnknownAPI/development-UnknownAPI-as/development-UnknownAPI-ASG UnknownAPIdevelopmentUnknownAPIasdevelopmentUnknownAPIASGEC1B4F9C
[+] AWS::IAM::Role UnknownAPI/UnknownAPI-deployment-group-role UnknownAPIUnknownAPIdeploymentgrouprole6E048442
[+] AWS::IAM::Policy UnknownAPI/UnknownAPI-deployment-group-role/DefaultPolicy UnknownAPIUnknownAPIdeploymentgrouproleDefaultPolicy176FEC37
[+] AWS::CodeDeploy::Application UnknownAPI/development-UnknownAPI-cd/UnknownAPI-development UnknownAPIdevelopmentUnknownAPIcdUnknownAPIdevelopment72A04EEC
[+] AWS::CodeDeploy::DeploymentGroup UnknownAPI/development-UnknownAPI-cd/development UnknownAPIdevelopmentUnknownAPIcddevelopmentC502CFAD
```

this is a trimmed output.

Deploy using

```
~ -> cdk deploy
```

PS: Because of an [aws-cdk issue](https://github.com/aws/aws-cdk/issues/6803), creating a Route 53 record from existing load balancer is not possible using cdk.
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

import aws_cdk
import aws_cdk.aws_autoscaling
import aws_cdk.aws_ec2
import aws_cdk.aws_elasticloadbalancingv2
import constructs


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.ApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "resource_type": "resourceType",
        "type": "type",
    },
)
class ApplicationProps:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        resource_type: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param application_name: 
        :param resource_type: 
        :param type: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application_name": application_name,
            "resource_type": resource_type,
            "type": type,
        }

    @builtins.property
    def application_name(self) -> builtins.str:
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutoScaler(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/aws-cdk-microservice.AutoScaler",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        app_name: builtins.str,
        asg_name: builtins.str,
        max_size: builtins.str,
        min_size: builtins.str,
        network_props: typing.Sequence["NetworkProps"],
        subnets: typing.Sequence[builtins.str],
        template_props: "InternalLaunchTemplateProps",
        tags: typing.Optional[typing.Sequence[aws_cdk.aws_autoscaling.CfnAutoScalingGroup.TagPropertyProperty]] = None,
        tg_props: typing.Optional["TargetGroupProps"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app_name: 
        :param asg_name: 
        :param max_size: 
        :param min_size: 
        :param network_props: 
        :param subnets: 
        :param template_props: 
        :param tags: 
        :param tg_props: 
        '''
        props = AutoScalerProps(
            app_name=app_name,
            asg_name=asg_name,
            max_size=max_size,
            min_size=min_size,
            network_props=network_props,
            subnets=subnets,
            template_props=template_props,
            tags=tags,
            tg_props=tg_props,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerProperties")
    def load_balancer_properties(
        self,
    ) -> typing.Optional[typing.List["LoadBalancerProps"]]:
        return typing.cast(typing.Optional[typing.List["LoadBalancerProps"]], jsii.get(self, "loadBalancerProperties"))


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.AutoScalerProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_name": "appName",
        "asg_name": "asgName",
        "max_size": "maxSize",
        "min_size": "minSize",
        "network_props": "networkProps",
        "subnets": "subnets",
        "template_props": "templateProps",
        "tags": "tags",
        "tg_props": "tgProps",
    },
)
class AutoScalerProps:
    def __init__(
        self,
        *,
        app_name: builtins.str,
        asg_name: builtins.str,
        max_size: builtins.str,
        min_size: builtins.str,
        network_props: typing.Sequence["NetworkProps"],
        subnets: typing.Sequence[builtins.str],
        template_props: "InternalLaunchTemplateProps",
        tags: typing.Optional[typing.Sequence[aws_cdk.aws_autoscaling.CfnAutoScalingGroup.TagPropertyProperty]] = None,
        tg_props: typing.Optional["TargetGroupProps"] = None,
    ) -> None:
        '''
        :param app_name: 
        :param asg_name: 
        :param max_size: 
        :param min_size: 
        :param network_props: 
        :param subnets: 
        :param template_props: 
        :param tags: 
        :param tg_props: 
        '''
        if isinstance(template_props, dict):
            template_props = InternalLaunchTemplateProps(**template_props)
        if isinstance(tg_props, dict):
            tg_props = TargetGroupProps(**tg_props)
        self._values: typing.Dict[str, typing.Any] = {
            "app_name": app_name,
            "asg_name": asg_name,
            "max_size": max_size,
            "min_size": min_size,
            "network_props": network_props,
            "subnets": subnets,
            "template_props": template_props,
        }
        if tags is not None:
            self._values["tags"] = tags
        if tg_props is not None:
            self._values["tg_props"] = tg_props

    @builtins.property
    def app_name(self) -> builtins.str:
        result = self._values.get("app_name")
        assert result is not None, "Required property 'app_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asg_name(self) -> builtins.str:
        result = self._values.get("asg_name")
        assert result is not None, "Required property 'asg_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_size(self) -> builtins.str:
        result = self._values.get("max_size")
        assert result is not None, "Required property 'max_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def min_size(self) -> builtins.str:
        result = self._values.get("min_size")
        assert result is not None, "Required property 'min_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_props(self) -> typing.List["NetworkProps"]:
        result = self._values.get("network_props")
        assert result is not None, "Required property 'network_props' is missing"
        return typing.cast(typing.List["NetworkProps"], result)

    @builtins.property
    def subnets(self) -> typing.List[builtins.str]:
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def template_props(self) -> "InternalLaunchTemplateProps":
        result = self._values.get("template_props")
        assert result is not None, "Required property 'template_props' is missing"
        return typing.cast("InternalLaunchTemplateProps", result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.CfnAutoScalingGroup.TagPropertyProperty]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_autoscaling.CfnAutoScalingGroup.TagPropertyProperty]], result)

    @builtins.property
    def tg_props(self) -> typing.Optional["TargetGroupProps"]:
        result = self._values.get("tg_props")
        return typing.cast(typing.Optional["TargetGroupProps"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoScalerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BalancerEntry(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/aws-cdk-microservice.BalancerEntry",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        app_name: builtins.str,
        host_header: builtins.str,
        lb_arn: builtins.str,
        ssl_enabled: builtins.bool,
        target_group_arn: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app_name: 
        :param host_header: 
        :param lb_arn: 
        :param ssl_enabled: 
        :param target_group_arn: 
        '''
        props = LoadBalancerProps(
            app_name=app_name,
            host_header=host_header,
            lb_arn=lb_arn,
            ssl_enabled=ssl_enabled,
            target_group_arn=target_group_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class Deployment(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/aws-cdk-microservice.Deployment",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_props: ApplicationProps,
        asg_names: typing.Sequence[builtins.str],
        deployment_config_name: builtins.str,
        deployment_group_name: builtins.str,
        role_arn: builtins.str,
        tg_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param application_props: 
        :param asg_names: 
        :param deployment_config_name: 
        :param deployment_group_name: 
        :param role_arn: 
        :param tg_name: 
        '''
        props = DeploymentProps(
            application_props=application_props,
            asg_names=asg_names,
            deployment_config_name=deployment_config_name,
            deployment_group_name=deployment_group_name,
            role_arn=role_arn,
            tg_name=tg_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.DeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_props": "applicationProps",
        "asg_names": "asgNames",
        "deployment_config_name": "deploymentConfigName",
        "deployment_group_name": "deploymentGroupName",
        "role_arn": "roleArn",
        "tg_name": "tgName",
    },
)
class DeploymentProps:
    def __init__(
        self,
        *,
        application_props: ApplicationProps,
        asg_names: typing.Sequence[builtins.str],
        deployment_config_name: builtins.str,
        deployment_group_name: builtins.str,
        role_arn: builtins.str,
        tg_name: builtins.str,
    ) -> None:
        '''
        :param application_props: 
        :param asg_names: 
        :param deployment_config_name: 
        :param deployment_group_name: 
        :param role_arn: 
        :param tg_name: 
        '''
        if isinstance(application_props, dict):
            application_props = ApplicationProps(**application_props)
        self._values: typing.Dict[str, typing.Any] = {
            "application_props": application_props,
            "asg_names": asg_names,
            "deployment_config_name": deployment_config_name,
            "deployment_group_name": deployment_group_name,
            "role_arn": role_arn,
            "tg_name": tg_name,
        }

    @builtins.property
    def application_props(self) -> ApplicationProps:
        result = self._values.get("application_props")
        assert result is not None, "Required property 'application_props' is missing"
        return typing.cast(ApplicationProps, result)

    @builtins.property
    def asg_names(self) -> typing.List[builtins.str]:
        result = self._values.get("asg_names")
        assert result is not None, "Required property 'asg_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def deployment_config_name(self) -> builtins.str:
        result = self._values.get("deployment_config_name")
        assert result is not None, "Required property 'deployment_config_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_group_name(self) -> builtins.str:
        result = self._values.get("deployment_group_name")
        assert result is not None, "Required property 'deployment_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tg_name(self) -> builtins.str:
        result = self._values.get("tg_name")
        assert result is not None, "Required property 'tg_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.IngressRule",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "source_sg": "sourceSG",
        "description": "description",
    },
)
class IngressRule:
    def __init__(
        self,
        *,
        port: jsii.Number,
        source_sg: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: 
        :param source_sg: 
        :param description: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "port": port,
            "source_sg": source_sg,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def port(self) -> jsii.Number:
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def source_sg(self) -> builtins.str:
        result = self._values.get("source_sg")
        assert result is not None, "Required property 'source_sg' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IngressRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.InstanceStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "asg_name": "asgName",
        "instance_props": "instanceProps",
        "instance_volume_size": "instanceVolumeSize",
        "role": "role",
        "security_group": "securityGroup",
        "tags": "tags",
        "target_group_props": "targetGroupProps",
        "vpc": "vpc",
    },
)
class InstanceStackProps:
    def __init__(
        self,
        *,
        asg_name: builtins.str,
        instance_props: aws_cdk.aws_ec2.InstanceProps,
        instance_volume_size: typing.Optional[aws_cdk.aws_autoscaling.BlockDevice] = None,
        role: typing.Optional["InternalRole"] = None,
        security_group: typing.Optional["InternalSG"] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_group_props: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroupProps] = None,
        vpc: typing.Optional["InternalVPC"] = None,
    ) -> None:
        '''
        :param asg_name: 
        :param instance_props: 
        :param instance_volume_size: 
        :param role: 
        :param security_group: 
        :param tags: 
        :param target_group_props: 
        :param vpc: 
        '''
        if isinstance(instance_props, dict):
            instance_props = aws_cdk.aws_ec2.InstanceProps(**instance_props)
        if isinstance(instance_volume_size, dict):
            instance_volume_size = aws_cdk.aws_autoscaling.BlockDevice(**instance_volume_size)
        if isinstance(role, dict):
            role = InternalRole(**role)
        if isinstance(security_group, dict):
            security_group = InternalSG(**security_group)
        if isinstance(target_group_props, dict):
            target_group_props = aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroupProps(**target_group_props)
        if isinstance(vpc, dict):
            vpc = InternalVPC(**vpc)
        self._values: typing.Dict[str, typing.Any] = {
            "asg_name": asg_name,
            "instance_props": instance_props,
        }
        if instance_volume_size is not None:
            self._values["instance_volume_size"] = instance_volume_size
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if tags is not None:
            self._values["tags"] = tags
        if target_group_props is not None:
            self._values["target_group_props"] = target_group_props
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def asg_name(self) -> builtins.str:
        result = self._values.get("asg_name")
        assert result is not None, "Required property 'asg_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_props(self) -> aws_cdk.aws_ec2.InstanceProps:
        result = self._values.get("instance_props")
        assert result is not None, "Required property 'instance_props' is missing"
        return typing.cast(aws_cdk.aws_ec2.InstanceProps, result)

    @builtins.property
    def instance_volume_size(
        self,
    ) -> typing.Optional[aws_cdk.aws_autoscaling.BlockDevice]:
        result = self._values.get("instance_volume_size")
        return typing.cast(typing.Optional[aws_cdk.aws_autoscaling.BlockDevice], result)

    @builtins.property
    def role(self) -> typing.Optional["InternalRole"]:
        result = self._values.get("role")
        return typing.cast(typing.Optional["InternalRole"], result)

    @builtins.property
    def security_group(self) -> typing.Optional["InternalSG"]:
        result = self._values.get("security_group")
        return typing.cast(typing.Optional["InternalSG"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target_group_props(
        self,
    ) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroupProps]:
        result = self._values.get("target_group_props")
        return typing.cast(typing.Optional[aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroupProps], result)

    @builtins.property
    def vpc(self) -> typing.Optional["InternalVPC"]:
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["InternalVPC"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.InternalBD",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "size": "size", "type": "type"},
)
class InternalBD:
    def __init__(
        self,
        *,
        name: builtins.str,
        size: jsii.Number,
        type: aws_cdk.aws_autoscaling.EbsDeviceVolumeType,
    ) -> None:
        '''
        :param name: 
        :param size: 
        :param type: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "size": size,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size(self) -> jsii.Number:
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> aws_cdk.aws_autoscaling.EbsDeviceVolumeType:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(aws_cdk.aws_autoscaling.EbsDeviceVolumeType, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalBD(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.InternalLaunchTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "ami_image_id": "amiImageId",
        "block_device": "blockDevice",
        "detailed_monitoring": "detailedMonitoring",
        "instance_type": "instanceType",
        "role": "role",
        "security_group": "securityGroup",
        "ssh_key": "sshKey",
        "template_name": "templateName",
        "type": "type",
        "vpc": "vpc",
        "existing_attributes": "existingAttributes",
        "instance_volume_size": "instanceVolumeSize",
    },
)
class InternalLaunchTemplateProps:
    def __init__(
        self,
        *,
        ami_image_id: builtins.str,
        block_device: InternalBD,
        detailed_monitoring: builtins.bool,
        instance_type: builtins.str,
        role: "InternalRole",
        security_group: "InternalSG",
        ssh_key: builtins.str,
        template_name: builtins.str,
        type: builtins.str,
        vpc: "InternalVPC",
        existing_attributes: typing.Optional[aws_cdk.aws_ec2.LaunchTemplateAttributes] = None,
        instance_volume_size: typing.Optional[aws_cdk.aws_autoscaling.BlockDevice] = None,
    ) -> None:
        '''
        :param ami_image_id: 
        :param block_device: 
        :param detailed_monitoring: 
        :param instance_type: 
        :param role: 
        :param security_group: 
        :param ssh_key: 
        :param template_name: 
        :param type: 
        :param vpc: 
        :param existing_attributes: 
        :param instance_volume_size: 
        '''
        if isinstance(block_device, dict):
            block_device = InternalBD(**block_device)
        if isinstance(role, dict):
            role = InternalRole(**role)
        if isinstance(security_group, dict):
            security_group = InternalSG(**security_group)
        if isinstance(vpc, dict):
            vpc = InternalVPC(**vpc)
        if isinstance(existing_attributes, dict):
            existing_attributes = aws_cdk.aws_ec2.LaunchTemplateAttributes(**existing_attributes)
        if isinstance(instance_volume_size, dict):
            instance_volume_size = aws_cdk.aws_autoscaling.BlockDevice(**instance_volume_size)
        self._values: typing.Dict[str, typing.Any] = {
            "ami_image_id": ami_image_id,
            "block_device": block_device,
            "detailed_monitoring": detailed_monitoring,
            "instance_type": instance_type,
            "role": role,
            "security_group": security_group,
            "ssh_key": ssh_key,
            "template_name": template_name,
            "type": type,
            "vpc": vpc,
        }
        if existing_attributes is not None:
            self._values["existing_attributes"] = existing_attributes
        if instance_volume_size is not None:
            self._values["instance_volume_size"] = instance_volume_size

    @builtins.property
    def ami_image_id(self) -> builtins.str:
        result = self._values.get("ami_image_id")
        assert result is not None, "Required property 'ami_image_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def block_device(self) -> InternalBD:
        result = self._values.get("block_device")
        assert result is not None, "Required property 'block_device' is missing"
        return typing.cast(InternalBD, result)

    @builtins.property
    def detailed_monitoring(self) -> builtins.bool:
        result = self._values.get("detailed_monitoring")
        assert result is not None, "Required property 'detailed_monitoring' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def instance_type(self) -> builtins.str:
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> "InternalRole":
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast("InternalRole", result)

    @builtins.property
    def security_group(self) -> "InternalSG":
        result = self._values.get("security_group")
        assert result is not None, "Required property 'security_group' is missing"
        return typing.cast("InternalSG", result)

    @builtins.property
    def ssh_key(self) -> builtins.str:
        result = self._values.get("ssh_key")
        assert result is not None, "Required property 'ssh_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_name(self) -> builtins.str:
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> "InternalVPC":
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast("InternalVPC", result)

    @builtins.property
    def existing_attributes(
        self,
    ) -> typing.Optional[aws_cdk.aws_ec2.LaunchTemplateAttributes]:
        result = self._values.get("existing_attributes")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.LaunchTemplateAttributes], result)

    @builtins.property
    def instance_volume_size(
        self,
    ) -> typing.Optional[aws_cdk.aws_autoscaling.BlockDevice]:
        result = self._values.get("instance_volume_size")
        return typing.cast(typing.Optional[aws_cdk.aws_autoscaling.BlockDevice], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalLaunchTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.InternalRole",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "additional_policies": "additionalPolicies",
        "role_arn": "roleArn",
        "role_name": "roleName",
    },
)
class InternalRole:
    def __init__(
        self,
        *,
        type: builtins.str,
        additional_policies: typing.Optional[typing.Sequence[typing.Any]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: 
        :param additional_policies: 
        :param role_arn: 
        :param role_name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
        }
        if additional_policies is not None:
            self._values["additional_policies"] = additional_policies
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_policies(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("additional_policies")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.InternalSG",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "allow_all_outbound": "allowAllOutbound",
        "description": "description",
        "disable_inline_rules": "disableInlineRules",
        "ingress_rules": "ingressRules",
        "security_group_name": "securityGroupName",
        "sg_group_id": "sgGroupId",
    },
)
class InternalSG:
    def __init__(
        self,
        *,
        type: builtins.str,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        disable_inline_rules: typing.Optional[builtins.bool] = None,
        ingress_rules: typing.Optional[typing.Sequence[IngressRule]] = None,
        security_group_name: typing.Optional[builtins.str] = None,
        sg_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: 
        :param allow_all_outbound: 
        :param description: 
        :param disable_inline_rules: 
        :param ingress_rules: 
        :param security_group_name: 
        :param sg_group_id: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
        }
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if description is not None:
            self._values["description"] = description
        if disable_inline_rules is not None:
            self._values["disable_inline_rules"] = disable_inline_rules
        if ingress_rules is not None:
            self._values["ingress_rules"] = ingress_rules
        if security_group_name is not None:
            self._values["security_group_name"] = security_group_name
        if sg_group_id is not None:
            self._values["sg_group_id"] = sg_group_id

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("allow_all_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_inline_rules(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("disable_inline_rules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ingress_rules(self) -> typing.Optional[typing.List[IngressRule]]:
        result = self._values.get("ingress_rules")
        return typing.cast(typing.Optional[typing.List[IngressRule]], result)

    @builtins.property
    def security_group_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("security_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sg_group_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("sg_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalSG(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.InternalVPC",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "vpc_name": "vpcName", "vpc_props": "vpcProps"},
)
class InternalVPC:
    def __init__(
        self,
        *,
        type: builtins.str,
        vpc_name: builtins.str,
        vpc_props: typing.Optional[aws_cdk.aws_ec2.VpcProps] = None,
    ) -> None:
        '''
        :param type: 
        :param vpc_name: 
        :param vpc_props: 
        '''
        if isinstance(vpc_props, dict):
            vpc_props = aws_cdk.aws_ec2.VpcProps(**vpc_props)
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
            "vpc_name": vpc_name,
        }
        if vpc_props is not None:
            self._values["vpc_props"] = vpc_props

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_name(self) -> builtins.str:
        result = self._values.get("vpc_name")
        assert result is not None, "Required property 'vpc_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_props(self) -> typing.Optional[aws_cdk.aws_ec2.VpcProps]:
        result = self._values.get("vpc_props")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.VpcProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalVPC(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.LoadBalancerProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_name": "appName",
        "host_header": "hostHeader",
        "lb_arn": "lbArn",
        "ssl_enabled": "sslEnabled",
        "target_group_arn": "targetGroupArn",
    },
)
class LoadBalancerProps:
    def __init__(
        self,
        *,
        app_name: builtins.str,
        host_header: builtins.str,
        lb_arn: builtins.str,
        ssl_enabled: builtins.bool,
        target_group_arn: builtins.str,
    ) -> None:
        '''
        :param app_name: 
        :param host_header: 
        :param lb_arn: 
        :param ssl_enabled: 
        :param target_group_arn: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "app_name": app_name,
            "host_header": host_header,
            "lb_arn": lb_arn,
            "ssl_enabled": ssl_enabled,
            "target_group_arn": target_group_arn,
        }

    @builtins.property
    def app_name(self) -> builtins.str:
        result = self._values.get("app_name")
        assert result is not None, "Required property 'app_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_header(self) -> builtins.str:
        result = self._values.get("host_header")
        assert result is not None, "Required property 'host_header' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lb_arn(self) -> builtins.str:
        result = self._values.get("lb_arn")
        assert result is not None, "Required property 'lb_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssl_enabled(self) -> builtins.bool:
        result = self._values.get("ssl_enabled")
        assert result is not None, "Required property 'ssl_enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def target_group_arn(self) -> builtins.str:
        result = self._values.get("target_group_arn")
        assert result is not None, "Required property 'target_group_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MicroService(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/aws-cdk-microservice.MicroService",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        app_name: builtins.str,
        env: builtins.str,
        role: InternalRole,
        ssh_key: builtins.str,
        subnets: typing.Sequence[builtins.str],
        vpc: builtins.str,
        ami: typing.Optional[builtins.str] = None,
        application_type: typing.Optional[builtins.str] = None,
        asg_max_size: typing.Optional[builtins.str] = None,
        asg_min_size: typing.Optional[builtins.str] = None,
        create_codedeploy_application: typing.Optional[builtins.bool] = None,
        deployment_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        instance_labels: typing.Optional[typing.Sequence[aws_cdk.aws_autoscaling.CfnAutoScalingGroup.TagPropertyProperty]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        network_props: typing.Optional[typing.Sequence["NetworkProps"]] = None,
        security_group_props: typing.Optional[InternalSG] = None,
        tcp_rules: typing.Optional[typing.Sequence[IngressRule]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app_name: 
        :param env: 
        :param role: 
        :param ssh_key: 
        :param subnets: 
        :param vpc: 
        :param ami: 
        :param application_type: 
        :param asg_max_size: 
        :param asg_min_size: 
        :param create_codedeploy_application: 
        :param deployment_policies: 
        :param disk_size: 
        :param disk_type: 
        :param instance_labels: 
        :param instance_type: 
        :param network_props: 
        :param security_group_props: 
        :param tcp_rules: 
        '''
        props = MicroServiceProps(
            app_name=app_name,
            env=env,
            role=role,
            ssh_key=ssh_key,
            subnets=subnets,
            vpc=vpc,
            ami=ami,
            application_type=application_type,
            asg_max_size=asg_max_size,
            asg_min_size=asg_min_size,
            create_codedeploy_application=create_codedeploy_application,
            deployment_policies=deployment_policies,
            disk_size=disk_size,
            disk_type=disk_type,
            instance_labels=instance_labels,
            instance_type=instance_type,
            network_props=network_props,
            security_group_props=security_group_props,
            tcp_rules=tcp_rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="appName")
    def app_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> InternalRole:
        return typing.cast(InternalRole, jsii.get(self, "role"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sshKey")
    def ssh_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshKey"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetGroupProps")
    def target_group_props(self) -> typing.List["TargetGroupProps"]:
        return typing.cast(typing.List["TargetGroupProps"], jsii.get(self, "targetGroupProps"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpc"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationType")
    def application_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="asgMaxSize")
    def asg_max_size(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "asgMaxSize"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="asgMinSize")
    def asg_min_size(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "asgMinSize"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="createCodedeployApplication")
    def create_codedeploy_application(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "createCodedeployApplication"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentPolicies")
    def deployment_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deploymentPolicies"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="diskSize")
    def disk_size(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSize"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "env"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceLabels")
    def instance_labels(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.CfnAutoScalingGroup.TagPropertyProperty]]:
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_autoscaling.CfnAutoScalingGroup.TagPropertyProperty]], jsii.get(self, "instanceLabels"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="networkProps")
    def network_props(self) -> typing.Optional[typing.List["NetworkProps"]]:
        return typing.cast(typing.Optional[typing.List["NetworkProps"]], jsii.get(self, "networkProps"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroupProps")
    def security_group_props(self) -> typing.Optional[InternalSG]:
        return typing.cast(typing.Optional[InternalSG], jsii.get(self, "securityGroupProps"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tcpRules")
    def tcp_rules(self) -> typing.Optional[typing.List[IngressRule]]:
        return typing.cast(typing.Optional[typing.List[IngressRule]], jsii.get(self, "tcpRules"))


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.MicroServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_name": "appName",
        "env": "env",
        "role": "role",
        "ssh_key": "sshKey",
        "subnets": "subnets",
        "vpc": "vpc",
        "ami": "ami",
        "application_type": "applicationType",
        "asg_max_size": "asgMaxSize",
        "asg_min_size": "asgMinSize",
        "create_codedeploy_application": "createCodedeployApplication",
        "deployment_policies": "deploymentPolicies",
        "disk_size": "diskSize",
        "disk_type": "diskType",
        "instance_labels": "instanceLabels",
        "instance_type": "instanceType",
        "network_props": "networkProps",
        "security_group_props": "securityGroupProps",
        "tcp_rules": "tcpRules",
    },
)
class MicroServiceProps:
    def __init__(
        self,
        *,
        app_name: builtins.str,
        env: builtins.str,
        role: InternalRole,
        ssh_key: builtins.str,
        subnets: typing.Sequence[builtins.str],
        vpc: builtins.str,
        ami: typing.Optional[builtins.str] = None,
        application_type: typing.Optional[builtins.str] = None,
        asg_max_size: typing.Optional[builtins.str] = None,
        asg_min_size: typing.Optional[builtins.str] = None,
        create_codedeploy_application: typing.Optional[builtins.bool] = None,
        deployment_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        instance_labels: typing.Optional[typing.Sequence[aws_cdk.aws_autoscaling.CfnAutoScalingGroup.TagPropertyProperty]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        network_props: typing.Optional[typing.Sequence["NetworkProps"]] = None,
        security_group_props: typing.Optional[InternalSG] = None,
        tcp_rules: typing.Optional[typing.Sequence[IngressRule]] = None,
    ) -> None:
        '''
        :param app_name: 
        :param env: 
        :param role: 
        :param ssh_key: 
        :param subnets: 
        :param vpc: 
        :param ami: 
        :param application_type: 
        :param asg_max_size: 
        :param asg_min_size: 
        :param create_codedeploy_application: 
        :param deployment_policies: 
        :param disk_size: 
        :param disk_type: 
        :param instance_labels: 
        :param instance_type: 
        :param network_props: 
        :param security_group_props: 
        :param tcp_rules: 
        '''
        if isinstance(role, dict):
            role = InternalRole(**role)
        if isinstance(security_group_props, dict):
            security_group_props = InternalSG(**security_group_props)
        self._values: typing.Dict[str, typing.Any] = {
            "app_name": app_name,
            "env": env,
            "role": role,
            "ssh_key": ssh_key,
            "subnets": subnets,
            "vpc": vpc,
        }
        if ami is not None:
            self._values["ami"] = ami
        if application_type is not None:
            self._values["application_type"] = application_type
        if asg_max_size is not None:
            self._values["asg_max_size"] = asg_max_size
        if asg_min_size is not None:
            self._values["asg_min_size"] = asg_min_size
        if create_codedeploy_application is not None:
            self._values["create_codedeploy_application"] = create_codedeploy_application
        if deployment_policies is not None:
            self._values["deployment_policies"] = deployment_policies
        if disk_size is not None:
            self._values["disk_size"] = disk_size
        if disk_type is not None:
            self._values["disk_type"] = disk_type
        if instance_labels is not None:
            self._values["instance_labels"] = instance_labels
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if network_props is not None:
            self._values["network_props"] = network_props
        if security_group_props is not None:
            self._values["security_group_props"] = security_group_props
        if tcp_rules is not None:
            self._values["tcp_rules"] = tcp_rules

    @builtins.property
    def app_name(self) -> builtins.str:
        result = self._values.get("app_name")
        assert result is not None, "Required property 'app_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def env(self) -> builtins.str:
        result = self._values.get("env")
        assert result is not None, "Required property 'env' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> InternalRole:
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(InternalRole, result)

    @builtins.property
    def ssh_key(self) -> builtins.str:
        result = self._values.get("ssh_key")
        assert result is not None, "Required property 'ssh_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnets(self) -> typing.List[builtins.str]:
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc(self) -> builtins.str:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ami(self) -> typing.Optional[builtins.str]:
        result = self._values.get("ami")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("application_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asg_max_size(self) -> typing.Optional[builtins.str]:
        result = self._values.get("asg_max_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asg_min_size(self) -> typing.Optional[builtins.str]:
        result = self._values.get("asg_min_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_codedeploy_application(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("create_codedeploy_application")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deployment_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("deployment_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_labels(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.CfnAutoScalingGroup.TagPropertyProperty]]:
        result = self._values.get("instance_labels")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_autoscaling.CfnAutoScalingGroup.TagPropertyProperty]], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_props(self) -> typing.Optional[typing.List["NetworkProps"]]:
        result = self._values.get("network_props")
        return typing.cast(typing.Optional[typing.List["NetworkProps"]], result)

    @builtins.property
    def security_group_props(self) -> typing.Optional[InternalSG]:
        result = self._values.get("security_group_props")
        return typing.cast(typing.Optional[InternalSG], result)

    @builtins.property
    def tcp_rules(self) -> typing.Optional[typing.List[IngressRule]]:
        result = self._values.get("tcp_rules")
        return typing.cast(typing.Optional[typing.List[IngressRule]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MicroServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.NetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "health_check_path": "healthCheckPath",
        "host": "host",
        "lb_arn": "lbArn",
        "port": "port",
        "protocol": "protocol",
        "ssl_enabled": "sslEnabled",
    },
)
class NetworkProps:
    def __init__(
        self,
        *,
        health_check_path: builtins.str,
        host: builtins.str,
        lb_arn: builtins.str,
        port: jsii.Number,
        protocol: builtins.str,
        ssl_enabled: builtins.bool,
    ) -> None:
        '''
        :param health_check_path: 
        :param host: 
        :param lb_arn: 
        :param port: 
        :param protocol: 
        :param ssl_enabled: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "health_check_path": health_check_path,
            "host": host,
            "lb_arn": lb_arn,
            "port": port,
            "protocol": protocol,
            "ssl_enabled": ssl_enabled,
        }

    @builtins.property
    def health_check_path(self) -> builtins.str:
        result = self._values.get("health_check_path")
        assert result is not None, "Required property 'health_check_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lb_arn(self) -> builtins.str:
        result = self._values.get("lb_arn")
        assert result is not None, "Required property 'lb_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssl_enabled(self) -> builtins.bool:
        result = self._values.get("ssl_enabled")
        assert result is not None, "Required property 'ssl_enabled' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/aws-cdk-microservice.TargetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "health_path": "healthPath",
        "name": "name",
        "port": "port",
        "protocol": "protocol",
        "tg_arn": "tgArn",
        "threshold_count": "thresholdCount",
        "timeout": "timeout",
    },
)
class TargetGroupProps:
    def __init__(
        self,
        *,
        type: builtins.str,
        health_path: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        tg_arn: typing.Optional[builtins.str] = None,
        threshold_count: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: 
        :param health_path: 
        :param name: 
        :param port: 
        :param protocol: 
        :param tg_arn: 
        :param threshold_count: 
        :param timeout: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
        }
        if health_path is not None:
            self._values["health_path"] = health_path
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if tg_arn is not None:
            self._values["tg_arn"] = tg_arn
        if threshold_count is not None:
            self._values["threshold_count"] = threshold_count
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def health_path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("health_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tg_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("tg_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold_count(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ApplicationProps",
    "AutoScaler",
    "AutoScalerProps",
    "BalancerEntry",
    "Deployment",
    "DeploymentProps",
    "IngressRule",
    "InstanceStackProps",
    "InternalBD",
    "InternalLaunchTemplateProps",
    "InternalRole",
    "InternalSG",
    "InternalVPC",
    "LoadBalancerProps",
    "MicroService",
    "MicroServiceProps",
    "NetworkProps",
    "TargetGroupProps",
]

publication.publish()
