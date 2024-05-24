init: 
	docker compose up
	open http://localhost:8081

remove:
	docker rm $(docker ps -a -q)
	docker volume rm sportfirst-back_SportFirstVolume

dockup:
	docker compose up

dockdown:
	docker compose down