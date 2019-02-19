from artifactory import ArtifactoryPath

path = ArtifactoryPath(
    "http://nveuplktwrepo:8081/artifactory/webapp/#/home")

for p in path:
    print (p)