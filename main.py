from app.app import app
from config_reader.config_reader import config

if __name__ == "__main__":
    app.run(debug=config.log_level)
