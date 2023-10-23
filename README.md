# Installation

Create your environment :

```sh
python -m venv <env_name>
```

Activate your environment :

```sh
source <env_name>/bin/activate
```

Install requirements :

```sh
python -m pip install -r requirements.txt
```

Download the tool for spacy :

```sh
python -m spacy download en_core_web_sm
```

Run this project :

```sh
python transform.py
```

# Research

The purpose of this research is to guess if a change request or an issue fix will impact legacy files (not changed for a while).

Objective of the demonstrator (first iterate):
 1. From the repo list all files and make an estimate of the last modification time (without a costly tree walk)
 2. In the list (1) mark all legacy files (modified more than 20% of project elapsed time)
 3. Take an issue (e.g. Quarkus #34261)
 4. Compute the distance form the text of the issue with all files of (1). This implie to transform all source file with the algo in transform.py (note: we might use a local DB in order not to do this operation and/or cache the result - with a cache invalidation on modified date).


Proof: 
 4 - Take a PR with modified files in the bug fixing (e.g.)

Install:
pip3 install spacy
python3 -m spacy download en_core_web_sm

Example with Quarkus:
Issue: https://github.com/quarkusio/quarkus/issues/34261
PR solving the issue: https://github.com/quarkusio/quarkus/pull/34371/commits

Impacted files:
https://github.com/SivaM07/quarkus/blob/61a56c79dc3dbf9beb7075076af40f4ea98c5d9c/extensions/grpc/deployment/src/main/java/io/quarkus/grpc/deployment/GrpcServerProcessor.java
https://github.com/SivaM07/quarkus/blob/61a56c79dc3dbf9beb7075076af40f4ea98c5d9c/extensions/grpc/deployment/src/test/java/io/quarkus/grpc/server/GrpcCustomHttpRootPathTest.java
https://github.com/SivaM07/quarkus/blob/61a56c79dc3dbf9beb7075076af40f4ea98c5d9c/extensions/vertx-http/deployment/src/main/java/io/quarkus/vertx/http/deployment/VertxHttpProcessor.java
https://github.com/SivaM07/quarkus/blob/61a56c79dc3dbf9beb7075076af40f4ea98c5d9c/extensions/vertx-http/deployment/src/main/java/io/quarkus/vertx/http/deployment/VertxWebRouterBuildItem.java


File not related with the issue:
https://github.com/quarkusio/quarkus/blob/main/core/runtime/src/main/java/io/quarkus/runtime/graal/AwtImageIO.java
