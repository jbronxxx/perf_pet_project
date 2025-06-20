from app.app import app
from config_reader.config_reader import config_reader

if __name__ == "__main__":
    app.run(debug=config_reader.logging_level)
