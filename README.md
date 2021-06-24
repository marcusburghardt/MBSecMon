InfoSec Monitoring
==================

This is a very flexible and powerful monitoring system focused in CyberSecurity.
The goal of this solution is to reduce manual and time-consuming tasks and improve
the CyberSecurity monitoring by centralizing the information from different sources,
analyzing them systematically to detect atypical behaviors or generate insights.

Concerning about privacy, the focus of this tool is based on events and not in
individuals. Events give us insights about potential security issues and the
Security Team should investigate the details, including the involved stakeholders.

Motivation
----------

During all my career working with Security and Infrastructure, in this both areas,
monitoring was always important to allow me doing a better job. In addition, open-source
is part of my life. This brought me to find and explore these amazing tools which I
like to use for working and personal projects. Buuut, since my free time is usually
very limited, I decided to make the implementation of these tools easier while applying
the knowledge got from studying new tools, techniques and solutions. In this case,
containers, APIs, automation, etc. : )

Relevant Projects
-----------------

The solution is based on the following projects:
- Zabbix
  - Is the core of this solution. It is used to collect, store and process the measures
  from many sources, according to the enabled templates.
  - The templates use the Zabbix engine to make the magic happen, collecting information
  from the agents with encryption, comparing the values to detect atypical behaviors
  and sending effective alerts.
  - https://www.zabbix.com/documentation/current/manual/config/templates/template

- Grafana
  - We can check deep details in the Zabbix side, but this is not useful for daily tasks.
  For that, Grafana is a very important component to create clear and easy dashboards
  focused in generating insights.
  - https://grafana.com/docs/grafana/latest/installation/docker/

- Docker Compose
  - All the provisioning and integration of this solution is orchestrated by 
  Docker Compose files. I decided to not use SWARM initially, since initially I don't
  need high availability by the cost of more complexity. However, this is not excluded
  for the future.
  - https://github.com/zabbix/zabbix-docker

- Ansible (ToDo)
  - Once the solution is deployed, all the maintenance is made by Ansible playbooks.
    For the future, is considered more automation with Ansible modules and Playbooks
    together in an Ansible role.

- Python
  - This solution interact with many APIs to collect and centralize the information
  for analysis. Python 3 should be used to interact with these APIs.
  - If desired to monitor a new system, the respective documentation should be consulted.
  Any kind of script is possible, but Python is more flexible. So, I left an example
  as reference in "zabbix-agent/scripts" folder, including the reference for documentation.

Currently, for flexibility and limited time purposes, the Zabbix Agent which interact
with the APIs is not containerized. It is a typical Zabbix Agent with some extra 
configuration files. In the future, this agent will be converted to container too.
For that, a new image need to be prepared before. This would be great but is not a 
priority now and my free time is quite limited. Contributors are always welcome. : )

This app was developed in a very short time (my free time) to make the things happen
and, for sure, a lot of nice and extra features could be added. Actually, as any CyberSec
project, it demands continual improvement to be aligned with the reality.

Important Points:
- This solution interact with the APIs only using official solutions and with read-only
permissions. The solution is intended to monitor, not to manage the monitored systems
and this should not be changed without a deep and detailed analysis of the entire solution.
- The credentials used in the APIs are end-user credentials and the permissions are
compatible with the credential used. This make the management easier and, of course,
should be used only by who knows what is doing. CyberSecurity demands experience and
complete knowledge of the actions and their consequences.

References:
- https://www.zabbix.com/documentation/current/manual/config/templates/template
- https://grafana.com/docs/grafana/latest/installation/docker/
- https://github.com/zabbix/zabbix-docker
- https://www.python.org/
- https://docs.github.com/en/rest
- https://github.com/PyGithub/PyGithub
- https://developers.google.com/admin-sdk/
- https://docs.ansible.com/

Content
------------

This solution comes with these files and folders:

- README.md
  - This one. : )
