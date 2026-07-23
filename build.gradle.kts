plugins {
    kotlin("jvm") version "1.9.22"
}

repositories {
    mavenCentral()
    maven("https://jitpack.io")
}

dependencies {
    implementation("com.github.recloudstream:cloudstream:master-SNAPSHOT")
}

tasks.jar {
    manifest {
        attributes["Plugin-Class"] = "com.uncenx.UncenxProvider"
    }
}
