library(ggplot2)
library(dplyr) # For data manipulation

# Probabilities of success
p_success_values <- c(0.10, 0.20, 0.30,0.40,0.50)

# Number of trials to consider
n_trials_range <- 1:52

# Create an empty data frame to store the results
df_all <- data.frame()

# Calculate probabilities for each success rate
for (p_success in p_success_values) {
  probabilities <- sapply(n_trials_range, function(n) {
    1 - (1 - p_success)^n
  })
  
  # Create a temporary data frame for this success rate
  df_temp <- data.frame(
    Number_of_Trials = n_trials_range,
    Probability_of_Success = probabilities,
    Success_Rate = factor(p_success) # Add a factor for color grouping
  )
  
  # Append the temporary data frame to the main data frame
  df_all <- rbind(df_all, df_temp)
}

# Create the plot using ggplot2
ggplot(df_all, aes(x = Number_of_Trials, y = Probability_of_Success, color = Success_Rate)) +
  geom_line() +
  geom_point() +
  geom_hline(yintercept = 0.95, linetype = "dashed", color = "red") +
  labs(
    title = "Probability of at Least One Cleanup on each Tenant vs. Number of Runs",
    x = "Number of Runs Up to a year(52 weekends)",
    y = "Probability of at Least One Cleanup",
    color = "% Deletion per run" # Legend title
  ) +
  scale_color_discrete(labels = c("10%", "20%", "30%", "40%", "50%")) + # Custom legend labels
  theme_bw()