import yaml


class GameConfig:
    def __init__(self, config_file):
        self.config_file = config_file
        self.parameters = {}
        self.load_config()

    def load_config(self):
        """Load the configuration from a YAML file."""
        with open(self.config_file, 'r') as file:
            self.parameters = yaml.safe_load(file)

    def get_parameter(self, key):
        """Get a specific parameter value."""
        keys = key.split('.')
        value = self.parameters
        for k in keys:
            value = value.get(k)
        return value

    def set_parameter(self, key, value):
        """Set a specific parameter value and save to file."""
        keys = key.split('.')
        param = self.parameters
        for k in keys[:-1]:
            param = param.setdefault(k, {})
        param[keys[-1]] = value
        self.save_config()

    def save_config(self):
        """Save the current parameters to the YAML file without anchors."""
        with open(self.config_file, 'w') as file:
            # Use the default Dumper to avoid anchors and maintain a flat structure
            yaml.dump(self.parameters, file, default_flow_style=False)

    def get_options(self, key):
        """Get possible options for a specific parameter."""
        return self.get_parameter(f"options.{key}")
