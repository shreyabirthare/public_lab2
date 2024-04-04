import matplotlib.pyplot as plt

# Data
clients = [1, 2, 3, 4, 5]

# buy Latency
buy_with_docker = [4.490663767, 5.123154521, 5.774055322, 6.12833333, 6.24968853]
buy_without_docker = [1.385770082, 2.027086258, 2.442425807, 2.485036421, 2.711467683]

# Query Latency
query_with_docker = [2.469878435, 3.209934592, 3.355884155, 3.494788647, 3.957850981]
query_without_docker = [0.788919687, 1.024381161, 1.504482269, 1.605131483, 1.681178451]

# Creating plots
fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# Function to label the data points on the plot
def label_data_points(x, y, ax):
    for i, txt in enumerate(y):
        ax.annotate(f"{txt:.2f}", (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Plot for buy latency
axs[0].plot(clients, buy_with_docker, marker='o', color='blue', label='BUY WITH DOCKER')
axs[0].plot(clients, buy_without_docker, marker='x', color='red', label='BUY WITHOUT DOCKER')
label_data_points(clients, buy_with_docker, axs[0])
label_data_points(clients, buy_without_docker, axs[0])
axs[0].set_xlabel('Number of Clients')
axs[0].set_ylabel('Average Latency (sec)')
axs[0].set_title('Buy Latency Comparison')
axs[0].legend()

# Plot for QUERY latency
axs[1].plot(clients, query_with_docker, marker='o', color='green', label='QUERY WITH DOCKER')
axs[1].plot(clients, query_without_docker, marker='x', color='purple', label='QUERY WITHOUT DOCKER')
label_data_points(clients, query_with_docker, axs[1])
label_data_points(clients, query_without_docker, axs[1])
axs[1].set_xlabel('Number of Clients')
axs[1].set_ylabel('Average Latency (sec)')
axs[1].set_title('Query Latency Comparison')
axs[1].legend()

# Display the plots
plt.tight_layout()
plt.show()
