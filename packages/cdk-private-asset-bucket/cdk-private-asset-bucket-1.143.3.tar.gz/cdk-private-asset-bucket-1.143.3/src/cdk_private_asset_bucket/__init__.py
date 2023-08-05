'''
[![NPM version](https://badge.fury.io/js/cdk-private-asset-bucket.svg)](https://badge.fury.io/js/cdk-private-asset-bucket)
[![PyPI version](https://badge.fury.io/py/cdk-private-asset-bucket.svg)](https://badge.fury.io/py/cdk-private-asset-bucket)
[![.NET version](https://img.shields.io/nuget/v/com.github.mmuller88.cdkPrivateAssetBucket.svg?style=flat-square)](https://www.nuget.org/packages/com.github.mmuller88.cdkPrivateAssetBucket/)
![Release](https://github.com/mmuller88/cdk-private-asset-bucket/workflows/Release/badge.svg)

# cdk-private-asset-bucket

A construct to create a private asset S3 bucket. Cognito will be used for token validation with Lambda@Edge.

## Architecture

![Diagram](misc/cdkPrivateAssetBucket.drawio.png)

# Example

```python
import { ProwlerAudit } from 'cdk-prowler';
...
    const app = new core.App();

    const stack = new core.Stack(app, 'PrivateAssetBucket-stack2', {
      env: {
        account: '981237193288',
        region: 'us-east-1',
      },
    });

    const userPool = new cognito.UserPool(stack, 'userPool', {
      removalPolicy: core.RemovalPolicy.DESTROY,
    });

    const userPoolWebClient = new cognito.UserPoolClient(stack, 'userPoolWebClient', {
      userPool: userPool,
      generateSecret: false,
      preventUserExistenceErrors: true,
      authFlows: {
        adminUserPassword: true,
        userPassword: true,
      },
      oAuth: {
        flows: {
          authorizationCodeGrant: false,
          implicitCodeGrant: true,
        },
      },
    });

    const privateAssetBucket = new PrivateAssetBucket(stack, 'privateAssetBucket', {
      userPoolId: userPool.userPoolId,
      userPoolClientId: userPoolWebClient.userPoolClientId,
    });

    new core.CfnOutput(stack, 'AssetBucketName', {
      value: privateAssetBucket.assetBucketName,
    });

    new core.CfnOutput(stack, 'AssetBucketCloudfrontUrl', {
      value: privateAssetBucket.assetBucketCloudfrontUrl,
    });
```

## Properties

[API.md](API.md)

## Test PrivateBucketAsset

If you forged / cloned that repo you can test directly from here. Don't forget to init with:

```bash
yarn install
```

Create a test cdk stack with one of the following:

```bash
yarn cdk deploy
yarn cdk deploy --watch
yarn cdk deploy --require-approval never
```

* Upload a picture named like pic.png to the private asset bucket
* Create a user pool user and get / save the token:

```bash
USER_POOL_ID=us-east-1_0Aw1oPvD6
CLIENT_ID=3eqcgvghjbv4d5rv32hopmadu8
USER_NAME=martindev
USER_PASSWORD=M@rtindev1
REGION=us-east-1
CFD=d1f2bfdek3mzi7.cloudfront.net

aws cognito-idp admin-create-user --user-pool-id $USER_POOL_ID --username $USER_NAME --region $REGION
aws cognito-idp admin-set-user-password --user-pool-id $USER_POOL_ID --username $USER_NAME --password $USER_PASSWORD  --permanent --region $REGION
ACCESS_TOKEN=$(aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH --client-id $CLIENT_ID --auth-parameters USERNAME=$USER_NAME,PASSWORD=$USER_PASSWORD  --region $REGION | jq -r '.AuthenticationResult.AccessToken')

echo "curl --location --request GET "https://$CFD/pic.png" --cookie "Cookie: token=$ACCESS_TOKEN""
```

* You can use the curl for importing in Postman. but it looks like Postman can't import the cookie. So you need to set the cookie manually in Postman!
* In Postman you should see your picture :)

## Planned Features

* Support S3 bucket import ootb.
* Support custom authorizer

## Thanks To

* Crespo Wang for his pioneer work regarding private S3 assets https://javascript.plainenglish.io/use-lambda-edge-jwt-to-secure-s3-bucket-dcca6eec4d7e
* As always to the amazing CDK / Projen Community. Join us on [Slack](https://cdk-dev.slack.com)!
* [Projen](https://github.com/projen/projen) project and the community around it
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

import aws_cdk.aws_route53
import aws_cdk.core


@jsii.data_type(
    jsii_type="cdk-private-asset-bucket.CustomDomain",
    jsii_struct_bases=[],
    name_mapping={"domain_name": "domainName", "zone": "zone"},
)
class CustomDomain:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        zone: aws_cdk.aws_route53.IHostedZone,
    ) -> None:
        '''
        :param domain_name: domainName needs to be part of the hosted zone e.g.: image.example.com.
        :param zone: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
            "zone": zone,
        }

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''domainName needs to be part of the hosted zone e.g.: image.example.com.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone(self) -> aws_cdk.aws_route53.IHostedZone:
        result = self._values.get("zone")
        assert result is not None, "Required property 'zone' is missing"
        return typing.cast(aws_cdk.aws_route53.IHostedZone, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomDomain(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivateAssetBucket(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-private-asset-bucket.PrivateAssetBucket",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        user_pool_client_id: builtins.str,
        user_pool_id: builtins.str,
        asset_bucket_name: typing.Optional[builtins.str] = None,
        asset_bucket_name_import: typing.Optional[builtins.str] = None,
        custom_domain: typing.Optional[CustomDomain] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param user_pool_client_id: 
        :param user_pool_id: 
        :param asset_bucket_name: 
        :param asset_bucket_name_import: if you want to use an imported bucket instead.
        :param custom_domain: 
        '''
        props = PrivateAssetBucketProps(
            user_pool_client_id=user_pool_client_id,
            user_pool_id=user_pool_id,
            asset_bucket_name=asset_bucket_name,
            asset_bucket_name_import=asset_bucket_name_import,
            custom_domain=custom_domain,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assetBucketCloudfrontUrl")
    def asset_bucket_cloudfront_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetBucketCloudfrontUrl"))

    @asset_bucket_cloudfront_url.setter
    def asset_bucket_cloudfront_url(self, value: builtins.str) -> None:
        jsii.set(self, "assetBucketCloudfrontUrl", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assetBucketName")
    def asset_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetBucketName"))

    @asset_bucket_name.setter
    def asset_bucket_name(self, value: builtins.str) -> None:
        jsii.set(self, "assetBucketName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assetBucketRecordDomainName")
    def asset_bucket_record_domain_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetBucketRecordDomainName"))

    @asset_bucket_record_domain_name.setter
    def asset_bucket_record_domain_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "assetBucketRecordDomainName", value)


@jsii.data_type(
    jsii_type="cdk-private-asset-bucket.PrivateAssetBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "user_pool_client_id": "userPoolClientId",
        "user_pool_id": "userPoolId",
        "asset_bucket_name": "assetBucketName",
        "asset_bucket_name_import": "assetBucketNameImport",
        "custom_domain": "customDomain",
    },
)
class PrivateAssetBucketProps:
    def __init__(
        self,
        *,
        user_pool_client_id: builtins.str,
        user_pool_id: builtins.str,
        asset_bucket_name: typing.Optional[builtins.str] = None,
        asset_bucket_name_import: typing.Optional[builtins.str] = None,
        custom_domain: typing.Optional[CustomDomain] = None,
    ) -> None:
        '''
        :param user_pool_client_id: 
        :param user_pool_id: 
        :param asset_bucket_name: 
        :param asset_bucket_name_import: if you want to use an imported bucket instead.
        :param custom_domain: 
        '''
        if isinstance(custom_domain, dict):
            custom_domain = CustomDomain(**custom_domain)
        self._values: typing.Dict[str, typing.Any] = {
            "user_pool_client_id": user_pool_client_id,
            "user_pool_id": user_pool_id,
        }
        if asset_bucket_name is not None:
            self._values["asset_bucket_name"] = asset_bucket_name
        if asset_bucket_name_import is not None:
            self._values["asset_bucket_name_import"] = asset_bucket_name_import
        if custom_domain is not None:
            self._values["custom_domain"] = custom_domain

    @builtins.property
    def user_pool_client_id(self) -> builtins.str:
        result = self._values.get("user_pool_client_id")
        assert result is not None, "Required property 'user_pool_client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("asset_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_bucket_name_import(self) -> typing.Optional[builtins.str]:
        '''if you want to use an imported bucket instead.'''
        result = self._values.get("asset_bucket_name_import")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_domain(self) -> typing.Optional[CustomDomain]:
        result = self._values.get("custom_domain")
        return typing.cast(typing.Optional[CustomDomain], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivateAssetBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CustomDomain",
    "PrivateAssetBucket",
    "PrivateAssetBucketProps",
]

publication.publish()
