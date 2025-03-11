# Repo2Run

<p align="center">
  <img width="150" alt="Repo2Run" src="https://github.com/user-attachments/assets/b7ee9681-d05b-468f-bbef-3040d8c6683b" />
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2502.13681"><img src="https://img.shields.io/badge/cs.SE-arXiv%3A2502.13681-B31B1B.svg"></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"></a>
</p>

An LLM-based build agent system that helps manage and automate build processes in containerized environments. This project provides tools for handling dependencies, resolving conflicts, and managing build configurations.

## Features

- Docker-based sandbox environment for isolated builds
- Automated dependency management and conflict resolution
- Support for Python version management
- Waiting list and conflict list management for package dependencies
- Error format handling and output collection

## Prerequisites

- Python 3.x
- Docker
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bytedance/repo2run.git
cd repo2run
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The main entry point is through the build agent's main script. You can run it with the following arguments:

```bash
python build_agent/main.py <repository_full_name> <sha> <root_path>
```

Where:
- `repository_full_name`: The full name of the repository (e.g., user/repo)
- `sha`: The commit SHA
- `root_path`: The root path for the build process

## Project Structure

- `build_agent/` - Main package directory
  - `agents/` - Agent implementations for build configuration
  - `utils/` - Utility functions and helper classes
  - `docker/` - Docker-related configurations
  - `main.py` - Main entry point
  - `multi_main.py` - Multi-process support

## Features in Detail

### Sandbox Environment
The project uses Docker containers to create isolated build environments, ensuring clean and reproducible builds.

### Dependency Management
- **Waiting List**: Manages package installation queue
- **Conflict Resolution**: Handles version conflicts between packages
- **Error Handling**: Formats and processes build errors

### Configuration Agent
Utilizes GPT models to assist in build configuration and problem resolution.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Citation

```bibtex
@article{hu2025llm,
  title={An LLM-based Agent for Reliable Docker Environment Configuration},
  author={Hu, Ruida and Peng, Chao and Wang, Xinchen and Gao, Cuiyun},
  journal={arXiv preprint arXiv:2502.13681},
  year={2025}
}
```

## License

Apache-2.0

## Ackowledgement

[https://github.com/Aider-AI/aider](https://github.com/Aider-AI/aider)

## Contact

pengchao.x@bytedance.com
