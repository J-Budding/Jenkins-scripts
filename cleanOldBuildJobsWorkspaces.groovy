// Run this script as freestyle Jenkins job with a build step Execute system groovy.
// It deletes the workspace of jobs that are older than one month.
// This script does this for Maven jobs (it instanceof hudson.maven.MavenModuleSet) but
// can be easily adapted to do this for all types of jobs.

import hudson.model.*
import jenkins.model.Jenkins
import hudson.maven.*

def dryrun = build.buildVariableResolver.resolve("dryrun").toBoolean()

Jenkins.instance.getAllItems(Job.class).each{ 
    if (it instanceof hudson.maven.MavenModuleSet) {
        println "Maven build " + it.name
        if(!it.isBuilding()) {
            if ( it.getLastBuild() ) {
                def todayMinusOneMonth = new Date() - 30
                todayMinusOneMonth = todayMinusOneMonth.format("yyyyMMdd")
                //println todayMinusOneMonth
                def buildDate = it.getLastBuild().getTime().format("yyyyMMdd")
                //println buildDate
                if (buildDate < todayMinusOneMonth) {
                    //   println(">>> Wiping out workspace of job " + it.fullName )
                    if (!dryrun) {
                        println "Wipe out workspace for " + it.fullName + " date: " + buildDate + " url: http://localhost:8080/" + it.url
                        it.doDoWipeOutWorkspace()
                    } else {
                        println "[Dry run] Workspace wipeout " + it.fullName + " date: " + buildDate + " url: http://localhost:8080/" + it.url                        
                    }
                    
                }
            }
        } else {
            println("Skipping job " + it.fullName + ", currently building !!!")
        }
    }

}

return "DONE"