- docker-compose.yaml
  - Used to provisioning the solution. Some extra files support the docker compose script:
      - .env_db_mysql: Environment variables to configure the MySQL container.
      - .env_grafana: Environment variables to configure the Grafana container.
      - .env_srv: Environment variables to configure the Zabbix Server container.
      - .env_web: Environment variables to configure the NGINX Frontend container.
      - .GRAFANA_ADMIN_PASSWORD: One line file used to define the default admin password for Grafana.
      - .MYSQL_ROOT_PASSWORD: One line file used to define the default root password for MySQL.
      - .MYSQL_PASSWORD: One line file used to define the password used for Zabbix database.
      - .MYSQL_USER: One line file used to define the username for Zabbix database.
      - gfn_env: volumes mapped to Grafana container or auxiliary files used inside the container.
      - zbx_env: volumes mapped to Zabbix container or auxiliary files used inside the container.
- zabbix-agent
  - Files and folders used to configure the zabbix-agent according the Zabbix server templates.
    - scritps: Python scripts used to interact with APIs.
    - zabbix_agentd.d: Relationship between keys used in the templates and the commands to collect
      desired information.
    - zabbix_agentd.conf: Recommended configuration file for the agent. Tested in CentOS and Fedora.
- zabbix-templates
  - Zabbix templates exported in JSON files so they can be easily imported or updated.
    - We can manage templates directly on the files, but I strongly recommend doing by the
    Zabbix interface, and exporting from there in JSON format trough the Zabbix API.

Templates
------------

- Template InfoSec - Github
  - Inform the Organization Name.
  - Zabbix discover some relevant information, like:
    - How many members.
    - Monitor public and private repositories

ToDo
------------

Container Agent

- Define a new image with zabbix-agent configured appropriately and python3 support.
- It will improve the automation of the project and consequently the stability.

Templates

Template InfoSec - WebServices (ToDo)
  - Inform the FQDNs to be monitored.
  - Verify the TLS versions.
  - Verify the CipherSuites configurations.
  - Verify certificates expiration dates.
  - Verify HTTP headers.

Requirements
------------

For Zabbix-Agent:

- python3 and the following modules:
  - pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
  - pip3 install --upgrade jira

For Container Server:

  Packages
  - docker
  - docker-compose
  - ansible

Dependencies
------------

None. The code was make thinking in the best compatibility.

Dirtying the Hands
----------------

1 - First we need to satisfy the SO requirements:
For Fedora/CentOS/RedHat:
- $ sudo dnf install -y python3 docker docker-compose epel-release
- $ sudo systemctl enable docker; sudo systemctl start docker ; sudo systemctl status docker
- $ sudo dnf install -y zabbix40-agent

2 - Adjust the Zabbix Agent.
- $ sudo cp -a scripts
- $ sudo cp -a conf
- $ sudo systemctl enable zabbix-agent; sudo systemctl start zabbix-agent; sudo systemctl status zabbix-agent

3 - Adjust the passwords and file locations on the respective files:
- .GRAFANA_ADMIN_PASSWORD
- .MYSQL_PASSWORD
- .MYSQL_ROOT_PASSWORD
- .gfn_env/provisioning/datasources/all.yml

4 - Adjust the firewall access:
  sudo firewall-cmd --add-service=zabbix-agent --permanent
  sudo firewall-cmd --add-service=https --permanent
  sudo firewall-cmd --add-service=http --permanent
  sudo firewall-cmd --reload

5 - Generate self-signed certificates or copy "valid" ones:
$ cd zbx_env/var/lib/zabbix/enc
$ sudo openssl req -subj '/CN=localhost' -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365

5 - Now we have to start our solution.
- $ sudo docker-compose -f ./docker-compose.yaml up -d

Troubleshooting commands:

- zabbix_agentd -t 'mbsec.security.github_discovery[ORG]'
- sudo docker logs -f $(sudo docker inspect --format="{{.Id}}" mb_zabbix-server_1)
- sudo docker exec -it $(sudo docker inspect --format="{{.Id}}" mb_zabbix-server_1) /bin/bash
- tail -f /var/log/zabbix/zabbix_agentd.log

License
-------

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, you can obtain one at http://mozilla.org/MPL/2.0/.

Author Information
------------------

- Marcus Burghardt
- https://www.linkedin.com/in/marcusburghardt/
