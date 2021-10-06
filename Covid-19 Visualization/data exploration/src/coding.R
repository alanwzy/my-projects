covid19_city <- read.csv("covid19_city.csv")


covid19_detail <- read.csv("covid19_detail.csv")
head(covid19_detail)

covid19_location <- read.csv("China province.csv")
head(covid19_location)

covid19_data<- read.csv("covid19_data.csv")



# To answer question 1, need to filter and subset data 

library(dplyr)

covid19_china <- filter(covid19_data, Country.Region == "Mainland China" | Province.State == "HongKong")

#convert obsercationDate from factor to date

covid19_detail$reporting.date <-as.Date(covid19_detail$reporting.date, format="%m/%d/%y")
covid19_china$ObservationDate <- as.Date(covid19_china$ObservationDate, format ="%m/%d/%y")

#rename the column name for joining the table
#tabluau won't recongnize Mainland China, change value in columns to china
#in the country.Region column

covid19_location<- covid19_location %>% rename(Province.State = ï..Province.State)
#first convert everything in to character, its easier this way
covid19_china$Country.Region <- as.character(covid19_china$Country.Region)
#change Mainland china to china

covid19_china$Country.Region[covid19_china$Country.Region == "Mainland China"] <- "China"
covid19_china$Country.Region <- as.factor(covid19_china$Country.Region)
#join

covid19_china_merged <- merge(x=covid19_china, y=covid19_location, by ="Province.State")

#output
write.csv(covid19_china_merged, "covie19_china_merged.csv")

#question 2
#find many Na values, empty values and N/A
covid19_age <- filter(covid19_city, country == "China")
covid19_age$date_confirmation <- as.Date(covid19_age$date_confirmation, format ="%d.%m.%y")
is.na(covid19_age$age)
covid19_age$age[covid19_age$age == ""] <- NA
covid19_age$age[covid19_age$age == "N/A"] <- NA
is.na(covid19_age$age)
covid19_age_clean <- covid19_age %>% filter(!is.na(covid19_age$age))
covid19_age_clean <- covid19_age_clean[-c(524)]
covid19_age_clean$age[covid19_age_clean$age == "16-80"] <- '48'
covid19_age_clean$age[covid19_age_clean$age == "19-77"] <- (19+77)/2
covid19_age_clean$age[covid19_age_clean$age == "21-72"] <- '46'
covid19_age_clean$age[covid19_age_clean$age == "22-80"] <- '53'
covid19_age_clean$age[covid19_age_clean$age == "23-72"] <- '48'
covid19_age_clean$age[covid19_age_clean$age == "38-68"] <- '53'
covid19_age_clean$age[covid19_age_clean$age == "36-45"] <- '40'
covid19_age_clean$age[covid19_age_clean$age == "8-68"] <- '38'
covid19_age_clean$age <- as.character(covid19_age_clean$age)
covid19_age_clean$age <- as.numeric(covid19_age_clean$age)
write.csv(covid19_age_clean,"covid19_age_clean.csv")
library(ggplot2)

#plot age graph

#PLOT CITY 
covid19_age_clean$city[covid19_age_clean$city == ""] <- NA
covid19_age_clean <- covid19_age_clean %>% filter(!is.na(covid19_age_clean$city))
write.csv(covid19_age_clean,"covid19_age_clean.csv")



#question3 
covid19_country <- read.csv("covid19_data.csv")
covid19_country$Country.Region <- as.character(covid19_country$Country.Region)
covid19_country$Country.Region[covid19_country$Country.Region == "Mainland China"] <- "China"
covid19_country$Country.Region <- as.factor(covid19_country$Country.Region)
covid19_country$ObservationDate <- as.Date(covid19_country$ObservationDate, format ="%m/%d/%y")
write.csv(covid19_country,"covid19_country.csv")




       