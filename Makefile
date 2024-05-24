# Start docker-compose and open the browser : browser is not opened
init: 
	docker compose up
	open http://localhost:8081

# Remove all containers and volumes : doesn't work, need a target
remove:
	docker rm $(docker ps -a -q)
	docker volume rm sportfirst-back_SportFirstVolume

# Start the containers
dockup:
	docker compose up

# Stop the containers : doesn't work, need a target
dockdown:
	docker compose down