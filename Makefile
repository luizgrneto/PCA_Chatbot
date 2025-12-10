.PHONY: help create-env delete-env checks lint run terra-init terra-plan terra-apply deploy

PYTHON_VERSION := 3.13.0
TERRAFORM_DIR := terraform

help:
	@echo "ADK Agent Makefile Commands:"
	@echo ""
	@echo "Environment Management:"
	@echo "  create-env          Create Python virtual environment"
	@echo "  delete-env          Delete Python virtual environment"
	@echo ""
	@echo "Code Quality:"
	@echo "  checks              Run ruff code quality checks"
	@echo "  lint                Format code with ruff"
	@echo ""
	@echo "Development:"
	@echo "  run                 Run the ADK agent web server locally"
	@echo ""
	@echo "Terraform Commands:"
	@echo "  terra-init env=ENV                    Initialize Terraform for environment (dev/prd)"
	@echo "  terra-plan app_name=NAME env_secret=SECRET   Plan Terraform changes (env optional)"
	@echo "  terra-apply app_name=NAME env_secret=SECRET  Apply Terraform changes (env optional)"
	@echo ""
	@echo "Deployment:"
	@echo "  deploy app_name=NAME env=ENV          Deploy app with terraform-generated name"
	@echo ""
	@echo "Examples:"
	@echo "  # Plan/apply with required parameters:"
	@echo "  make terra-plan app_name=my-agent env_secret=agent_secrets"
	@echo "  make terra-apply app_name=my-agent env_secret=agent_secrets"
	@echo ""
	@echo "  # Deploy with same app_name and env used in terraform:"
	@echo "  make deploy app_name=my-agent env=dev"
	@echo ""
	@echo "  # Initialize for specific environment:"
	@echo "  make terra-init env=dev"
	@echo ""

create-env:
	@echo "Creating virtual environment with uv..."
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Error: uv is not installed. Please install uv first."; \
		exit 1; \
	fi
	@echo "Creating virtual environment with Python ${PYTHON_VERSION}..."
	@uv venv --python ${PYTHON_VERSION}
	@echo "Virtual environment created successfully!"

delete-env:
	@echo "Deleting virtual environment..."
	@if [ -d ".venv" ]; then \
		rm -rf .venv; \
		echo "Virtual environment deleted successfully!"; \
	else \
		echo "Virtual environment not found."; \
	fi

checks:
	@echo "Running code quality checks..."
	@echo "Checking with ruff..."
	uv run ruff check .
	@echo "All checks passed!"

lint:
	@echo "Running code linter..."
	@echo "Checking with ruff..."
	uv run ruff format .
	@echo "Linting and formatting completed!"

run:
	@echo "Starting ADK agent web server..."
	@echo "Setting PYTHONPATH to current directory and loading environment variables..."
	@if [ -f .env ]; then \
		echo "Loading environment variables from .env..."; \
		export $$(grep -v '^#' .env | xargs) && PYTHONPATH=$(shell pwd) python app/main.py; \
	else \
		echo "No .env file found, running without additional environment variables..."; \
		PYTHONPATH=$(shell pwd) python app/main.py; \
	fi

terra-init:
	@if [ -z "$(env)" ]; then \
		echo "Error: env parameter is required. Usage: make terra-init env=dev"; \
		exit 1; \
	fi
	@echo "Running Terraform init with environment: $(env)"
	@echo "Terraform directory: $(TERRAFORM_DIR)"
	terraform -chdir=$(TERRAFORM_DIR) init -backend-config=backend-$(env).hcl -reconfigure
	terraform -chdir=$(TERRAFORM_DIR) workspace new $(env) || true
	terraform -chdir=$(TERRAFORM_DIR) workspace select $(env)

terra-plan:
	@if [ -z "$(app_name)" ]; then \
		echo "Error: app_name parameter is required. Usage: make terra-plan app_name=my-app env_secret=my-secret [env=dev]"; \
		exit 1; \
	fi
	@if [ -z "$(env_secret)" ]; then \
		echo "Error: env_secret parameter is required. Usage: make terra-plan app_name=my-app env_secret=my-secret [env=dev]"; \
		exit 1; \
	fi
	@if [ -n "$(env)" ]; then \
		make terra-init; \
	fi
	@echo "Running Terraform plan with app_name: $(app_name), env_secret: $(env_secret)"
	@echo "Terraform directory: $(TERRAFORM_DIR)"
	terraform -chdir=$(TERRAFORM_DIR) plan \
		-var 'app_name={"dev":"$(app_name)-dev","prd":"$(app_name)-prd"}' \
		-var 'env_secret=$(env_secret)'

terra-apply:
	@if [ -z "$(app_name)" ]; then \
		echo "Error: app_name parameter is required. Usage: make terra-apply app_name=my-app env_secret=my-secret [env=dev]"; \
		exit 1; \
	fi
	@if [ -z "$(env_secret)" ]; then \
		echo "Error: env_secret parameter is required. Usage: make terra-apply app_name=my-app env_secret=my-secret [env=dev]"; \
		exit 1; \
	fi
	@if [ -n "$(env)" ]; then \
		make terra-init; \
	fi
	@echo "Running Terraform apply with app_name: $(app_name), env_secret: $(env_secret)"
	@echo "Terraform directory: $(TERRAFORM_DIR)"
	terraform -chdir=$(TERRAFORM_DIR) apply \
		-var 'app_name={"dev":"$(app_name)-dev","prd":"$(app_name)-prd"}' \
		-var 'env_secret=$(env_secret)'

deploy:
	@if [ -z "$(app_name)" ]; then \
		echo "Error: app_name parameter is required. Usage: make deploy app_name=my-app env=dev"; \
		exit 1; \
	fi
	@if [ -z "$(env)" ]; then \
		echo "Error: env parameter is required. Usage: make deploy app_name=my-app env=dev"; \
		exit 1; \
	fi
	@echo "Deploying ADK Agent app: $(app_name)-$(env)"
	@tsuru app-deploy -a $(app_name)-$(env) --dockerfile ./Dockerfile .
