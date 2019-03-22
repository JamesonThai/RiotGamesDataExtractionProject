"
  Data analysis script will move into notebook later on
"


get_data <- function(){
  print("csv's to dataframes start")
  tic("match.cores")
  if (!exists('match.cores')) match.cores <- read_csv("data/proplayerdatapreprocessed/matchcores.csv")
  toc()
  tic("match.parti")
  if (!exists('match.parti')) match.parti <- read_csv("data/proplayerdatapreprocessed/matchparticipants.csv")
  toc()
  tic("match.stats")
  if (!exists('match.stats')) match.stats <- read_csv("data/proplayerdatapreprocessed/matchstats.csv")
  toc()
  tic("time.events")
  if (!exists('time.events')) time.events <- read_csv("data/proplayerdatapreprocessed/timelineEvents.csv")
  toc()
  tic("time.partis")
  if (!exists('time.partis')) time.partis <- read_csv("data/proplayerdatapreprocessed/timelineParticipants.csv")
  toc()
  print("csv's to dataframes end")
  return(list(match.cores, match.parti, match.stats, time.events, time.partis))
}


main <- function(){
  # check if libraries are installed
  package.list <- c("ggplot2", "tidyverse")
  new.packages <- package.list[!(package.list %in% installed.packages()[,"Package"])]
  if (length(new.packages)) {
    install.packages(new.packages, dependencies = TRUE)
  } else {
    print("packages checked")
    library(ggplot2)
    library(tidyverse)
    # install.packages("tictoc", repos = "http://cran.us.r-project.org")
    library(tictoc)
  }

  # getting all of the cores into their respective dataframes
  print("Main Program Start")
  results <- get_data()
  match.cores <- results[1]
  match.parti <- results[2]
  match.stats <- results[3]
  time.events <- results[4]
  time.partis <- results[5]

  
  print("Main Program End")
  

}

if (!interactive()){
  print("entering program")
  main()
  print("Program finished")
}

