
#socio-economic contains census data per ward.
#the second table contains the score (personal / personal+impersonal) per ward
total <- merge(socio_economic,table2_pers_pers_impers,by=c("Ward","Ward"))

#chooose the columns we want
tolinreg <- total[c("median_age", "household_size", "economic_activity", "diversity","distance_to_work", "2018")]
#eliminate wards where we don't have scores ( score = -1)
tolinreg<-tolinreg[!(tolinreg$`2018`== -1),]
#apply log to the following columns (diversity, distance to work, actual score) as they are skewed
tolinreg[, 4:6] <- log(tolinreg[4:6])

#scale = calculate the z-score for each column
tolinreg <- scale(tolinreg)

#matrix convert to data frame
tolinregdf <- as.data.frame(tolinreg)

multi.fit = lm(`2018`~median_age+household_size+economic_activity+diversity+distance_to_work, data=tolinregdf)
summary(multi.fit)


