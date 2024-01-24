# VPN Service
Test Task Overview

This project is a simple VPN service that allows customers to register, use a personal account, edit personal data, and create their own sites to browse through VPN.

# Running a project with Docker
To run the project locally, follow these steps:

1. Clone the forked repo
    ```
    git clone https://github.com/vshvanska/vpn-service.git
    ```
2. Open the project folder in your IDE
3. Open a terminal in the project folder
4. Create .env file, inside define variables from .env.sample
5. Run with docker
    ```
    docker-compose up --build
    ```
6. You can use this data for login or register your own user
    ```
   username: test_user
   password: Test123321
    ```
