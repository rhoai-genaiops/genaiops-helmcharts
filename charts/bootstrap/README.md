# bootstrap-projects

This Helm chart is designed to deploy and manage OpenShift projects.

## Introduction

The `bootstrap-projects` chart facilitates the creation of OpenShift projects and the assignment of user roles to those projects.

## Configuration

The following table lists the configurable parameters of the `bootstrap-projects` chart and their default values.

| Parameter      | Description                                     | Default                               |
|----------------|-------------------------------------------------|---------------------------------------|
| `namespaces`   | A list of namespaces to create.                 | `[]`                                  |
| `namespaces.name` | The name of the namespace to create.         | `nil`                                 |
| `namespaces.bindings` | A list of role bindings for the namespace. | `nil`                                 |
| `bindings`     | A list of user bindings to be applied to the namespaces. | `nil` |
| `bindings.name`| The name of the user or group.                  | `nil`                                 |
| `bindings.kind`| The kind of binding (e.g., `User`, `Group`).    | `nil`                                 |
| `bindings.role`| The role to assign to the user or group.        | `nil`                                 |

## Example Configuration

```yaml
namespaces:
  - name: user1-test
    bindings: 
      - name: user1
        kind: User
        role: admin
  - name: user1-prod
    bindings: 
      - name: user1
        kind: User
        role: admin
```
