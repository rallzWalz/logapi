
dir=$PWD

docker build -t test -f ./API_Dockerfile . 

docker run -p 8080:8080 -v $dir:/src --rm test