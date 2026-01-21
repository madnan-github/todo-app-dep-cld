# Data Model: Helm Chart Packaging

**Feature**: Helm Chart Packaging (007-helm-chart-packaging)
**Date**: 2026-01-22
**Status**: Complete

## Overview

This document defines the data structures and configurations for the Helm chart packaging feature. Since this feature focuses on deployment configuration rather than application data, the "data model" refers to the configuration structures and parameters that define the Helm chart.

## Key Entities

### Helm Chart Configuration

**Chart.yaml**
- `name`: Name of the chart (e.g., "todo-app")
- `version`: Semantic version of the chart (e.g., "0.1.0")
- `description`: Brief description of the chart's purpose
- `apiVersion`: Helm API version (e.g., "v2")
- `type`: Chart type ("application")
- `appVersion`: Version of the application being deployed

### Values Configuration

**values.yaml Structure**
- `frontend`:
  - `image.repository`: Docker image repository for frontend
  - `image.tag`: Docker image tag for frontend
  - `image.pullPolicy`: Image pull policy
  - `replicaCount`: Number of frontend pod replicas
  - `resources`: Resource requests and limits for frontend
  - `service.type`: Service type (ClusterIP, NodePort, LoadBalancer)
  - `service.port`: Port for frontend service
  - `env`: Environment variables for frontend

- `backend`:
  - `image.repository`: Docker image repository for backend
  - `image.tag`: Docker image tag for backend
  - `image.pullPolicy`: Image pull policy
  - `replicaCount`: Number of backend pod replicas
  - `resources`: Resource requests and limits for backend
  - `service.type`: Service type (ClusterIP, NodePort, LoadBalancer)
  - `service.port`: Port for backend service
  - `env`: Environment variables for backend

- `database`:
  - `url`: Database connection URL
  - `secretName`: Name of secret containing database credentials

- `global`:
  - `imageRegistry`: Global image registry to use
  - `storageClass`: Default storage class to use
  - `ingress`: Ingress configuration

### Kubernetes Resources

**Deployment Resources**
- Metadata (name, labels, annotations)
- Pod template specifications
- Container configurations (image, ports, environment, resources)
- Replica count
- Update strategy

**Service Resources**
- Service type (ClusterIP, NodePort, LoadBalancer)
- Port mappings (targetPort, port)
- Selector labels to match pods

**Secret Resources**
- Key-value pairs for sensitive data
- Base64 encoded values
- Labels and annotations

**ConfigMap Resources**
- Key-value pairs for configuration data
- Labels and annotations

## Relationships

### Service Dependencies
- Frontend service may depend on backend service for API calls
- Both services depend on database configuration
- All services share common namespace and labels

### Configuration Hierarchy
- Global values provide defaults
- Environment-specific values override globals
- Release-specific values override environment values

## Validation Rules

### Chart.yaml Requirements
- Name must be lowercase and follow DNS-1123 label standard
- Version must follow semantic versioning
- Description must be present and non-empty
- apiVersion must be "v2" for Helm 3

### Values.yaml Requirements
- Required parameters must have default values
- Resource limits must be specified as valid Kubernetes resource quantities
- Image tags must follow Docker tag naming conventions
- Port numbers must be valid (1-65535)

### Template Validation
- All template references must correspond to values in values.yaml
- Template syntax must be valid Go templates
- Generated YAML must be syntactically correct

## State Transitions (if applicable)

### Deployment States
- `pending`: Chart package created but not yet installed
- `installing`: Helm install command in progress
- `installed`: Chart successfully deployed
- `upgrading`: Helm upgrade command in progress
- `upgraded`: Chart successfully updated
- `deleting`: Helm uninstall command in progress
- `deleted`: Chart successfully removed

## Data Flow

### Configuration Flow
1. User defines values in values.yaml or via --set flags
2. Helm templates substitute values into Kubernetes manifests
3. Kubernetes API validates and applies the manifests
4. Controllers create and manage the resources

### Parameter Inheritance
- Global parameters apply to all services
- Service-specific parameters override global defaults
- Release-specific parameters override service defaults

## Constraints

### Naming Constraints
- All Kubernetes resource names must follow DNS-1123 label standard
- Names must be 1-63 characters long
- Names must contain only lowercase alphanumeric characters and hyphens
- Names must not start or end with a hyphen

### Resource Constraints
- Memory limits must be specified in valid Kubernetes memory units (Mi, Gi)
- CPU limits must be specified in valid Kubernetes CPU units (m, cores)
- Storage requests/limits must be specified in valid Kubernetes storage units (Mi, Gi)

### Security Constraints
- Sensitive data must be stored in Secrets, not ConfigMaps
- Default security contexts should prevent running as root
- Image pull policies should be configurable for different environments