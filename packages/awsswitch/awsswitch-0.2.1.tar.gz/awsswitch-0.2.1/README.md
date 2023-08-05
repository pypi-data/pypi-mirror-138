# awsswitch - AWS profile switcher

Easily switch between AWS Profiles


## Credits

This is a pure python implementation of [Johnny Opao's](https://github.com/johnnyopao) tool [awsp](https://github.com/johnnyopao/awsp)


<img src="awsswitch_demo.gif" width="300">


## Prerequisites
Setup your profiles using the aws cli

```sh
aws configure --profile PROFILE_NAME
```

You can also leave out the `--profile PROFILE_NAME` param to set your `default` credentials

Refer to this doc for more information
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html


## Setup

### Install with pip

```sh
python -m pip install awsswitch
```

### Install with [pipx](https://github.com/pypa/pipx) *(recommended)*

 ```sh
pipx install awsswitch
```

### Shell configuration

Add the following to your .bashrc or .zshrc config:
```sh
alias awsp='awsswitch; sp="$(cat ~/.awsswitch)"; if [ -z "$sp" ]; then unset AWS_PROFILE; else export AWS_PROFILE="$sp";fi'
```


## Usage
```sh
awsp
```
