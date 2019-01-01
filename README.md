# Garage Telegram bot on a container

This is a Telegram bot that manages your garage door and that works on any of the devices supported by [balena][balena-link].


To get this project up and running, you will need to signup for a balena account [here][signup-page] and set up a device, you will need to clone this repo locally:

```
$ git clone git@github.com:paroque28/GarageTelegramBot.git
```
Set environment variables on balena:
```
POSTGRES_HOST
POSTGRES_PASSWORD
TELEGRAM_TOKEN
```
Then add your balena application's remote:
```
$ git remote add balena username@git.balena-cloud.com:username/myapp.git
```
and push the code to the newly added remote:
```
$ git push balena master
```
Connect to postgres db and apply initial.sql to populate db

[balena-link]:https://balena.io/