# Async Nickname Checker

This Python script asynchronously checks the availability of nicknames on the [Lichess](https://lichess.org/) platform using their autocomplete API. It takes a list of keywords from a provided JSON file and checks each keyword to see if it's available as a nickname on Lichess.

## Requirements

- Python 3.7 or higher
- aiohttp library

## Usage

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/async-nickname-checker.git
    ```

2. Install dependencies:

    ```bash
    pip install aiohttp
    ```

3. Run the script:

    ```bash
    python liparse.py
    ```

4. The script will output the result in a JSON file named `result.json`.

## Configuration

- `base_url`: Base URL of the Lichess autocomplete API.
- `json_file`: Name of the JSON file where results will be stored.
- `threads`: Number of concurrent requests to make.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
