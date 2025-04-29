# Dijkstra's Algorithm Implementation with Apache Spark on Azure

## Project Overview

This project implements Dijkstra's shortest path algorithm using Apache Spark in a standalone deployment on Microsoft Azure. The implementation finds the shortest paths from a source node to all other nodes in a weighted graph, leveraging Spark's distributed computing capabilities.

## Features

- Implementation of Dijkstra's algorithm using Spark RDDs (Resilient Distributed Datasets)
- Support for large graphs (tested with 10,000 nodes, 100,000 edges)
- Standalone Spark deployment on Azure VM
- Early convergence detection for performance optimization
- Automatic output file generation

## Requirements

- Azure account for VM deployment
- JDK 11
- Apache Spark 3.4.1
- Python 3
- PySpark

## Project Files

```
dijkstra-spark/
├── dijkstra_spark.py       # Python implementation using Spark RDDs
├── weighted_graph.txt      # Input graph file in edge list format
└── README.md               # This file
```

## Setup Instructions

### 1. Azure VM Setup

A lightweight Azure VM configuration was used for this implementation:

#### VM Configuration:
- **Size**: Standard B2s (2 vCPUs, 4 GB RAM)
- **Operating System**: Ubuntu Server 22.04 LTS
- **Authentication**: SSH public key
- **Networking**: Allow SSH (port 22)

#### Using Azure Portal:

1. Log in to the [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" > "Compute" > "Virtual Machine"
3. Configure the VM with the specifications above

#### Using Azure CLI:

```bash
# Login to Azure
az login

# Create a resource group
az group create --name dijkstraSparkRG --location eastus

# Create VM
az vm create \
  --resource-group dijkstraSparkRG \
  --name spark-server \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys \
  --size Standard_B2s

# Open SSH port
az vm open-port --resource-group dijkstraSparkRG --name spark-server --port 22
```

### 2. Environment Setup

Connect to your VM using SSH:

```bash
ssh -i <private_key.pem> azureuser@<vm_public_ip>
```

Install necessary dependencies:

```bash
# Update package lists
sudo apt update

# Install OpenJDK 11, Scala, and Python
sudo apt install openjdk-11-jdk scala python3-pip -y

# Verify installations
java -version
scala -version
python3 --version
pip3 --version
```

### 3. Apache Spark Installation

```bash
# Download Spark 3.4.1
wget https://dlcdn.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz

# Extract Spark
tar -xvzf spark-3.4.1-bin-hadoop3.tgz

# Move Spark to /opt
sudo mv spark-3.4.1-bin-hadoop3 /opt/spark

# Set environment variables
echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Install PySpark
pip3 install pyspark
```

### 4. Uploading Project Files

From your local machine, upload the Python code and input graph file to the VM:

```bash
# Set proper permissions for private key
chmod 400 <private_key.pem>

# Upload files to VM
scp -i <private_key.pem> dijkstra_spark.py azureuser@<vm_public_ip>:~
scp -i <private_key.pem> weighted_graph.txt azureuser@<vm_public_ip>:~
```

Alternatively, you can edit files directly on the VM using an editor like `nano`:

```bash
nano dijkstra_spark.py
```

Inside nano:
- Save changes: `Ctrl + O`, then `Enter`
- Exit editor: `Ctrl + X`

## Input Format

The input graph should be in the following edge list format:

```
num_nodes num_edges
u1 v1 weight1
u2 v2 weight2
...
```

Example:
```
5 6
0 1 7
0 2 3
1 3 9
2 4 4
3 4 6
1 4 2
```

## Running the Application

To run the Dijkstra's algorithm implementation:

```bash
spark-submit dijkstra_spark.py weighted_graph.txt <source_node>
```

Where:
- `dijkstra_spark.py` is the Python implementation file
- `weighted_graph.txt` is the input graph file
- `<source_node>` is the starting node from which shortest paths will be calculated

Example:
```bash
spark-submit dijkstra_spark.py weighted_graph.txt 8168
```

## Output

After successful execution, the program generates an output file with the naming convention:
```
shortest_distances_from_<source_node>.txt
```

For example:
```
shortest_distances_from_8168.txt
```

This file contains the computed shortest distances for each node. If a node is unreachable, its distance is marked as `INF`.

## Performance Features

The implementation includes several performance optimizations:

1. **Full Spark RDD Parallelism**: Leverages Spark's distributed computing capabilities
   
2. **Early Convergence Detection**: Stops processing when no more distances can be improved

3. **Clean Input-Output Handling**: Efficiently reads input and writes output

4. **Memory Optimization**: Keeps only necessary data in memory during computation

## Full Command Sequence Example

Here's a complete example workflow from setting up the VM to running the algorithm:

```bash
# On Local Machine
chmod 400 SparkVM_key.pem
scp -i SparkVM_key.pem dijkstra_spark.py azureuser@<vm_public_ip>:~
scp -i SparkVM_key.pem weighted_graph.txt azureuser@<vm_public_ip>:~

# SSH into VM
ssh -i SparkVM_key.pem azureuser@<vm_public_ip>

# On VM - Install dependencies
sudo apt update
sudo apt install openjdk-11-jdk scala python3-pip -y

# Install Spark
wget https://dlcdn.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz
tar -xvzf spark-3.4.1-bin-hadoop3.tgz
sudo mv spark-3.4.1-bin-hadoop3 /opt/spark
echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
pip3 install pyspark

# Run the algorithm
spark-submit dijkstra_spark.py weighted_graph.txt 8168
```

## Troubleshooting

Common issues and solutions:

1. **Permission denied when SSH or SCP**:
   ```bash
   chmod 600 <private_key.pem>
   ```

2. **Spark not found after setup**:
   ```bash
   source ~/.bashrc
   ```

3. **Java version issues**: Ensure you're using JDK 11
   ```bash
   java -version
   ```

4. **Python package not found**: Install any missing packages
   ```bash
   pip3 install <package_name>
   ```

5. **File not found errors**: Check paths and file permissions
   ```bash
   ls -la
   chmod +r weighted_graph.txt
   ```

## Implementation Details

The Python implementation (`dijkstra_spark.py`) uses Spark's RDD API to implement Dijkstra's algorithm in a distributed manner. Key aspects include:

1. **Graph Representation**: The graph is represented as an adjacency list using RDDs

2. **Distance Tracking**: A distances RDD maintains current shortest paths

3. **Iterative Processing**: The algorithm runs until convergence (no distance updates)

4. **Result Output**: Results are written to a file for easy access

## References

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)
- [Microsoft Azure Documentation](https://docs.microsoft.com/en-us/azure/)
- [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

## About This Project

This project was implemented as part of the assignment "Implementing Dijkstra's Algorithm with Apache Spark on Azure VMs." It demonstrates the use of distributed computing techniques for graph processing algorithms.
