#add required libraries
library(readr)
library(dplyr)
library(factoextra)


df_service <- read.csv("Subscription_Service_Churn_Dataset.csv")
view(df_service)

#Data_cleaning
df_clean <- df_service %>% 
  filter(!is.na(MonthlyCharges) & !is.na(TotalCharges))

df_clean$SubscriptionType <- as.numeric(factor(df_clean$SubscriptionType))

df_clean <- df_clean %>% 
  mutate(AverageSpending = TotalCharges / AccountAge)

df_cluster <- df_clean %>% select(MonthlyCharges, TotalCharges, AverageSpending)

df_scaled <- scale(df_cluster)

# K - means clustering
fviz_nbclust(df_scaled, kmeans, method = "wss")

set.seed(123)

kmeans_result <- kmeans(df_scaled, centers = 3, nstart = 20)

df_clean$Cluster <- kmeans_result$cluster

cluster_summary <- df_clean %>%
  group_by(Cluster) %>%
  summarise(
    MonthlyCharges_mean = mean(MonthlyCharges),
    TotalCharges_mean = mean(TotalCharges),
    AverageSpending_mean = mean(AverageSpending),
    Count = n()
  )

print(cluster_summary)

segment_names <- c("low-spending","average-spending", "high-spending")

cluster_summary$Segment <- segment_names

print(cluster_summary)
view(cluster_summary)

#plotting the clusters
library(ggplot2)

pca_result <- prcomp(df_scaled)


df_viz <- data.frame(pca_result$x, Cluster = as.factor(df_clean$Cluster))


ggplot(df_viz, aes(x = PC1, y = PC2, color = Cluster)) +
  geom_point(alpha = 0.6, size = 2) +
  labs(title = "Customer Segmentation Based on Spending Levels",
       x = "Principal Component 1", y = "Principal Component 2") +
  theme_minimal()
