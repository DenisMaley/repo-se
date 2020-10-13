## Repo Search Engine

An API to search public repositories.

### Architecture
The aim of this project is to build the API  
to search public repositories on a hosting platform for version control using Git. 
For example Gitlab, Github, or Bitbucket. 
It should be possible to search within different integrations (so hosting platforms).
All these integrations are different, an uniform should communicate with them so it makes sense
to use the [microservices architectural pattern][microservices_article].

It is common to use HTTP (and REST), but as we’ll see, 
we can use other types of communication protocols such as RPC (Remote Procedure Call) 
over AMQP (Advanced Message Queuing Protocol).

For that, we will use [Nameko][nameko], a Python microservices framework. 
It has RPC over AMQP built in, allowing for you to easily communicate between your services. 
It also has a simple interface for HTTP queries, which we’ll use in this project for simplicity. 
However, for writing Microservices that expose an HTTP endpoint, 
it is recommended that you use another framework, such as [Flask][flask] or [FastAPI][fastapi]. 
To call Nameko methods over RPC using Flask, you can use [flask_nameko][flask_nameko], 
a wrapper built just for interoperating Flask with Nameko.

Also Nameko allows to scale the service very easily.
Nameko is built to robustly handle methods calls in a cluster.
It’s important to build services with some backward compatibility in mind, 
since in a production environment it can happen for several different versions of the same 
service to be running at the same time, especially during deployment. 
If you use Kubernetes, during deployment it will only kill all the old version containers 
when there are enough running new containers.

For Nameko, having several different versions of the same service running at the same 
time is not a problem. Since it distributes the calls in a round-robin fashion, 
the calls might go through old or new versions. 

The service classes are instantiated at the moment a call is made and destroyed after 
the call is completed. 
Therefore, they should be inherently stateless, meaning you should not try to keep any 
state in the object or class between calls. 
This implies that the services themselves must be stateless. 
With the assumption that all services are stateless, 
Nameko is able to leverage concurrency by using [eventlet][eventlet] greenthreads. 
The instantiated services are called “workers,” and there can be a configured maximum 
number of workers running at the same time.

## Requirements

* [Docker][docker]
* [Docker-compose][docker-compose]


### Running

```shell script
$ docker-compose up -d
```

or 

```shell script
$ docker-compose up
```
if you want to see logs.

Then you can use the search endpoint:

```shell script
$ curl --header "GITLAB-ACCESS-TOKEN: <gitlab token>" "http://localhost:8000/repos?q=stochastic%20time%20generator"
```
```json
{"repos": [
  {"name": "ymullr/libturbgen", "url": "https://github.com/ymullr/libturbgen"}, 
  {"name": "jglemne/rngs", "url": "https://github.com/jglemne/rngs"}, 
  {"name": "njdepsky/GCM-Downscaling-Tool", "url": "https://github.com/njdepsky/GCM-Downscaling-Tool"}, 
  {"name": "Gaelle Faure / loadstochgen", "url": "https://gitlab.com/GFaure/loadstochgen"}
]}
```
It found 3 repos from Github and 1 from Gitlab, 
and all of them are represented in the uniform response.
If you don't have Gitlab access token, you can just omit it 
and the API will exclude Gitlab repos:

```shell script
$ curl  "http://localhost:8000/repos?q=stochastic%20time%20generator"
```
```json
{"repos": [
  {"name": "ymullr/libturbgen", "url": "https://github.com/ymullr/libturbgen"}, 
  {"name": "jglemne/rngs", "url": "https://github.com/jglemne/rngs"}, 
  {"name": "njdepsky/GCM-Downscaling-Tool", "url": "https://github.com/njdepsky/GCM-Downscaling-Tool"}
]}
```

To enter a service shell and nameko shell inside it:

```shell script
$ docker-compose exec github bash
```

```shell script
$ nameko shell --config config.yml
Nameko Python 3.9.0 (default, Oct  6 2020, 21:52:53) 
[GCC 8.3.0] shell on linux
Broker: amqp://guest:guest@rabbit:5672/ (from --config)
>>> 

```

And to interract with a service inside nameko shell:

```shell script
n.rpc.github_service.search('stochastic time generator')
```

It will give the result of the method in the Github service.
It's very useful to debug and test the services.
You can access all the services.

Use exit() or Ctrl-D (i.e. EOF) to exit.

### Logs

To see the logs of queries and results:

```shell script
$ docker-compose exec uniform bash
```

```shell script
$ nameko shell --config config.yml

```

```shell script
n.rpc.uniform_service.get_logs()
```

### Docs

To view API specs open swagger.yaml in [Swagger Editor][swagger-editor]

### To Do

* Add Flask or Fast API with a proper validation ans schemas
* Add Flasgger
* Add CI/CD
* Add Swagger documentation
* Add Unit and functional tests
* Transform services to packages
* Catch negative use case scenarios
* Add k8s to manage the nodes running the service

[microservices_article]: https://martinfowler.com/articles/microservices.html
[nameko]: https://nameko.readthedocs.io/en/stable/
[flask]: https://flask.palletsprojects.com/en/1.1.x/
[fastapi]: https://fastapi.tiangolo.com/
[flask_nameko]: https://github.com/jessepollak/flask-nameko
[eventlet]: http://eventlet.net/
[docker]: https://docs.docker.com/get-docker/
[docker-compose]: https://docs.docker.com/compose/install/
[swagger-editor]: https://editor.swagger.io/
