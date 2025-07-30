# 🎈 GenAIOps Helm Charts

This repository provides a collection of Helm charts designed to support the genaiops-enablement-workshop. These charts simplify the deployment of essential components and services needed for the workshop.

## Introduction

The genaiops-enablement-workshop is designed to provide hands-on experience with GenAIOps. This repository contains the Helm charts to deploy the necessary infrastructure and applications.

For more information on the workshop, please refer to the [genaiops-enablement-workshop repository](https://github.com/redhat-na-ssa/genaiops-enablement-workshop).

In addition to the charts in this repository, the workshop also uses Helm charts from the [Red Hat Co-op Helm Charts](https://github.com/redhat-cop/helm-charts/) repository.

## Usage

To use these Helm charts, you will need to have Helm installed and configured on your machine. You can then add this repository to your Helm client:

```bash
helm repo add genaiops https://redhat-na-ssa.github.io/genaiops-helmcharts/
helm repo update
```

Once the repository has been added, you can install any of the charts by running:

```bash
helm install my-release genaiops/<chart-name>
```

Replace `<chart-name>` with the name of the chart you wish to install.

## Contributing

We welcome contributions to this repository. If you have a chart you would like to add or an improvement to an existing chart, please open a pull request.

## License

This project is licensed under the [Apache 2.0 License](LICENSE).
