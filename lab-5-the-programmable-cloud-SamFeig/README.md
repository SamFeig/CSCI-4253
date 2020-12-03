# lab5-programmable-cloud
An assignment to demonstrate programmatic interfaces to cloud software

## Overview

The goal of this assignment is to have you understand the benefit of cloud environments in constructing and managing datacenter applications.

This assignment consistts of three parts:
* You will write a program that creates and configures a virtual machine, installs a software application from a `git` repository, modifies firewall rules so that the software is accessible and then instructs the user to visit a specific web page to use the software.
* You will write another program that will create a "snapshot" of the virtual machine created in the first exercise and use that snapshot to create an [image](https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#before-you-begin). You will then create three new instances using your image while measuring the time needed to create each instance.
* You will use a [service account](https://cloud.google.com/iam/docs/understanding-service-accounts) and use those credentials to create a virtual machine that will then create another virtual machine. This essentially amounts to stuffing the code from the first part into another virtual machine.

We will be usinng the [python interface](https://cloud.google.com/compute/docs/tutorials/python-guide) to the Google cloud API's to write our code. You can either use your laptop if you can install the [cloud sdk](https://cloud.google.com/sdk/) on it or you can use the Google cloud console for your project.

> Note: Google recently released a code-editor interface to Google Cloud Console
> You can [read more about it here](https://cloud.google.com/shell/docs/features#code_editor).

It's difficult to add new `.ssh` keys into your Google cloud console which means it's hard to use the `git` access method pull in your class repo. You can either add the public key that Google provides to your `github.com` account or use the [`https` transport and password authentication](https://help.github.com/en/articles/which-remote-url-should-i-use).

## Details

You should write your code using the template files in each subdirectory. Each part has a `README.md` file that contains more details on each part.

I recommend you start by going through the tutorial mentioned in `part1/README.md`. Then, for each step, first do each of the needed steps using the Google console and only then start to write the code to do the same thing. This will help you identify which Google API's are needed.

You will make extensive use of the [Google cloud API's](https://cloud.google.com/compute/docs/reference/rest/v1/). The API's are organized by service (e.g. `instace` has all the information about creating an instance). At the bottom of each API documentation is a code snippet showing how to use the API in Python. Many API's allow you to specify configuration or details using a Python `dict` which is more or less `json`.

