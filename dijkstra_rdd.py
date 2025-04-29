from pyspark import SparkContext, SparkConf
import sys

def extract_edge_data(line):
    """Extract source, target, and weight from an input line."""
    elements = line.strip().split()
    return int(elements[0]), int(elements[1]), int(elements[2])

def execute_algorithm():
    # Validate command line arguments
    if len(sys.argv) != 3:
        print("Usage: dijkstra_spark.py <input_file> <source_node>")
        sys.exit(-1)
        
    # Get input parameters
    graph_file = sys.argv[1]
    start_node = int(sys.argv[2])
    
    # Initialize Spark environment
    config = SparkConf().setAppName("DijkstraShortestPath").setMaster("local[*]")
    spark = SparkContext(conf=config)
    
    # Read the input graph file
    file_content = spark.textFile(graph_file)
    
    # Separate header from edge data
    metadata = file_content.first()
    edge_data = file_content.filter(lambda x: x != metadata).map(extract_edge_data)
    
    # Transform edges to adjacency format
    formatted_edges = edge_data.map(lambda x: (x[0], (x[1], x[2])))
    
    # Create adjacency lists for each node
    graph_structure = formatted_edges.groupByKey().mapValues(list).cache()
    
    # Identify all vertices in the graph
    vertices = formatted_edges.flatMap(lambda x: [x[0], x[1][0]]).distinct()
    
    # Set initial distances (0 for source, infinity for others)
    path_lengths = vertices.map(
        lambda node: (node, 0) if node == start_node else (node, float('inf'))
    ).cache()
    
    # Set iteration limit to prevent infinite loops
    iteration_limit = 20
    
    # Main algorithm loop
    for step in range(iteration_limit):
        # Collect current state of distances
        distance_snapshot = dict(path_lengths.collect())
        shared_distances = spark.broadcast(distance_snapshot)
        
        # Calculate potential distance improvements
        improved_paths = graph_structure.flatMap(lambda x: [
            (neighbor, shared_distances.value[x[0]] + weight)
            for neighbor, weight in x[1]
            if shared_distances.value.get(x[0], float('inf')) + weight < shared_distances.value.get(neighbor, float('inf'))
        ])
        
        # Keep shortest path if multiple paths to same node
        best_improvements = improved_paths.reduceByKey(min)
        
        # Merge existing distances with improvements
        updated_paths = path_lengths.fullOuterJoin(best_improvements).mapValues(
            lambda values: min(v for v in values if v is not None)
        ).cache()
        
        # Check for convergence (no further improvements)
        previous_state = path_lengths.collectAsMap()
        current_state = updated_paths.collectAsMap()
        converged = all(previous_state.get(k, float('inf')) == current_state.get(k, float('inf')) for k in previous_state.keys())
        
        # Update working distances
        path_lengths = updated_paths
        
        # Early termination if no changes
        if converged:
            print(f"Converged after {step + 1} iterations!")
            break
    
    # Prepare final results
    final_distances = sorted(path_lengths.collect(), key=lambda x: x[0])
    
    # Format output
    result_lines = [f"Shortest distances from node {start_node}:"]
    for node, distance in final_distances:
        display_dist = "INF" if distance == float('inf') else str(int(distance))
        result_lines.append(f"Node {node}: {display_dist}")
    
    # Write results to file
    output_file = f"shortest_distances_from_{start_node}.txt"
    with open(output_file, 'w') as output:
        for line in result_lines:
            output.write(line + "\n")
            
    print(f"Output written to {output_file}")
    
    # Clean up Spark resources
    spark.stop()

if __name__ == "__main__":
    execute_algorithm()