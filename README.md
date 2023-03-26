<p align="center">
  <a href="https://github.com/jenniferNeto/ColPal/graphs/contributors" alt="Contributors">
    <img src="https://github.com/jenniferNeto/ColPal/actions/workflows/docker-compose-build.yml/badge.svg">
  </a>
</p>
<p align="center">
  <a href="https://github.com/jenniferNeto/ColPal/graphs/contributors" alt="Contributors">
    <img src="https://img.shields.io/github/contributors/jenniferNeto/ColPal.svg?style=for-the-badge">
  </a>
  <a href="https://github.com/jenniferNeto/ColPal/network/members" alt="Forks">
    <img src="https://img.shields.io/github/forks/jenniferNeto/ColPal.svg?style=for-the-badge">
  </a>
  <a href="https://github.com/jenniferNeto/ColPal/stargazers" alt="Stars">
    <img src="https://img.shields.io/github/stars/jenniferNeto/ColPal?style=for-the-badge">
  </a>
  <a href="https://github.com/jenniferNeto/ColPal/blob/main/LICENSE" alt="License">
    <img src="https://img.shields.io/github/license/jenniferNeto/ColPal.svg?style=for-the-badge">
  </a>
</p>

<p align="center">
  <a href="">
    <img src="https://img.shields.io/badge/Django-20232A?style=for-the-badge&logo=react&logoColor=61DAFB">
  </a>
  <a href="">
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB">
  </a>
  <a href="">
    <img src="https://img.shields.io/badge/Postgres-20232A?style=for-the-badge&logo=react&logoColor=61DAFB">
  </a>
</p>

<br />
<div align="center">
  <a href="https://github.com/jenniferNeto/ColPal">
    <img src="https://i.imgur.com/kVx53I2.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Stable Data</h3>

<p align="center">
    Stable data is a full stack web app that allows users to create and manage data upload pipelines to meet their specific requirements. Stable Data allows users to specify data constraints, upload frequency requirements, and pipeline viewers, uploaders, and managers.
    <br />
    <a href="https://github.com/jenniferNeto/ColPal"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/jenniferNeto/ColPal/tree/development">View Demo</a>
    ·
    <a href="https://github.com/jenniferNeto/ColPal/issues">Report Bug</a>
    ·
    <a href="https://github.com/jenniferNeto/ColPal/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

![Product Name Screen Shot](https://i.imgur.com/IoVCmEJ.png)

<!-- GETTING STARTED -->

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This project requires docker and docker-compose to build

### Installation

1. Clone the repo

   ```sh
   git clone https://github.com/jenniferNeto/ColPal.git
   ```
2. Create a .env file in the root directory
   Required attributes are:

   ```sh
   DB_HOST
   DB_NAME
   DB_USER
   DB_PASS

   POSTGRES_DB
   POSTGRES_USER
   POSTGRES_PASSWORD
   ```

   * DB_HOST must be 'db'
   * DB_x must match POSTGRES_x
3. Build the docker containers

   ```sh
   docker-compose up --build
   ```

<!-- USAGE EXAMPLES -->

## Usage

<!-- ROADMAP -->

## Roadmap

- [X] Pipeline create
  - [X] Create pipeline groups: viewer, uploader, manager
    - [X] Add groups to pipelines
- [X] Pipeline update, admin/manager vs uploader
- [X] Django test cases for actions
- [X] Basic file upload
  - [ ] Upload temporary file to cloud storage
  - [ ] Generate schema for csv files
    - [ ] Generate schema for google sheets
  - [ ] Validate file against pipeline constraints
  - [ ] Upload approved file to snowflake

See the [open issues](https://github.com/jenniferNeto/ColPal/issues) for a full list of proposed features (and known issues).

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.
