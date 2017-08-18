(defproject bigforecast "0.0.1-SNAPSHOT"
  :source-paths ["topologies"]
  :resource-paths ["_resources"]
  :target-path "_build"
  :min-lein-version "2.0.0"
  :jvm-opts ["-client"]
  :dependencies  [[org.apache.storm/storm-core "1.1.0"]
                  [com.parsely/streamparse "0.0.4-SNAPSHOT"]
                  [org.apache.storm/flux-core "1.0.2"]
                  ]
  :jar-exclusions     [#"log4j\.properties" #"backtype" #"trident" #"META-INF" #"meta-inf" #"\.yaml"]
  :uberjar-exclusions [#"log4j\.properties" #"backtype" #"trident" #"META-INF" #"meta-inf" #"\.yaml"]
  )
