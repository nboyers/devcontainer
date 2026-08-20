# Coder Dev Container on EC2

This repository is a small Dev Container example for a Coder workspace running on an
Amazon EC2 Linux host. Coder provisions or selects the EC2 instance, and Envbuilder
builds `.devcontainer/devcontainer.json` on that host.

## 1. Prepare the host

The Coder template that creates the EC2 instance must provide:

- Linux on `amd64` or `arm64` matching the Coder agent architecture.
- Docker Engine, with the Coder agent allowed to run Docker commands.
- Git, `curl`, Node.js, and `npm` for the Dev Container CLI.
- Network access to `ghcr.io` so Dev Container features can be downloaded.
- An instance role or credentials with only the AWS permissions required by the
	template. Do not put AWS access keys in this repository.

The instance security group only needs the ports and access paths required by the
Coder deployment. The code-server app below is exposed through Coder, so port `13337`
does not need to be opened publicly.

## 2. Use the Dev Container tools

Install the Dev Container CLI on the EC2 host or on a developer workstation with
Docker:

```sh
npm install --global @devcontainers/cli
```

Build and start this repository as a Dev Container:

```sh
git clone https://github.com/jatcod3r/devcontainer.git
cd devcontainer

devcontainer build --workspace-folder .
devcontainer up --workspace-folder .
devcontainer exec --workspace-folder . bash
```

The commands above use [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json),
build [.devcontainer/Dockerfile](.devcontainer/Dockerfile), install the code-server
feature, and run the container as the `coder` user. From another terminal, verify the
example configuration inside the container:

```sh
devcontainer exec --workspace-folder . sh -lc \
	'whoami && printf "SOME_ENV_VAR=%s\\n" "$SOME_ENV_VAR" && vim --version | head -n 1'
devcontainer exec --workspace-folder . sh -lc \
	'curl --fail http://127.0.0.1:13337/healthz'
devcontainer down --workspace-folder .
```

Run the example Python app inside the container:

```sh
devcontainer exec --workspace-folder . python3 example/app.py
```

Open `http://localhost:8000` in a browser. The app also exposes `/health` and `/config`
to demonstrate a container health check and reading `SOME_ENV_VAR` from Python.

In VS Code, install the Dev Containers extension, open this repository, and run
**Dev Containers: Reopen in Container**. In Coder, open the code-server app created by
the `coder` customization; it points at the same workspace folder.

## 3. Run it from a Coder workspace on EC2

Coder's template can clone the repository and invoke the same Dev Container workflow.
Adapt the agent resource and EC2 provisioning to your existing Coder AWS template:

```hcl
resource "coder_agent" "dev" {
	arch = "amd64"
	os   = "linux"

	dir = "/home/coder/workspace"

	startup_script = <<-EOT
		set -eu

		sudo apt-get update
		sudo apt-get install -y git curl nodejs npm
		rm -rf /home/coder/workspace
		git clone https://github.com/jatcod3r/devcontainer.git /home/coder/workspace

		npm install --global @devcontainers/cli
		devcontainer up --workspace-folder /home/coder/workspace
	EOT
}
```

For private repositories, use Coder's Git authentication or an instance role and
keep the repository credentials out of the startup script. If the EC2 image is
intentionally Dockerless, use [Envbuilder](https://github.com/coder/envbuilder)
instead of the Dev Container CLI; it consumes the same `.devcontainer` files.

## 4. What this example provides

- Ubuntu 24.04 with `vim`, `curl`, `net-tools`, and passwordless `sudo` for the
	non-root `coder` user.
- A Coder code-server app on port `13337`, shared only with the workspace owner.
- VS Code settings and extensions from `.devcontainer/devcontainer.json`.
- A sample `SOME_ENV_VAR` remote environment variable.

The container specification is in [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json)
and its image definition is in [.devcontainer/Dockerfile](.devcontainer/Dockerfile).

## References

- [Dev Container specification](https://containers.dev/overview)
- [Coder Dev Containers](https://coder.com/docs/admin/templates/managing-templates/devcontainers)
- [Envbuilder](https://github.com/coder/envbuilder)
- [Envbuilder supported features](https://github.com/coder/envbuilder/blob/main/docs/devcontainer-spec-support.md)