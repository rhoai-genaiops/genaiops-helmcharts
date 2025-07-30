# 🎈 GenAIOps Helm Charts

This repository contains a collection of Helm charts designed to support the GenAIOps Enablement Workshop. These charts facilitate the deployment of essential components and services required throughout the workshop.

Additionally, the workshop leverages Helm charts from the [Red Hat CoP Helm Charts](https://github.com/redhat-cop/helm-charts/) repository to complement the deployment process.
## Prerequisites

Before using these Helm charts, you need to have the following prerequisites installed and configured:

- [Kubernetes](https://kubernetes.io/) cluster (v1.22+)
- [Helm](https://helm.sh/) (v3.8+)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

## Usage

To use these Helm charts, you first need to add the repository to your Helm client:

```bash
helm repo add genaiops https://rhoai-genaiops.github.io/genaiops-helmcharts/
helm repo update
```

Once the repository is added, you can install any of the available charts using the `helm install` command. For example, to install the `app-of-apps` chart, you would run:

```bash
helm install my-release genaiops/app-of-apps
```

## Contributing

We welcome contributions to this repository. If you would like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b my-new-feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin my-new-feature`)
6. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

