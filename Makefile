init : 
	docker compose up
	open http://localhost:8081

docker-rm:
	docker rm $(docker ps -a -q)
	docker volume rm sportfirst-back_SportFirstVolume

docker-up:
	docker compose up

docker-down:
	docker compose down

