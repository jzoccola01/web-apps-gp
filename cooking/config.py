# config.py
# Toggle the true/false values to switch between development and testing modes.

class Config:
    DEBUG = True
    # Other configurations

class TestingConfig(Config):
    TESTING = False
    # Other testing configurations
