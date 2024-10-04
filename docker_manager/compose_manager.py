import subprocess
import os

class ComposeManager:

    def __init__(self, compose_file='docker-compose.yml', docker_compose_path='/usr/bin/docker'):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.compose_file_path = os.path.join(self.base_dir, compose_file)
        self.docker_compose_path = docker_compose_path

    def check_compose_file(self):
        """Checks if compose.yml exists."""
        if not os.path.exists(self.compose_file_path):
            raise FileNotFoundError(f"{self.compose_file_path} not found.")

    def start_services(self):
        """Starts the services defined in compose.yml. """
        try:
            self.check_compose_file()
            print("Starting services from Docker Compose")
            subprocess.run([self.docker_compose_path, 'compose', '-f', self.compose_file_path, 'up', '-d'], check=True)
            print("Services started successfully.")
        except subprocess.CalledProcessError as e:
            print("Error starting Docker Compose services: {e}")

    def stop_services(self):
        """Stop and removes the services"""
        try:
            self.check_compose_file()
            print("Stopping Docker Compose services...")
            subprocess.run([self.docker_compose_path, 'compose','-f', self.compose_file_path, 'down'])
            print("Services stopped successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error stopping Docker Compose services: {e}")
            
    def status(self):
        """Check the status of Docker Compose services."""
        try:
            self.check_compose_file()
            print("Checking Docker Compose service status...")
            subprocess.run([self.docker_compose_path, 'compose', '-f', self.compose_file_path, 'ps'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error checking status: {e}")
