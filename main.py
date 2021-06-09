import data_preprocessing
reviews_unified = data_preprocessing.read_reviews("C:\\Saurabh\\MLPriority\\VodafoneNZ_External.csv", False)
data_preprocessing.export(reviews_unified, "C:\\Saurabh\\MLPriorityPre\\VodafoneNZ_External_Pre.csv")