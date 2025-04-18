# SFI Checker

<div align="center">

```
   _____ __________   ________              __            
  / ___// ____/  _/  / ____/ /_  ___  _____/ /_____  _____
  \__ \/ /_   / /   / /   / __ \/ _ \/ ___/ //_/ _ \/ ___/
 ___/ / __/ _/ /   / /___/ / / /  __/ /__/ ,< /  __/ /    
/____/_/   /___/   \____/_/ /_/\___/\___/_/|_|\___/_/     
                                                          
```

<a href="https://t.me/divinus_xyz">
    <img src="https://img.shields.io/badge/Telegram-Channel-blue?style=for-the-badge&logo=telegram" alt="Telegram Channel">
</a>
<a href="https://t.me/divinus_py">
    <img src="https://img.shields.io/badge/Telegram-Contact-blue?style=for-the-badge&logo=telegram" alt="Telegram Contact">
</a>
<br>
<b>Donarions: 0x63F78ecCB360516C13Dd48CA3CA3f72eB3D4Fd3e</b>
</div>
## Description

Script for mass verification of airdrop SFI tokens to your wallets

## Project Structure

```
.
├── config/
│   └── settings.yaml     # Configuration file
├── src/
│   ├── api/
│   │   └── base_client.py     # Base API client
│   ├── logger/
│   │   └── logging_config.py  # Logging configuration
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── checker.py         # Task checker
│   ├── utils/
│   │   ├── load_config.py     # Configuration loader
│   │   └── utils.py           # Utility functions
│   ├── task_manager.py        # Task manager
│   └── wallet.py              # Wallet operations
└── run.py                     # Main execution file
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Divvinus/SFI-Checker
   cd project-name
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Edit the `config/settings.yaml` file according to your requirements.

2. Ensure all necessary environment variables are set.

## Usage

Run the project using the command:

```bash
python run.py
```

## Requirements

- Python 3.11+
- Additional dependencies listed in requirements.txt

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin new-feature`
5. Submit a pull request

## License

MIT