name := "PageRank Project"

version := "1.0"

scalaVersion := "2.12.14"

libraryDependencies += "org.apache.spark" %% "spark-core" % "3.1.2"

updateOptions := updateOptions.value.withCachedResolution(false)
