# 🎈 GenAIOps Helm Charts

This repository contains a collection of Helm charts designed to support the GenAIOps Enablement Workshop. These charts facilitate the deployment of essential components and services required throughout the workshop.

## Purpose

The primary purpose of these Helm charts is to streamline the setup and deployment of the necessary infrastructure for the GenAIOps Enablement Workshop. By using these charts, participants can quickly and easily deploy the required services and focus on the workshop's learning objectives.

## Getting Started

To use the charts in this repository, you'll first need to add the repository to your local Helm installation:

```bash
helm repo add genaiops https://github.com/redhat-na-ssa/genaiops-helmcharts
```

Once the repository has been added, you can install any of the charts using the `helm install` command. For example, to install the `genaiops-all-in-one` chart, you would run the following command:

```bash
helm install genaiops-all-in-one genaiops/genaiops-all-in-one
```

For more information on how to use Helm, please refer to the [official Helm documentation](https://helm.sh/docs/).

## External Dependencies

Additionally, the workshop leverages Helm charts from the [Red Hat CoP Helm Charts](https://github.com/redhat-cop/helm-charts/) repository to complement the deployment process.
