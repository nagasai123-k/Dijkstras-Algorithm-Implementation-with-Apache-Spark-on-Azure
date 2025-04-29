# Spark-Based Dijkstra's Algorithm on Azure

## Overview

This project showcases a distributed computing approach to finding shortest paths in large graphs. Using Apache Spark's parallel processing capabilities on an Azure cloud platform, we implement the classic Dijkstra's algorithm to calculate optimal routes from a starting node to all other nodes in a weighted network.

## Key Capabilities

- Spark RDD framework for distributed graph processing
- Optimized for large-scale networks (successfully tested on 10K nodes/100K edges)
- Smart convergence detection to minimize processing time
- Streamlined I/O with automatic result generation
- Lightweight deployment on cost-effective Azure infrastructure

## System Requirements

- Active Azure subscription
- Java Development Kit 11
- Apache Spark 3.4.1
- Python 3 with PySpark package

## File Structure

```
project-directory/
├── dijkstra_spark.py       # Main algorithm implementation 
├── weighted_graph.txt      # Graph data in edge list format
└── README.md               # Documentation
```

## Azure Environment Configuration

### Creating Your Cloud Server

Our implementation runs on a modest Azure virtual machine:

**VM Specifications:**
- Type: Standard B2s with 2 vCPUs and 4GB memory
- OS: Ubuntu Server 22.04 LTS
- Security: SSH key authentication
- Network: Basic SSH connectivity (port 22)

### Software Installation

After connecting to your VM, set up the required software:

```bash
# System updates and core packages
sudo apt update
sudo apt install openjdk-11-jdk scala python3-pip -y

# Confirm successful installation
java -version
scala -version
python3 --version
pip3 --version

# Download and install Spark
wget https://dlcdn.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz
tar -xvzf spark-3.4.1-bin-hadoop3.tgz
sudo mv spark-3.4.1-bin-hadoop3 /opt/spark

# Configure environment paths
echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Install Python Spark interface
pip3 install pyspark
```

### Transferring Project Files

Move your code and data from your local machine to the cloud server:

```bash
# Set key permissions
chmod 400 yourkeyfile.pem

# Upload files to VM
scp -i yourkeyfile.pem dijkstra_spark.py username@vm-ip-address:~
scp -i yourkeyfile.pem weighted_graph.txt username@vm-ip-address:~
```

To make changes directly on the server, use a text editor like nano:

```bash
nano dijkstra_spark.py
# Save with Ctrl+O, Exit with Ctrl+X
```

## Input Data Format

The algorithm works with weighted graph data in edge list format:

```
total_nodes total_edges
source1 destination1 weight1
source2 destination2 weight2
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

## Running the Algorithm

Execute the implementation with Spark's distributed engine:

```bash
spark-submit dijkstra_spark.py weighted_graph.txt starting_node_id
```

For example:
```bash
spark-submit dijkstra_spark.py weighted_graph.txt 8168
```

## Results

The algorithm generates a text file with all shortest path distances:
```
shortest_distances_from_X.txt
```

Where X is your specified starting node. Unreachable nodes are marked with "INF".

## Optimization Features

Our implementation includes several performance enhancements:

1. **Distributed Computation**: Leverages Spark's parallel processing
2. **Smart Termination**: Stops when no further improvements are possible
3. **Efficient Memory Usage**: Optimized data structures to minimize memory footprint
4. **Streamlined I/O**: Fast processing of input and output

## Complete Deployment Example

Here's the full process from setup to execution:

```bash
# From your local computer
chmod 400 your_key.pem
scp -i your_key.pem dijkstra_spark.py username@vm-ip:~
scp -i your_key.pem weighted_graph.txt username@vm-ip:~

# Connect to VM
ssh -i your_key.pem username@vm-ip

# On the VM - Setup environment
sudo apt update
sudo apt install openjdk-11-jdk scala python3-pip -y
wget https://dlcdn.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz
tar -xvzf spark-3.4.1-bin-hadoop3.tgz
sudo mv spark-3.4.1-bin-hadoop3 /opt/spark
echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
pip3 install pyspark

# Execute algorithm
spark-submit dijkstra_spark.py weighted_graph.txt 8168
```

## Common Issues & Solutions

1. **SSH Connection Problems**:
   ```bash
   chmod 600 your_key.pem
   ```

2. **Missing Spark Commands**:
   ```bash
   source ~/.bashrc
   ```

3. **Java Configuration Issues**:
   ```bash
   java -version  # Should show version 11
   ```

4. **Missing Python Dependencies**:
   ```bash
   pip3 install package_name
   ```

5. **File Permission Problems**:
   ```bash
   chmod +r weighted_graph.txt
   ```

## Technical Implementation

The `dijkstra_spark.py` script implements the distributed Dijkstra's algorithm with these components:

1. **Graph Structure**: Adjacency list representation via RDDs
2. **Distance Tracking**: Current shortest paths stored in distributed format
3. **Iterative Algorithm**: Continues until no further improvement or all reachable nodes visited
4. **Result Management**: Automated storage of calculated distances

## References

- [Spark Official Documentation](https://spark.apache.org/docs/latest/)
- [PySpark Programming Guide](https://spark.apache.org/docs/latest/api/python/index.html)
- [Azure Cloud Documentation](https://docs.microsoft.com/en-us/azure/)
- [Dijkstra's Algorithm Details](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

## Project Context

This implementation fulfills the requirements for the "Implementing Dijkstra's Algorithm with Apache Spark on Azure VMs" assignment, demonstrating cloud-based distributed graph processing.
