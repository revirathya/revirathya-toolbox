build:
	uv build
	docker build -t avidito/revirathya-toolbox:0.1.0 .
	docker push avidito/revirathya-toolbox:0.1.0