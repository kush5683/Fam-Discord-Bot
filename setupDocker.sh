git pull
sudo docker stop fam-discord-bot
sudo docker rm fam-discord-bot
sudo docker build -t fam-discord-bot -f Dockerfile .
sudo docker run -d --name fam-discord-bot fam-discord-bot
sudo docker logs fam-discord-bot
